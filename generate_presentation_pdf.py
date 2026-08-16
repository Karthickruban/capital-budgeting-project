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
            self.drawString(54, 750, "Financial Engineering Mid-Review Presentation Guide (INR)")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential — Student Presentation Script & Review Guide (INR)")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def generate_presentation_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "Mid_Review_Presentation_Guide.pdf")
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
    c_script_bg = colors.HexColor("#EBF8FF")

    style_title = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=c_primary, spaceAfter=4)
    style_subtitle = ParagraphStyle('DocSubTitle', fontName='Helvetica', fontSize=11, leading=15, textColor=c_secondary, spaceAfter=12)
    style_h1 = ParagraphStyle('Heading1_Custom', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=c_primary, spaceBefore=12, spaceAfter=6, keepWithNext=True)
    style_h2 = ParagraphStyle('Heading2_Custom', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=c_secondary, spaceBefore=8, spaceAfter=4, keepWithNext=True)
    style_body = ParagraphStyle('Body_Custom', fontName='Helvetica', fontSize=9, leading=13, textColor=c_dark, spaceAfter=5)
    style_script = ParagraphStyle('Script_Text', fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=colors.HexColor("#2C5282"), spaceAfter=4)
    style_table_header = ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white)
    style_table_cell = ParagraphStyle('TableCell', fontName='Helvetica', fontSize=8, leading=11, textColor=c_dark)

    story = []

    # Title & Banner
    story.append(Paragraph("Financial Engineering Mid-Review Presentation Guide (INR)", style_subtitle))
    story.append(Paragraph("Capital Budgeting and Infrastructure Valuation with Monte Carlo Risk Simulation (INR)", style_title))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceBefore=4, spaceAfter=10))

    summary_data = [
        [Paragraph("<b>Project Title:</b> Capital Budgeting and Infrastructure Project Valuation with Monte Carlo Risk Simulation", style_table_cell),
         Paragraph("<b>Dataset:</b> Kaggle / World Bank PPI Database", style_table_cell)],
        [Paragraph("<b>Currency Standard:</b> Indian Rupees (INR ₹ Crores & ₹/kWh)", style_table_cell),
         Paragraph("<b>Target Audience:</b> CFO / Infrastructure Committee", style_table_cell)]
    ]
    sum_table = Table(summary_data, colWidths=[270, 234])
    sum_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sum_table)
    story.append(Spacer(1, 10))

    # Milestones Table
    story.append(Paragraph("1. Project Milestones: Mid-Review vs. Final Review", style_h1))
    milestone_rows = [
        [Paragraph("Phase", style_table_header), Paragraph("Key Deliverables & Capabilities", style_table_header), Paragraph("Status", style_table_header)],
        [Paragraph("<b>Mid-Review (Today)</b>", style_table_cell),
         Paragraph("• Public Kaggle dataset cleaning and Indian Rupees standardization.<br/>"
                   "• <b>Analysis 1:</b> Deterministic Valuation (NPV, IRR, LCOE, PI, Payback in ₹ Crores).<br/>"
                   "• <b>Analysis 2:</b> 5,000-scenario Monte Carlo Risk Engine & 2D Sensitivity Heatmap.<br/>"
                   "• Deployed live on Streamlit Cloud.", style_table_cell),
         Paragraph("<b>100% COMPLETED</b>", style_table_cell)],
        [Paragraph("<b>Final Review (Future)</b>", style_table_cell),
         Paragraph("• <b>Multi-Asset Portfolio Optimization:</b> Balancing Solar vs Wind vs Battery Storage.<br/>"
                   "• <b>Carbon Offset Revenues:</b> Integrating SECI / Carbon Credit cash flows.<br/>"
                   "• <b>GPU High-Throughput Scaling:</b> 1,000,000+ path CUDA batch rollout on compute node.<br/>"
                   "• <b>Bank Debt Financing:</b> Loan amortization & DSCR schedules.", style_table_cell),
         Paragraph("Planned Next Steps", style_table_cell)]
    ]
    ms_table = Table(milestone_rows, colWidths=[90, 314, 100])
    ms_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(ms_table)
    story.append(Spacer(1, 10))

    # UI Walkthrough Table
    story.append(Paragraph("2. Step-by-Step UI Component Breakdown (INR)", style_h1))
    ui_rows = [
        [Paragraph("UI Component", style_table_header), Paragraph("What It Shows (INR)", style_table_header), Paragraph("Why It Is Useful in Real Life", style_table_header)],
        [Paragraph("<b>1. Sidebar Inputs</b>", style_table_cell),
         Paragraph("Project presets, CapEx (₹ Cr), OpEx (₹ Cr), PPA Tariff (₹/kWh), WACC (%), Inflation (%).", style_table_cell),
         Paragraph("Allows real-time tweaking of project parameters matching Indian tariff auctions.", style_table_cell)],
        [Paragraph("<b>2. Tab 1 Scorecard</b>", style_table_cell),
         Paragraph("<b>NPV:</b> +₹275.50 Cr | <b>IRR:</b> 18.52%<br/><b>LCOE:</b> ₹1.99/kWh | <b>PI:</b> 2.10x<br/><b>Payback:</b> 7 Years", style_table_cell),
         Paragraph("Provides immediate executive viability: NPV shows wealth creation, IRR beats 8% WACC by +10.5%, and LCOE proves profit vs ₹3.85/kWh tariff.", style_table_cell)],
        [Paragraph("<b>3. Tab 1 Cash Flow Waterfall</b>", style_table_cell),
         Paragraph("Year 0 outflow (-₹250 Cr) + annual positive inflows (+₹46.7 Cr/yr) reaching break-even at Year 7.", style_table_cell),
         Paragraph("Visually tracks cumulative debt reduction and profit accumulation over 20 years.", style_table_cell)],
        [Paragraph("<b>4. Tab 2 Monte Carlo Engine</b>", style_table_cell),
         Paragraph("Histogram of 5,000 simulated scenarios, 95% VaR (+₹152.8 Cr), Probability of Loss (0.00%).", style_table_cell),
         Paragraph("Proves the project remains resilient and profitable even under severe tariff and cost shocks.", style_table_cell)],
        [Paragraph("<b>5. Tab 2 2D Sensitivity Heatmap</b>", style_table_cell),
         Paragraph("Color-coded matrix of NPV (₹ Cr) across PPA Tariffs (₹2.90 to ₹4.80/kWh) vs. WACC (6% to 12%).", style_table_cell),
         Paragraph("Shows the exact boundary where the project shifts from profit to loss.", style_table_cell)]
    ]
    ui_table = Table(ui_rows, colWidths=[110, 204, 190])
    ui_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(ui_table)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Presentation Script
    story.append(Paragraph("3. Spoken Presentation Script for Mid-Review (INR)", style_h1))

    def make_script_box(title, speech, action):
        return [
            Paragraph(f"<b>{title}</b>", style_h2),
            Paragraph(f"<b>👉 Action on Screen:</b> {action}", style_body),
            Table([[Paragraph(f"<b>What to Say:</b> \"{speech}\"", style_script)]], colWidths=[504], style=[
                ('BACKGROUND', (0, 0), (-1, -1), c_script_bg),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BEE3F8")),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]),
            Spacer(1, 6)
        ]

    for elem in make_script_box(
        "Phase 1: Introduction & Problem Statement",
        "Good morning/afternoon, Sir. Our project is titled Capital Budgeting and Infrastructure Project Valuation with Monte Carlo Risk Simulation. "
        "When an Indian energy company or government invests ₹250 Crores to build a 100MW Solar Park or Wind Farm, the CFO needs to know: "
        "Will 20 years of electricity revenues at ₹3.85 per unit justify this massive upfront cost, and what is our financial risk if tariffs drop? We built this quantitative tool to answer that.",
        "Show Title & Overview on website."
    ): story.append(elem)

    for elem in make_script_box(
        "Phase 2: Analysis 1 (Deterministic Valuation in INR)",
        "In Tab 1, we pull real project benchmarks from our Kaggle / World Bank dataset in Indian Rupees. "
        "Discounting all cash flows at an 8% cost of capital (WACC): Our Net Present Value (NPV) is +₹275.50 Crores, proving the project is highly value-accretive. "
        "The Internal Rate of Return (IRR) is 18.52%, beating our 8% hurdle rate by +10.5%. "
        "Our Levelized Cost of Energy (LCOE) is ₹1.99 per unit (kWh), giving a strong profit margin against our ₹3.85 PPA selling tariff. "
        "The Cash Flow Waterfall chart proves our ₹250 Cr investment is fully paid back in 7 Years.",
        "Click on Tab 1, point to metric cards and the Waterfall chart."
    ): story.append(elem)

    for elem in make_script_box(
        "Phase 3: Analysis 2 (Monte Carlo Risk Simulation in INR)",
        "In Tab 2, a static NPV is not enough because real tariffs fluctuate and construction often faces overruns. "
        "So we built a 5,000-scenario Monte Carlo Risk Engine. In each run, we simultaneously shock tariffs by ±15%, CapEx overruns up to +25%, and inflation. "
        "As you can see, our Probability of Loss is 0.00%, and our 95% Value-at-Risk is +₹152.8 Crores. "
        "The 2D sensitivity heatmap shows our exact break-even boundary across different interest rates and unit tariffs.",
        "Click on Tab 2, drag slider to 10,000 runs, point to histogram and heatmap."
    ): story.append(elem)

    for elem in make_script_box(
        "Phase 4: Conclusion & Next Steps",
        "Tab 4 auto-generates an Executive Investment Memo recommending board approval. "
        "For our Final Review, our next milestones are: (1) multi-asset portfolio optimization for Solar vs Wind vs Battery Storage, "
        "(2) integrating Carbon Offset revenues, and (3) scaling our Monte Carlo engine to 1,000,000 paths on our college GPU cluster. Thank you, Sir!",
        "Show Tab 4 memo, then return to Tab 1."
    ): story.append(elem)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Presentation PDF successfully updated at: {pdf_path}")

if __name__ == "__main__":
    generate_presentation_pdf()
