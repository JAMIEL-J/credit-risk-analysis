# Credit Portfolio Macroeconomic Stress Testing Engine

**Point-in-Time (PiT) Machine Learning, Risk-Adjusted Return Optimization, and Dynamic ECL Stress Testing under CECL / IFRS 9 Guidelines**

**Tech Stack:** Python 3.10+, Streamlit, DuckDB, XGBoost, LightGBM, Scikit-Learn

## The Business Problem

Traditional credit risk scorecards are fundamentally flawed in two ways:
1. **Through-the-Cycle (TTC) Blindness:** They evaluate borrower risk on static attributes, ignoring dynamic macroeconomic conditions like unemployment (UNRATE) and interest rates (FEDFUNDS).
2. **Naive Loss-Based Cutoffs:** Halting originations purely due to elevated default rates is financially suboptimal. If higher-risk borrowers pay sufficiently high interest rates (e.g., 14%-18%), the yield covers default losses and generates positive net returns.

**The Objective:** Quantify how macroeconomic downturns transmit into default losses across a $7.5B consumer loan portfolio, calculate Expected Credit Loss (ECL), and deploy risk-adjusted underwriting rules to maximize Net Profit while cutting loss-making segments.

## Core Impact & Accomplishments

* **Big Data Ingestion:** Built an out-of-core data pipeline in DuckDB to ingest 1,345,310 loan records and 234 months of Federal Reserve macroeconomic data, maintaining sub-3-second query times with 100% sample retention.
* **Predictive Default Risk Modeling:** Engineered Point-in-Time (PiT) behavioral credit features and trained a LightGBM champion model, improving Out-of-Time ROC-AUC from 0.6265 to 0.6919 and Gini from 0.2531 to 0.3839.
* **Forward-Looking Macro Stress Testing:** Executed a regulatory stress test across 518,706 active loans, quantifying a $32.8M severe loss expansion ($909.0M base vs. $941.8M severe ECL) using econometric shock simulations (+3.5% UNRATE, +1.5% FEDFUNDS).
* **Return Optimization:** Formulated a SQL-based risk-adjusted net profit model that eliminated $30.8M in net losses from high-risk tiers while preserving $55.7M in profitable originations.
* **Interactive Analytics Engine:** Deployed a Streamlit dashboard and BI export pipeline operating under a 180MB RAM footprint with sub-10ms render latency.

## Architecture & Pipeline

**Phase 1: Data Engineering**
Ingested 1.34M closed loans and FRED macro data via DuckDB streaming. Extracted behavioral features including revolving utilization, 2-year delinquencies, inquiries, and interest rates.
* **Artifacts:** `cleaned_loans_phase1.parquet`, `Phase1_Data_Engineering_Report.md`

**Phase 2: ML Benchmark**
Calibrated Point-in-Time default risk using a chronological Out-of-Time split (Train: 2007-2015, Test: 2016-2018).
* **Artifacts:** `02_phase2_model_engine.ipynb`, `models/all_models.joblib`

**Phase 3: Macro Stress Testing**
Simulated baseline, adverse, and severe loan-level default probabilities across $7.5B exposure by perturbing macro parameters.
* **Artifacts:** `03_phase3_stress_testing.ipynb`, `stressed_portfolio_phase3.parquet`

**Phase 4: Financial Math & Return Optimization**
Calculated Gross Revenue, Base ECL, and Net Profit using the following framework:
* ECL = PD * 0.50 * EAD
* Net Profit = Gross Revenue - ECL
* **Artifacts:** `phase4_ecl_calculation.sql`, `loan_level_ecl_results.parquet`

**Phase 5: Export & Delivery**
Built a 5-tab web application for real-time portfolio cross-filtering and automated CSV serialization for Power BI / Tableau.
* **Artifacts:** `app.py`, `power_bi_exports/`

## Model Benchmark (Out-of-Time Test Set)

Evaluated on a 518,706 Out-of-Time test cohort (2016-2018 vintages):

| Model Architecture | ROC-AUC | Gini | KS Statistic | PR-AUC | Log-Loss | Brier Score | Inference Time |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LightGBM (Champion)** | **0.6919** | **0.3839** | **27.90%** | **0.3756** | **0.4959** | **0.1623** | **2.78s** |
| XGBoost (Challenger) | 0.6917 | 0.3833 | 27.80% | 0.3750 | 0.4967 | 0.1624 | 6.60s |
| Random Forest | 0.6883 | 0.3766 | 27.59% | 0.3692 | 0.4986 | 0.1629 | 43.06s |
| Logistic Regression | 0.6809 | 0.3618 | 26.30% | 0.3601 | 0.5071 | 0.1668 | 2.36s |

## Financial Impact & Risk-Adjusted Net Profit Matrix

* **Total Portfolio Exposure (EAD):** $7,499,413,504
* **Expected Annual Gross Revenue:** $1,041,159,076 (13.88% Gross Yield)
* **Baseline Expected Credit Loss (ECL):** $909,049,024 (12.12% Loss Rate)
* **Baseline Net Profit:** $132,110,032 (1.76% Net Margin)
* **Severe Scenario Net Profit:** $99,326,110 (1.32% Net Margin, $32.8M severe loss expansion)

