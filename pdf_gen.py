# src/pdf_gen.py
# ======================================================
# AFP ESTIMATOR - PDF GENERATION MODULE
# Version: v2.9.5
# Updated: 2026-01-26
# Description: Generates PDF quotes. 
#              v2.9.5 adds Markdown Table support, Emoji sanitization, 
#              and "Rate Schedule" page breaks.
# ======================================================

from fpdf import FPDF
import datetime
import os
from data import DATA_DIR 

class PDF(FPDF):
    def header(self):
        logo = "afp_logo.jpg"
        if not os.path.exists(logo): logo = os.path.join(DATA_DIR, "afp_logo.jpg")
        if os.path.exists(logo): self.image(logo, 10, 8, 30)
        
        self.set_y(10); self.set_font('Arial', 'B', 14); self.set_text_color(192, 0, 0)
        self.cell(0, 5, 'AFP CORP dba Associated Fire Protection', 0, 1, 'R')
        self.set_font('Arial', '', 9); self.set_text_color(0, 0, 0)
        self.cell(0, 4, '4905 South 97th Street', 0, 1, 'R')
        self.cell(0, 4, 'Omaha, NE 68127', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-35)
        iso_path = "iso_logo.jpg"
        if not os.path.exists(iso_path): iso_path = os.path.join(DATA_DIR, "iso_logo.jpg")
        if not os.path.exists(iso_path): iso_path = os.path.join(DATA_DIR, "iso_logo.png")
        
        if os.path.exists(iso_path): self.image(iso_path, 170, self.get_y(), 26)
        
        self.set_font('Arial', 'I', 7); self.set_text_color(100, 100, 100)
        self.multi_cell(140, 3, "AFP Confidentiality: This quote is privileged information intended for the addressee only.")
        self.set_y(-15); self.set_font('Arial', 'I', 8); self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_table_row(self, col_data, col_widths, align):
        """Standard row renderer for Service/Parts tables."""
        x_start = self.get_x(); y_start = self.get_y()
        self.multi_cell(col_widths[0], 5, col_data[0], 0, align[0], False)
        row_h = max(self.get_y() - y_start, 5.5) 
        
        self.set_xy(x_start, y_start)
        self.multi_cell(col_widths[0], 5, col_data[0], 1, align[0])
        next_x = x_start + col_widths[0]
        for i in range(1, len(col_data)):
            self.set_xy(next_x, y_start)
            self.cell(col_widths[i], row_h, str(col_data[i]), 1, 0, align[i])
            next_x += col_widths[i]
        self.ln(row_h)

    def add_dynamic_row(self, col_data, col_widths, align):
        """
        Robust row renderer for Markdown Tables. 
        Calculates max height across ALL columns (allowing wrapping in any column).
        """
        x_start = self.get_x()
        y_start = self.get_y()
        max_y = y_start
        
        # 1. Determine Max Height
        for i, text in enumerate(col_data):
            self.set_xy(x_start + sum(col_widths[:i]), y_start)
            self.multi_cell(col_widths[i], 5, str(text), 0, align[i])
            if self.get_y() > max_y:
                max_y = self.get_y()
        
        row_h = max(max_y - y_start, 6) # Min height 6
        
        # 2. Draw Borders
        for i in range(len(col_widths)):
             x = x_start + sum(col_widths[:i])
             self.rect(x, y_start, col_widths[i], row_h)
             
        # 3. Draw Text
        for i, text in enumerate(col_data):
            self.set_xy(x_start + sum(col_widths[:i]), y_start)
            self.multi_cell(col_widths[i], 5, str(text), 0, align[i])
            
        self.set_xy(x_start, y_start + row_h)

    def write_markdown(self, text):
        """
        Enhanced Markdown Parser.
        Supports: Tables, H1-H3, Blockquotes, Lists, Bold, Italics.
        Includes Emoji Sanitization.
        """
        if not text: return
        
        # --- SANITIZE ---
        # Strip unsupported characters (Emojis) to prevent crashes
        text = text.encode('latin-1', 'ignore').decode('latin-1')
        
        lines = text.split('\n')
        table_buffer = []
        
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        
        for line in lines:
            raw = line.strip()
            
            # --- TABLE DETECTION ---
            if raw.startswith('|'):
                table_buffer.append(raw)
                continue
            
            # If buffer has content, render table now
            if table_buffer:
                self._render_markdown_table(table_buffer)
                table_buffer = []
            
            # --- HEADERS ---
            if raw.startswith('# '):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 6, raw[2:], 0, 1)
                self.set_font('Arial', '', 9)
            elif raw.startswith('## '):
                self.set_font('Arial', 'B', 10)
                self.cell(0, 5, raw[3:], 0, 1)
                self.set_font('Arial', '', 9)
            elif raw.startswith('### '):
                self.set_font('Arial', 'BI', 9)
                self.cell(0, 5, raw[4:], 0, 1)
                self.set_font('Arial', '', 9)
                
            # --- BLOCKQUOTES ---
            elif raw.startswith('> '):
                self.set_x(15); self.set_text_color(80, 80, 80); self.set_font('Arial', 'I', 9)
                self.multi_cell(0, 5, raw[2:])
                self.set_font('Arial', '', 9); self.set_text_color(0, 0, 0)
                
            # --- LISTS ---
            elif raw.startswith('- ') or raw.startswith('* '):
                self.set_x(15); self.cell(5, 5, chr(149), 0, 0)
                self._parse_inline(raw[2:]); self.ln()
            elif len(raw) > 2 and raw[0].isdigit() and raw[1] == '.':
                self.set_x(15); dot = raw.find('.'); self.cell(8, 5, raw[:dot+1], 0, 0)
                self._parse_inline(raw[dot+1:].strip()); self.ln()
                
            # --- TEXT ---
            else:
                if raw: 
                    self.set_x(10); self._parse_inline(raw); self.ln()
                    
        # Flush remaining table
        if table_buffer: self._render_markdown_table(table_buffer)

    def _render_markdown_table(self, lines):
        if not lines: return
        
        # 1. Parse Header
        header = [h.strip() for h in lines[0].split('|') if h.strip()]
        
        # 2. Determine Widths (Heuristic for 3-col rate tables)
        # Default Layout: [Description, Rate, Notes] -> [50, 40, 100]
        widths = [50, 40, 100]
        if len(header) != 3:
            # Fallback: Equal width
            w = 190 / max(1, len(header))
            widths = [w] * len(header)
            
        # 3. Skip Separator Row (lines like |---|)
        start_row = 1
        if len(lines) > 1 and '---' in lines[1]:
            start_row = 2
            
        # 4. Render Header
        self.set_font('Arial', 'B', 9); self.set_fill_color(240, 240, 240)
        for i, h in enumerate(header):
            if i < len(widths): self.cell(widths[i], 6, h, 1, 0, 'L', 1)
        self.ln()
        
        # 5. Render Rows
        self.set_font('Arial', '', 9)
        for i in range(start_row, len(lines)):
            row_raw = lines[i]
            # Split and clean bold markers from data (PDF looks cleaner without ** chars)
            cols = [c.strip().replace('**', '') for c in row_raw.split('|') if c.strip()]
            
            # Pad or truncate columns to match header
            if len(cols) < len(widths): cols += [''] * (len(widths) - len(cols))
            if len(cols) > len(widths): cols = cols[:len(widths)]
            
            self.add_dynamic_row(cols, widths, ['L']*len(widths))
        
        self.ln(2)

    def _parse_inline(self, text):
        parts_bold = text.split('**')
        for i, part in enumerate(parts_bold):
            is_bold = (i % 2 == 1)
            parts_italic = part.split('*')
            for j, subpart in enumerate(parts_italic):
                is_italic = (j % 2 == 1)
                style = ''
                if is_bold: style += 'B'
                if is_italic: style += 'I'
                self.set_font('Arial', style, 9)
                self.write(5, subpart)

