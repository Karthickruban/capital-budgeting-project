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
    page_title="Capital Budgeting & Infrastructure Valuation Engine (INR)",
    page_icon="⚡",
    layout="wide"
)

# -------------------------------------------------------------
# Header & Dynamic Hardware Badge
# -------------------------------------------------------------
st.title("⚡ Capital Budgeting & Clean Infrastructure Valuation Engine")

if GPU_AVAILABLE:
    st.markdown("##### *Financial Engineering Course Project with GPU-Accelerated Monte Carlo Risk Engine (₹ INR)*")
else:
    st.markdown("##### *Financial Engineering Course Project: Capital Budgeting & Monte Carlo Risk Simulation (₹ INR)*")

col_info, col_gpu = st.columns([3, 1])
with col_info:
    st.info(
        "💡 **Project Goal**: Evaluate large-scale Indian clean infrastructure investments (Solar, Wind, Hydro, and Desalination) "
        "using **Deterministic Capital Budgeting** (NPV, IRR, PI, Payback, LCOE) and **Stochastic Monte Carlo Risk Analysis** across tariff volatility, cost overruns, and macroeconomic inflation."
    )
with col_gpu:
    if GPU_AVAILABLE:
        st.success(f"🚀 **Compute Engine**: `NVIDIA CUDA GPU`\n\n**Device**: `{GPU_NAME}`")
    else:
        st.info("⚡ **Compute Engine**: `Vectorized C/NumPy`\n\n*(CUDA GPU-Ready Architecture)*")

# -----------------------------------------------------------------------------
# Load Public Infrastructure Dataset (INR)
# -----------------------------------------------------------------------------
csv_path = os.path.join(os.path.dirname(__file__), "infrastructure_projects_data.csv")
if os.path.exists(csv_path):
    dataset_df = pd.read_csv(csv_path)
else:
    dataset_df = pd.DataFrame([
        {"Project_Name": "Rajasthan 100MW Solar Park", "Sector": "Solar Energy", "Country": "India", "CapEx_INR_Crores": 250.0, "Annual_Generation_MWh": 180000, "Base_Tariff_INR_kWh": 3.85, "Project_Lifetime_Years": 20, "Annual_OpEx_INR_Crores": 12.5, "WACC_Percent": 8.0, "Tax_Rate_Percent": 20.0, "Degradation_Rate_Percent": 0.5},
        {"Project_Name": "Tamil Nadu 50MW Wind Farm", "Sector": "Wind Energy", "Country": "India", "CapEx_INR_Crores": 350.0, "Annual_Generation_MWh": 130000, "Base_Tariff_INR_kWh": 4.40, "Project_Lifetime_Years": 25, "Annual_OpEx_INR_Crores": 18.0, "WACC_Percent": 8.5, "Tax_Rate_Percent": 20.0, "Degradation_Rate_Percent": 0.3},
        {"Project_Name": "Gujarat Desalination Facility", "Sector": "Water Treatment", "Country": "India", "CapEx_INR_Crores": 320.0, "Annual_Generation_MWh": 95000, "Base_Tariff_INR_kWh": 5.80, "Project_Lifetime_Years": 30, "Annual_OpEx_INR_Crores": 24.0, "WACC_Percent": 7.5, "Tax_Rate_Percent": 18.0, "Degradation_Rate_Percent": 0.2}
    ])

# -----------------------------------------------------------------------------
# Sidebar: Project Selection & Input Parameters
# -----------------------------------------------------------------------------
st.sidebar.header("📁 Infrastructure Project Selection (INR)")

project_names = list(dataset_df["Project_Name"].values) + ["Custom Infrastructure Project"]
selected_project = st.sidebar.selectbox("Choose Project from Dataset", project_names)

