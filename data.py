# src/data.py
# ======================================================
# AFP ESTIMATOR - DATA MODULE
# Version: v2.9.2 (External Templates Fix)
# Updated: 2026-01-23
# Description: Handles CSV loading, Rate Lookups, and External Template Loading.
# ======================================================

import pandas as pd
import os
import streamlit as st
import glob

@st.cache_resource
def get_data_dir():
    """Smart Path Finder for Shared_Data."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        check_path = os.path.join(current_dir, "Shared_Data")
        if os.path.exists(check_path): return check_path
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir: break
        current_dir = parent_dir
    return "Shared_Data"

DATA_DIR = get_data_dir()

@st.cache_data
def load_client_db():
    comp_path = os.path.join(DATA_DIR, "companies.csv")
    loc_path = os.path.join(DATA_DIR, "locations.csv")
    if not os.path.exists(comp_path) or not os.path.exists(loc_path): return pd.DataFrame(), pd.DataFrame()
    try:
        df_comp = pd.read_csv(comp_path); df_comp.columns = df_comp.columns.str.lower().str.strip()
        if 'name' in df_comp.columns: df_comp = df_comp[['name']].rename(columns={'name': 'company_name'}).drop_duplicates()
        else: return pd.DataFrame(), pd.DataFrame()
        
        df_loc = pd.read_csv(loc_path); df_loc.columns = df_loc.columns.str.lower().str.strip()
        col_map = {'company': 'company_name', 'location_name': 'site_name', 'street': 'street', 'city': 'city', 'state': 'state', 'postalcode': 'zip'}
        valid_cols = [c for c in col_map.keys() if c in df_loc.columns]
        df_loc = df_loc[valid_cols].rename(columns=col_map); df_loc.fillna('', inplace=True)
        return df_comp, df_loc
    except: return pd.DataFrame(), pd.DataFrame()

def get_domestic_rate(zip_code, travel_date):
    path = os.path.join(DATA_DIR, "FY2026_GSA_ZipCodeFile.csv")
    if not os.path.exists(path): return None
    try:
        df = pd.read_csv(path, dtype={'Zip': str})
        row = df[df['Zip'] == str(zip_code).zfill(5)]
        if not row.empty:
            month_col = travel_date.strftime("%b")
            try: lodging = float(row.iloc[0].get(month_col, 110.0))
            except: lodging = 110.0
            return {"lodging": lodging, "mie": float(row.iloc[0]['Meals']), "city": row.iloc[0]['Name']}
    except: pass
    return None

def get_international_options(country_search):
    path = os.path.join(DATA_DIR, "2026-01_Dept-of-State_PerDiem_PD.csv")
    if not os.path.exists(path): return []
    try:
        df = pd.read_csv(path)
        matches = df[df['Country'].str.contains(country_search, case=False, na=False)]
        if not matches.empty: return matches[['Country', 'Location']].drop_duplicates().to_dict('records')
    except: pass
    return []

def get_international_rate(country, city):
    path = os.path.join(DATA_DIR, "2026-01_Dept-of-State_PerDiem_PD.csv")
    if not os.path.exists(path): return None
    try:
        df = pd.read_csv(path)
        match = df[(df['Country'] == country) & (df['Location'] == city)]
        if not match.empty:
            rec = match.iloc[0]
            l_rate = float(rec['Lodging']); 
            if l_rate == 0: l_rate = 150.0
            return {"lodging": l_rate, "mie": float(rec['Meals & Incidentals']), "city": rec['Location'], "country": rec['Country']}
    except: pass
    return None

def get_term_templates():
    """
    Scans 'Shared_Data/Templates' for .md files.
    Returns dict: {Filename (no ext): Content}
    """
    template_dir = os.path.join(DATA_DIR, "Templates")
    templates = {}
    
    if not os.path.exists(template_dir):
        return {"Error": "Templates folder missing in Shared_Data"}
        
    # Look for .md files
    for file_path in glob.glob(os.path.join(template_dir, "*.md")):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                templates[file_name] = f.read()
        except Exception as e:
            templates[f"Error loading {file_name}"] = str(e)
            
    return templates