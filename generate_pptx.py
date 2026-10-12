import sys
import os

try:
    import pptx
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    import pptx
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Modern High-Impact Color Palette
    c_navy = RGBColor(15, 23, 42)        # #0F172A - Ultra Dark Slate/Navy
    c_blue = RGBColor(37, 99, 235)      # #2563EB - Vibrant Blue
    c_teal = RGBColor(13, 148, 136)     # #0D9488 - Modern Teal
    c_dark = RGBColor(51, 65, 85)       # #334155 - Slate Charcoal Text
    c_light = RGBColor(248, 250, 252)   # #F8FAFC - Clean Card Background
    c_white = RGBColor(255, 255, 255)
    c_gray = RGBColor(100, 116, 139)
    c_green = RGBColor(22, 163, 74)     # #16A34A - Success Emerald
    c_red = RGBColor(220, 38, 38)       # #DC2626 - Alert Red
    c_box_bg = RGBColor(238, 242, 255)  # #EEF2FF - Soft Indigo Card

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_white
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="FINANCIAL ENGINEERING FINAL PROJECT"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.15))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_sub = tf.paragraphs[0]
        p_sub.text = category_text.upper()
        p_sub.font.name = 'Helvetica'
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = c_teal
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = 'Helvetica'
        p_title.font.size = Pt(25)
        p_title.font.bold = True
        p_title.font.color.rgb = c_navy
        
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.733), Inches(0.025))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(226, 232, 240)
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=c_light, border_color=RGBColor(226, 232, 240)):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: Title / Cover Slide with Team Details & Roll Numbers
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(0.18), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = c_teal
    bar.line.fill.background()

    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(3.6))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "FINANCIAL ENGINEERING FINAL END-SEMESTER DEFENSE  |  AI & DATA SCIENCE"
    p0.font.name = 'Helvetica'
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = c_teal
    p0.space_after = Pt(8)
    
    p1 = tf.add_paragraph()
    p1.text = "Capital Budgeting, Infrastructure Project Valuation\n& Clean Energy Portfolio Optimizer"
    p1.font.name = 'Helvetica'
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = c_navy
    p1.space_after = Pt(10)
    
    p2 = tf.add_paragraph()
    p2.text = "Multi-Stage DCF, Bank Loan DSCR, ESG Carbon Offsets, Monte Carlo Risk & Markowitz Frontier (₹ INR)"
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(14)
    p2.font.color.rgb = c_blue

    # Team Members Card
    add_card(s1, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.8), bg_color=c_light)
    tb_box = s1.shapes.add_textbox(Inches(1.1), Inches(5.3), Inches(11.133), Inches(1.6))
    tf_tb = tb_box.text_frame
    tf_tb.word_wrap = True
    
    p_th = tf_tb.paragraphs[0]
    p_th.text = "PROJECT TEAM MEMBERS & REGISTRATION DETAILS:"
    p_th.font.name = 'Helvetica'
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = c_gray
    p_th.space_after = Pt(8)
    
    team_members = [
        "•  KARTHICK RUBAN.T  —  CB.AI.U4AID23017",
        "•  SANJAY SENTHIL  —  CB.AI.U4AID23042",
        "•  HARI PRAKASH  —  CB.AI.U4AID23047",
        "•  VIGNESH  —  CB.AI.U4AID23057"
    ]
    for tm in team_members:
        p_m = tf_tb.add_paragraph()
        p_m.text = tm
        p_m.font.name = 'Helvetica'
        p_m.font.size = Pt(12)
        p_m.font.bold = True
        p_m.font.color.rgb = c_navy
        p_m.space_after = Pt(2)

    # =========================================================================
    # SLIDE 2: Problem Motivation - The ₹250 Cr Dilemma
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Real-World Dilemma: The ₹250 Crore Infrastructure Decision")

    col_w = Inches(3.64)
    col_h = Inches(5.2)

    add_card(s2, Inches(0.8), Inches(1.7), col_w, col_h)
    b1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.9), col_w - Inches(0.4), col_h - Inches(0.4))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. Heavy Capital Intensity"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.space_after = Pt(12)
    bullets1 = [
        "Building a 100MW Solar Park requires ₹250 Crores upfront on Day 1.",
        "Over 70% of capital is borrowed from commercial banks requiring strict repayment.",
        "A bad capital allocation decision destroys hundreds of crores in shareholder value."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = c_dark
        p.space_after = Pt(8)

    add_card(s2, Inches(4.84), Inches(1.7), col_w, col_h)
    b2 = s2.shapes.add_textbox(Inches(5.04), Inches(1.9), col_w - Inches(0.4), col_h - Inches(0.4))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. Multi-Decade Uncertainty"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_navy
    p.space_after = Pt(12)
    bullets2 = [
        "Long 20 to 25 Year Concessions: Cash flows occur across changing economic cycles.",
        "Tariff & Cost Volatility: Energy auction prices shift and construction delays escalate costs.",
        "The Core CFO Question: 'Will power revenues pay off bank debt, beat our 8% WACC, and remain solvent?'"
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = c_dark
        p.space_after = Pt(8)

    add_card(s2, Inches(8.88), Inches(1.7), col_w, col_h, bg_color=c_box_bg, border_color=c_blue)
    b3 = s2.shapes.add_textbox(Inches(9.08), Inches(1.9), col_w - Inches(0.4), col_h - Inches(0.4))
    tf3 = b3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. Complete Decision Suite"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.space_after = Pt(12)
    bullets3 = [
        "Analysis 1: Deterministic Multi-Stage DCF (NPV, IRR, LCOE, Payback).",
        "Analysis 2: Bank Debt Amortization (DSCR >= 1.30x) & ESG Carbon Offsets.",
        "Analysis 3: 5,000-Scenario Monte Carlo Risk Engine (95% VaR & Sensitivity).",
        "Analysis 4: Markowitz Clean Energy Portfolio Optimizer (Efficient Frontier)."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = c_dark
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: Public Dataset Architecture (12 Benchmark Projects)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Public Dataset Architecture: 12 Clean Infrastructure Assets")

    add_card(s3, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.65), bg_color=c_light)
    ds_top = s3.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.333), Inches(0.55))
    ds_tf = ds_top.text_frame
    p = ds_tf.paragraphs[0]
    p.text = "DATA SOURCES: Kaggle / World Bank PPI Database, SECI Auction Tenders, MNRE Cost Benchmarks & Global Clean Tech"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = c_teal

    table_shape = s3.shapes.add_table(7, 4, Inches(0.8), Inches(2.45), Inches(11.733), Inches(4.5))
    table = table_shape.table
    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(3.7)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(3.333)

    headers = ["Feature Name", "Financial Definition", "Baseline Value (INR)", "Role in Valuation"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(10)
        cell.text_frame.paragraphs[0].font.color.rgb = c_white

    table_data = [
        ["CapEx_INR_Crores", "Initial construction, land & interconnection cost", "₹ 250.0 Crores", "Year 0 cash outflow ($I_0$)"],
        ["Annual_Gen_MWh", "Total annual energy generated (180M kWh)", "180,000 MWh", "Volume driver for annual power revenue"],
        ["Base_Tariff_INR_kWh", "Contracted PPA auction price per unit (kWh)", "₹ 3.85 / kWh", "Unit price driver for annual revenue"],
        ["Project_Lifetime_Years", "Operational concession duration of asset", "20 Years", "Discounting time horizon ($N$)"],
        ["Annual_OpEx_Crores", "Yearly maintenance, cleaning, labor & grid fees", "₹ 12.5 Crores/yr", "Annual operational cash outflow"],
        ["WACC_Percent", "Weighted Average Cost of Capital (Hurdle Rate)", "8.00%", "Discount rate ($r$) for NPV discounting"]
    ]

    for row_idx, row in enumerate(table_data, start=1):
        for col_idx, text in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_light if row_idx % 2 == 0 else c_white
            cell.text = text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = c_dark

    # =========================================================================
    # SLIDE 4: Analysis 1 (Part A) - Cash Flow, Discounting & NPV
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Analysis 1: Core Formulations (Cash Flow, NPV & IRR in 1 Sentence)")

    card_w2 = Inches(5.7)
    card_h2 = Inches(5.2)

    add_card(s4, Inches(0.8), Inches(1.7), card_w2, card_h2)
    b_f1 = s4.shapes.add_textbox(Inches(1.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf = b_f1.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "1. Annual Revenue Formula"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    p = tf.add_paragraph()
    p.text = "Formula: Revenue = Units of Power Generated × Price per Unit"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_blue
    p = tf.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'This is simply the total money we earn in a year by multiplying the electricity units produced by the price the government pays us per unit.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "2. Annual Net Cash Flow (CF_t)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    p = tf.add_paragraph()
    p.text = "Formula: CF_t = (Revenue_t - OpEx_t) × (1 - Tax Rate)"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_blue
    p = tf.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'This is the actual take-home profit we keep in our bank account each year after paying maintenance expenses and government taxes.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "3. The Discounting Formula"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    p = tf.add_paragraph()
    p.text = "Formula: Discount Factor = 1 / (1 + Interest Rate)^t"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_blue
    p = tf.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'Because ₹100 today is worth more than ₹100 ten years from now, this formula shrinks future money back to what it is truly worth in today's pocket.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark

    add_card(s4, Inches(6.8), Inches(1.7), card_w2, card_h2, bg_color=c_box_bg, border_color=c_blue)
    b_f2 = s4.shapes.add_textbox(Inches(7.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf2 = b_f2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "4. Net Present Value (NPV)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_blue
    p = tf2.add_paragraph()
    p.text = "Formula: NPV = -Initial CapEx + Σ [ Future Cash Flows / (1+WACC)^t ]"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_navy
    p = tf2.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'NPV tells us the exact extra wealth we create in today's money: if positive (+₹275 Cr), the project makes us rich; if negative, we lose money.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(10)

    p = tf2.add_paragraph()
    p.text = "5. Internal Rate of Return (IRR)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_blue
    p = tf2.add_paragraph()
    p.text = "Formula: Rate where Total Discounted Cash Inflows = Initial CapEx"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_navy
    p = tf2.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'IRR is simply the annual percentage profit rate generated by our project (18.5%), and as long as it is higher than our bank loan interest rate (8%), we make a handsome profit.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark

    # =========================================================================
    # SLIDE 5: Analysis 1 (Part B) - LCOE, Profitability Index & Payback
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Analysis 1: LCOE, Profitability Index & 7-Year Payback")

    add_card(s5, Inches(0.8), Inches(1.7), card_w2, card_h2)
    b_l = s5.shapes.add_textbox(Inches(1.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_l = b_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "6. Levelized Cost of Energy (LCOE)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    p = tf_l.add_paragraph()
    p.text = "Formula: LCOE = Total Lifetime Costs / Total Lifetime Units of Electricity"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_blue
    p = tf_l.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'LCOE is our exact production cost per unit of power (₹1.99/unit): selling power above this cost (₹3.85/unit) guarantees a +₹1.86/unit profit margin.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(12)

    p = tf_l.add_paragraph()
    p.text = "7. Profitability Index (PI)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    p = tf_l.add_paragraph()
    p.text = "Formula: PI = Total Future Present Value Created / Initial CapEx"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_blue
    p = tf_l.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'PI measures our bang-for-the-buck: a score of 2.10x means for every ₹1.00 we invest today, we get back ₹2.10 in total value.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark

    add_card(s5, Inches(6.8), Inches(1.7), card_w2, card_h2, bg_color=c_light)
    b_r = s5.shapes.add_textbox(Inches(7.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "8. Discounted Payback Period: 7 Years"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    p = tf_r.add_paragraph()
    p.text = "Formula: The exact year where Cumulative Discounted Cash Flow = 0"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_blue
    p = tf_r.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'This tells us how many years (7 years) it takes to fully recover our initial ₹250 Crore construction loan before we enter 13 years of 100% pure profit.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(12)

    p = tf_r.add_paragraph()
    p.text = "📊 Cash Flow Waterfall Breakdown:"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = c_navy
    wf_bullets = [
        "Year 0: -₹250 Cr initial capital construction outflow.",
        "Years 1-6: +₹46.7 Cr/yr net cash inflow paying down initial capital.",
        "Year 7: Debt fully recovered (Cumulative Cash Flow crosses ₹0).",
        "Years 8-20: 13 continuous years generating pure shareholder profit."
    ]
    for w in wf_bullets:
        p = tf_r.add_paragraph()
        p.text = "• " + w
        p.font.size = Pt(9)
        p.font.color.rgb = c_gray
        p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 6: Analysis 2 (Part A) - Project Finance & Debt DSCR (NEW FINAL FEATURE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Analysis 2: Project Finance Debt Structuring & Bank Loan DSCR")

    add_card(s6, Inches(0.8), Inches(1.7), card_w2, card_h2)
    b_df1 = s6.shapes.add_textbox(Inches(1.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_df1 = b_df1.text_frame
    tf_df1.word_wrap = True

    p = tf_df1.paragraphs[0]
    p.text = "🏦 70:30 Debt-to-Equity Capital Structure"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    p.space_after = Pt(8)

    df_pts = [
        ("Bank Debt (70%):", "₹ 175.0 Crores borrowed from institutional lenders (SBI, IREDA, PFC)."),
        ("Sponsor Equity (30%):", "₹ 75.0 Crores invested by developer equity shareholders."),
        ("Loan Term:", "12-Year Amortization @ 8.50% annual commercial interest rate."),
        ("Annual Debt Service:", "Equal Principal Amortization (₹14.58 Cr/yr) + Declining Interest.")
    ]
    for lbl, desc in df_pts:
        p = tf_df1.add_paragraph()
        p.text = lbl
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_blue
        p = tf_df1.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(4)

    add_card(s6, Inches(6.8), Inches(1.7), card_w2, card_h2, bg_color=c_box_bg, border_color=c_blue)
    b_df2 = s6.shapes.add_textbox(Inches(7.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_df2 = b_df2.text_frame
    tf_df2.word_wrap = True

    p = tf_df2.paragraphs[0]
    p.text = "📊 Debt Service Coverage Ratio (DSCR)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_blue
    p.space_after = Pt(6)

    p = tf_df2.add_paragraph()
    p.text = "Formula: DSCR_t = Cash Flow Available for Debt / Annual (Principal + Interest)"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_navy
    p = tf_df2.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'DSCR measures if our annual cash flow is safely large enough to pay the bank loan installment without defaulting.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(10)

    dscr_benchmarks = [
        ("Rajasthan 100MW Solar Minimum DSCR: 1.54x", "Well above the banking safety threshold (>= 1.30x), qualifying as 'Bankable'."),
        ("Average Project DSCR: 1.82x", "Generates an 82% cash flow buffer above required loan obligations."),
        ("Bank Default Risk: ZERO", "Project cash flows maintain complete solvency throughout the 12-year debt tenure.")
    ]
    for lbl, desc in dscr_benchmarks:
        p = tf_df2.add_paragraph()
        p.text = "• " + lbl
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = c_green if "1.54x" in lbl else c_navy
        p = tf_df2.add_paragraph()
        p.text = "   ↳ " + desc
        p.font.size = Pt(9)
        p.font.color.rgb = c_gray
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 7: Analysis 2 (Part B) - ESG Carbon Credit Modeling (NEW FINAL FEATURE)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Analysis 2: ESG Carbon Offset & Green Revenue Modeling")

    add_card(s7, Inches(0.8), Inches(1.7), card_w2, card_h2, bg_color=RGBColor(240, 255, 244), border_color=c_green)
    b_esg1 = s7.shapes.add_textbox(Inches(1.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_esg1 = b_esg1.text_frame
    tf_esg1.word_wrap = True

    p = tf_esg1.paragraphs[0]
    p.text = "🌿 Physical Decarbonization Metrics"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_green
    p.space_after = Pt(8)

    esg_pts = [
        ("Grid Baseline Factor:", "Central Electricity Authority (CEA) India baseline: 0.82 tCO2 / MWh displaced."),
        ("Annual Carbon Abatement:", "180,000 MWh × 0.82 = 147,600 Metric Tonnes of CO2 avoided per year."),
        ("20-Year Lifetime Impact:", "Over 2.85 Million Metric Tonnes of CO2 emissions permanently averted from atmosphere."),
        ("Equivalency:", "Equivalent to planting over 4.7 Million mature trees or removing 65,000 fossil cars from Indian roads annually.")
    ]
    for lbl, desc in esg_pts:
        p = tf_esg1.add_paragraph()
        p.text = lbl
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_navy
        p = tf_esg1.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(4)

    add_card(s7, Inches(6.8), Inches(1.7), card_w2, card_h2)
    b_esg2 = s7.shapes.add_textbox(Inches(7.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_esg2 = b_esg2.text_frame
    tf_esg2.word_wrap = True

    p = tf_esg2.paragraphs[0]
    p.text = "💰 Green Revenue Expansion (CCTS / VCM)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    p.space_after = Pt(8)

    rev_pts = [
        ("Carbon Price Benchmark:", "Modeled at ₹ 1,000 per Tonne of CO2 under India's Carbon Credit Trading Scheme."),
        ("Annual Carbon Cash Flow:", "147,600 tonnes × ₹1,000 = +₹ 14.76 Crores / year extra cash income."),
        ("Revenue Expansion Impact:", "Increases total annual project cash inflow by +21.3% over base power sales."),
        ("Financial Valuation Uplift:", "Boosts Project IRR from 18.52% up to 21.40%, significantly expanding equity returns.")
    ]
    for lbl, desc in rev_pts:
        p = tf_esg2.add_paragraph()
        p.text = lbl
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_teal
        p = tf_esg2.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 8: Analysis 3 (Part A) - Monte Carlo Risk Engine (5,000 Runs)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Analysis 3: Stochastic Monte Carlo Simulation (5,000 Runs)")

    add_card(s8, Inches(0.8), Inches(1.7), card_w2, card_h2)
    b_mc1 = s8.shapes.add_textbox(Inches(1.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_mc1 = b_mc1.text_frame
    tf_mc1.word_wrap = True

    p = tf_mc1.paragraphs[0]
    p.text = "What is Monte Carlo Simulation?"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    p.space_after = Pt(4)
    p = tf_mc1.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'Instead of guessing one static future, the computer rolls the dice 5,000 times with bad weather, rising costs, and price drops to prove we still won't lose money.'"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.space_after = Pt(12)

    p = tf_mc1.add_paragraph()
    p.text = "Why Do We Need It?"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = c_navy
    mc_reasons = [
        "Static DCF assumes electricity tariffs and costs never vary for 20 years.",
        "Monte Carlo replaces static numbers with 5,000 randomized future market scenarios.",
        "Vectorized execution discounts all 5,000 paths in under 50 milliseconds."
    ]
    for r in mc_reasons:
        p = tf_mc1.add_paragraph()
        p.text = "• " + r
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(4)

    add_card(s8, Inches(6.8), Inches(1.7), card_w2, card_h2, bg_color=c_light)
    b_mc2 = s8.shapes.add_textbox(Inches(7.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_mc2 = b_mc2.text_frame
    tf_mc2.word_wrap = True

    p = tf_mc2.paragraphs[0]
    p.text = "⚡ The 3 Randomized Shocks We Test:"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    p.space_after = Pt(8)

    shocks = [
        ("1. Power Tariff Drops (±15%):", "Simulates what happens if market electricity prices drop from ₹3.85 down to ₹3.20/unit."),
        ("2. Construction Cost Overruns (0% to +25%):", "Simulates supply chain and equipment delays pushing CapEx from ₹250 Cr up to ₹310 Cr."),
        ("3. Inflation Spikes (1.5% to 4.5%):", "Simulates rising labor and maintenance costs squeezing annual profit margins.")
    ]
    for s_lbl, s_desc in shocks:
        p = tf_mc2.add_paragraph()
        p.text = s_lbl
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_teal
        p = tf_mc2.add_paragraph()
        p.text = s_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 9: Analysis 3 (Part B) - VaR & 2D Sensitivity Heatmap
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Analysis 3: Value-at-Risk & 2D Sensitivity Matrix")

    add_card(s9, Inches(0.8), Inches(1.7), card_w2, card_h2, bg_color=RGBColor(240, 255, 244), border_color=c_green)
    b_var = s9.shapes.add_textbox(Inches(1.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_var = b_var.text_frame
    tf_var.word_wrap = True

    p = tf_var.paragraphs[0]
    p.text = "95% Value-at-Risk (VaR)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_green
    p = tf_var.add_paragraph()
    p.text = "Formula: The 5th percentile worst-case outcome across 5,000 simulations"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_navy
    p = tf_var.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'VaR tells us our financial safety net: in 95 out of 100 extreme market disasters, our project will still make at least ₹152.8 Crores in profit.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(10)

    p = tf_var.add_paragraph()
    p.text = "Probability of Loss: 0.00%"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = c_green
    p = tf_var.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'Out of 5,000 random market combinations, not a single simulated future resulted in negative NPV.'"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark

    add_card(s9, Inches(6.8), Inches(1.7), card_w2, card_h2)
    b_sm = s9.shapes.add_textbox(Inches(7.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_sm = b_sm.text_frame
    tf_sm.word_wrap = True

    p = tf_sm.paragraphs[0]
    p.text = "2D Sensitivity Matrix Heatmap"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy
    p = tf_sm.add_paragraph()
    p.text = "Formula: 5 × 5 Matrix Testing PPA Tariff (₹2.90–₹4.80) vs WACC (6%–12%)"
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_blue
    p = tf_sm.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'The heatmap is a color-coded traffic light showing exactly how high interest rates or how low electricity prices can go before the project turns red (losses).'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(8)

    p = tf_sm.add_paragraph()
    p.text = "Commercial Value for CFO:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = c_navy
    p = tf_sm.add_paragraph()
    p.text = "• Green Zone: Profitable contract terms.\n• Red Zone: Terms that result in financial distress.\n• Decision: Guides contract tariff negotiation."
    p.font.size = Pt(9)
    p.font.color.rgb = c_gray

    # =========================================================================
    # SLIDE 10: Analysis 4 - Multi-Asset Clean Energy Portfolio Optimizer (NEW FINAL FEATURE)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Analysis 4: Multi-Asset Clean Energy Portfolio Optimizer")

    add_card(s10, Inches(0.8), Inches(1.7), card_w2, card_h2)
    b_mpt1 = s10.shapes.add_textbox(Inches(1.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_mpt1 = b_mpt1.text_frame
    tf_mpt1.word_wrap = True

    p = tf_mpt1.paragraphs[0]
    p.text = "📈 Markowitz Efficient Frontier in Energy"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    p.space_after = Pt(6)

    p = tf_mpt1.add_paragraph()
    p.text = "💬 1-Sentence Meaning: 'Instead of putting all money in one solar farm, we balance investments across Solar, Wind, and Batteries so daytime sun and nighttime wind balance each other perfectly.'"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.space_after = Pt(10)

    mpt_benefits = [
        ("Negative Correlation Benefit:", "Solar generates during peak daylight; Wind peaks at night/monsoon. Their correlation (-0.25) significantly cuts portfolio risk."),
        ("Battery Storage Integration:", "Batteries absorb peak noon solar power and discharge during evening peak tariff hours."),
        ("Optimal Risk-Adjusted Allocation:", "45% Solar + 25% Wind + 20% Hybrid BESS + 10% Hydro Storage produces a superior Sharpe ratio of 1.48.")
    ]
    for lbl, desc in mpt_benefits:
        p = tf_mpt1.add_paragraph()
        p.text = lbl
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = c_navy
        p = tf_mpt1.add_paragraph()
        p.text = desc
        p.font.size = Pt(9)
        p.font.color.rgb = c_dark
        p.space_after = Pt(4)

    add_card(s10, Inches(6.8), Inches(1.7), card_w2, card_h2, bg_color=c_box_bg, border_color=c_blue)
    b_mpt2 = s10.shapes.add_textbox(Inches(7.0), Inches(1.85), card_w2 - Inches(0.4), card_h2 - Inches(0.3))
    tf_mpt2 = b_mpt2.text_frame
    tf_mpt2.word_wrap = True

    p = tf_mpt2.paragraphs[0]
    p.text = "📊 Optimal Portfolio Performance (₹1,000 Cr Fund)"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_blue
    p.space_after = Pt(8)

    opt_metrics = [
        ("Blended Portfolio IRR:", "14.85% (Consistent multi-asset annual return)"),
        ("Portfolio Risk / Volatility:", "6.85% (Drastically lower than standalone Wind at 14.5%)"),
        ("Sharpe Ratio:", "1.48 (Exceptional risk-adjusted excess return)"),
        ("Diversification Premium:", "Reduces probability of negative annual cash flow to ZERO across entire 25-year fund lifecycle.")
    ]
    for lbl, desc in opt_metrics:
        p = tf_mpt2.add_paragraph()
        p.text = lbl
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_navy
        p = tf_mpt2.add_paragraph()
        p.text = "↳ " + desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 11: System Architecture & GPU Acceleration
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "System Architecture & High-Performance Implementation")

    stack_cards = [
        ("🖥️ Streamlit Cloud UI", "Responsive Dashboard", "• 6 multi-page analytical tabs\n• Real-time reactive sliders\n• Automated Investment Memo"),
        ("📈 Visual Analytics", "Plotly Graph Objects", "• Cash Flow Waterfall\n• 5,000-scenario histogram\n• Markowitz Efficient Frontier"),
        ("⚡ Financial Core", "NumPy & SciPy", "• Multi-year matrix discounting\n• Brent's Numerical Root Solver\n• Bank loan amortization DSCR"),
        ("🚀 GPU Acceleration", "PyTorch CUDA Architecture", "• Scalable to 1,000,000 paths\n• Auto-detects NVIDIA GPUs\n• Sub-millisecond tensor batch")
    ]

    card_w_s = Inches(2.7)
    gap_s = Inches(0.3)
    start_x_s = Inches(0.8)

    for idx, (title, sub, details) in enumerate(stack_cards):
        x_pos = start_x_s + (idx * (card_w_s + gap_s))
        add_card(s11, x_pos, Inches(1.8), card_w_s, Inches(5.1))
        box = s11.shapes.add_textbox(x_pos + Inches(0.15), Inches(2.0), card_w_s - Inches(0.3), Inches(4.7))
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = c_navy
        p.space_after = Pt(4)
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = c_teal
        p_sub.space_after = Pt(10)
        p_det = tf.add_paragraph()
        p_det.text = details
        p_det.font.size = Pt(9.5)
        p_det.font.color.rgb = c_dark

    # =========================================================================
    # SLIDE 12: Final Review Academic Defense & Live App Demonstration
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Final Review Academic Defense & Live System Demonstration")

    add_card(s12, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.2), bg_color=RGBColor(240, 255, 244), border_color=c_green)
    tb_m = s12.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.3), Inches(4.8))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    
    p = tf_m.paragraphs[0]
    p.text = "🎯 End-Semester Accomplishments"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_green
    p.space_after = Pt(8)
    
    m_pts = [
        "Expanded Dataset: 12 clean tech assets (Solar, Wind, Hybrid BESS, Hydro, Desalination).",
        "Analysis 1: Multi-Stage DCF (NPV +₹275.5 Cr, IRR 18.52%, LCOE ₹1.99/unit).",
        "Analysis 2: Project Finance Debt Amortization (DSCR 1.54x) & ESG Carbon Offsets.",
        "Analysis 3: 5,000-Scenario Monte Carlo Risk Engine & 2D Sensitivity Heatmap.",
        "Analysis 4: Markowitz Portfolio Optimizer with interactive Efficient Frontier."
    ]
    for pt in m_pts:
        p = tf_m.add_paragraph()
        p.text = "✔ " + pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(5)

    add_card(s12, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.2), bg_color=c_box_bg, border_color=c_blue)
    tb_f = s12.shapes.add_textbox(Inches(7.0), Inches(1.9), Inches(5.3), Inches(4.8))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    
    p = tf_f.paragraphs[0]
    p.text = "🌐 Live System Demonstration"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = c_blue
    p.space_after = Pt(8)

    p_summary = tf_f.add_paragraph()
    p_summary.text = "A CFO-grade quantitative platform combining data science, AI high-speed simulation, and corporate financial engineering."
    p_summary.font.size = Pt(10)
    p_summary.font.color.rgb = c_dark
    p_summary.space_after = Pt(12)
    
    p_url_t = tf_f.add_paragraph()
    p_url_t.text = "LIVE CLOUD DEPLOYED WEB DASHBOARD:"
    p_url_t.font.size = Pt(10.5)
    p_url_t.font.bold = True
    p_url_t.font.color.rgb = c_teal
    p_url_t.space_after = Pt(2)
    
    p_url = tf_f.add_paragraph()
    p_url.text = "https://capital-budgeting-project-karthickruban.streamlit.app"
    p_url.font.size = Pt(11)
    p_url.font.bold = True
    p_url.font.color.rgb = c_navy
    p_url.space_after = Pt(14)

    p_qa = tf_f.add_paragraph()
    p_qa.text = "Thank you, Sir! We are ready for your questions."
    p_qa.font.size = Pt(12)
    p_qa.font.bold = True
    p_qa.font.color.rgb = c_navy

    pptx_path = os.path.join(os.path.dirname(__file__), "Capital_Budgeting_Presentation.pptx")
    prs.save(pptx_path)
    print(f"Final Review 12-Slide PPTX successfully created at: {pptx_path}")

if __name__ == "__main__":
    create_presentation()