### Underwriting Optimization Matrix (Net Profit in Millions)

| FICO Tier | DTI: 0-10% | DTI: 10-20% | DTI: 20-30% | DTI: 30-40% | DTI: 40%+ | Decision Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **660-699** | +$23.6M | +$32.2M | -$11.9M | -$14.9M | -$3.2M | Halt DTI >= 20% |
| **700-749** | +$20.6M | +$38.3M | +$15.5M | -$0.4M | -$0.4M | Halt DTI >= 30% |
| **750-799** | +$9.0M | +$11.6M | +$5.0M | +$0.8M | +$0.1M | Approve All |
| **800+** | +$2.7M | +$2.3M | +$0.9M | +$0.2M | +$0.04M | Approve All |

**Risk Committee Output:** Halt originations exclusively for segments generating negative net returns to eliminate $30.8M in net losses, while preserving $55.7M in profitable originations from lower-DTI cohorts.

## Model Lineage, Data Governance & Auditability

| Attribute | Specification / Version Reference |
| :--- | :--- |
| **Data Universe** | LendingClub Closed Loans (2007-06 to 2018-12) via FRED Macro Series |
| **Total Cohort Count** | 1,345,310 loans (100% sample retention) |
| **Chronological Cutoff** | Train: 2007-06 to 2015-12 (826,604 loans) \| OOT Test: 2016-01 to 2018-12 (518,706 loans) |
| **Champion Model** | LightGBM Classifier (`models/champion_pd_model.joblib`) |
| **Challenger Suite** | XGBoost (Hist), Random Forest, Logistic Regression (`models/all_models.joblib`) |
| **Regulatory Framework** | CECL / IFRS 9 Point-in-Time Lifetime Loss Formulation |
| **Environment** | Python 3.10+, DuckDB 1.1+, Scikit-Learn 1.3+, LightGBM 4.1+, XGBoost 2.0+ |

## Evidence Hierarchy & Artifact Lineage

To ensure audit traceability across credit committee reviews and downstream modeling:
1. **Primary Ground-Truth Datasets:**
   - Preprocessed Loan Base: `data/cleaned_loans_phase1.parquet`
   - Stressed Scenario Cohort: `data/stressed_portfolio_phase3.parquet`
   - Loan-Level Financial ECL: `data/loan_level_ecl_results.parquet`
2. **Aggregated Decision Matrices & BI Feeds:**
   - Underwriting Cutoff Grid: `power_bi_exports/ecl_risk_matrix_fico_dti.csv`
   - Portfolio Overview & Macro Shifts: `power_bi_exports/portfolio_kpis_overview.csv`, `power_bi_exports/macro_stress_comparison.csv`
3. **Technical Governance Reports:**
   - Data Engineering: [Phase 1 Report](file:///J:/Finance%20Projects/Credit/reports/Phase1_Data_Engineering_Report.md)
   - ML Benchmark: [Phase 2 Report](file:///J:/Finance%20Projects/Credit/reports/Phase2_Model_Evaluation_Report.md)
   - Stress Testing: [Phase 3 Report](file:///J:/Finance%20Projects/Credit/reports/Phase3_Stress_Testing_Report.md)
   - Financial Math: [Phase 4 Report](file:///J:/Finance%20Projects/Credit/reports/Phase4_Financial_Math_Report.md)
   - BI Specification: [Phase 5 Guide](file:///J:/Finance%20Projects/Credit/reports/Phase5_Power_BI_Deliverable_Guide.md)
4. **Executive Synthesis:**
   - [Executive Business Summary & Glossary](file:///J:/Finance%20Projects/Credit/reports/Executive_Business_Summary_and_Glossary.md)

## Usage

**1. Environment Setup**
```bash
git clone https://github.com/JAMIEL-J/credit-risk-analysis.git
cd credit-risk-analysis
pip install -r requirements.txt
```

**2. Launch Dashboard**
```bash
streamlit run app.py
```

**3. BI Integration**
Pre-aggregated cuts are generated in `power_bi_exports/`. Connect Power BI/Tableau directly to `ecl_risk_matrix_fico_dti.csv` or `stressed_portfolio_phase3.csv`.

## MLOps Production Roadmap

Transitioning this engine to an enterprise-grade system involves:

1. **CI/CD Pipeline (GitHub Actions):** Unit testing for financial math ($\text{ECL} = \text{PD} \times \text{LGD} \times \text{EAD}$) and schema assertions via Great Expectations.
2. **Model Registry (MLflow/DVC):** Tracking serialized candidate models with full lineage metadata (dataset hashes, ROC-AUC, Brier scores) for regulatory auditability.
3. **Containerization (Docker):** Packaging the SQL engine and Scikit-Learn pipelines into isolated containers optimized for cloud deployment.
4. **Drift Monitoring (SR 11-7):** Automated Population Stability Index (PSI) trackers on incoming applicant batches, triggering alerts when $\text{PSI} \ge 0.25$.
5. **Continuous Training:** Event-driven retraining pipelines running Challenger models in Shadow Mode before gated promotion.
6. **Dynamic Data Ingestion:** Automated monthly webhooks directly to the `fredapi` to refresh `UNRATE` and `FEDFUNDS` scenarios.