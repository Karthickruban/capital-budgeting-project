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
            self.drawString(54, 750, "Financial Engineering Final End-Semester Review Presentation Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential — Student Presentation Guide & Spoken Script (Final Review)")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def generate_presentation_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "Final_Review_Presentation_Guide.pdf")
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
    style_subtitle = ParagraphStyle('DocSubTitle', fontName='Helvetica', fontSize=10.5, leading=14, textColor=c_secondary, spaceAfter=8)
    style_h1 = ParagraphStyle('Heading1_Custom', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_primary, spaceBefore=8, spaceAfter=4, keepWithNext=True)
    style_h2 = ParagraphStyle('Heading2_Custom', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=c_secondary, spaceBefore=6, spaceAfter=3, keepWithNext=True)
    style_body = ParagraphStyle('Body_Custom', fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_dark, spaceAfter=4)
    style_script = ParagraphStyle('Script_Text', fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=colors.HexColor("#2C5282"), spaceAfter=3)
    style_table_header = ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white)
    style_table_cell = ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.5, leading=10, textColor=c_dark)

    story = []

    # Title & Banner
    story.append(Paragraph("Financial Engineering Final End-Semester Review Defense Guide", style_subtitle))
    story.append(Paragraph("12-Slide Presentation Walkthrough & Word-for-Word Spoken Script", style_title))
    story.append(HRFlowable(width="100%", thickness=2, color=c_secondary, spaceBefore=4, spaceAfter=8))

    team_data = [
        [Paragraph("<b>Team Member</b>", style_table_header), Paragraph("<b>Registration No</b>", style_table_header), Paragraph("<b>Degree & Role</b>", style_table_header)],
        [Paragraph("KARTHICK RUBAN.T", style_table_cell), Paragraph("<b>CB.AI.U4AID23017</b>", style_table_cell), Paragraph("Lead Quant & UI Architect", style_table_cell)],
        [Paragraph("SANJAY SENTHIL", style_table_cell), Paragraph("<b>CB.AI.U4AID23042</b>", style_table_cell), Paragraph("Financial Model & DCF Engineer", style_table_cell)],
        [Paragraph("HARI PRAKASH", style_table_cell), Paragraph("<b>CB.AI.U4AID23047</b>", style_table_cell), Paragraph("Monte Carlo Risk Simulation Lead", style_table_cell)],
        [Paragraph("VIGNESH", style_table_cell), Paragraph("<b>CB.AI.U4AID23057</b>", style_table_cell), Paragraph("Portfolio Optimizer & ESG Modeler", style_table_cell)]
    ]
    t_team = Table(team_data, colWidths=[170, 150, 184])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light])
    ]))
    story.append(t_team)
    story.append(Spacer(1, 8))

    # Spoken Script Section
    story.append(Paragraph("Word-for-Word Final Presentation Script (3-Minute Live Demo)", style_h1))

    def make_script_box(title, speech, action):
        return [
            Paragraph(f"<b>{title}</b>", style_h2),
            Paragraph(f"<b>👉 Action on Screen:</b> {action}", style_body),
            Table([[Paragraph(f"<b>What to Say:</b> \"{speech}\"", style_script)]], colWidths=[504], style=[
                ('BACKGROUND', (0, 0), (-1, -1), c_script_bg),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BEE3F8")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]),
            Spacer(1, 4)
        ]

    for elem in make_script_box(
        "Phase 1: Project Overview & Motivation (30 Seconds)",
        "Good morning, Sir. For our Final End-Semester Review, our project is titled Capital Budgeting, Infrastructure Project Valuation & Clean Energy Portfolio Optimizer. "
        "When investing ₹250 Crores into utility-scale clean infrastructure, CFOs and commercial banks need to verify: Will 20 years of electricity sales beat our 8% cost of capital, "
        "can we safely service our bank loans, how do carbon credits expand revenue, and how can we optimize our renewable asset portfolio across Solar, Wind, and Batteries? We built this full-stack quantitative platform to answer these questions.",
        "Show Header and Title on your live deployed Streamlit web application."
    ): story.append(elem)

    for elem in make_script_box(
        "Phase 2: Analysis 1 — DCF Valuation & Bank Debt DSCR (45 Seconds)",
        "In Tab 1, we implement our Deterministic Valuation and Bank Debt Financing model. For our Rajasthan 100MW Solar Park: "
        "Our Net Present Value is +₹275.50 Crores, our IRR is 18.52% (beating the 8% WACC hurdle by +10.52%), our Levelized Cost (LCOE) is ₹1.99 per unit against a ₹3.85 PPA tariff, "
        "and the initial construction debt is fully paid back in 7 Years. Furthermore, our project finance module models 70:30 debt-to-equity financing: our minimum DSCR is 1.54x, "
        "well above the 1.30x banking benchmark, proving the project is fully bankable with zero default risk.",
        "Click on Tab 1, point out the top Scorecard metrics (NPV, IRR, LCOE, Min DSCR), then show the Waterfall chart."
    ): story.append(elem)

    for elem in make_script_box(
        "Phase 3: Analysis 2 — ESG Carbon Credit Monetization (30 Seconds)",
        "In Tab 2, we introduce our new ESG Carbon Offset module. Generating 180,000 MWh of clean electricity displaces 147,600 tonnes of CO2 from the coal-heavy Indian grid every year. "
        "Monetizing these carbon offsets at ₹1,000 per tonne under India's Carbon Credit Trading Scheme injects an additional +₹14.76 Crores per year in green revenue, "
        "expanding annual cash flows by +21.3% and elevating project IRR above 21%.",
        "Click on Tab 2, show the Carbon Abatement metric and the stacked Revenue breakdown bar chart."
    ): story.append(elem)

    story.append(PageBreak())

    for elem in make_script_box(
        "Phase 4: Analysis 3 — Monte Carlo Risk Engine (30 Seconds)",
        "In Tab 3, we test market volatility through our 5,000-scenario Monte Carlo Risk Engine, simultaneously shocking electricity tariffs by ±15%, CapEx overruns up to +25%, and inflation. "
        "Our Probability of Loss is 0.00%, and our 95% Value-at-Risk is +₹152.80 Crores, meaning even in the worst 5% market disaster, the project generates over ₹152 Crores in profit. "
        "The 2D heatmap on the right maps out our break-even frontier across interest rates and tariffs.",
        "Click on Tab 3, point to the histogram and the 2D green/red sensitivity heatmap."
    ): story.append(elem)

    for elem in make_script_box(
        "Phase 5: Analysis 4 — Multi-Asset Portfolio Optimizer (45 Seconds)",
        "In Tab 4, we showcase our major final-review innovation: a Multi-Asset Clean Energy Portfolio Optimizer implementing Markowitz Modern Portfolio Theory. "
        "Because Solar generates during the day while Wind peaks at night and during monsoons, their negative correlation (-0.25) provides powerful diversification. "
        "Combining 45% Solar, 25% Wind, 20% Hybrid BESS Storage, and 10% Pumped Hydro compresses portfolio risk down to 6.85% and produces an optimal Sharpe ratio of 1.48. "
        "The scatter plot visualizes the complete Markowitz Efficient Frontier across 2,000 portfolio combinations.",
        "Click on Tab 4, adjust the allocation sliders, and point to the Donut Chart and Markowitz Efficient Frontier curve."
    ): story.append(elem)

    for elem in make_script_box(
        "Phase 6: Conclusion & Executive Recommendation (15 Seconds)",
        "Finally, Tab 6 synthesizes all calculations into an automated Board Investment Memo recommending investment approval. "
        "Our system provides institutional CFOs with an end-to-end quantitative decision suite from project appraisal to portfolio management. Thank you, Sir, we are happy to take questions!",
        "Show Tab 6 (Executive Memo) and conclude."
    ): story.append(elem)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Final Presentation Guide PDF successfully generated at: {pdf_path}")

if __name__ == "__main__":
    generate_presentation_pdf()
