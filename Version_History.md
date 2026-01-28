# Version History: AFP Field Service Estimator

This document tracks the development lifecycle of the **AFP Field Service Estimator**, detailing the evolution from an initial monolithic script to the current modular, enterprise-grade application.

---

## **v2.9 Series: Enterprise Refinements & Stability**

### **v2.9.3** (2026-01-23)
* **Feature: Minimum Billing Value (MBV) Guardrail:** Implemented automatic logic to ensure total labor value meets regional minimum thresholds ($7,000 Domestic / $16,000 International).
* **Feature: Adjustment Line Item:** System automatically adds a "Minimum Billing Adjustment" line item to the quote if the calculated labor falls short of the MBV target.
* **Feature: MBV Override:** Added a "Disable Min Billing Guardrail" checkbox to the sidebar, allowing users to bypass the automatic adjustment logic.
* **Fix: Version Header:** Restored the comprehensive version tracking table to the header of `app.py`.

### **v2.9.2** (2026-01-23)
* **Architecture: External Templates:** Updated the Template Engine in `data.py` to scan an external `Shared_Data/Templates/` folder for `.md` files, replacing the temporary hardcoded dictionary.
* **Integration:** Aligned `app.py` to use the dynamic `ctx` dictionary for injecting live values (e.g., `{mbv_domestic}`) into external templates.

### **v2.9.1** (2026-01-23)
* **Feature: Dynamic Template Variables:** Markdown templates now support placeholders like `{rate_rt}`, `{payment_terms}`, and `{validity}` for live data injection.
* **UI: Commercial Terms:** Added sidebar inputs for "Net Terms" and "Validity Days" (defaulting to 30).
* **Logic: Context Injection:** Created the `ctx` context dictionary in `app.py` to map session state values to template placeholders during the "Apply" action.

### **v2.9** (2026-01-23)
* **Core Logic: Smart Schedule:** Implemented `calculate_onsite_duration` logic. The system now correctly accounts for non-working weekends when calculating the Return Date (e.g., a 5-day job starting Tuesday now correctly ends the following Monday/Tuesday, rather than over the weekend).
* **UI: Live Recalculation:** Added callbacks to "Work Days", "Sat", "Sun", and "Start Date" inputs to instantly update the "Return Date" field.
* **Output: Enhanced Markdown:** Upgraded the parser in `pdf_gen.py` to support Headers (H1-H3), Blockquotes (`>`), and nested Bold/Italics.

---

## **v2.8 Series: Template Engine**

### **v2.8** (2026-01-23)
* **Feature: T&C Template Engine:** Added functionality for users to select pre-defined Terms & Conditions templates (e.g., "AERO", "Standard", "International") from a dropdown in the Notes tab.
* **Data Layer:** Added `get_term_templates()` to `data.py` to manage the library of legal text.

---

## **v2.7 Series: Persistence & State**

### **v2.7** (2026-01-23)
* **Feature: Save/Load System:** Added functionality to export the current quote state to a JSON file and reload it later to restore all inputs exactly as they were.
* **Feature: Status Tracker:** Added a "Quote Status" dropdown (Draft, Submitted, Won, Lost) to track the lifecycle of a quote.
* **Output:** The JSON save file includes all sidebar inputs, rates, and the selected status.

---

## **v2.6 Series: Audit & Critical Fixes**

### **v2.6** (2026-01-23)
* **Critical Fix: Subsistence Logic:** Corrected quantities for Lodging and Subsistence. Lodging now multiplies `Days × Rooms`, and Subsistence multiplies `Days × Techs`.
* **Feature: Audit Trail:** Added a "Calculation Breakdown" section to the text audit log. This "sausage making" view details exactly how every line item total was derived (e.g., `11.0 hrs -> 12.0 billable * $160`).
* **Polish:** Tightened PDF table row heights and added "Expenses: Cost + 15%" to the Terms section.

