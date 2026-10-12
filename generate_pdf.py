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
            self.drawString(54, 750, "Financial Engineering Final End-Semester Project Report (INR)")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential — Academic Course Project Final Report (AI & Data Science)")
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

    style_title = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=c_primary, spaceAfter=4)
    style_subtitle = ParagraphStyle('DocSubTitle', fontName='Helvetica', fontSize=10.5, leading=14, textColor=c_secondary, spaceAfter=10)
    style_h1 = ParagraphStyle('Heading1_Custom', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_primary, spaceBefore=10, spaceAfter=5, keepWithNext=True)
    style_h2 = ParagraphStyle('Heading2_Custom', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=c_secondary, spaceBefore=6, spaceAfter=3, keepWithNext=True)
    style_body = ParagraphStyle('Body_Custom', fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_dark, spaceAfter=4)
    style_body_bold = ParagraphStyle('Body_Bold_Custom', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=c_primary, spaceAfter=4)
    style_table_header = ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white)
    style_table_cell = ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.5, leading=10, textColor=c_dark)
    style_formula = ParagraphStyle('FormulaText', fontName='Courier-Bold', fontSize=8, leading=11, textColor=c_primary)

    story = []

    # Title & Banner
    story.append(Paragraph("Financial Engineering Final End-Semester Comprehensive Report", style_subtitle))
    story.append(Paragraph("Capital Budgeting, Infrastructure Project Valuation & Clean Energy Portfolio Optimizer", style_title))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceBefore=4, spaceAfter=8))

    meta_data = [
        [Paragraph("<b>Authors & Registration:</b><br/>• KARTHICK RUBAN.T (CB.AI.U4AID23017)<br/>• SANJAY SENTHIL (CB.AI.U4AID23042)", style_table_cell),
         Paragraph("<b>Co-Authors & Registration:</b><br/>• HARI PRAKASH (CB.AI.U4AID23047)<br/>• VIGNESH (CB.AI.U4AID23057)", style_table_cell)],
        [Paragraph("<b>Data Sources:</b> Kaggle / World Bank PPI Database, SECI & MNRE Records", style_table_cell),
         Paragraph("<b>Platform:</b> Live Streamlit Cloud Web Application (PyTorch GPU-Ready)", style_table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Section 1: Executive Motivation
    story.append(Paragraph("1. Executive Motivation & Project Scope (Final End-Semester Defense)", style_h1))
    story.append(Paragraph(
        "Large-scale clean infrastructure projects—such as a <b>100MW Solar Park in Rajasthan (₹250 Crores)</b> or a "
        "50MW Wind Farm in Tamil Nadu (₹350 Crores)—involve substantial Day-0 capital outlays funded by 70% bank loans. "
        "Traditional single-scenario Excel sheets fail to capture multi-decade revenue risks, bank debt service coverage, "
        "and portfolio diversification. This project provides a full-fledged quantitative decision suite delivering: "
        "<b>(1) Deterministic Multi-Stage DCF & LCOE</b>, <b>(2) Bank Loan Debt DSCR Amortization</b>, <b>(3) ESG Carbon Offset Monetization</b>, "
        "<b>(4) 5,000-Scenario Monte Carlo Tail-Risk Engine</b>, and <b>(5) Multi-Asset Markowitz Portfolio Optimizer</b>.",
        style_body
    ))
    story.append(Spacer(1, 6))

    # Section 2: Core Financial Engineering Mathematical Formulations
    story.append(Paragraph("2. Mathematical Formulations Across the 4 Core Analyses", style_h1))
    
    story.append(Paragraph("<b>Analysis 1: Deterministic Multi-Stage DCF, NPV, IRR & LCOE</b>", style_body_bold))
    story.append(Paragraph("• Net Cash Flow (CF<sub>t</sub>) = (Revenue<sub>t</sub> - OpEx<sub>t</sub>) × (1 - Tax Rate)", style_formula))
    story.append(Paragraph("• Net Present Value (NPV) = -CapEx + Σ<sub>t=1</sub><sup>N</sup> [ CF<sub>t</sub> / (1 + WACC)<sup>t</sup> ]  (NPV = +₹275.50 Cr)", style_formula))
    story.append(Paragraph("• Internal Rate of Return (IRR): Root where NPV(IRR) = 0 solved via Brent's method (IRR = 18.52% vs WACC = 8.00%)", style_formula))
    story.append(Paragraph("• Levelized Cost of Energy (LCOE in ₹/kWh) = [ Total Discounted Lifetime Costs (₹) ] / [ Total Discounted Energy (kWh) ] = ₹1.99/kWh", style_formula))
    story.append(Paragraph("• Profitability Index (PI) = Present Value of Inflows / CapEx = 2.10x | Discounted Payback = 7 Years", style_formula))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Analysis 2: Project Finance Debt Structuring & ESG Carbon Offsets</b>", style_body_bold))
    story.append(Paragraph("• Bank Loan Debt Service Coverage Ratio (DSCR<sub>t</sub>) = CFADS<sub>t</sub> / [ Principal Amortization<sub>t</sub> + Interest<sub>t</sub> ]", style_formula))
    story.append(Paragraph("• Banking Decision Rule: Project is Bankable if Minimum DSCR ≥ 1.30x (Our Project: Min DSCR = 1.54x, Average = 1.82x)", style_formula))
    story.append(Paragraph("• Annual Carbon Abatement = Annual Generation (MWh) × 0.82 tCO<sub>2</sub>/MWh = 147,600 Tonnes CO<sub>2</sub> avoided/yr", style_formula))
    story.append(Paragraph("• Carbon Revenue Stream = 147,600 tonnes × ₹1,000/tonne = +₹14.76 Crores/year extra income (+21.3% revenue expansion)", style_formula))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Analysis 3: Stochastic Monte Carlo Simulation (5,000 Iterations)</b>", style_body_bold))
    story.append(Paragraph("• 3 Joint Random Shocks: Tariff ~ N(μ = ₹3.85, σ = 15%), CapEx ~ U(1.0, 1.25), Inflation ~ N(μ = 2.5%, σ = 1.0%)", style_formula))
    story.append(Paragraph("• Quantitative Tail-Risk: Probability of Loss = 0.00% | 95% Value-at-Risk (VaR) = +₹152.80 Crores", style_formula))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Analysis 4: Multi-Asset Markowitz Clean Energy Portfolio Optimizer</b>", style_body_bold))
    story.append(Paragraph("• Portfolio Return: R<sub>p</sub> = Σ w<sub>i</sub> × IRR<sub>i</sub> | Portfolio Variance: σ<sub>p</sub><sup>2</sup> = w<sup>T</sup> Σ w", style_formula))
    story.append(Paragraph("• Correlation: Solar (Day) vs Wind (Night) = -0.25 (Drastically reduces portfolio cash flow variance from 14.5% to 6.85%)", style_formula))
    story.append(Paragraph("• Optimal Allocation (₹1,000 Cr Fund): 45% Solar + 25% Wind + 20% Hybrid BESS + 10% Hydro -> Sharpe = 1.48", style_formula))
    story.append(Spacer(1, 6))

    # Section 3: 12 Benchmark Projects Table
    story.append(Paragraph("3. Clean Infrastructure Benchmark Dataset (12 Representative Assets)", style_h1))
    
    table_rows = [
        [Paragraph("Project Name", style_table_header), Paragraph("Sector", style_table_header), Paragraph("CapEx (₹ Cr)", style_table_header), Paragraph("Gen (MWh)", style_table_header), Paragraph("Tariff (₹/u)", style_table_header), Paragraph("LCOE (₹/u)", style_table_header), Paragraph("NPV (₹ Cr)", style_table_header), Paragraph("IRR (%)", style_table_header), Paragraph("Decision", style_table_header)],
        [Paragraph("Rajasthan 100MW Solar", style_table_cell), Paragraph("Solar", style_table_cell), Paragraph("₹ 250", style_table_cell), Paragraph("180k", style_table_cell), Paragraph("₹ 3.85", style_table_cell), Paragraph("₹ 1.99", style_table_cell), Paragraph("<b>+₹ 275.5</b>", style_table_cell), Paragraph("<b>18.5%</b>", style_table_cell), Paragraph("✅ ACCEPT", style_table_cell)],
        [Paragraph("Tamil Nadu 50MW Wind", style_table_cell), Paragraph("Wind", style_table_cell), Paragraph("₹ 350", style_table_cell), Paragraph("130k", style_table_cell), Paragraph("₹ 4.40", style_table_cell), Paragraph("₹ 4.45", style_table_cell), Paragraph("<b>-₹ 74.9</b>", style_table_cell), Paragraph("<b>5.5%</b>", style_table_cell), Paragraph("❌ REJECT", style_table_cell)],
        [Paragraph("Gujarat Desalination", style_table_cell), Paragraph("Water", style_table_cell), Paragraph("₹ 320", style_table_cell), Paragraph("95k", style_table_cell), Paragraph("₹ 5.80", style_table_cell), Paragraph("₹ 4.75", style_table_cell), Paragraph("<b>+₹ 68.2</b>", style_table_cell), Paragraph("<b>10.2%</b>", style_table_cell), Paragraph("✅ ACCEPT", style_table_cell)],
        [Paragraph("Kutch 150MW Hybrid+BESS", style_table_cell), Paragraph("Hybrid", style_table_cell), Paragraph("₹ 520", style_table_cell), Paragraph("310k", style_table_cell), Paragraph("₹ 4.60", style_table_cell), Paragraph("₹ 3.10", style_table_cell), Paragraph("<b>+₹ 312.4</b>", style_table_cell), Paragraph("<b>15.8%</b>", style_table_cell), Paragraph("✅ ACCEPT", style_table_cell)],
        [Paragraph("Tehri 200MW Pumped Hydro", style_table_cell), Paragraph("Hydro", style_table_cell), Paragraph("₹ 850", style_table_cell), Paragraph("340k", style_table_cell), Paragraph("₹ 5.20", style_table_cell), Paragraph("₹ 4.15", style_table_cell), Paragraph("<b>+₹ 284.1</b>", style_table_cell), Paragraph("<b>12.4%</b>", style_table_cell), Paragraph("✅ ACCEPT", style_table_cell)],
        [Paragraph("Khambhat Offshore Wind", style_table_cell), Paragraph("Wind", style_table_cell), Paragraph("₹ 920", style_table_cell), Paragraph("260k", style_table_cell), Paragraph("₹ 6.40", style_table_cell), Paragraph("₹ 5.80", style_table_cell), Paragraph("<b>+₹ 82.5</b>", style_table_cell), Paragraph("<b>10.8%</b>", style_table_cell), Paragraph("✅ ACCEPT", style_table_cell)]
    ]
    t_bench = Table(table_rows, colWidths=[100, 45, 50, 45, 45, 45, 55, 45, 74])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F0FFF4"), colors.HexColor("#FFF5F5"), colors.white, colors.white, colors.white, colors.white])
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 8))

    # Section 4: Academic Compliance Summary
    story.append(Paragraph("4. Final Course Rubric Compliance & Conclusion", style_h1))
    story.append(Paragraph(
        "• <b>Complete Pipeline:</b> Ingests Kaggle World Bank macroeconomic series, cleans them into project-level empirical benchmarks, and runs multi-stage financial valuations.<br/>"
        "• <b>Real Decision Value:</b> Distinguishes viable commercial assets from value-destructive contracts, tests banking solvency (DSCR), and optimizes renewable energy capital mix.<br/>"
        "• <b>Cloud Deployed Application:</b> <u>https://capital-budgeting-project-karthickruban.streamlit.app</u>",
        style_body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Final Report PDF successfully updated at: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
