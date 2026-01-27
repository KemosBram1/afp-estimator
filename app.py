import streamlit as st
import pandas as pd
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="AFP Quote Estimator",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("💰 AFP Quote Estimator")
st.markdown("### Generate accurate quotes for your projects")

# Sidebar for project information
st.sidebar.header("Project Information")
project_name = st.sidebar.text_input("Project Name", "New Project")
client_name = st.sidebar.text_input("Client Name", "")
quote_date = st.sidebar.date_input("Quote Date", datetime.now())

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Cost Breakdown")
    
    # Labor costs
    st.subheader("Labor Costs")
    labor_hours = st.number_input("Estimated Labor Hours", min_value=0.0, value=40.0, step=0.5)
    hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=75.0, step=5.0)
    labor_cost = labor_hours * hourly_rate
    
    # Material costs
    st.subheader("Material Costs")
    material_cost = st.number_input("Total Material Costs ($)", min_value=0.0, value=500.0, step=50.0)
    
    # Additional costs
    st.subheader("Additional Costs")
    equipment_cost = st.number_input("Equipment/Tools ($)", min_value=0.0, value=200.0, step=50.0)
    travel_cost = st.number_input("Travel/Transportation ($)", min_value=0.0, value=100.0, step=25.0)
    misc_cost = st.number_input("Miscellaneous ($)", min_value=0.0, value=50.0, step=10.0)
    
    # Markup percentage
    st.subheader("Markup")
    markup_percentage = st.slider("Markup Percentage (%)", min_value=0, max_value=100, value=20, step=5)

with col2:
    st.header("Quote Summary")
    
    # Calculate totals
    subtotal = labor_cost + material_cost + equipment_cost + travel_cost + misc_cost
    markup_amount = subtotal * (markup_percentage / 100)
    total = subtotal + markup_amount
    
    # Display summary
    st.metric("Subtotal", f"${subtotal:,.2f}")
    st.metric("Markup", f"${markup_amount:,.2f}", f"{markup_percentage}%")
    st.metric("Total Quote", f"${total:,.2f}", delta=None)
    
    st.divider()
    
    # Breakdown table
    st.subheader("Cost Breakdown")
    breakdown_data = {
        "Item": ["Labor", "Materials", "Equipment", "Travel", "Miscellaneous", "Markup"],
        "Amount": [
            f"${labor_cost:,.2f}",
            f"${material_cost:,.2f}",
            f"${equipment_cost:,.2f}",
            f"${travel_cost:,.2f}",
            f"${misc_cost:,.2f}",
            f"${markup_amount:,.2f}"
        ]
    }
    st.table(pd.DataFrame(breakdown_data))

# Export section
st.divider()
st.header("Export Quote")

# Sanitize filename
def sanitize_filename(filename):
    """Remove or replace invalid filename characters"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # If empty after sanitization, use default
    return filename if filename else 'quote'

safe_project_name = sanitize_filename(project_name)

col3, col4 = st.columns(2)

with col3:
    # Generate quote text
    quote_text = f"""
QUOTE ESTIMATE
==============

Project: {project_name}
Client: {client_name}
Date: {quote_date}

COST BREAKDOWN:
--------------
Labor ({labor_hours} hours @ ${hourly_rate}/hr): ${labor_cost:,.2f}
Materials: ${material_cost:,.2f}
Equipment: ${equipment_cost:,.2f}
Travel: ${travel_cost:,.2f}
Miscellaneous: ${misc_cost:,.2f}

Subtotal: ${subtotal:,.2f}
Markup ({markup_percentage}%): ${markup_amount:,.2f}

TOTAL QUOTE: ${total:,.2f}
"""
    
    st.download_button(
        label="Download Quote as Text",
        data=quote_text,
        file_name=f"quote_{safe_project_name}_{quote_date}.txt",
        mime="text/plain"
    )

with col4:
    # Create CSV data
    csv_data = pd.DataFrame({
        "Category": ["Labor", "Materials", "Equipment", "Travel", "Miscellaneous", "Subtotal", "Markup", "Total"],
        "Amount": [labor_cost, material_cost, equipment_cost, travel_cost, misc_cost, subtotal, markup_amount, total]
    })
    
    st.download_button(
        label="Download Quote as CSV",
        data=csv_data.to_csv(index=False),
        file_name=f"quote_{safe_project_name}_{quote_date}.csv",
        mime="text/csv"
    )

# Footer
st.divider()
st.caption("AFP Quote Estimator - Professional quote generation made easy")