---

## **v2.5 Series: Schedule & Travel Rules**

### **v2.5** (2026-01-23)
* **Logic: Date-Based Schedule:** Replaced simple "Travel Days" logic with strict Date-Based Logic (Mobilization Date -> Onsite Start -> Return Date).
* **Logic: Travel Labor Rules:** Implemented rule: Minimum 8 hours per leg; actuals >8 hours rounded up to the nearest 2-hour increment.
* **Feature: Contingency Unlocked:** Removed the 5% floor for contingency, allowing 0% or 1%.
* **UI:** Clarified "Misc Expenses" label to include "(Car Rental, Visa, Transport)".

---

## **v2.4 Series: Architecture & Features**

### **v2.4** (2026-01-23)
* **Architecture: Modular Refactor:** Split the monolithic `app.py` into `src/app.py`, `src/logic.py`, `src/data.py`, and `src/pdf_gen.py`.
* **Feature: Travel Modes:** Added "FLY then DRIVE" travel mode for scenarios involving both flights and significant rental car travel.
* **Feature: Commuter Rule Fix:** Logic now triggers "Commuter Mode" (No Lodging, 50% M&I) strictly based on miles < 50, regardless of the travel mode selected.
* **Output:** Split the PDF output into two distinct tables: "Service & Expenses" vs. "Parts & Materials".

---

## **v2.3 Series: Refinements**

### **v2.3**
* **UI: GPS Integration:** Added "GPS Coordinates" lookup link/button to assist with mileage calculations.
* **Logic: Early Commuter Logic:** Adjusted subsistence logic to automatically zero out Lodging if the "Drive" option was selected with <50 miles.

---

## **v2.0 - v2.2 Series: Web Application & Data Integration**

### **v2.2**
* **Feature: Advanced Pricing Logic:** Introduced the "Rational Decay Curve" for parts pricing, replacing static markups.
* **Logic:** Refined Part Price calculation to include Freight Burden (3.5%) and Inflation Adjustment factors.
* **UI:** Added the "Pricing Tier" slider (Standard vs. Preferred) to adjust markup ceilings and floors.

### **v2.1**
* **Data: Client Database Integration:** Connected the application to `companies.csv` and `locations.csv`.
* **UI:** Replaced manual text inputs for Client/Site with Dropdown Selectors, auto-filling address fields.
* **Logic:** Implemented basic GSA Rate lookup scaffolding.

### **v2.0**
* **Platform Shift:** Migrated from local Python script to **Streamlit Web Application**.
* **UI:** Introduced the Sidebar navigation for inputs and Tabbed interface for "Project", "Travel", "Schedule", and "Parts".
* **Output:** Integrated `fpdf` library to generate professional PDF quotes directly from the browser.

---

## **v1.x Series: MVP & Scripting Era**

### **v1.9.3 (The "Stable Monolith")**
* **Architecture:** Final stable version of the single-file script (`app.py`).
* **Feature:** Added the "Text Record" tab for basic auditing of user inputs.
* **Logic:** Established the core labor buckets (RT/OT/DT) and "Smart Rounding" (up to nearest $10) for pricing.

### **v1.5 - v1.8**
* **v1.8:** Added support for "Parts Only" quote type, hiding irrelevant service inputs.
* **v1.7:** Refined Overtime Logic: Introduced the "Weekly Cap" (40 vs 45 hours) to trigger OT automatically.
* **v1.6:** Added "International" vs "Domestic" region toggle, adjusting base labor rates ($140 vs $160).
* **v1.5:** Initial PDF Generation capability (replacing console text output).

### **v1.0 - v1.4**
* **v1.4:** Added "Misc Expenses" and "Contingency" fields.
* **v1.2:** Implemented basic `Haversine` formula for calculating distance between GPS coordinates.
* **v1.0:** Proof of Concept. Command-line interface accepting days/hours and printing a total cost estimate.