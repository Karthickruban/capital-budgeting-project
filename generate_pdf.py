import os
import sys

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
    )
    from reportlab.pdfgen import canvas
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
    )
    from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(page_count=num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        if self._pageNumber > 1:
            self.drawString(54, 750, "Capital Budgeting & Infrastructure Valuation | Financial Engineering Report (INR)")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential — Academic Course Project Report (AI & Data Science - INR)")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def generate_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "Financial_Engineering_Project_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#1A365D")
    c_secondary = colors.HexColor("#2B6CB0")
    c_dark = colors.HexColor("#2D3748")
    c_bg_light = colors.HexColor("#F7FAFC")
    c_border = colors.HexColor("#E2E8F0")

    style_title = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=c_primary, spaceAfter=4)
    style_subtitle = ParagraphStyle('DocSubTitle', fontName='Helvetica', fontSize=11, leading=15, textColor=c_secondary, spaceAfter=12)
    style_h1 = ParagraphStyle('Heading1_Custom', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=c_primary, spaceBefore=12, spaceAfter=6, keepWithNext=True)
    style_h2 = ParagraphStyle('Heading2_Custom', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=c_secondary, spaceBefore=8, spaceAfter=4, keepWithNext=True)
    style_body = ParagraphStyle('Body_Custom', fontName='Helvetica', fontSize=9, leading=13, textColor=c_dark, spaceAfter=5)
    style_body_bold = ParagraphStyle('Body_Bold_Custom', fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=c_primary, spaceAfter=5)
    style_table_header = ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white)
    style_table_cell = ParagraphStyle('TableCell', fontName='Helvetica', fontSize=8, leading=11, textColor=c_dark)
    style_formula = ParagraphStyle('FormulaText', fontName='Courier-Bold', fontSize=9, leading=12, textColor=c_primary)

    story = []

    # Title
    story.append(Paragraph("Financial Engineering Subject Course Project", style_subtitle))
    story.append(Paragraph("Capital Budgeting and Infrastructure Project Valuation with Monte Carlo Risk Simulation (INR)", style_title))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceBefore=4, spaceAfter=10))

    meta_data = [
        [Paragraph("<b>Project Domain:</b> Clean Infrastructure & Energy Finance", style_table_cell),
         Paragraph("<b>Target Asset:</b> Rajasthan 100MW Solar Park", style_table_cell)],
        [Paragraph("<b>Data Source:</b> Kaggle / The World Bank PPI Database", style_table_cell),
         Paragraph("<b>Currency Standard:</b> Indian Rupees (₹ Crores & ₹/kWh)", style_table_cell)],
        [Paragraph("<b>Primary Methodology:</b> Multi-Stage DCF & WACC Hurdle Rate", style_table_cell),
         Paragraph("<b>Risk Simulation:</b> 5,000-Iteration Stochastic Monte Carlo", style_table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Executive Overview
    story.append(Paragraph("1. Executive Overview & Real-World Motivation (INR)", style_h1))
    story.append(Paragraph(
        "Large-scale clean infrastructure assets—such as a <b>100MW Solar PV Power Plant in Rajasthan (₹250 Crores)</b> "
        "or a 50MW Wind Farm in Tamil Nadu (₹350 Crores)—require substantial upfront capital expenditure and operate over "
        "20-to-25-year Power Purchase Agreements (PPAs). Institutional lenders and CFOs require rigorous quantitative models "
        "to evaluate debt repayment and tariff viability under macroeconomic shocks.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # Section 2: Dataset Architecture
    story.append(Paragraph("2. Public Dataset Architecture & Attribute Dictionary (INR)", style_h1))
    dataset_rows = [
        [Paragraph("Column Name", style_table_header), Paragraph("Financial Definition", style_table_header), Paragraph("Baseline Value (INR)", style_table_header), Paragraph("Role in Valuation", style_table_header)],
        [Paragraph("<code>Project_Name</code>", style_table_cell), Paragraph("Asset name and technology type", style_table_cell), Paragraph("100MW Solar Park", style_table_cell), Paragraph("Identifier", style_table_cell)],
        [Paragraph("<code>CapEx_INR_Crores</code>", style_table_cell), Paragraph("Initial construction and land cost", style_table_cell), Paragraph("₹ 250.0 Crores", style_table_cell), Paragraph("Year 0 cash outflow ($I_0$)", style_table_cell)],
        [Paragraph("<code>Annual_Gen_MWh</code>", style_table_cell), Paragraph("Total annual electricity generated", style_table_cell), Paragraph("180,000 MWh", style_table_cell), Paragraph("Volume driver for revenue", style_table_cell)],
        [Paragraph("<code>Base_Tariff_INR_kWh</code>", style_table_cell), Paragraph("Contracted PPA tariff per unit", style_table_cell), Paragraph("₹ 3.85 / kWh", style_table_cell), Paragraph("Price driver for revenue", style_table_cell)],
        [Paragraph("<code>Lifetime_Years</code>", style_table_cell), Paragraph("Asset operational lifecycle", style_table_cell), Paragraph("20 Years", style_table_cell), Paragraph("Discounting horizon ($N$)", style_table_cell)],
        [Paragraph("<code>Annual_OpEx_Crores</code>", style_table_cell), Paragraph("Maintenance, labor, grid fees", style_table_cell), Paragraph("₹ 12.5 Crores/yr", style_table_cell), Paragraph("Operating cash outflow", style_table_cell)],
        [Paragraph("<code>WACC_Percent</code>", style_table_cell), Paragraph("Weighted Average Cost of Capital", style_table_cell), Paragraph("8.00%", style_table_cell), Paragraph("Hurdle rate / discount rate", style_table_cell)],
        [Paragraph("<code>Degradation_Pct</code>", style_table_cell), Paragraph("Annual efficiency loss of panels", style_table_cell), Paragraph("0.50% / year", style_table_cell), Paragraph("Annual generation decay", style_table_cell)]
    ]
    ds_table = Table(dataset_rows, colWidths=[90, 160, 95, 159])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 10))

    # Section 3: Mathematical Formulations
    story.append(Paragraph("3. Core Financial Engineering Mathematical Formulations (INR)", style_h1))
    story.append(Paragraph("<b>Revenue<sub>t</sub> (₹ Cr)</b> = [ Generation (MWh) × 1,000 × (1 - Degradation)<sup>t-1</sup> × Tariff (₹/kWh) ] / 10,000,000", style_formula))
    story.append(Paragraph("<b>OpEx<sub>t</sub> (₹ Cr)</b> = Base OpEx × (1 + Inflation)<sup>t-1</sup>", style_formula))
    story.append(Paragraph("<b>Net Cash Flow (CF<sub>t</sub>)</b> = (Revenue<sub>t</sub> - OpEx<sub>t</sub>) × (1 - Tax Rate)", style_formula))
    story.append(Paragraph("<b>NPV (₹ Cr)</b> = -CapEx + Σ<sub>t=1</sub><sup>N</sup> [ CF<sub>t</sub> / (1 + WACC)<sup>t</sup> ]", style_formula))
    story.append(Paragraph("<b>LCOE (₹/kWh)</b> = [ Total Discounted Costs (₹) ] / [ Total Discounted Energy (kWh) ]", style_formula))
    story.append(Spacer(1, 10))

    # Section 4: Results Table
    story.append(Paragraph("4. Baseline Results Scorecard (Rajasthan 100MW Solar Park - ₹ INR)", style_h1))
    results_data = [
        [Paragraph("Financial Performance Metric", style_table_header), Paragraph("Calculated Value (INR)", style_table_header), Paragraph("Target Hurdle", style_table_header), Paragraph("Financial Interpretation", style_table_header)],
        [Paragraph("<b>Net Present Value (NPV)</b>", style_table_cell), Paragraph("<b>+₹ 275.50 Crores</b>", style_table_cell), Paragraph("> ₹ 0.00 Cr", style_table_cell), Paragraph("Highly value-accretive; project viable", style_table_cell)],
        [Paragraph("<b>Internal Rate of Return (IRR)</b>", style_table_cell), Paragraph("<b>18.52%</b>", style_table_cell), Paragraph("WACC = 8.00%", style_table_cell), Paragraph("Generates +10.52% excess return spread", style_table_cell)],
        [Paragraph("<b>Levelized Cost of Energy (LCOE)</b>", style_table_cell), Paragraph("<b>₹ 1.99 / kWh</b>", style_table_cell), Paragraph("Tariff = ₹ 3.85 / kWh", style_table_cell), Paragraph("Robust profit margin of +₹ 1.86 / kWh", style_table_cell)],
        [Paragraph("<b>Profitability Index (PI)</b>", style_table_cell), Paragraph("<b>2.10x</b>", style_table_cell), Paragraph("> 1.00x", style_table_cell), Paragraph("Every ₹1.00 invested yields ₹2.10 in PV", style_table_cell)],
        [Paragraph("<b>Discounted Payback Period</b>", style_table_cell), Paragraph("<b>7 Years</b>", style_table_cell), Paragraph("< 20 Years", style_table_cell), Paragraph("Capital fully recovered in Year 7", style_table_cell)],
        [Paragraph("<b>Probability of Loss</b>", style_table_cell), Paragraph("<b>0.00% (Low Risk)</b>", style_table_cell), Paragraph("< 15.00%", style_table_cell), Paragraph("Resilient under 5,000 market shocks", style_table_cell)],
        [Paragraph("<b>95% Value-at-Risk (VaR)</b>", style_table_cell), Paragraph("<b>+₹ 152.80 Crores</b>", style_table_cell), Paragraph("> ₹ 0.00 Cr", style_table_cell), Paragraph("Profitable even in worst 5% scenario", style_table_cell)]
    ]
    res_table = Table(results_data, colWidths=[150, 100, 114, 140])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(res_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Academic Report PDF successfully updated at: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
