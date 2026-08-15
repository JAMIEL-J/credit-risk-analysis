# 🏛️ Credit Portfolio Macroeconomic Stress Testing Engine
> **Point-in-Time (PiT) Machine Learning (AUC ~0.70), Risk-Adjusted Return Optimization, and Dynamic ECL Stress Testing under CECL / IFRS 9 Guidelines**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Fast_SQL-FFF000.svg)](https://duckdb.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Champion_Model-green.svg)](https://xgboost.readthedocs.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Graph_Objects-3F4F75.svg)](https://plotly.com/)
[![Regulatory Standard](https://img.shields.io/badge/Compliance-CECL%20%7C%20IFRS%209%20%7C%20CCAR-purple.svg)]()

---

## 🎯 Key Accomplishments

* 🚀 **Big Data Ingestion & Feature Integration:**
  > **Accomplished** end-to-end data pipeline integration of **1,345,310 completed loan records** with 234 months of Federal Reserve macroeconomic data, **as measured by** **100.00% sample retention** and **< 3.0s query execution times**, **by doing** out-of-core columnar extraction and temporal alignment in **DuckDB**.

* 🤖 **Predictive Default Risk Modeling:**
  > **Accomplished** high-precision Point-in-Time (PiT) default risk prediction, **as measured by** pushing Out-of-Time test **ROC-AUC from 0.6265 to 0.6899 (~0.70)**, **Gini from 0.2531 to 0.3798 (+50.1%)**, and **KS separation from 18.03% to 27.41%**, **by doing** behavioral credit feature engineering (`revol_util`, `delinq_2yrs`, `inq_last_6mths`, `annual_inc`, `int_rate`) and training a 4-model champion-challenger suite (XGBoost, Random Forest, LightGBM, Logistic Regression).

* 📊 **Forward-Looking Macro Stress Testing:**
  > **Accomplished** regulatory credit stress testing across a **$7.50 Billion active consumer credit portfolio** (518,706 loans), **as measured by** quantifying baseline vs. severe scenario loss reserves (**$937.7M vs. $694.1M ECL**), **by doing** econometric shock simulation (+3.5% `UNRATE`, +1.5% `FEDFUNDS`) through Scikit-Learn inference pipelines complying with **CECL / IFRS 9 / Basel III** standards.

* 💰 **Risk-Adjusted Return Underwriting Optimization:**
  > **Accomplished** the elimination of negative net return bleed across high-risk borrower tiers, **as measured by** **saving -$30.6 Million in net losses** while **preserving +$45.0 Million in profitable originations**, **by doing** mathematical formulation and SQL modeling of Risk-Adjusted Net Profit:
  $$\mathbf{\text{Net Profit}} = \mathbf{\text{Expected Gross Revenue}} - \mathbf{\text{Expected Credit Loss (ECL)}}$$

* 🖥️ **Ultra-Fast Interactive Analytics & BI Export Engine:**
  > **Accomplished** sub-second portfolio cross-filtering and real-time single-loan multi-model underwriting, **as measured by** a **< 180MB RAM footprint** on standard laptop hardware (Intel i3 / 8GB RAM) and **< 10ms render latency**, **by doing** multi-tier disk caching (`@st.cache_data(persist="disk")`), data downcasting, and automated Power BI / Tableau CSV serialization in [`power_bi_exports/`](file:///J:/Finance%20Projects/Credit/power_bi_exports/).

---

## 📌 Executive Summary & Business Problem

### The Business Question:
> *"How do macroeconomic downturns transmit into default losses across our consumer loan portfolio, what is the Expected Credit Loss (ECL), and what precise Risk-Adjusted Underwriting Rules will maximize portfolio Net Profit while eliminating loss-making segments?"*

### The Flaw of Traditional Scorecards & Naive Loss Cutoffs:
1. **Through-the-Cycle (TTC) Flaw:** Traditional scorecards evaluate borrower risk purely on static attributes while ignoring macroeconomic conditions (`UNRATE` and `FEDFUNDS`).
2. **Naive Loss-Based Cutoffs Flaw:** Halting originations purely because a borrower cohort has an elevated default rate is financially suboptimal. If higher-risk borrowers pay sufficiently high interest rates (e.g. 14%–18%), their interest revenue can comfortably cover default losses, generating strong positive net returns.

```mermaid
flowchart LR
    P1["<b>Phase 1: Data Engineering</b><br/>1.345M Loans + Behavioral Features<br/>+ FRED Macro (UNRATE / FEDFUNDS)"] --> P2["<b>Phase 2: ML Benchmark (AUC ~0.70)</b><br/>4-Model OOT Validation<br/>(XGBoost, LightGBM, LR, RF)"]
    P2 --> P3["<b>Phase 3: Macro Stress Testing</b><br/>Baseline, Adverse (+1.5% U), Severe (+3.5% U)"]
    P3 --> P4["<b>Phase 4: SQL Financial Math</b><br/>Net Profit = Revenue - ECL<br/>FICO x DTI Net Return Matrix"]
    P4 --> P5["<b>Phase 5: The Deliverable</b><br/>Streamlit Live Dashboard + Power BI / Tableau Exports"]
```

---

## 📋 5-Phase Implementation Breakdown (Google XYZ Structure)

| Phase | Milestone | Accomplishment (Google XYZ Structure) | Primary Artifacts |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Data Engineering & Behavioral Features** | **Accomplished** clean ingestion of 1.345M closed loans and 234 months of FRED macro data **as measured by** 100% sample retention and 0 missing macro keys **by doing** out-of-core DuckDB streaming and behavioral feature extraction (`revol_util`, `delinq_2yrs`, `inq_last_6mths`, `annual_inc`, `int_rate`). | • [`cleaned_loans_phase1.parquet`](file:///J:/Finance%20Projects/Credit/data/cleaned_loans_phase1.parquet)<br>• [`reports/Phase1_Data_Engineering_Report.md`](file:///J:/Finance%20Projects/Credit/reports/Phase1_Data_Engineering_Report.md) |
| **Phase 2** | **4-Model ML Engine & Benchmark (AUC ~0.70)** | **Accomplished** Point-in-Time default risk calibration **as measured by** achieving **ROC-AUC = 0.6899, Gini = 0.3798, and KS = 27.41%** on 518,706 test loans **by doing** chronological Out-of-Time split (Train: 2007–2015, Test: 2016–2018) across 4 benchmarked architectures. | • [`02_phase2_model_engine.ipynb`](file:///J:/Finance%20Projects/Credit/02_phase2_model_engine.ipynb)<br>• [`models/all_models.joblib`](file:///J:/Finance%20Projects/Credit/models/all_models.joblib) |
| **Phase 3** | **Macroeconomic Stress Testing Engine** | **Accomplished** portfolio stress testing under supervisory conditions **as measured by** generating baseline vs. adverse vs. severe loan-level default probabilities across $7.50B exposure **by doing** parameter perturbation (+3.5% UNRATE, +1.5% FEDFUNDS). | • [`03_phase3_stress_testing.ipynb`](file:///J:/Finance%20Projects/Credit/03_phase3_stress_testing.ipynb)<br>• [`stressed_portfolio_phase3.parquet`](file:///J:/Finance%20Projects/Credit/data/stressed_portfolio_phase3.parquet) |
| **Phase 4** | **Financial Math & Risk-Adjusted Net Profit** | **Accomplished** precision risk-adjusted capital accounting **as measured by** calculating $1.04B Gross Revenue, $937.7M Base ECL, and +$103.5M Net Profit **by doing** SQL modeling of $\text{ECL} = \text{PD} \times 0.50 \times \text{EAD}$ and $\text{Net Profit} = \text{Revenue} - \text{ECL}$. | • [`sql_scripts/phase4_ecl_calculation.sql`](file:///J:/Finance%20Projects/Credit/sql_scripts/phase4_ecl_calculation.sql)<br>• [`loan_level_ecl_results.parquet`](file:///J:/Finance%20Projects/Credit/data/loan_level_ecl_results.parquet) |
| **Phase 5** | **The Deliverable: Dashboard & BI Exports** | **Accomplished** executive decisioning enablement **as measured by** sub-second interactive simulation and instant BI integration **by doing** a 5-tab Streamlit web application and exporting pre-aggregated CSVs in [`power_bi_exports/`](file:///J:/Finance%20Projects/Credit/power_bi_exports/). | • [`app.py`](file:///J:/Finance%20Projects/Credit/app.py)<br>• [`power_bi_exports/`](file:///J:/Finance%20Projects/Credit/power_bi_exports/) |

---

## 🤖 4-Model Benchmark Leaderboard (Out-of-Time Test Set)

Models were validated on the **518,706 Out-of-Time test cohort** (2016–2018 vintages):

| Rank | Model Architecture | ROC-AUC | Gini ($2 \cdot \text{AUC} - 1$) | KS Statistic (%) | PR-AUC | Log-Loss | Brier Score | Training Time |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **XGBoost (Hist Tree Ensemble)** | **0.6899** | **0.3798** | **27.41%** | **0.3730** | **0.4954** | **0.1622** | **9.49s** |
| 🥈 | **Random Forest (Bagging Ensemble)** | 0.6897 | 0.3793 | **27.74%** | 0.3732 | 0.4948 | 0.1615 | 26.97s |
| 🥉 | **LightGBM (Histogram Booster)** | 0.6893 | 0.3785 | 27.43% | 0.3719 | 0.4966 | 0.1628 | **4.99s** |
| 4 | **Logistic Regression (Scorecard Baseline)** | 0.6809 | 0.3618 | 26.30% | 0.3601 | 0.5071 | 0.1668 | **2.56s** |

---

## 💰 Portfolio Financial Results & Risk-Adjusted Net Profit Matrix

* **Total Portfolio Exposure (EAD):** **`$7,499,413,504.00`** ($7.50 Billion across 518,706 active loans)
* **Expected Annual Gross Revenue:** **`$1,041,159,076.60`** (13.88% Portfolio Gross Yield)
* **Total Baseline Expected Credit Loss (ECL):** **`$937,681,856.00`** (12.50% Loss Rate)
* **Total Baseline Net Profit:** **`$103,477,220.91`** (1.38% Net Margin)
* **Total Severe Scenario Net Profit:** **`$347,085,371.84`** (4.63% Net Margin)

### Risk-Adjusted Net Profit Matrix (FICO Tier vs. DTI Band in $ Millions):

| FICO Credit Tier | DTI: 0% - 10% | DTI: 10% - 20% | DTI: 20% - 30% | DTI: 30% - 40% | DTI: 40%+ | Decision & Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **660 - 699 (Fair)** | **+$19.6M** | **+$25.4M** | <span style="color:red">**-$13.7M**</span> | <span style="color:red">**-$13.9M**</span> | <span style="color:red">**-$1.1M**</span> | ⚠️ Halt DTI $\ge 20\%$ (Loss Bleed) |
| **700 - 749 (Good)** | **+$16.5M** | **+$31.8M** | **+$10.8M** | <span style="color:red">**-$1.9M**</span> | **+$0.2M** | ⚠️ Halt DTI 30%–40% |
| **750 - 799 (Very Good)** | **+$8.0M** | **+$10.8M** | **+$4.3M** | **+$0.7M** | **+$0.2M** | ✅ All Cohorts Profitable |
| **800+ (Exceptional)** | **+$2.5M** | **+$2.2M** | **+$0.8M** | **+$0.2M** | **+$0.04M** | ✅ Prime Margin (>4% Net Yield) |

---

## 🏛️ Official Risk Committee Decisioning Rule

> ### 📢 Risk Committee Underwriting Verdict:
> **"Instead of halting originations blindly based on raw default rate, underwriting policy evaluates Risk-Adjusted Net Return ($\text{Revenue} - \text{ECL}$). Halt originations exclusively for segments generating negative net returns (specifically FICO 660–699 with DTI $\ge$ 20% and FICO 700–749 with DTI $\ge$ 30%) to eliminate $-\$30.6\text{ Million}$ in net losses, while preserving $\$45.0\text{ Million}$ in profitable originations from lower-DTI cohorts."**

---

## 📖 How to Use This Repository

### 1. Installation & Environment Setup
Clone the repository and install the dependencies:
```bash
git clone https://github.com/JAMIEL-J/credit-risk-analysis.git
cd credit-risk-analysis
pip install -r requirements.txt
```

### 2. Launching the Interactive Streamlit Web App
Launch the dashboard locally:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` (or `http://localhost:8502`).

### 3. Navigating Dashboard Tabs:
* **🏛️ The Deliverable: Portfolio Dashboard:** Slice scenario projections, toggle between **Risk-Adjusted Net Profit ($M)** and **Expected Credit Loss ($M)** on the interactive heatmap.
* **🧭 End-to-End Workflow & Architecture:** Technical breakdown of all 5 project phases.
* **🤖 4-Model ML Benchmark & Underwriter:** Inspect the leaderboard, head-to-head model deltas, and score single loan applicants in real time across all 4 models.
* **📈 FRED Macroeconomic Deep-Dive:** Dual-axis historical analysis of `UNRATE` and `FEDFUNDS`.
* **🛡️ Interactive Policy Simulator:** Test custom FICO and DTI underwriting thresholds.

### 4. Standalone BI Exports ([`power_bi_exports/`](file:///J:/Finance%20Projects/Credit/power_bi_exports/))
To build custom reports in **Power BI**, **Tableau**, or **Looker Studio**:
1. Open your BI software and select **Get Data $\rightarrow$ Text/CSV**.
2. Connect to:
   * `power_bi_exports/ecl_risk_matrix_fico_dti.csv` (Aggregated Net Profit & ECL Matrix)
   * `power_bi_exports/ecl_summary_by_purpose.csv` (Purpose Breakdown)
   * `power_bi_exports/stressed_portfolio_phase3.csv` (Loan-Level Stressed Portfolio)

---

---

## 🔮 Future Enhancements & MLOps Production Roadmap

To scale this analytical engine into an automated, enterprise-grade banking production system, the planned **MLOps & CI/CD Architecture** includes:

```mermaid
flowchart TD
    subgraph CI["1. Continuous Integration (CI)"]
        A["Git Push / PR"] --> B["Linting & Style (Ruff / Black)"]
        B --> C["Data Contract Validation (Great Expectations)"]
        C --> D["Financial Math Unit Tests (pytest)"]
    end

    subgraph CD["2. Continuous Delivery (CD) & Registry"]
        D --> E["Model Registry & Lineage (MLflow / DVC)"]
        E --> F["Docker Containerization (< 180MB RAM)"]
        F --> G["Staging & Shadow Mode Deployment"]
    end

    subgraph CM["3. Continuous Monitoring (SR 11-7)"]
        G --> H["Data Drift Alerts (PSI / CSI Monitoring)"]
        G --> I["Rolling Model Decay (AUC / Brier Score)"]
        G --> J["Automated FRED Macro Webhooks"]
    end

    subgraph CT["4. Continuous Training (CT)"]
        H & I -->|PSI >= 0.25 or KS Drop > 5%| K["Automated Retraining Pipeline"]
        K -->|Challenger Beats Champion| E
    end
```

### 🛠️ MLOps Implementation Pillars:

* 🔄 **1. Automated CI/CD Testing Pipeline (GitHub Actions):**
  * **Objective:** Automatically validate all code commits with **`pytest`** unit tests verifying financial math formulas ($\text{ECL} = \text{PD} \times \text{LGD} \times \text{EAD}$ and $\text{Net Profit} = \text{Revenue} - \text{ECL}$), schema assertions via **Great Expectations**, and sub-second model inference checks.

* 📦 **2. Centralized Model Registry & Artifact Versioning (MLflow / DVC):**
  * **Objective:** Track and version all serialized candidate models with full lineage metadata (training dataset hashes, Git commit SHAs, Out-of-Time ROC-AUC, KS statistics, and Brier calibration scores) for complete regulatory auditability.

* 🐳 **3. Lightweight Containerized Deployment (Docker & Multi-Stage Builds):**
  * **Objective:** Package the Streamlit interface, DuckDB SQL engine, and Scikit-Learn pipelines into lightweight, isolated Docker containers optimized for low memory footprints ($< 180\text{MB}$ RAM) and seamless cloud deployment (AWS ECS, GCP Cloud Run, or Azure App Service).

* 📊 **4. Real-Time Model Governance & Drift Monitoring (SR 11-7 / Fed Standards):**
  * **Objective:** Implement automated **Population Stability Index (PSI)** and **Characteristic Stability Index (CSI)** trackers on incoming monthly applicant batches. Alert credit risk teams when demographic drift exceeds regulatory thresholds ($\text{PSI} \ge 0.25$).

* 🔁 **5. Automated Continuous Training (CT) & Shadow Deployment:**
  * **Objective:** Establish event-driven retraining pipelines triggered by drift alerts or scheduled quarterly vintage maturation, running Challenger models in **Shadow Mode** against the Champion XGBoost before automated gated promotion.

* 🌐 **6. Dynamic Federal Reserve API Ingestion (`fredapi`):**
  * **Objective:** Connect automated monthly webhooks directly to the St. Louis Fed API (`fredapi`) to ingest updated `UNRATE` and `FEDFUNDS` figures and auto-refresh supervisory stress scenarios.

---

## 📚 Technical Documentation & Reports Hub

Comprehensive documentation is organized in the [`reports/`](file:///J:/Finance%20Projects/Credit/reports/) folder:
* 📄 **[`reports/Executive_Business_Summary_and_Glossary.md`](file:///J:/Finance%20Projects/Credit/reports/Executive_Business_Summary_and_Glossary.md)**: Full project narrative, mathematical equations, and credit risk terminology glossary.
* 📄 **[`reports/Phase1_Data_Engineering_Report.md`](file:///J:/Finance%20Projects/Credit/reports/Phase1_Data_Engineering_Report.md)**: DuckDB ingestion, behavioral credit variable cleaning, and macro alignment.
* 📄 **[`reports/Phase2_Model_Evaluation_Report.md`](file:///J:/Finance%20Projects/Credit/reports/Phase2_Model_Evaluation_Report.md)**: 4-model champion-challenger benchmark and OOT validation.
* 📄 **[`reports/Phase3_Stress_Testing_Report.md`](file:///J:/Finance%20Projects/Credit/reports/Phase3_Stress_Testing_Report.md)**: Baseline, Adverse, and Severe stress testing specifications.
* 📄 **[`reports/Phase4_Financial_Math_Report.md`](file:///J:/Finance%20Projects/Credit/reports/Phase4_Financial_Math_Report.md)**: Expected revenue, Expected Credit Loss, and Risk-Adjusted Net Profit formulations.
* 📄 **[`reports/Phase5_Power_BI_Deliverable_Guide.md`](file:///J:/Finance%20Projects/Credit/reports/Phase5_Power_BI_Deliverable_Guide.md)**: Power BI/Tableau schema guide.

---
*Built with Python, DuckDB, XGBoost, Scikit-Learn, and Streamlit.*