def generate_pdf(proj_data, svc_lines, part_lines, client_data, totals, is_parts_only, rates=None, exp_markup=None):
    pdf = PDF(); pdf.set_auto_page_break(auto=True, margin=15); pdf.add_page()
    
    # Metadata
    pdf.set_font('Arial', 'B', 9); y = pdf.get_y(); left = 130
    pdf.set_xy(left, y); pdf.cell(30, 6, "Quote Date:", 1, 0)
    pdf.set_font('Arial', '', 9); pdf.cell(30, 6, datetime.date.today().strftime("%m/%d/%Y"), 1, 1, 'R')
    pdf.set_xy(left, y+6); pdf.set_font('Arial', 'B', 9); pdf.cell(30, 6, "Valid Until:", 1, 0)
    pdf.set_font('Arial', '', 9); pdf.cell(30, 6, (datetime.date.today()+datetime.timedelta(days=30)).strftime("%m/%d/%Y"), 1, 1, 'R')
    
    # Client
    pdf.set_xy(10, y); pdf.set_font('Arial', 'B', 10); pdf.cell(100, 5, "Quote For:", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(100, 5, client_data.get('Company', proj_data.get('ManualClient', '')), 0, 1)
    if client_data.get('Street'): pdf.cell(100, 5, str(client_data['Street']), 0, 1)
    city_line = f"{client_data.get('City','')}, {client_data.get('State','')} {client_data.get('Zip','')}"
    if len(city_line) > 3: pdf.cell(100, 5, city_line, 0, 1)
    pdf.ln(8)
    
    # Header
    pdf.set_font('Arial', 'B', 12); pdf.set_fill_color(230, 230, 230)
    label = "Reference:" if is_parts_only else "Project:"
    pdf.cell(0, 8, f"{label} {proj_data['Project']}", 1, 1, 'L', 1)
    
    pdf.set_font('Arial', '', 10)
    if not is_parts_only:
        pdf.cell(25, 6, "Site:", 0, 0); pdf.cell(0, 6, f"{proj_data['Site']} ({proj_data['Region']})", 0, 1)
        pdf.cell(25, 6, "Dispatch:", 0, 0); pdf.cell(40, 6, proj_data['Start'], 0, 0)
        pdf.cell(25, 6, "Return:", 0, 0); pdf.cell(0, 6, proj_data['Return'], 0, 1)
    else:
        pdf.cell(25, 6, "Type:", 0, 0); pdf.cell(0, 6, "Parts / Materials Only", 0, 1)
    pdf.ln(4)
    
    # SOW
    pdf.set_font('Arial', 'B', 10); pdf.cell(0, 6, "Scope of Work / Notes:", 0, 1)
    pdf.write_markdown(proj_data['SOW'])
    pdf.ln(5)

    # TABLE 1: SERVICE
    if svc_lines:
        pdf.set_font('Arial', 'B', 9); pdf.set_fill_color(240, 240, 240)
        pdf.cell(100, 6, "Service & Expenses", 1, 0, 'L', 1)
        pdf.cell(20, 6, "Qty", 1, 0, 'C', 1); pdf.cell(35, 6, "Rate", 1, 0, 'R', 1); pdf.cell(35, 6, "Total", 1, 1, 'R', 1)
        pdf.ln()
        pdf.set_font('Arial', '', 9)
        for l in svc_lines:
            pdf.add_table_row([l['Description'], f"{l['Qty']:.1f}", f"${l['Rate']:,.2f}", f"${l['Total']:,.2f}"], [100, 20, 35, 35], ['L', 'C', 'R', 'R'])
        
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(155, 6, "Service Subtotal:", 0, 0, 'R'); pdf.cell(35, 6, f"${totals['Service']:,.2f}", 1, 1, 'R')
        pdf.ln(5)

    # TABLE 2: PARTS
    if part_lines:
        pdf.set_font('Arial', 'B', 9); pdf.set_fill_color(240, 240, 240)
        w = [75, 15, 25, 25, 50]
        pdf.cell(w[0], 6, "Line Item", 1, 0, 'L', 1); pdf.cell(w[1], 6, "Qty", 1, 0, 'C', 1)
        pdf.cell(w[2], 6, "Price Ea.", 1, 0, 'R', 1); pdf.cell(w[3], 6, "Total", 1, 0, 'R', 1)
        pdf.cell(w[4], 6, "Lead Time", 1, 1, 'L', 1); pdf.ln()
        
        pdf.set_font('Arial', '', 8)
        for p in part_lines:
            line_str = f"{p['Line']} - {p['Part']} - {p['Desc']}"
            pdf.add_table_row([line_str, str(p['Qty']), f"${p['Rate']:,.2f}", f"${p['Total']:,.2f}", p['Lead']], w, ['L', 'C', 'R', 'R', 'L'])
            
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(140, 6, "Parts Subtotal:", 0, 0, 'R'); pdf.cell(25, 6, f"${totals['Parts']:,.2f}", 1, 1, 'R')
        pdf.ln(5)

    # Grand Total
    pdf.ln(2); pdf.set_font('Arial', 'B', 12); pdf.set_x(130)
    pdf.cell(25, 8, "TOTAL:", 0, 0, 'R'); pdf.cell(35, 8, f"${totals['Grand']:,.2f}", 1, 1, 'R')
    
    # -------------------------------------------------------------
    # PAGE BREAK BEFORE RATES/TERMS
    # -------------------------------------------------------------
    pdf.add_page()
    # -------------------------------------------------------------

    # Rate Schedule (Hardcoded - Kept for reference, but after page break)
    if not is_parts_only and rates:
        pdf.set_font('Arial', 'B', 9); pdf.cell(0, 5, "Rate Schedule (Reference):", 0, 1)
        pdf.set_font('Arial', '', 8); w = 45
        pdf.cell(w, 5, f"Standard Labor: ${rates['rt']:.2f}/hr", 0, 0)
        pdf.cell(w, 5, f"Overtime: ${rates['ot']:.2f}/hr", 0, 0)
        pdf.cell(w, 5, f"Doubletime: ${rates['dt']:.2f}/hr", 0, 1)
        pdf.cell(w, 5, f"Travel Rate: ${rates['tr']:.2f}/hr", 0, 0)
        cutoff_txt = "> 45 Hrs (Cumulative)" if rates.get('cap') == 45 else "> 40 Hrs (Weekly)"
        pdf.cell(w, 5, f"OT Threshold: {cutoff_txt}", 0, 1)
        if exp_markup:
            markup_pct = int(round((exp_markup-1)*100))
            pdf.cell(w, 5, f"Expenses: Cost + {markup_pct}%", 0, 1)
        pdf.ln(5)

    # Terms (Markdown with Table Support)
    pdf.set_font('Arial', 'B', 9); pdf.cell(0, 5, "Terms & Conditions:", 0, 1)
    pdf.write_markdown(proj_data['Assumptions'])
    
    pdf.set_font('Arial', '', 8)
    std_terms = "\n- Payment Net 30.\n- Validity 30 days."
    if not is_parts_only: std_terms += "\n- Travel Billed at Straight Time."
    pdf.write_markdown(std_terms)
    
    return pdf.output(dest='S').encode('latin-1')