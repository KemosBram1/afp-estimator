# src/app.py
# ==============================================================================
# AFP ESTIMATOR - MAIN APPLICATION
# ==============================================================================
# VERSION HISTORY
# ------------------------------------------------------------------------------
# v2.9.3 | 2026-01-23 | Added Minimum Billing Value (MBV) Guardrail & Override.
#                     | Restored Version Header Table.
# v2.9.2 | 2026-01-23 | Fixed Template Engine to scan external folder.
# v2.9.1 | 2026-01-23 | Added Dynamic Variables to Template Engine.
# v2.9   | 2026-01-23 | Implemented "Smart Schedule" Fix (Weekends) & Markdown V2.
# v2.7   | 2026-01-23 | Added JSON Save/Load & Status Tracking.
# v2.6   | 2026-01-23 | Critical Fix: Lodging/Sub Qty Logic & Audit Trail.
# ==============================================================================

import streamlit as st
import datetime
import pandas as pd
import os
import math
import json

import logic
import data
import pdf_gen

st.set_page_config(page_title="AFP Field Service Estimator v2.9.3", layout="wide", page_icon="🛠️")

# --- SESSION STATE ---
if 'rate_rt' not in st.session_state: st.session_state.rate_rt = 140.0
if 'rate_ot' not in st.session_state: st.session_state.rate_ot = 210.0
if 'rate_dt' not in st.session_state: st.session_state.rate_dt = 280.0
if 'rate_tr' not in st.session_state: st.session_state.rate_tr = 140.0
if 'loc_rates' not in st.session_state: st.session_state.loc_rates = {'lodging': 150.0, 'mie': 64.0}
defaults = {
    'proj_name': "New Project", 'days': 5, 'tfas': 1, 'hrs': 10, 'flight_cost': 650.0, 
    'miles': 0.0, 't_hrs': 6.0, 'misc_exp': 0.0, 'cont_pct': 5.0, 'sow': "", 'assume': "", 
    'man_sub_days': 0, 'override_sub': False, 'sat': False, 'sun': False, 'status': "Draft",
    'payment_terms': 30, 'validity': 30, 'disable_mbv': False
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

def update_rates():
    if st.session_state.region_select == "INTERNATIONAL":
        st.session_state.rate_rt = 160.0; st.session_state.rate_ot = 240.0; st.session_state.rate_dt = 320.0; st.session_state.rate_tr = 160.0
    else:
        st.session_state.rate_rt = 140.0; st.session_state.rate_ot = 210.0; st.session_state.rate_dt = 280.0; st.session_state.rate_tr = 140.0

# --- SCHEDULE CALLBACK ---
def recalc_dates():
    """Recalculates Return Date based on Onsite Start + Working Days + Weekends."""
    if 'start_date' in st.session_state and 'days' in st.session_state:
        duration = logic.calculate_onsite_duration(
            st.session_state.start_date, 
            st.session_state.days, 
            st.session_state.sat, 
            st.session_state.sun
        )
        st.session_state.return_date = st.session_state.start_date + datetime.timedelta(days=duration)

DF_COMP, DF_LOC = data.load_client_db()

# --- SIDEBAR ---
st.sidebar.header("⚙️ Estimator v2.9.3")
uploaded_file = st.sidebar.file_uploader("📂 Load Saved Quote (JSON)", type=["json"])
if uploaded_file is not None:
    try:
        data_json = json.load(uploaded_file)
        for key, value in data_json.items():
            if key in ['mob_date', 'start_date', 'return_date']: st.session_state[key] = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            else: st.session_state[key] = value
        st.sidebar.success("✅ Quote Loaded!")
    except Exception as e: st.sidebar.error(f"Error loading file: {e}")

st.sidebar.markdown("---")
sel_status = st.sidebar.selectbox("Quote Status", ["Draft", "Submitted", "Customer Approved", "Booked", "Lost"], key="status")

st.sidebar.subheader("Client")
sel_site_data = {"Company": "", "Site": "", "Street": "", "City": "", "State": "", "Zip": ""}
is_key_account = False
tier_selection = "Standard"

if not DF_COMP.empty:
    client_list = ["Select Client..."] + sorted(DF_COMP['company_name'].unique().tolist())
    sel_client = st.sidebar.selectbox("Customer", client_list)
    if sel_client != "Select Client...":
        sel_site_data['Company'] = sel_client
        if "Mitsubishi Power Aero" in sel_client or "Mitsubishi Power Americas" in sel_client:
            is_key_account = True; tier_selection = "Key Account (AERO/MPWA)"; st.sidebar.success("🔑 Key Account Detected")
        locs = DF_LOC[DF_LOC['company_name'] == sel_client]
        site_list = ["Select Site..."] + sorted(locs['site_name'].unique().tolist())
        sel_site = st.sidebar.selectbox("Location", site_list)
        if sel_site != "Select Site...":
            r = locs[locs['site_name'] == sel_site].iloc[0]
            sel_site_data.update({"Site": sel_site, "Street": r['street'], "City": r['city'], "State": r['state'], "Zip": str(r['zip']).replace('.0','')})

st.sidebar.markdown("---")
quote_type = st.sidebar.radio("Quote Type", ["Service & Parts", "Parts Only"])
is_parts_only = (quote_type == "Parts Only")
if not is_key_account: tier_selection = st.sidebar.select_slider("Pricing Tier", options=["Standard", "Preferred"], value="Standard")

if not is_parts_only:
    st.sidebar.markdown("---"); st.sidebar.subheader("Labor & Markup")
    c1, c2 = st.sidebar.columns(2)
    rate_rt = c1.number_input("Std ($/hr)", key='rate_rt')
    rate_ot = c2.number_input("OT ($/hr)", key='rate_ot')
    rate_dt = c1.number_input("DT ($/hr)", key='rate_dt')
    rate_tr = c2.number_input("Trv ($/hr)", key='rate_tr')
    rt_cap = st.sidebar.number_input("OT Threshold", value=45 if is_key_account else 40)
    exp_markup_pct = st.sidebar.number_input("Exp Markup %", value=15.0, step=0.5)
    EXP_MARKUP = (exp_markup_pct / 100.0) + 1.0

# --- COMMERCIAL TERMS & MBV ---
st.sidebar.markdown("---")
st.sidebar.subheader("Commercial Terms")
c_term1, c_term2 = st.sidebar.columns(2)
payment_terms = c_term1.number_input("Net Terms (Days)", value=30, key='payment_terms')
validity_days = c_term2.number_input("Validity (Days)", value=30, key='validity')
disable_mbv = st.sidebar.checkbox("Disable Min Billing Guardrail?", value=False, key='disable_mbv')

# --- TABS ---
if is_parts_only:
    tabs = st.tabs(["📍 Project", "📦 Parts Engine", "📝 Notes", "🔍 Preview", "💾 Text/JSON"])
    t_proj, t_parts, t_notes, t_prev, t_text = tabs[0], tabs[1], tabs[2], tabs[3], tabs[4]
else:
    tabs = st.tabs(["📍 Project", "✈️ Travel", "👷 Schedule", "📦 Parts", "📝 Notes", "🔍 Preview", "💾 Text/JSON"])
    t_proj, t_travel, t_sched, t_parts, t_notes, t_prev, t_text = tabs[0], tabs[1], tabs[2], tabs[3], tabs[4], tabs[5], tabs[6]

# --- VARIABLES ---
mob_date = None; return_date = None; flight_cost = 0.0; miles = 0.0; t_hrs = 0.0; man_labor = 0.0; is_commuter = False

# --- TAB LOGIC ---
with t_proj:
    c1, c2 = st.columns(2)
    proj_name = c1.text_input("Project Name", key='proj_name')
    region = c1.radio("Region", ["DOMESTIC", "INTERNATIONAL"], horizontal=True, key='region_select', on_change=update_rates)
    site_manual = c2.text_input("Manual Site Name", value=sel_site_data['Site'])
    final_site = site_manual if site_manual else sel_site_data['Site']
    
    if not is_parts_only:
        if region == "DOMESTIC":
            zip_code = c1.text_input("Zip Code", value=sel_site_data['Zip'])
            if zip_code:
                res = data.get_domestic_rate(zip_code, datetime.date.today())
                if res: st.success(f"✅ GSA: {res['city']} (${res['lodging']})"); st.session_state.loc_rates = res
        else:
            country = c1.text_input("Country")
            if country:
                opts = data.get_international_options(country)
                if opts:
                    c_str = st.selectbox("City", [f"{x['Location']} ({x['Country']})" for x in opts])
                    if c_str:
                        res = data.get_international_rate(c_str.split(" (")[1][:-1], c_str.split(" (")[0])
                        if res: st.success(f"✅ State: {res['city']} (${res['lodging']})"); st.session_state.loc_rates = res
        
        with st.expander("Override Rates"):
            c1, c2 = st.columns(2)
            st.session_state.loc_rates['lodging'] = c1.number_input("Lodging", value=float(st.session_state.loc_rates.get('lodging', 150.0)))
            st.session_state.loc_rates['mie'] = c2.number_input("M&I", value=float(st.session_state.loc_rates.get('mie', 64.0)))

if not is_parts_only:
    with t_travel:
        mode = st.radio("Mode", ["FLY", "DRIVE", "FLY then DRIVE"], horizontal=True, key='mode_select')
        if mode == "FLY": 
            flight_cost = st.number_input("Flight Cost", key='flight_cost'); t_hrs = st.number_input("One-Way Hours", key='t_hrs'); miles = 0.0
        elif mode == "FLY then DRIVE":
            c1, c2 = st.columns(2); flight_cost = c1.number_input("Flight Cost", key='flight_cost'); t_hrs = c2.number_input("Total One-Way Hours (Flight+Drive)", key='t_hrs'); miles = st.number_input("Rental Drive Miles (Round Trip)", key='miles') 
        else:
            c1, c2 = st.columns(2); gps = c1.text_input("GPS (Lat,Lon)", "41.25, -95.93")
            try: 
                lat, lon = map(float, gps.split(","))
                c2.info(f"Calc: {int(logic.haversine(41.209, -96.065, lat, lon)*1.3*1.15)} mi")
            except: pass
            miles = st.number_input("Billable Miles", key='miles'); t_hrs = miles / 50.0; flight_cost = 0.0
        
        if miles > 0 and miles < 50: is_commuter = True; st.warning("ℹ️ **Commuter Rule Active (<50mi):** Lodging=$0, M&I=50%"); man_labor = st.number_input("Actual Drive Time (Total)", 2.0)

    with t_sched:
        c1, c2, c3 = st.columns(3)
        tfas = c1.number_input("TFAs", min_value=1, key='tfas')
        days = c2.number_input("Work Days", min_value=1, key='days', on_change=recalc_dates)
        hrs = c3.number_input("Hrs/Day", min_value=1, key='hrs')
        sat = st.checkbox("Sat?", key='sat', on_change=recalc_dates)
        sun = st.checkbox("Sun?", key='sun', on_change=recalc_dates)
        
        st.markdown("---"); st.markdown("### 📅 Trip Schedule"); c_d1, c_d2, c_d3 = st.columns(3)
        def_mob = st.session_state.get('mob_date', datetime.date.today())
        mob_date = c_d1.date_input("Mobilization Date", def_mob)
        
        def_start = mob_date + datetime.timedelta(days=1)
        if 'start_date' in st.session_state: def_start = st.session_state.start_date
        start_date = c_d2.date_input("Onsite Start", def_start, key='start_date', on_change=recalc_dates)
        
        if 'return_date' not in st.session_state:
             st.session_state.return_date = start_date + datetime.timedelta(days=int(days))
        return_date = c_d3.date_input("Return Date", st.session_state.return_date, key='return_date')
        
        trip_days = (return_date - mob_date).days + 1
        st.info(f"🗓️ Total Trip Duration: **{trip_days} Days**"); override_sub = st.checkbox("Override Subsistence Count?", key='override_sub'); man_sub_days = 0
        if override_sub: man_sub_days = st.number_input("Manual Subsistence Days", key='man_sub_days')

with t_parts:
    if 'parts_list' not in st.session_state: st.session_state.parts_list = [{"Part #": "", "Description": "", "Qty": 1, "Cost": 0.0, "Lead Time": "2-4 Weeks"}]
    edited_parts = st.data_editor(pd.DataFrame(st.session_state.parts_list), num_rows="dynamic", use_container_width=True, column_config={"Lead Time": st.column_config.SelectboxColumn(options=["Stock", "2-4 Weeks", "6-8 Weeks"])})
    misc_exp = st.number_input("Misc Expenses", key='misc_exp') if not is_parts_only else 0.0
    val_cont = st.session_state.get('cont_pct', 5.0)
    cont_pct = st.number_input("Contingency %", min_value=0.0, max_value=100.0, step=0.5, key='cont_pct') / 100.0 if not is_parts_only else 0.0

with t_notes:
    st.markdown("### 📋 Load Terms & Conditions")
    c_t1, c_t2 = st.columns([3, 1])
    term_dict = data.get_term_templates()
    sel_term = c_t1.selectbox("Select Template", ["Choose..."] + list(term_dict.keys()), label_visibility="collapsed")
    
    if c_t2.button("📥 Apply"):
        if sel_term != "Choose...":
            raw_tmpl = term_dict[sel_term]
            
            # --- DYNAMIC INJECTION LOGIC ---
            ctx = {
                'rate_rt': st.session_state.rate_rt,
                'rate_ot': st.session_state.rate_ot,
                'rate_dt': st.session_state.rate_dt,
                'rate_rt_night': st.session_state.rate_rt * 1.2,
                
                # Minimum Billing Values
                'mbv_domestic': st.session_state.rate_rt * 50,   
                'mbv_intl': 160.00 * 100,                        
                
                # International equivalents
                'rate_rt_intl': 160.00,
                'rate_ot_intl': 240.00,
                'rate_dt_intl': 320.00,
                'rate_nt_intl': 192.00,
                
                'payment_terms': st.session_state.payment_terms,
                'validity': st.session_state.validity
            }
            
            try:
                final_text = raw_tmpl.format(**ctx)
                st.session_state.assume = final_text
                st.success("Template Applied with Live Rates!")
                st.rerun()
            except KeyError as e:
                st.error(f"Template Error: Missing placeholder {e}")
            except Exception as e:
                st.error(f"Error applying template: {e}")
            
    sow = st.text_area("Scope of Work", help="Supports **bold** and - bullets", key='sow')
    assume = st.text_area("Assumptions / T&Cs", key='assume', height=400)

if st.button("🚀 Calculate Quote", type="primary"):
    svc_lines = []; part_lines_pdf = []; calc_log = []
    
    user_inputs = {'status': sel_status, 'proj_name': proj_name, 'is_parts_only': is_parts_only, 'mode': mode if not is_parts_only else "N/A", 'tfas': tfas if not is_parts_only else 0, 'days': days if not is_parts_only else 0, 'hrs': hrs if not is_parts_only else 0, 'sat': sat if not is_parts_only else False, 'sun': sun if not is_parts_only else False, 'flight_cost': flight_cost, 'miles': miles, 't_hrs': t_hrs, 'override_sub': override_sub if not is_parts_only else False, 'man_sub_days': man_sub_days if not is_parts_only else 0, 'cont_pct': cont_pct * 100 if not is_parts_only else 0, 'misc_exp': misc_exp, 'sow': sow, 'assume': assume, 'mob_date': str(mob_date), 'start_date': str(start_date), 'return_date': str(return_date), 'payment_terms': payment_terms, 'validity': validity_days, 'disable_mbv': disable_mbv}

    rates_snap = {}
    if not is_parts_only:
        rates_snap = {'rt': st.session_state.rate_rt, 'ot': st.session_state.rate_ot, 'dt': st.session_state.rate_dt, 'tr': st.session_state.rate_tr, 'cap': rt_cap}
        labor_bk, sub_days = logic.simulate_schedule(start_date, days, hrs, sat, sun, {'cap_rt_weekly': rt_cap}, is_key_account)
        calc_log.append(f"Schedule Logic: {days} Work Days, {hrs} Hrs/Day (Sat={sat}, Sun={sun}) -> RT:{labor_bk['RT']}, OT:{labor_bk['OT']}, DT:{labor_bk['DT']}")
        
        if is_commuter: t_bill_leg = man_labor / 2.0; calc_log.append(f"Travel (Commuter): Manual Override {man_labor} hours total.")
        else: t_bill_leg = logic.calculate_travel_billable(t_hrs); calc_log.append(f"Travel (Standard): {t_hrs} hrs one-way -> {t_bill_leg} hrs billable per leg (Min 8, Round up 2).")
        t_bill_total = t_bill_leg * 2.0
        
        l_tr_tot = t_bill_total * tfas * rates_snap['tr']; svc_lines.append({"Description": "TFA Labor - Travel", "Qty": t_bill_total * tfas, "Rate": rates_snap['tr'], "Total": l_tr_tot}); calc_log.append(f"Labor Travel: {tfas} TFAs * {t_bill_total} hrs * ${rates_snap['tr']} = ${l_tr_tot}")
        if labor_bk['RT']: l_rt_tot = labor_bk['RT']*tfas*rates_snap['rt']; svc_lines.append({"Description": "Labor - Onsite (RT)", "Qty": labor_bk['RT']*tfas, "Rate": rates_snap['rt'], "Total": l_rt_tot}); calc_log.append(f"Labor RT: {tfas} TFAs * {labor_bk['RT']} hrs * ${rates_snap['rt']} = ${l_rt_tot}")
        if labor_bk['OT']: l_ot_tot = labor_bk['OT']*tfas*rates_snap['ot']; svc_lines.append({"Description": "Labor - Onsite (OT)", "Qty": labor_bk['OT']*tfas, "Rate": rates_snap['ot'], "Total": l_ot_tot}); calc_log.append(f"Labor OT: {tfas} TFAs * {labor_bk['OT']} hrs * ${rates_snap['ot']} = ${l_ot_tot}")
        if labor_bk['DT']: l_dt_tot = labor_bk['DT']*tfas*rates_snap['dt']; svc_lines.append({"Description": "Labor - Onsite (DT)", "Qty": labor_bk['DT']*tfas, "Rate": rates_snap['dt'], "Total": l_dt_tot})
        
        # --- NEW: MINIMUM BILLING VALUE (MBV) GUARDRAIL ---
        if not disable_mbv:
            # 1. Define Target
            if region == "INTERNATIONAL":
                mbv_target = 160.00 * 100.0
            else:
                mbv_target = rates_snap['rt'] * 50.0
            
            # 2. Calculate Current Labor (Travel + RT/OT/DT)
            current_labor_value = 0.0
            for line in svc_lines:
                if "Labor" in line['Description']:
                    current_labor_value += line['Total']
            
            # 3. Check and Adjust
            if current_labor_value < mbv_target:
                shortfall = mbv_target - current_labor_value
                svc_lines.append({
                    "Description": f"Minimum Billing Adjustment (Target ${mbv_target:,.2f})", 
                    "Qty": 1, 
                    "Rate": shortfall, 
                    "Total": shortfall
                })
                calc_log.append(f"MBV Guardrail: Labor ${current_labor_value:,.2f} < Target ${mbv_target:,.2f}. Added Adjustment: ${shortfall:,.2f}")
            else:
                calc_log.append(f"MBV Guardrail: Labor ${current_labor_value:,.2f} meets Target ${mbv_target:,.2f}. No adjustment.")
        else:
            calc_log.append("MBV Guardrail: Disabled by user.")
        # --------------------------------------------------

        if flight_cost: f_rate = logic.smart_round(flight_cost * EXP_MARKUP); f_tot = f_rate * tfas; svc_lines.append({"Description": "Airfare", "Qty": tfas, "Rate": f_rate, "Total": f_tot}); calc_log.append(f"Airfare: {tfas} Tix * ${f_rate} (Cost ${flight_cost} + {int((EXP_MARKUP-1)*100)}%) = ${f_tot}")
        if (mode == "DRIVE" or mode == "FLY then DRIVE") and miles > 0: m_tot = logic.smart_round(miles * 1.10); svc_lines.append({"Description": "Mileage / Rental Fuel", "Qty": miles, "Rate": 1.10, "Total": m_tot})
        if misc_exp: m_rate = logic.smart_round(misc_exp * EXP_MARKUP); svc_lines.append({"Description": "Misc Expenses (Car Rental, Visa, Transport)", "Qty": 1, "Rate": m_rate, "Total": m_rate}); calc_log.append(f"Misc Exp: ${misc_exp} + Markup = ${m_rate}")
            
        final_days = man_sub_days if override_sub else trip_days; rooms = math.ceil(tfas / 2)
        lodg_rate = 0.0 if is_commuter else logic.smart_round(st.session_state.loc_rates['lodging']*1.2*EXP_MARKUP)
        mie_rate = logic.smart_round(st.session_state.loc_rates['mie']*(0.5 if is_commuter else 1.0)*EXP_MARKUP)
        
        if lodg_rate > 0: l_qty = final_days * rooms; l_tot = lodg_rate * l_qty; svc_lines.append({"Description": f"Lodging ({rooms} Room{'s' if rooms > 1 else ''})", "Qty": l_qty, "Rate": lodg_rate, "Total": l_tot}); calc_log.append(f"Lodging: {final_days} nights * {rooms} rooms * ${lodg_rate} = ${l_tot}")
        mie_qty = final_days * tfas; mie_tot = mie_rate * mie_qty; svc_lines.append({"Description": f"Subsistence ({tfas} Tech{'s' if tfas > 1 else ''})", "Qty": mie_qty, "Rate": mie_rate, "Total": mie_tot}); calc_log.append(f"Subsistence: {final_days} days * {tfas} techs * ${mie_rate} = ${mie_tot}")

    for i, row in edited_parts.iterrows():
        qty = float(row['Qty']) if row['Qty'] else 0.0
        cost = float(row['Cost']) if row['Cost'] else 0.0
        if qty > 0:
            sell, markup = logic.calculate_part_price(cost, tier_selection); sell = round(sell, 2); total = sell * qty
            part_lines_pdf.append({"Line": f"Line {i+1:02d}", "Part": row['Part #'], "Desc": row['Description'], "Qty": qty, "Rate": sell, "Total": total, "Lead": row['Lead Time']})
            calc_log.append(f"Part: {row['Part #']} Cost ${cost} -> Sell ${sell} (Markup {markup:.2f}x)")

    svc_total = sum([x['Total'] for x in svc_lines]); parts_total = sum([x['Total'] for x in part_lines_pdf])
    c_cost = 0.0
    if not is_parts_only and cont_pct > 0: c_cost = logic.smart_round((svc_total + parts_total) * cont_pct); svc_lines.append({"Description": "Contingency", "Qty": 1, "Rate": c_cost, "Total": c_cost}); calc_log.append(f"Contingency: {cont_pct*100}% of (${svc_total} + ${parts_total}) = ${c_cost}"); svc_total += c_cost

    grand_total = svc_total + parts_total
    st.success(f"### Grand Total: ${grand_total:,.2f}")
    proj_data = {"Project": proj_name, "Site": final_site, "Region": region, "Start": mob_date.strftime("%Y-%m-%d") if mob_date else "N/A", "Return": return_date.strftime("%Y-%m-%d") if return_date else "N/A", "SOW": sow, "Assumptions": assume, "ManualClient": sel_site_data['Company']}
    totals = {"Service": svc_total, "Parts": parts_total, "Grand": grand_total}
    all_lines = svc_lines + [{'Description': p['Desc'], 'Qty': p['Qty'], 'Rate': p['Rate'], 'Total': p['Total']} for p in part_lines_pdf]
    audit_text = logic.generate_audit_text(proj_data, all_lines, totals, rates_snap, user_inputs, calc_log)
    json_str = json.dumps(user_inputs, indent=4)

    try:
        pdf_bytes = pdf_gen.generate_pdf(proj_data, svc_lines, part_lines_pdf, sel_site_data, totals, is_parts_only, rates_snap if not is_parts_only else None, EXP_MARKUP if not is_parts_only else None)
        with t_prev: st.dataframe(pd.DataFrame(svc_lines if not is_parts_only else part_lines_pdf)); st.download_button("💾 Download PDF", data=pdf_bytes, file_name=f"{proj_name}_v2.9.3.pdf", mime="application/pdf")
        with t_text:
            st.subheader("💾 Save / Audit"); st.download_button("📥 Save Quote to JSON", data=json_str, file_name=f"{proj_name}_DATA.json", mime="application/json")
            st.markdown("---"); st.text_area("Audit Record (Text)", value=audit_text, height=400); st.download_button("💾 Download Text Record", data=audit_text, file_name=f"{proj_name}_RECORD.txt", mime="text/plain")
    except Exception as e: st.error(f"PDF Error: {e}")