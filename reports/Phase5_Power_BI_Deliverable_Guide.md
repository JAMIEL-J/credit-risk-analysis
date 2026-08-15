# Phase 5: Power BI Dashboard & Executive Deliverable Guide

**Project:** Credit Portfolio Macroeconomic Stress Testing & ECL Model  
**Aggregated Data Source:** `data/ecl_risk_matrix_fico_dti.csv`  
**Purpose Breakdown Source:** `data/ecl_summary_by_purpose.csv`  
**Granular Source:** `data/loan_level_ecl_results.parquet`  

---

## 1. Executive Dashboard Architecture

```
+---------------------------------------------------------------------------------------------------------+
|                                  CREDIT PORTFOLIO STRESS TESTING DASHBOARD                             |
+------------------------------------+------------------------------------+-------------------------------+
|        TOTAL PORTFOLIO EAD         |          TOTAL BASELINE ECL        |       TOTAL SEVERE ECL        |
|          $7.48 Billion             |           $785.23 Million          |        $650.70 Million        |
+------------------------------------+------------------------------------+-------------------------------+
|                                                                                                         |
|   [HEATMAP MATRIX: FICO SCORE BANDS (Rows) vs. DEBT-TO-INCOME BANDS (Columns)]                          |
|   Values: Total Base ECL ($) & Total Severe ECL ($) (Color Gradients: Green -> Amber -> Deep Red)       |
|                                                                                                         |
|   +-------------------+------------+-------------+-------------+-------------+-----------+              |
|   | FICO Band         | 0% - 10%   | 10% - 20%   | 20% - 30%   | 30% - 40%   | 40%+      |              |
|   +-------------------+------------+-------------+-------------+-------------+-----------+              |
|   | < 660 (Subprime)  | $4.5M      | $22.1M      | $28.4M      | $13.9M      | $0.1M     |              |
|   | 660 - 699 (Fair)  | $28.2M     | $137.4M     | $161.8M     | $74.5M      | $0.9M     |              |
|   | 700 - 749 (Good)  | $19.4M     | $89.2M      | $96.5M      | $41.8M      | $0.4M     |              |
|   | 750 - 799 (V.Good)| $6.8M      | $30.1M      | $29.8M      | $11.6M      | $0.1M     |              |
|   | 800+ (Exceptional)| $2.3M      | $8.7M       | $7.6M       | $2.8M       | $0.0M     |              |
|   +-------------------+------------+-------------+-------------+-------------+-----------+              |
|                                                                                                         |
+---------------------------------------------------------------------------------------------------------+
|                                    POLICY VERDICT & RISK ACTION                                         |
|  "Halt originations for unsecured loans where DTI >= 25% and FICO < 680 to eliminate $276.4M in         |
|   high-risk default exposure and protect portfolio capital adequacy."                                  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Power BI Step-by-Step Setup Instructions

### Step 1: Import the Data
1. In **Power BI Desktop**, click **Get Data** $\rightarrow$ **Text/CSV**.
2. Select `data/ecl_risk_matrix_fico_dti.csv` (or `data/loan_level_ecl_results.parquet`).
3. Verify data types:
   - `fico_band`: Text
   - `dti_band`: Text
   - `total_loans`: Whole Number
   - `total_exposure`: Decimal / Currency
   - `total_ecl_base`: Decimal / Currency
   - `total_ecl_severe`: Decimal / Currency

---

### Step 2: Create DAX Measures

Create a dedicated measures table or add the following DAX measures:

```dax
// 1. Total Portfolio Exposure (EAD)
Total_Exposure = SUM('ecl_risk_matrix_fico_dti'[total_exposure])

// 2. Total Baseline Expected Credit Loss (Base ECL)
Total_Base_ECL = SUM('ecl_risk_matrix_fico_dti'[total_ecl_base])

// 3. Total Severe Scenario Expected Credit Loss (Severe ECL)
Total_Severe_ECL = SUM('ecl_risk_matrix_fico_dti'[total_ecl_severe])

// 4. Baseline Loss Rate (%)
Baseline_Loss_Rate_Pct = DIVIDE([Total_Base_ECL], [Total_Exposure], 0) * 100

// 5. Severe Loss Rate (%)
Severe_Loss_Rate_Pct = DIVIDE([Total_Severe_ECL], [Total_Exposure], 0) * 100
```

---

### Step 3: Configure Report Visuals

#### A. Top KPI Cards
* **Card 1:** Field = `[Total_Exposure]`, Title = `"Total Portfolio Balance (EAD)"`, Display units = `Billions ($)`.
* **Card 2:** Field = `[Total_Base_ECL]`, Title = `"Baseline Expected Credit Loss (ECL)"`, Display units = `Millions ($)`.
* **Card 3:** Field = `[Total_Severe_ECL]`, Title = `"Severe Expected Credit Loss (ECL)"`, Display units = `Millions ($)`.

#### B. Heatmap Matrix Visual (FICO vs. DTI)
* **Visual Type:** `Matrix`
* **Rows:** `fico_band` (Sort order: `< 660`, `660 - 699`, `700 - 749`, `750 - 799`, `800+`)
* **Columns:** `dti_band` (Sort order: `0% - 10%`, `10% - 20%`, `20% - 30%`, `30% - 40%`, `40%+`)
* **Values:** `[Total_Base_ECL]` (or `[Total_Severe_ECL]`)
* **Conditional Formatting:**
  * Go to **Format visual** $\rightarrow$ **Cell elements** $\rightarrow$ Turn **Background color** ON.
  * Format style: **Gradient** (Lowest value = Light Green `#D4EDDA`, Mid value = Amber `#FFF3CD`, Highest value = Crimson Red `#F8D7DA`).

#### C. Executive Policy Verdict Box
Add a **Text Box** or **Card Visual** styled with a border and callout text:
> **"Halt originations for unsecured loans where DTI $\ge$ 25% and FICO $<$ 680 to eliminate $\$276.4\text{ Million}$ in high-risk default exposure and protect portfolio capital adequacy."**

---

## 3. Completed Project Deliverables Summary

| Phase | Milestone | Primary Output Files |
| :--- | :--- | :--- |
| **Phase 1** | Data Engineering & Macro Integration | • `data/cleaned_loans_phase1.parquet`<br>• `Phase1_Data_Engineering_Report.md` |
| **Phase 2** | ML Engine & 4-Model Benchmark | • `02_phase2_model_engine.ipynb`<br>• `models/champion_pd_model.joblib`<br>• `Phase2_Model_Evaluation_Report.md` |
| **Phase 3** | Macroeconomic Stress Testing | • `03_phase3_stress_testing.ipynb`<br>• `data/stressed_portfolio_phase3.parquet`<br>• `Phase3_Stress_Testing_Report.md` |
| **Phase 4** | Financial Math & SQL ECL Engine | • `sql_scripts/phase4_ecl_calculation.sql`<br>• `data/ecl_risk_matrix_fico_dti.csv`<br>• `Phase4_Financial_Math_Report.md` |
| **Phase 5** | Power BI Executive Deliverable | • `Phase5_Power_BI_Deliverable_Guide.md` |
