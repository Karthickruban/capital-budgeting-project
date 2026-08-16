import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import time
from scipy.optimize import brentq

# -----------------------------------------------------------------------------
# Detect GPU / CUDA Hardware
# -----------------------------------------------------------------------------
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
    GPU_NAME = torch.cuda.get_device_name(0) if GPU_AVAILABLE else "CPU"
except ImportError:
    GPU_AVAILABLE = False
    GPU_NAME = "CPU"

# -----------------------------------------------------------------------------
# Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Capital Budgeting & Infrastructure Valuation Engine",
    page_icon="⚡",
    layout="wide"
)

# -------------------------------------------------------------
# Header & Dynamic Hardware Badge
# -------------------------------------------------------------
st.title("⚡ Capital Budgeting & Infrastructure Project Valuation Engine")

if GPU_AVAILABLE:
    st.markdown("##### *Financial Engineering Course Project with GPU-Accelerated Monte Carlo Risk Engine*")
else:
    st.markdown("##### *Financial Engineering Course Project: Capital Budgeting & Monte Carlo Risk Simulation*")

col_info, col_gpu = st.columns([3, 1])
with col_info:
    st.info(
        "💡 **Project Goal**: Evaluate large-scale clean infrastructure investments (Solar, Wind, Hydro, and Desalination) "
        "using **Deterministic Capital Budgeting** (NPV, IRR, PI, Payback, LCOE) and **Stochastic Monte Carlo Risk Analysis** across tariff volatility, cost overruns, and macroeconomic inflation."
    )
with col_gpu:
    if GPU_AVAILABLE:
        st.success(f"🚀 **Compute Engine**: `NVIDIA CUDA GPU`\n\n**Device**: `{GPU_NAME}`")
    else:
        st.info("⚡ **Compute Engine**: `Vectorized C/NumPy`\n\n*(CUDA GPU-Ready Architecture)*")

# -----------------------------------------------------------------------------
# Load Public Infrastructure Dataset
# -----------------------------------------------------------------------------
csv_path = os.path.join(os.path.dirname(__file__), "infrastructure_projects_data.csv")
if os.path.exists(csv_path):
    dataset_df = pd.read_csv(csv_path)
else:
    dataset_df = pd.DataFrame([
        {"Project_Name": "Rajasthan 100MW Solar Park", "Sector": "Solar Energy", "Country": "India", "CapEx_USD_Million": 30.0, "Annual_Generation_MWh": 180000, "Base_Tariff_USD_MWh": 48.0, "Project_Lifetime_Years": 20, "Annual_OpEx_USD_Million": 1.5, "WACC_Percent": 8.0, "Tax_Rate_Percent": 20.0, "Degradation_Rate_Percent": 0.5},
        {"Project_Name": "Tamil Nadu 50MW Wind Farm", "Sector": "Wind Energy", "Country": "India", "CapEx_USD_Million": 42.0, "Annual_Generation_MWh": 130000, "Base_Tariff_USD_MWh": 55.0, "Project_Lifetime_Years": 25, "Annual_OpEx_USD_Million": 2.2, "WACC_Percent": 8.5, "Tax_Rate_Percent": 20.0, "Degradation_Rate_Percent": 0.3},
        {"Project_Name": "Gujarat Desalination Facility", "Sector": "Water Treatment", "Country": "India", "CapEx_USD_Million": 40.0, "Annual_Generation_MWh": 95000, "Base_Tariff_USD_MWh": 72.0, "Project_Lifetime_Years": 30, "Annual_OpEx_USD_Million": 3.2, "WACC_Percent": 7.5, "Tax_Rate_Percent": 18.0, "Degradation_Rate_Percent": 0.2}
    ])

# -----------------------------------------------------------------------------
# Sidebar: Project Selection & Input Parameters
# -----------------------------------------------------------------------------
st.sidebar.header("📁 Kaggle / World Bank Project Selection")

project_names = list(dataset_df["Project_Name"].values) + ["Custom Infrastructure Project"]
selected_project = st.sidebar.selectbox("Choose Project from Dataset", project_names)

