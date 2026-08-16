# ⚡ Capital Budgeting and Infrastructure Project Valuation with Monte Carlo Risk Simulation

### Financial Engineering Course Project (AI & Data Science)

---

## 📋 1. Project Submission Details

* **Project Title**: `Capital Budgeting and Infrastructure Project Valuation with Monte Carlo Risk Simulation`
* **Dataset Used**: `https://datacatalog.worldbank.org/search/dataset/0037798/Private-Participation-in-Infrastructure`
* **Source of Dataset**: `The World Bank Open Data Portal & IRENA Global Renewable Benchmarks`

---

## 🌍 2. Real-World Motivation & Industry Value

Large-scale clean infrastructure projects (such as 100MW Solar Parks, 50MW Wind Farms, and Desalination Plants) require **massive upfront capital expenditure ($20M - $100M)** and operate over **20 to 30 year lifetimes**.

Before capital deployment, institutional investors, banks, and Chief Financial Officers (CFOs) require:
1. **Deterministic Financial Viability**: Verifying whether discounted lifetime cash flows generate returns exceeding the cost of capital (**WACC**).
2. **Cost-Floor Benchmarking**: Computing the **Levelized Cost of Energy (LCOE)** to negotiate Power Purchase Agreement (PPA) tariffs.
3. **Tail-Risk Stress Testing**: Running **Stochastic Monte Carlo Simulations** across volatile energy prices, construction cost overruns, and inflation to calculate the exact probability of loss.

---

## 🧮 3. Core Financial Engineering Mathematical Formulations

### A. Net Present Value (NPV)
$$\text{NPV} = -I_0 + \sum_{t=1}^{N} \frac{CF_t}{(1 + \text{WACC})^t}$$
* $I_0$ = Initial Capital Expenditure (CapEx).
* $CF_t$ = Net annual cash flow at operational year $t = (\text{Revenue}_t - \text{OpEx}_t) \times (1 - \text{Tax Rate})$.
* $\text{WACC}$ = Weighted Average Cost of Capital.

### B. Internal Rate of Return (IRR)
The discount rate at which $\text{NPV} = 0$:
$$0 = -I_0 + \sum_{t=1}^{N} \frac{CF_t}{(1 + \text{IRR})^t}$$
* **Hurdle Rule**: Project is accepted if $\text{IRR} > \text{WACC}$.

### C. Levelized Cost of Energy (LCOE in $/MWh)
$$\text{LCOE} = \frac{\text{Initial CapEx} + \sum_{t=1}^{N} \frac{\text{OpEx}_t}{(1 + \text{WACC})^t}}{\sum_{t=1}^{N} \frac{\text{Annual Energy Output (MWh)}_t}{(1 + \text{WACC})^t}}$$

### D. Profitability Index (PI)
$$\text{PI} = \frac{\sum_{t=1}^{N} \frac{CF_t}{(1 + \text{WACC})^t}}{I_0}$$

### E. Stochastic Monte Carlo Simulation (5,000 Iterations)
* **Electricity Tariff**: $\mathcal{N}(\mu_{\text{tariff}}, \sigma = 15\%)$
* **CapEx Cost Overruns**: $\mathcal{U}(1.0, 1.25)$ (0% to +25% construction overrun)
* **Inflation Rate**: $\mathcal{N}(\mu_{\text{inflation}}, \sigma = 1\%)$
* **Risk Metrics**:
  * $\text{Probability of Loss} = P(\text{NPV} < 0) = \frac{\sum \mathbb{I}(\text{NPV}_i < 0)}{5000} \times 100\%$
  * **95% Value-at-Risk (VaR)** = 5th percentile worst-case simulated NPV.
  * **Conditional VaR (CVaR / Expected Shortfall)** = Mean loss in the worst 5% tail.

---

## 📊 4. The Two Distinct Analyses Required

| Analysis | Description | Key Outputs / Visuals |
| :--- | :--- | :--- |
| **Analysis 1** | Deterministic Capital Budgeting & Levelized Cost Valuation | NPV, IRR, PI, LCOE, Payback Horizon, Cash Flow Waterfall chart, Discounted Cumulative Trajectory |
| **Analysis 2** | Stochastic Monte Carlo Risk Engine (5,000 Runs) | Probability of Loss %, 95% VaR, CVaR, NPV Probability Density Histogram, 2D Sensitivity Heatmap across Tariff vs. WACC |

---

## 🚀 5. How to Run the Application

```bash
cd /Users/karthicksanjana/.gemini/antigravity/scratch/capital_budgeting_project
pip install -r requirements.txt
streamlit run app.py
```

---

## 🎯 6. Mid-Review Viva Preparation (Top 7 Questions & Answers)

### Q1: What is Levelized Cost of Energy (LCOE)?
> **Answer**: *"LCOE is the net present value of all capital and operational costs divided by the total discounted electricity output over the asset's lifetime. It represents the exact minimum price per MWh at which electricity must be sold to break even on the investment."*

### Q2: Why is IRR compared against WACC?
> **Answer**: *"WACC is the company's cost of capital. If a project's IRR is higher than WACC, the project creates net economic profit above its financing costs."*

### Q3: Why did you implement Monte Carlo simulation?
> **Answer**: *"A deterministic NPV assumes static energy tariffs and zero construction cost overruns for 20 years. Monte Carlo simulates 5,000 stochastic combinations of tariff volatility, cost overruns, and inflation to calculate the exact probability of loss and 95% Value-at-Risk (VaR)."*

### Q4: What does a Profitability Index (PI) of 1.35 mean?
> **Answer**: *"It means every $1.00 invested in initial CapEx creates $1.35 in present value terms, delivering a 35% net value addition."*

### Q5: What dataset is used?
> **Answer**: *"We utilize benchmark infrastructure parameters from The World Bank Private Participation in Infrastructure (PPI) database and IRENA Global Renewable Cost benchmarks."*

### Q6: How does annual asset degradation affect cash flows?
> **Answer**: *"Solar panels and wind turbines degrade over time (e.g. 0.5% per year). Our model discounts annual generation ($Gen_t = Gen_0 \times (1-d)^t$), ensuring revenues reflect realistic physical wear and tear."*

### Q7: How does this fulfill the course project guidelines?
> **Answer**: *"It pulls and cleans real infrastructure data, displays descriptive statistics on demand, and delivers two distinct financial engineering analyses: Deterministic Capital Budgeting (NPV/IRR/LCOE) and Stochastic Monte Carlo Risk Modeling."*
