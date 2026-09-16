# src/logic.py
# ======================================================
# AFP ESTIMATOR - LOGIC MODULE
# Version: v2.9
# Updated: 2026-01-23
# Description: Core math, pricing pricing curves, and schedule simulation.
# ======================================================

import math
import datetime

def smart_round(val):
    """Rounds up to the nearest $10 increment."""
    return math.ceil(val / 10.0) * 10.0

def calculate_travel_billable(one_way_hours):
    """Min 8 hrs. If > 8, round up to nearest 2 hrs."""
    if one_way_hours <= 8.0: return 8.0
    else: return math.ceil(one_way_hours / 2.0) * 2.0

def calculate_part_price(vendor_cost, tier="Standard"):
    if vendor_cost <= 0: return 0.0, 0.0
    landed_cost = vendor_cost * 1.035
    base_year = 2025
    current_year = datetime.date.today().year
    years_passed = max(0, current_year - base_year)
    inflation_factor = 1.05 ** years_passed
    
    if tier == "Key Account (AERO/MPWA)":
        pivot = 200.0 * inflation_factor; floor, ceiling = 1.539, 2.0
    elif tier == "Preferred":
        pivot = 100.0 * inflation_factor; floor, ceiling = 1.60, 3.5
    else:
        pivot = 70.0 * inflation_factor; floor, ceiling = 1.67, 4.0
        
    markup = floor + (ceiling - floor) / (1 + (landed_cost / pivot))
    sell_price = landed_cost * markup
    return sell_price, markup

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8 
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def calculate_onsite_duration(start_date, work_days, sat, sun):
    """
    Calculates calendar duration for N working days, skipping unauthorized weekends.
    """
    curr = start_date
    worked = 0
    calendar_days = 0
    # Guardrail: Limit loop to avoid hangs
    for _ in range(365):
        if worked >= work_days: break
        
        is_work = True
        if (curr.weekday() == 5 and not sat) or (curr.weekday() == 6 and not sun): 
            is_work = False
            
        if is_work: worked += 1
        calendar_days += 1
        curr += datetime.timedelta(days=1)
        
    return calendar_days

def simulate_schedule(start_date, work_days, hrs_day, sat, sun, rules, is_key_account):
    curr = start_date
    worked = 0
    sub_days = 0
    weekly_hours = 0.0
    bucket = {"RT": 0.0, "OT": 0.0, "DT": 0.0}
    cap = rules.get('cap_rt_weekly', 40)
    
    for _ in range(365):
        if worked >= work_days: break
        if not is_key_account and curr.weekday() == 0: weekly_hours = 0.0
        is_work = True
        if (curr.weekday() == 5 and not sat) or (curr.weekday() == 6 and not sun): is_work = False
        sub_days += 1
        
        if is_work:
            worked += 1
            d_rt, d_ot, d_dt = 0.0, 0.0, 0.0
            if curr.weekday() == 6: d_dt = hrs_day
            elif curr.weekday() == 5: d_ot = hrs_day
            else:
                rt_pot = min(10, hrs_day)
                ot_pot = max(0, hrs_day - 10)
                if weekly_hours >= cap: d_ot += rt_pot + ot_pot
                elif (weekly_hours + rt_pot) > cap:
                    avail_rt = max(0, cap - weekly_hours)
                    d_rt = avail_rt
                    d_ot = ot_pot + (rt_pot - avail_rt)
                    weekly_hours += avail_rt
                else:
                    d_rt = rt_pot; d_ot = ot_pot; weekly_hours += rt_pot
            bucket["RT"] += d_rt; bucket["OT"] += d_ot; bucket["DT"] += d_dt
        curr += datetime.timedelta(days=1)
    return bucket, sub_days

def generate_audit_text(proj_data, lines, totals, rates, user_inputs, calc_log):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt = f"========================================================\n"
    txt += f" AFP FIELD SERVICE ESTIMATOR - AUDIT RECORD\n"
    txt += f" Generated: {timestamp}\n"
    txt += f" Status:    {user_inputs.get('status', 'Draft').upper()}\n"
    txt += f"========================================================\n\n"
    
    txt += "1. PROJECT DETAILS\n--------------------------------------------------------\n"
    txt += f"Project Name:  {proj_data.get('Project')}\n"
    txt += f"Client:        {proj_data.get('ClientName')}\n"
    txt += f"Site:          {proj_data.get('Site')}\n"
    txt += f"Region:        {proj_data.get('Region')}\n"
    txt += f"Mobilization:  {proj_data.get('Start')}\n"
    txt += f"Return Date:   {proj_data.get('Return')}\n\n"
    
    txt += "2. USER CONFIGURATION (Inputs)\n--------------------------------------------------------\n"
    if user_inputs.get('is_parts_only'): txt += "Mode:          Parts Only\n"
    else:
        txt += f"Mode:          {user_inputs.get('mode')}\n"
        txt += f"Techs (TFAs):  {user_inputs.get('tfas')}\n"
        txt += f"Work Days:     {user_inputs.get('days')}\n"
        txt += f"Hours/Day:     {user_inputs.get('hrs')}\n"
        txt += f"Work Wknd:     Sat={user_inputs.get('sat')} | Sun={user_inputs.get('sun')}\n"
        txt += f"Travel:        Flight=${user_inputs.get('flight_cost')} | Miles={user_inputs.get('miles')} | Hrs={user_inputs.get('t_hrs')}\n"
        txt += f"Subsistence:   Override={user_inputs.get('override_sub')} | Manual Days={user_inputs.get('man_sub_days')}\n"
    txt += f"Contingency:   {user_inputs.get('cont_pct') * 100}%\n"
    txt += f"Misc Exp:      ${user_inputs.get('misc_exp')}\n\n"

    if rates:
        txt += "3. RATES APPLIED\n--------------------------------------------------------\n"
        txt += f"Standard:      ${rates['rt']}/hr\n"
        txt += f"Overtime:      ${rates['ot']}/hr\n"
        txt += f"Doubletime:    ${rates['dt']}/hr\n"
        txt += f"Travel:        ${rates['tr']}/hr\n"
        txt += f"OT Cap:        {rates.get('cap')} hours\n\n"

    txt += "4. CALCULATED LINE ITEMS\n--------------------------------------------------------\n"
    txt += f"{'Description':<50} | {'Qty':<6} | {'Rate':<10} | {'Total':<10}\n"
    txt += "-"*85 + "\n"
    for l in lines:
        txt += f"{l['Description'][:48]:<50} | {str(l['Qty']):<6} | ${l['Rate']:,.2f}    | ${l['Total']:,.2f}\n"
    txt += "-"*85 + "\n"
    txt += f"{'GRAND TOTAL':<70} {totals['Grand']:,.2f}\n\n"
    
    txt += "5. SCOPE OF WORK\n--------------------------------------------------------\n"
    txt += f"{proj_data.get('SOW')}\n\n"
    
    txt += "6. CALCULATION BREAKDOWN (Audit Trail)\n--------------------------------------------------------\n"
    if calc_log:
        for item in calc_log: txt += f"> {item}\n"
    else: txt += "No breakdown available.\n"
    txt += "\n"
    return txt