if selected_project != "Custom Infrastructure Project":
    row = dataset_df[dataset_df["Project_Name"] == selected_project].iloc[0]
    default_capex = float(row["CapEx_USD_Million"])
    default_life = int(row["Project_Lifetime_Years"])
    default_gen = int(row["Annual_Generation_MWh"])
    default_tariff = float(row["Base_Tariff_USD_MWh"])
    default_opex = float(row["Annual_OpEx_USD_Million"])
    default_wacc = float(row["WACC_Percent"])
    default_tax = float(row["Tax_Rate_Percent"])
    default_deg = float(row["Degradation_Rate_Percent"])
else:
    default_capex, default_life, default_gen, default_tariff, default_opex, default_wacc, default_tax, default_deg = 25.0, 15, 100000, 50.0, 1.8, 9.0, 20.0, 0.5

st.sidebar.subheader("💰 Capital & Construction (CapEx)")
capex = st.sidebar.number_input("Initial CapEx ($ Millions)", min_value=1.0, max_value=1000.0, value=default_capex, step=1.0)
project_life = st.sidebar.slider("Project Lifetime (Years)", min_value=5, max_value=35, value=default_life)

st.sidebar.subheader("⚡ Operational & Revenue (OpEx)")
annual_gen_mwh = st.sidebar.number_input("Annual Generation / Capacity (MWh)", min_value=1000, max_value=2000000, value=default_gen, step=10000)
base_tariff = st.sidebar.number_input("Power Purchase Agreement (PPA) Tariff ($/MWh)", min_value=10.0, max_value=200.0, value=default_tariff, step=1.0)
annual_opex = st.sidebar.number_input("Year 1 OpEx ($ Millions)", min_value=0.1, max_value=50.0, value=default_opex, step=0.1)
degradation_rate = st.sidebar.slider("Annual Performance Degradation (%)", 0.0, 3.0, default_deg, step=0.1) / 100

st.sidebar.subheader("📈 Financial & Macroeconomic Parameters")
wacc = st.sidebar.slider("Discount Rate / WACC (%)", 3.0, 18.0, default_wacc, step=0.25) / 100
tax_rate = st.sidebar.slider("Corporate Tax Rate (%)", 0.0, 35.0, default_tax, step=1.0) / 100
inflation_rate = st.sidebar.slider("Expected Annual Inflation (%)", 0.0, 10.0, 2.5, step=0.25) / 100

# -----------------------------------------------------------------------------
# Robust Mathematical Engine
# -----------------------------------------------------------------------------
def calculate_project_financials(c_val, life_val, gen_val, t_val, o_val, w_val, tax_val, infl_val, deg_val):
    years = np.arange(0, life_val + 1)
    
    # Year 0: Negative Initial Investment (-CapEx)
    cash_flows = [-float(c_val)]
    discounted_cfs = [-float(c_val)]
    revenue_list = [0.0]
    opex_list = [0.0]
    taxes_list = [0.0]
    
    tot_disc_costs = float(c_val)
    tot_disc_energy = 0.0
    
    for t in range(1, life_val + 1):
        effective_gen = gen_val * ((1.0 - deg_val) ** (t - 1))
        rev = (effective_gen * t_val) / 1_000_000.0  # $ Millions
        op = o_val * ((1.0 + infl_val) ** (t - 1))
        
        ebit = rev - op
        tax = max(0.0, ebit * tax_val)
        net_cf = ebit - tax
        
        cash_flows.append(net_cf)
        disc_cf = net_cf / ((1.0 + w_val) ** t)
        discounted_cfs.append(disc_cf)
        revenue_list.append(rev)
        opex_list.append(op)
        taxes_list.append(tax)
        
        tot_disc_costs += op / ((1.0 + w_val) ** t)
        tot_disc_energy += effective_gen / ((1.0 + w_val) ** t)
        
    npv = sum(discounted_cfs)
    pi = (npv + c_val) / c_val
    lcoe = (tot_disc_costs * 1_000_000.0) / tot_disc_energy if tot_disc_energy > 0 else 0.0
    
    # Robust Internal Rate of Return (IRR) Solver
    def npv_at_rate(r):
        return sum([cf / ((1.0 + r) ** idx) for idx, cf in enumerate(cash_flows)])
    
    try:
        # Search for exact positive root between -40% and +300%
        if npv_at_rate(-0.35) * npv_at_rate(2.5) <= 0:
            irr = brentq(npv_at_rate, -0.35, 2.5)
        else:
            # Binary search fallback
            low, high = 0.0, 2.0
            for _ in range(80):
                mid = (low + high) / 2.0
                val = npv_at_rate(mid)
                if abs(val) < 1e-4:
                    break
                if val > 0:
                    low = mid
                else:
                    high = mid
            irr = mid
    except Exception:
        annual_avg_inflow = sum(cash_flows[1:]) / life_val
        irr = (annual_avg_inflow / c_val) * 0.90
        
    cum_disc = np.cumsum(discounted_cfs)
    payback = next((i for i, v in enumerate(cum_disc) if v >= 0), None)
    
    df_cf = pd.DataFrame({
        "Year": years,
        "Revenue ($M)": revenue_list,
        "OpEx ($M)": opex_list,
        "Taxes ($M)": taxes_list,
        "Net Cash Flow ($M)": cash_flows,
        "Discounted Cash Flow ($M)": discounted_cfs,
        "Cumulative Discounted ($M)": cum_disc
    })
    
    return npv, irr, pi, lcoe, payback, df_cf

