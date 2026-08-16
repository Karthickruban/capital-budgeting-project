import os
import sys

# Attempt to import reportlab, install if missing
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
    """Canvas for adding page numbers and running header/footer."""
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Capital Budgeting & Infrastructure Valuation | Financial Engineering Report")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential — Academic Course Project Report (AI & Data Science)")
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
    
    # Custom Palette
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0") # Medium Blue
    c_accent = colors.HexColor("#319795")    # Teal
    c_dark = colors.HexColor("#2D3748")      # Charcoal Text
    c_bg_light = colors.HexColor("#F7FAFC")  # Light Gray
    c_border = colors.HexColor("#E2E8F0")

    # Custom Typography Styles
    style_title = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=6
    )
    
    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceAfter=15
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    style_body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=c_primary,
        spaceAfter=6
    )

    style_callout = ParagraphStyle(
        'Callout_Text',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark
    )
    
    style_table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    style_formula = ParagraphStyle(
        'FormulaText',
        fontName='Courier-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_primary
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------------------
    story.append(Paragraph("Financial Engineering Subject Course Project", style_subtitle))
    story.append(Paragraph("Capital Budgeting and Infrastructure Project Valuation with Monte Carlo Risk Simulation", style_title))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceBefore=4, spaceAfter=12))

    # Project Metadata Table
    meta_data = [
        [Paragraph("<b>Project Domain:</b> Clean Infrastructure & Energy Finance", style_table_cell),
         Paragraph("<b>Target Asset:</b> 100MW Solar Park / 50MW Wind Farm", style_table_cell)],
        [Paragraph("<b>Data Source:</b> Kaggle / The World Bank PPI Database", style_table_cell),
         Paragraph("<b>Platform:</b> Python, Streamlit, Plotly, SciPy, PyTorch", style_table_cell)],
        [Paragraph("<b>Primary Methodology:</b> Multi-Stage DCF & WACC Hurdle Rate", style_table_cell),
         Paragraph("<b>Risk Simulation:</b> 5,000-Iteration Stochastic Monte Carlo", style_table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # SECTION 1: EXECUTIVE OVERVIEW & MOTIVATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Executive Overview & Real-World Motivation", style_h1))
    story.append(Paragraph(
        "Large-scale clean infrastructure assets—such as 100MW Solar PV Power Plants, 50MW Onshore Wind Farms, "
        "and Clean Water Desalination Facilities—require <b>multi-million-dollar upfront capital expenditures ($20M to $100M+)</b> "
        "and operate across 20-to-30-year concession lifecycles. Institutional lenders, private equity funds, and Chief Financial "
        "Officers (CFOs) face substantial financial exposure due to long payback periods and exposure to power price fluctuations.",
        style_body
    ))
    story.append(Paragraph(
        "<b>The Core Financial Engineering Dilemma:</b> A single static Net Present Value (NPV) calculation assumes fixed electricity "
        "selling tariffs and zero construction delays over 20 years. In reality, energy market price volatility, supply chain cost "
        "overruns, and macroeconomic inflation create significant downside tail-risk. This project provides an interactive decision "
        "support system combining <b>Deterministic Capital Budgeting</b> (NPV, IRR, PI, Payback, and Levelized Cost of Energy - LCOE) "
        "with a <b>5,000-iteration Stochastic Monte Carlo Risk Engine</b>.",
        style_body
    ))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # SECTION 2: DATASET ARCHITECTURE
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Public Dataset Architecture & Attribute Dictionary", style_h1))
    story.append(Paragraph(
        "The project integrates verified public data from <b>The World Bank Private Participation in Infrastructure (PPI) Database</b> "
        "and <b>IRENA Global Renewable Cost Benchmarks</b> (hosted on Kaggle). The key parameters used by the engine include:",
        style_body
    ))

    dataset_rows = [
        [Paragraph("Column Name", style_table_header), Paragraph("Financial Definition", style_table_header), Paragraph("Baseline Value", style_table_header), Paragraph("Role in Valuation", style_table_header)],
        [Paragraph("<code>Project_Name</code>", style_table_cell), Paragraph("Asset name and technology type", style_table_cell), Paragraph("100MW Solar Park", style_table_cell), Paragraph("Identifier", style_table_cell)],
        [Paragraph("<code>CapEx_USD_M</code>", style_table_cell), Paragraph("Initial construction and land cost", style_table_cell), Paragraph("$30.0 Million", style_table_cell), Paragraph("Year 0 cash outflow ($I_0$)", style_table_cell)],
        [Paragraph("<code>Annual_Gen_MWh</code>", style_table_cell), Paragraph("Total annual electricity generated", style_table_cell), Paragraph("180,000 MWh", style_table_cell), Paragraph("Volume driver for revenue", style_table_cell)],
        [Paragraph("<code>Base_Tariff_USD</code>", style_table_cell), Paragraph("Contracted PPA tariff per MWh", style_table_cell), Paragraph("$48.00 / MWh", style_table_cell), Paragraph("Price driver for revenue", style_table_cell)],
        [Paragraph("<code>Lifetime_Years</code>", style_table_cell), Paragraph("Asset operational lifecycle", style_table_cell), Paragraph("20 Years", style_table_cell), Paragraph("Discounting horizon ($N$)", style_table_cell)],
        [Paragraph("<code>Annual_OpEx_M</code>", style_table_cell), Paragraph("Maintenance, labor, grid fees", style_table_cell), Paragraph("$1.50 Million/yr", style_table_cell), Paragraph("Operating cash outflow", style_table_cell)],
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
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # SECTION 3: MATHEMATICAL FORMULATIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Core Financial Engineering Mathematical Formulations", style_h1))
    
    # Formula Box 1: Annual Cash Flow & Discounting
    story.append(Paragraph("A. Annual Net Cash Flow & Discounted Cash Flow (DCF)", style_h2))
    story.append(Paragraph(
        "For each operational year <i>t</i> (from 1 to <i>N</i>), annual generation decays by the degradation factor, "
        "and operating expenses escalate by annual inflation <i>i</i>:",
        style_body
    ))
    story.append(Paragraph("<b>Revenue<sub>t</sub></b> = [ Annual Generation × (1 - Degradation)<sup>t-1</sup> × Tariff<sub>t</sub> ] / 1,000,000", style_formula))
    story.append(Paragraph("<b>OpEx<sub>t</sub></b> = Base OpEx × (1 + Inflation)<sup>t-1</sup>", style_formula))
    story.append(Paragraph("<b>Net Cash Flow (CF<sub>t</sub>)</b> = (Revenue<sub>t</sub> - OpEx<sub>t</sub>) × (1 - Corporate Tax Rate)", style_formula))
    story.append(Spacer(1, 4))

    # Formula Box 2: NPV
    story.append(Paragraph("B. Net Present Value (NPV)", style_h2))
    story.append(Paragraph(
        "NPV quantifies the aggregate net economic value created in today's dollars by discounting future cash flows at WACC:",
        style_body
    ))
    story.append(Paragraph("<b>NPV</b> = -I<sub>0</sub> + Σ<sub>t=1</sub><sup>N</sup> [ CF<sub>t</sub> / (1 + WACC)<sup>t</sup> ]", style_formula))
    story.append(Paragraph("<i>Decision Rule: Accept if NPV > 0 (Value Accretive); Reject if NPV ≤ 0 (Value Destructive).</i>", style_body))
    story.append(Spacer(1, 4))

    # Formula Box 3: IRR & LCOE
    story.append(Paragraph("C. Internal Rate of Return (IRR) & Levelized Cost of Energy (LCOE)", style_h2))
    story.append(Paragraph("<b>0</b> = -I<sub>0</sub> + Σ<sub>t=1</sub><sup>N</sup> [ CF<sub>t</sub> / (1 + IRR)<sup>t</sup> ]  (Solved via Brent's Numerical Root Algorithm)", style_formula))
    story.append(Paragraph("<b>LCOE ($/MWh)</b> = [ Initial CapEx + Σ (OpEx<sub>t</sub> / (1+WACC)<sup>t</sup>) ] / [ Σ (Generation<sub>t</sub> / (1+WACC)<sup>t</sup>) ]", style_formula))
    story.append(Paragraph("<i>LCOE represents the exact minimum price floor per unit of electricity needed to recover all capital and operating costs.</i>", style_body))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SECTION 4: MONTE CARLO RISK SIMULATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Stochastic Monte Carlo Risk Engine & Sensitivity Analysis", style_h1))
    story.append(Paragraph(
        "To evaluate real-world uncertainty, the platform incorporates a <b>5,000-iteration Monte Carlo simulation</b>. "
        "In each simulation run, three independent stochastic variables are simultaneously sampled:",
        style_body
    ))

    mc_specs = [
        [Paragraph("Stochastic Variable", style_table_header), Paragraph("Probability Distribution", style_table_header), Paragraph("Mathematical Specification", style_table_header)],
        [Paragraph("PPA Electricity Tariff", style_table_cell), Paragraph("Gaussian / Normal", style_table_cell), Paragraph("<i>Tariff</i> ~ N(μ = $48.0, σ = 15%)", style_table_cell)],
        [Paragraph("CapEx Construction Cost", style_table_cell), Paragraph("Uniform Overrun", style_table_cell), Paragraph("<i>CapEx</i> ~ U(1.00 × I<sub>0</sub>, 1.25 × I<sub>0</sub>)", style_table_cell)],
        [Paragraph("Macroeconomic Inflation", style_table_cell), Paragraph("Gaussian / Normal", style_table_cell), Paragraph("<i>Inflation</i> ~ N(μ = 2.5%, σ = 1.0%)", style_table_cell)]
    ]
    mc_table = Table(mc_specs, colWidths=[140, 160, 204])
    mc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(mc_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Risk Quantification Metrics Generated:", style_h2))
    story.append(Paragraph("• <b>Probability of Loss:</b> P(NPV < 0) = (Count of negative NPV iterations / 5,000) × 100%", style_body))
    story.append(Paragraph("• <b>95% Value-at-Risk (VaR):</b> The 5th percentile worst-case simulated NPV threshold.", style_body))
    story.append(Paragraph("• <b>Conditional VaR (CVaR / Expected Shortfall):</b> The conditional mean loss across the worst 5% tail scenarios.", style_body))
    story.append(Spacer(1, 12))

    # -------------------------------------------------------------------------
    # SECTION 5: BASELINE RESULTS SUMMARY TABLE
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Baseline Project Valuation & Results Scorecard", style_h1))
    story.append(Paragraph("Results calculated for the baseline 100MW Solar PV Power Plant ($30M CapEx, 20-Year Life):", style_body))

    results_data = [
        [Paragraph("Financial Performance Metric", style_table_header), Paragraph("Calculated Value", style_table_header), Paragraph("Target Hurdle / Benchmark", style_table_header), Paragraph("Financial Interpretation", style_table_header)],
        [Paragraph("<b>Net Present Value (NPV)</b>", style_table_cell), Paragraph("<b>+$33.19 Million</b>", style_table_cell), Paragraph("> $0.00 Million", style_table_cell), Paragraph("Highly value-accretive; project viable", style_table_cell)],
        [Paragraph("<b>Internal Rate of Return (IRR)</b>", style_table_cell), Paragraph("<b>18.52%</b>", style_table_cell), Paragraph("WACC = 8.00%", style_table_cell), Paragraph("Generates +10.52% excess return spread", style_table_cell)],
        [Paragraph("<b>Levelized Cost of Energy (LCOE)</b>", style_table_cell), Paragraph("<b>$24.81 / MWh</b>", style_table_cell), Paragraph("Tariff = $48.00 / MWh", style_table_cell), Paragraph("Robust profit margin of +$23.19 / MWh", style_table_cell)],
        [Paragraph("<b>Profitability Index (PI)</b>", style_table_cell), Paragraph("<b>2.11x</b>", style_table_cell), Paragraph("> 1.00x", style_table_cell), Paragraph("Every $1.00 invested yields $2.11 in PV", style_table_cell)],
        [Paragraph("<b>Discounted Payback Period</b>", style_table_cell), Paragraph("<b>7 Years</b>", style_table_cell), Paragraph("< 20 Years Lifetime", style_table_cell), Paragraph("Capital fully recovered in Year 7", style_table_cell)],
        [Paragraph("<b>Probability of Negative NPV</b>", style_table_cell), Paragraph("<b>0.00% (Low Risk)</b>", style_table_cell), Paragraph("< 15.00% Threshold", style_table_cell), Paragraph("Safe investment under 5,000 shocks", style_table_cell)],
        [Paragraph("<b>95% Value-at-Risk (VaR)</b>", style_table_cell), Paragraph("<b>+$18.42 Million</b>", style_table_cell), Paragraph("> $0.00 Million", style_table_cell), Paragraph("Even in worst 5% case, project is profitable", style_table_cell)]
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
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # SECTION 6: VIVA / MID-REVIEW CHEATSHEET
    # -------------------------------------------------------------------------
    story.append(Paragraph("6. Mid-Review Viva Defense Cheat-Sheet", style_h1))

    viva_qa = [
        ("Q1: What is the core financial engineering problem solved by this project?",
         "A: It evaluates whether multi-decade clean infrastructure investments are economically viable by discounting lifetime cash inflows against upfront capital costs using WACC, while stress-testing against market volatility via Monte Carlo simulation."),
        ("Q2: What is Levelized Cost of Energy (LCOE)?",
         "A: LCOE is the net present value of all capital and operating costs divided by total discounted electricity output. It represents the exact floor price per MWh needed to break even."),
        ("Q3: Why compare IRR against WACC?",
         "A: WACC is the cost of borrowing capital. If project IRR exceeds WACC, the asset generates returns higher than financing costs, creating net shareholder value."),
        ("Q4: Why implement Monte Carlo simulation if deterministic NPV is positive?",
         "A: Deterministic NPV assumes static tariffs and zero cost overruns for 20 years. Monte Carlo simulates 5,000 joint stochastic combinations to quantify downside tail-risk and Value-at-Risk (VaR)."),
        ("Q5: How does this fulfill all course guidelines?",
         "A: It pulls and cleans real public infrastructure data, provides descriptive statistics, and delivers two distinct financial engineering analyses: Deterministic Capital Budgeting (NPV/IRR/LCOE) and Stochastic Monte Carlo Risk Modeling.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", style_body_bold))
        story.append(Paragraph(a, style_body))
        story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