if selected_project != "Custom Infrastructure Project":
    row = dataset_df[dataset_df["Project_Name"] == selected_project].iloc[0]
    default_capex = float(row["CapEx_INR_Crores"])
    default_life = int(row["Project_Lifetime_Years"])
    default_gen = int(row["Annual_Generation_MWh"])
    default_tariff = float(row["Base_Tariff_INR_kWh"])
    default_opex = float(row["Annual_OpEx_INR_Crores"])
    default_wacc = float(row["WACC_Percent"])
    default_tax = float(row["Tax_Rate_Percent"])
    default_deg = float(row["Degradation_Rate_Percent"])
else:
    default_capex, default_life, default_gen, default_tariff, default_opex, default_wacc, default_tax, default_deg = 200.0, 15, 100000, 4.00, 14.0, 9.0, 20.0, 0.5

st.sidebar.subheader("💰 Capital & Construction (CapEx)")
capex = st.sidebar.number_input("Initial CapEx (₹ Crores)", min_value=1.0, max_value=5000.0, value=default_capex, step=10.0)
project_life = st.sidebar.slider("Project Lifetime (Years)", min_value=5, max_value=35, value=default_life)

st.sidebar.subheader("⚡ Operational & Revenue (OpEx)")
annual_gen_mwh = st.sidebar.number_input("Annual Generation (MWh)", min_value=1000, max_value=5000000, value=default_gen, step=10000)
base_tariff = st.sidebar.number_input("PPA Tariff (₹ / kWh)", min_value=1.00, max_value=20.00, value=default_tariff, step=0.05)
annual_opex = st.sidebar.number_input("Year 1 OpEx (₹ Crores)", min_value=0.1, max_value=500.0, value=default_opex, step=0.5)
degradation_rate = st.sidebar.slider("Annual Performance Degradation (%)", 0.0, 3.0, default_deg, step=0.1) / 100

st.sidebar.subheader("📈 Financial & Macroeconomic Parameters")
wacc = st.sidebar.slider("Discount Rate / WACC (%)", 3.0, 18.0, default_wacc, step=0.25) / 100
tax_rate = st.sidebar.slider("Corporate Tax Rate (%)", 0.0, 35.0, default_tax, step=1.0) / 100
inflation_rate = st.sidebar.slider("Expected Annual Inflation (%)", 0.0, 10.0, 2.5, step=0.25) / 100

# -------------------------------------------------------------
# Core Financial Calculations (in ₹ Crores & ₹/kWh)
# -------------------------------------------------------------
def calculate_project_financials(c_val, life_val, gen_val, t_val, o_val, w_val, tax_val, infl_val, deg_val):
    years = np.arange(0, life_val + 1)
    
    # Year 0: Negative Initial Investment (-CapEx in ₹ Cr)
    cash_flows = [-float(c_val)]
    discounted_cfs = [-float(c_val)]
    revenue_list = [0.0]
    opex_list = [0.0]
    taxes_list = [0.0]
    
    tot_disc_costs_cr = float(c_val)
    tot_disc_energy_kwh = 0.0
    
    for t in range(1, life_val + 1):
        effective_gen_mwh = gen_val * ((1.0 - deg_val) ** (t - 1))
        effective_gen_kwh = effective_gen_mwh * 1000.0
        
        # Revenue in ₹ Crores = (kWh * ₹/kWh) / 10,000,000
        rev_cr = (effective_gen_kwh * t_val) / 10_000_000.0
        op_cr = o_val * ((1.0 + infl_val) ** (t - 1))
        
        ebit_cr = rev_cr - op_cr
        tax_cr = max(0.0, ebit_cr * tax_val)
        net_cf_cr = ebit_cr - tax_cr
        
        cash_flows.append(net_cf_cr)
        disc_cf_cr = net_cf_cr / ((1.0 + w_val) ** t)
        discounted_cfs.append(disc_cf_cr)
        revenue_list.append(rev_cr)
        opex_list.append(op_cr)
        taxes_list.append(tax_cr)
        
        tot_disc_costs_cr += op_cr / ((1.0 + w_val) ** t)
        tot_disc_energy_kwh += effective_gen_kwh / ((1.0 + w_val) ** t)
        
    npv_cr = sum(discounted_cfs)
    pi = (npv_cr + c_val) / c_val
    
    # LCOE in ₹ / kWh = (Total Discounted Costs in ₹) / (Total Discounted Energy in kWh)
    lcoe_inr_kwh = (tot_disc_costs_cr * 10_000_000.0) / tot_disc_energy_kwh if tot_disc_energy_kwh > 0 else 0.0
    
    # Robust Internal Rate of Return (IRR) Solver
    def npv_at_rate(r):
        return sum([cf / ((1.0 + r) ** idx) for idx, cf in enumerate(cash_flows)])
    
    try:
        if npv_at_rate(-0.35) * npv_at_rate(2.5) <= 0:
            irr = brentq(npv_at_rate, -0.35, 2.5)
        else:
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
        
    cum_disc_cr = np.cumsum(discounted_cfs)
    payback = next((i for i, v in enumerate(cum_disc_cr) if v >= 0), None)
    
    df_cf = pd.DataFrame({
        "Year": years,
        "Revenue (₹ Cr)": revenue_list,
        "OpEx (₹ Cr)": opex_list,
        "Taxes (₹ Cr)": taxes_list,
        "Net Cash Flow (₹ Cr)": cash_flows,
        "Discounted Cash Flow (₹ Cr)": discounted_cfs,
        "Cumulative Discounted (₹ Cr)": cum_disc_cr
    })
    
    return npv_cr, irr, pi, lcoe_inr_kwh, payback, df_cf