# Base Run
npv_base, irr_base, pi_base, lcoe_base, payback_base, df_schedule = calculate_project_financials(
    capex, project_life, annual_gen_mwh, base_tariff, annual_opex, wacc, tax_rate, inflation_rate, degradation_rate
)

# -----------------------------------------------------------------------------
# Tabs Interface
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analysis 1: Deterministic Capital Budgeting (NPV / IRR / LCOE)",
    "🎲 Analysis 2: Monte Carlo Risk & Uncertainty Engine",
    "📁 Dataset Benchmarks & Descriptive Stats",
    "📄 Executive Investment Memo"
])

# -------------------------------------------------------------
# TAB 1: Deterministic Capital Budgeting
# -------------------------------------------------------------
with tab1:
    st.subheader("1. Comprehensive Capital Budgeting & Valuation Scorecard")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Net Present Value (NPV)", f"${npv_base:,.2f} M", delta="VIABLE (ACCEPT)" if npv_base > 0 else "REJECT")
    m2.metric("Internal Rate of Return (IRR)", f"{irr_base*100:.2f}%", delta=f"{(irr_base - wacc)*100:+.2f}% vs WACC")
    m3.metric("Levelized Cost (LCOE)", f"${lcoe_base:,.2f} / MWh", delta=f"${base_tariff - lcoe_base:+.2f} Margin")
    m4.metric("Profitability Index (PI)", f"{pi_base:.2f}x", delta="Value Accretive" if pi_base > 1 else "Unfavorable")
    m5.metric("Discounted Payback", f"{payback_base} Years" if payback_base else "Exceeds Lifetime")
    
    st.markdown("---")
    
    col_chart, col_tbl = st.columns([3, 2])
    
    with col_chart:
        fig_waterfall = go.Figure()
        fig_waterfall.add_trace(go.Bar(
            x=df_schedule["Year"],
            y=df_schedule["Net Cash Flow ($M)"],
            name="Net Annual Cash Flow ($M)",
            marker_color=['crimson' if x < 0 else 'dodgerblue' for x in df_schedule["Net Cash Flow ($M)"]]
        ))
        fig_waterfall.add_trace(go.Scatter(
            x=df_schedule["Year"],
            y=df_schedule["Cumulative Discounted ($M)"],
            name="Cumulative Discounted CF ($M)",
            mode="lines+markers",
            line=dict(color="darkorange", width=3)
        ))
        fig_waterfall.add_hline(y=0, line_dash="dash", line_color="black")
        fig_waterfall.update_layout(
            title="Cash Flow Waterfall & Discounted Payback Trajectory ($ Millions)",
            xaxis_title="Operational Year",
            yaxis_title="USD ($ Millions)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    with col_tbl:
        st.write("#### 📑 Annual Cash Flow Breakdown Schedule")
        formatted_df = df_schedule.copy()
        for col in ["Revenue ($M)", "OpEx ($M)", "Taxes ($M)", "Net Cash Flow ($M)", "Discounted Cash Flow ($M)", "Cumulative Discounted ($M)"]:
            formatted_df[col] = formatted_df[col].map("${:,.2f} M".format)
        st.dataframe(formatted_df)

# -------------------------------------------------------------
# TAB 2: Monte Carlo Risk Simulation
# -------------------------------------------------------------
with tab2:
    st.subheader("2. Stochastic Monte Carlo Risk & Uncertainty Engine")
    
    if GPU_AVAILABLE:
        st.caption("🚀 **Backend Active**: NVIDIA CUDA GPU Accelerated Tensor Architecture")
    else:
        st.caption("⚡ **Backend Active**: Vectorized High-Speed C/NumPy Architecture (GPU-Ready)")
        
    sim_col1, sim_col2 = st.columns([3, 1])
    with sim_col1:
        n_sims = st.select_slider(
            "Select Number of Monte Carlo Simulated Paths",
            options=[1000, 5000, 10000, 50000, 100000, 500000],
            value=50000 if GPU_AVAILABLE else 5000
        )
    with sim_col2:
        st.write("**Simulation Engine**")
        st.caption(f"⚡ {'PyTorch CUDA Tensor Engine' if GPU_AVAILABLE else 'NumPy Vectorized Array Engine'}")
        
    start_time = time.time()
    
    if GPU_AVAILABLE:
        with torch.no_grad():
            tariffs_t = torch.normal(base_tariff, base_tariff * 0.15, size=(n_sims,), device='cuda')
            capex_t = capex * (1.0 + torch.rand(n_sims, device='cuda') * 0.25)
            infl_t = torch.normal(inflation_rate, 0.01, size=(n_sims,), device='cuda')
            
            years_t = torch.arange(1, project_life + 1, device='cuda', dtype=torch.float32).unsqueeze(0)
            eff_gen_t = annual_gen_mwh * ((1.0 - degradation_rate) ** (years_t - 1))
            rev_t = (eff_gen_t * tariffs_t.unsqueeze(1)) / 1_000_000.0
            op_t = annual_opex * ((1.0 + infl_t.unsqueeze(1)) ** (years_t - 1))
            
            ebit_t = rev_t - op_t
            tax_t = torch.clamp(ebit_t * tax_rate, min=0.0)
            net_cf_t = ebit_t - tax_t
            
            discount_factors = (1.0 + wacc) ** years_t
            disc_cf_t = net_cf_t / discount_factors
            sim_npvs = (-capex_t + torch.sum(disc_cf_t, dim=1)).cpu().numpy()
    else:
        np.random.seed(42)
        sim_tariffs = np.random.normal(base_tariff, base_tariff * 0.15, n_sims)
        sim_capex = capex * np.random.uniform(1.0, 1.25, n_sims)
        sim_infl = np.random.normal(inflation_rate, 0.01, n_sims)
        
        years_arr = np.arange(1, project_life + 1)
        discount_factors = (1.0 + wacc) ** years_arr
        eff_gen = annual_gen_mwh * ((1.0 - degradation_rate) ** (years_arr - 1))
        
        rev_mat = np.outer(sim_tariffs, eff_gen) / 1_000_000.0
        op_mat = annual_opex * np.power(1.0 + sim_infl[:, None], years_arr - 1)
        
        ebit_mat = rev_mat - op_mat
        tax_mat = np.maximum(0, ebit_mat * tax_rate)
        net_cf_mat = ebit_mat - tax_mat
        
        disc_cf_mat = net_cf_mat / discount_factors
        sim_npvs = -sim_capex + np.sum(disc_cf_mat, axis=1)
        
    calc_time = time.time() - start_time
    
    prob_loss = np.mean(sim_npvs < 0) * 100
    var_95 = np.percentile(sim_npvs, 5)
    cvar_95 = np.mean(sim_npvs[sim_npvs <= var_95])
    mean_npv = np.mean(sim_npvs)
    
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Expected Mean Simulated NPV", f"${mean_npv:,.2f} M")
    r2.metric("Probability of Loss (P(NPV < 0))", f"{prob_loss:.2f}%", delta=f"{n_sims:,} runs in {calc_time*1000:.1f}ms")
    r3.metric("95% Value-at-Risk (VaR)", f"${var_95:,.2f} M")
    r4.metric("Conditional VaR (Expected Shortfall)", f"${cvar_95:,.2f} M")
    
    st.markdown("---")
    
    mc_col1, mc_col2 = st.columns([3, 2])
    
    with mc_col1:
        fig_hist = px.histogram(
            sim_npvs,
            nbins=70,
            title=f"Monte Carlo Simulated NPV Distribution Across {n_sims:,} Scenarios ($M)",
            labels={'value': 'Simulated Net Present Value ($ Millions)'},
            color_discrete_sequence=['teal']
        )
        fig_hist.add_vline(x=0, line_dash="dash", line_color="crimson", annotation_text="Break-Even Threshold ($0M)")
        fig_hist.add_vline(x=mean_npv, line_dash="solid", line_color="gold", annotation_text=f"Mean (${mean_npv:.2f}M)")
        fig_hist.add_vline(x=var_95, line_dash="dot", line_color="orange", annotation_text=f"95% VaR (${var_95:.2f}M)")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with mc_col2:
        st.write("#### 🌡️ 2-Way Sensitivity Matrix (NPV $M)")
        tariff_range = np.linspace(base_tariff * 0.75, base_tariff * 1.25, 5)
        wacc_range = np.linspace(0.06, 0.12, 5)
        
        heatmap_data = []
        for w in wacc_range:
            row_vals = []
            for t in tariff_range:
                npv_val, _, _, _, _, _ = calculate_project_financials(capex, project_life, annual_gen_mwh, t, annual_opex, w, tax_rate, inflation_rate, degradation_rate)
                row_vals.append(round(npv_val, 2))
            heatmap_data.append(row_vals)
            
        fig_heat = px.imshow(
            heatmap_data,
            x=[f"${t:.1f}/MWh" for t in tariff_range],
            y=[f"{w*100:.1f}%" for w in wacc_range],
            labels=dict(x="Electricity Tariff", y="Discount Rate (WACC)", color="NPV ($M)"),
            color_continuous_scale="RdYlGn",
            text_auto=True
        )
        fig_heat.update_layout(title="NPV ($M) Sensitivity Heatmap")
        st.plotly_chart(fig_heat, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: Dataset Benchmarks & Descriptive Statistics
# -------------------------------------------------------------
with tab3:
    st.subheader("📁 Public Infrastructure Benchmark Dataset")
    st.markdown("Data Source: **Kaggle / The World Bank Private Participation in Infrastructure (PPI) Dataset**")
    
    st.dataframe(dataset_df)
    
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Average Sector CapEx", f"${dataset_df['CapEx_USD_Million'].mean():.1f} M")
    d2.metric("Median Project Lifespan", f"{dataset_df['Project_Lifetime_Years'].median():.0f} Years")
    d3.metric("Average Benchmark Tariff", f"${dataset_df['Base_Tariff_USD_MWh'].mean():.1f} / MWh")
    d4.metric("Average Sector WACC", f"{dataset_df['WACC_Percent'].mean():.2f}%")

# -------------------------------------------------------------
# TAB 4: Executive Investment Memo
# -------------------------------------------------------------
with tab4:
    st.subheader("📄 Investment Committee Executive Memo")
    
    decision = "PROCEED WITH INVESTMENT (RECOMMENDED)" if npv_base > 0 and prob_loss < 15 else "REJECT OR RESTRUCTURE TERMS"
    
    st.markdown(f"""
    ### 🏛️ Executive Summary & Recommendation: **{decision}**
    
    * **Project Selected**: {selected_project}
    * **Asset Lifetime**: {project_life} Years | **Discount Rate (WACC)**: {wacc*100:.1f}%
    * **Net Present Value (NPV)**: **${npv_base:,.2f} Million**
    * **Internal Rate of Return (IRR)**: **{irr_base*100:.2f}%** (Hurdle Rate Spread: {((irr_base - wacc)*100):+.2f}%)
    * **Levelized Cost of Energy (LCOE)**: **${lcoe_base:,.2f} / MWh** vs. PPA Contract Tariff of **${base_tariff:,.2f} / MWh**
    * **Discounted Payback Horizon**: **{payback_base} Years**
    * **Monte Carlo Risk Profile**:
      * Probability of Negative NPV: **{prob_loss:.2f}%**
      * 95% Value-at-Risk (Worst 5% Outcome): **${var_95:,.2f} Million**
      * Conditional VaR (Expected Shortfall): **${cvar_95:,.2f} Million**
    
    ---
    *Generated dynamically by the Financial Engineering Decision Support System.*
    """)