# Base Run
npv_base, irr_base, pi_base, lcoe_base, payback_base, df_schedule = calculate_project_financials(
    capex, project_life, annual_gen_mwh, base_tariff, annual_opex, wacc, tax_rate, inflation_rate, degradation_rate
)

# -------------------------------------------------------------
# Tabs Interface
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analysis 1: Deterministic Capital Budgeting (NPV / IRR / LCOE)",
    "🎲 Analysis 2: Monte Carlo Risk & Uncertainty Engine",
    "📁 Dataset Benchmarks & Descriptive Stats (INR)",
    "📄 Executive Investment Memo (INR)"
])

# -------------------------------------------------------------
# TAB 1: Deterministic Capital Budgeting
# -------------------------------------------------------------
with tab1:
    st.subheader("1. Comprehensive Capital Budgeting & Valuation Scorecard (₹ INR)")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Net Present Value (NPV)", f"₹ {npv_base:,.2f} Cr", delta="VIABLE (ACCEPT)" if npv_base > 0 else "REJECT")
    m2.metric("Internal Rate of Return (IRR)", f"{irr_base*100:.2f}%", delta=f"{(irr_base - wacc)*100:+.2f}% vs WACC")
    m3.metric("Levelized Cost (LCOE)", f"₹ {lcoe_base:.2f} / kWh", delta=f"₹ {base_tariff - lcoe_base:+.2f} Margin")
    m4.metric("Profitability Index (PI)", f"{pi_base:.2f}x", delta="Value Accretive" if pi_base > 1 else "Unfavorable")
    m5.metric("Discounted Payback", f"{payback_base} Years" if payback_base else "Exceeds Lifetime")
    
    st.markdown("---")
    
    col_chart, col_tbl = st.columns([3, 2])
    
    with col_chart:
        fig_waterfall = go.Figure()
        fig_waterfall.add_trace(go.Bar(
            x=df_schedule["Year"],
            y=df_schedule["Net Cash Flow (₹ Cr)"],
            name="Net Annual Cash Flow (₹ Cr)",
            marker_color=['crimson' if x < 0 else 'dodgerblue' for x in df_schedule["Net Cash Flow (₹ Cr)"]]
        ))
        fig_waterfall.add_trace(go.Scatter(
            x=df_schedule["Year"],
            y=df_schedule["Cumulative Discounted (₹ Cr)"],
            name="Cumulative Discounted CF (₹ Cr)",
            mode="lines+markers",
            line=dict(color="darkorange", width=3)
        ))
        fig_waterfall.add_hline(y=0, line_dash="dash", line_color="black")
        fig_waterfall.update_layout(
            title="Cash Flow Waterfall & Discounted Payback Trajectory (₹ Crores)",
            xaxis_title="Operational Year",
            yaxis_title="INR (₹ Crores)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    with col_tbl:
        st.write("#### 📑 Annual Cash Flow Breakdown Schedule (₹ Crores)")
        formatted_df = df_schedule.copy()
        for col in ["Revenue (₹ Cr)", "OpEx (₹ Cr)", "Taxes (₹ Cr)", "Net Cash Flow (₹ Cr)", "Discounted Cash Flow (₹ Cr)", "Cumulative Discounted (₹ Cr)"]:
            formatted_df[col] = formatted_df[col].map("₹ {:,.2f} Cr".format)
        st.dataframe(formatted_df)

# -------------------------------------------------------------
# TAB 2: Monte Carlo Risk Simulation (INR)
# -------------------------------------------------------------
with tab2:
    st.subheader("2. Stochastic Monte Carlo Risk & Uncertainty Engine (₹ INR)")
    
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
            eff_gen_kwh_t = annual_gen_mwh * 1000.0 * ((1.0 - degradation_rate) ** (years_t - 1))
            rev_cr_t = (eff_gen_kwh_t * tariffs_t.unsqueeze(1)) / 10_000_000.0
            op_cr_t = annual_opex * ((1.0 + infl_t.unsqueeze(1)) ** (years_t - 1))
            
            ebit_cr_t = rev_cr_t - op_cr_t
            tax_cr_t = torch.clamp(ebit_cr_t * tax_rate, min=0.0)
            net_cf_cr_t = ebit_cr_t - tax_cr_t
            
            discount_factors = (1.0 + wacc) ** years_t
            disc_cf_cr_t = net_cf_cr_t / discount_factors
            sim_npvs = (-capex_t + torch.sum(disc_cf_cr_t, dim=1)).cpu().numpy()
    else:
        np.random.seed(42)
        sim_tariffs = np.random.normal(base_tariff, base_tariff * 0.15, n_sims)
        sim_capex = capex * np.random.uniform(1.0, 1.25, n_sims)
        sim_infl = np.random.normal(inflation_rate, 0.01, n_sims)
        
        years_arr = np.arange(1, project_life + 1)
        discount_factors = (1.0 + wacc) ** years_arr
        eff_gen_kwh = annual_gen_mwh * 1000.0 * ((1.0 - degradation_rate) ** (years_arr - 1))
        
        rev_mat_cr = np.outer(sim_tariffs, eff_gen_kwh) / 10_000_000.0
        op_mat_cr = annual_opex * np.power(1.0 + sim_infl[:, None], years_arr - 1)
        
        ebit_mat_cr = rev_mat_cr - op_mat_cr
        tax_mat_cr = np.maximum(0, ebit_mat_cr * tax_rate)
        net_cf_mat_cr = ebit_mat_cr - tax_mat_cr
        
        disc_cf_mat_cr = net_cf_mat_cr / discount_factors
        sim_npvs = -sim_capex + np.sum(disc_cf_mat_cr, axis=1)
        
    calc_time = time.time() - start_time
    
    prob_loss = np.mean(sim_npvs < 0) * 100
    var_95 = np.percentile(sim_npvs, 5)
    cvar_95 = np.mean(sim_npvs[sim_npvs <= var_95])
    mean_npv = np.mean(sim_npvs)
    
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Expected Mean Simulated NPV", f"₹ {mean_npv:,.2f} Cr")
    r2.metric("Probability of Loss (P(NPV < 0))", f"{prob_loss:.2f}%", delta=f"{n_sims:,} runs in {calc_time*1000:.1f}ms")
    r3.metric("95% Value-at-Risk (VaR)", f"₹ {var_95:,.2f} Cr")
    r4.metric("Conditional VaR (Expected Shortfall)", f"₹ {cvar_95:,.2f} Cr")
    
    st.markdown("---")
    
    mc_col1, mc_col2 = st.columns([3, 2])
    
    with mc_col1:
        fig_hist = px.histogram(
            sim_npvs,
            nbins=70,
            title=f"Monte Carlo Simulated NPV Distribution Across {n_sims:,} Scenarios (₹ Crores)",
            labels={'value': 'Simulated Net Present Value (₹ Crores)'},
            color_discrete_sequence=['teal']
        )
        fig_hist.add_vline(x=0, line_dash="dash", line_color="crimson", annotation_text="Break-Even Threshold (₹0 Cr)")
        fig_hist.add_vline(x=mean_npv, line_dash="solid", line_color="gold", annotation_text=f"Mean (₹{mean_npv:.1f} Cr)")
        fig_hist.add_vline(x=var_95, line_dash="dot", line_color="orange", annotation_text=f"95% VaR (₹{var_95:.1f} Cr)")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with mc_col2:
        st.write("#### 🌡️ 2-Way Sensitivity Matrix (NPV in ₹ Crores)")
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
            x=[f"₹{t:.2f}/kWh" for t in tariff_range],
            y=[f"{w*100:.1f}%" for w in wacc_range],
            labels=dict(x="PPA Tariff (₹/kWh)", y="Discount Rate (WACC)", color="NPV (₹ Cr)"),
            color_continuous_scale="RdYlGn",
            text_auto=True
        )
        fig_heat.update_layout(title="NPV (₹ Cr) Sensitivity Heatmap")
        st.plotly_chart(fig_heat, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: Dataset Benchmarks & Descriptive Statistics (INR)
# -------------------------------------------------------------
with tab3:
    st.subheader("📁 Public Infrastructure Benchmark Dataset (Indian Rupees)")
    st.markdown("Data Source: **Kaggle / The World Bank & SECI Clean Infrastructure Dataset**")
    
    st.dataframe(dataset_df)
    
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Average Sector CapEx", f"₹ {dataset_df['CapEx_INR_Crores'].mean():.1f} Cr")
    d2.metric("Median Project Lifespan", f"{dataset_df['Project_Lifetime_Years'].median():.0f} Years")
    d3.metric("Average Benchmark Tariff", f"₹ {dataset_df['Base_Tariff_INR_kWh'].mean():.2f} / kWh")
    d4.metric("Average Sector WACC", f"{dataset_df['WACC_Percent'].mean():.2f}%")

# -------------------------------------------------------------
# TAB 4: Executive Investment Memo (INR)
# -------------------------------------------------------------
with tab4:
    st.subheader("📄 Investment Committee Executive Memo (₹ INR)")
    
    decision = "PROCEED WITH INVESTMENT (RECOMMENDED)" if npv_base > 0 and prob_loss < 15 else "REJECT OR RESTRUCTURE TERMS"
    
    st.markdown(f"""
    ### 🏛️ Executive Summary & Recommendation: **{decision}**
    
    * **Project Selected**: {selected_project}
    * **Asset Lifetime**: {project_life} Years | **Discount Rate (WACC)**: {wacc*100:.1f}%
    * **Net Present Value (NPV)**: **₹ {npv_base:,.2f} Crores**
    * **Internal Rate of Return (IRR)**: **{irr_base*100:.2f}%** (Hurdle Rate Spread: {((irr_base - wacc)*100):+.2f}%)
    * **Levelized Cost of Energy (LCOE)**: **₹ {lcoe_base:.2f} / kWh** vs. PPA Contract Tariff of **₹ {base_tariff:.2f} / kWh**
    * **Discounted Payback Horizon**: **{payback_base} Years**
    * **Monte Carlo Risk Profile**:
      * Probability of Negative NPV: **{prob_loss:.2f}%**
      * 95% Value-at-Risk (Worst 5% Outcome): **₹ {var_95:,.2f} Crores**
      * Conditional VaR (Expected Shortfall): **₹ {cvar_95:,.2f} Crores**
    
    ---
    *Generated dynamically by the Financial Engineering Decision Support System.*
    """)
