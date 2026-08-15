# Phase 4: Financial Math & SQL Expected Credit Loss (ECL) Report

**Execution Status:** Completed Successfully  
**SQL Engine:** DuckDB High-Performance SQL Engine  
**Portfolio Scope:** 517,807 Loans (2016–2018 Vintage Cohort)  
**Assumed LGD (Loss Given Default):** 50.0%  
**Export Files Generated:**  
- `data/ecl_risk_matrix_fico_dti.csv` (Power BI Heatmap Matrix)  
- `data/ecl_summary_by_purpose.csv` (Purpose Breakdown)  
- `data/loan_level_ecl_results.parquet` (Complete Loan-Level Audit Table)  

---

## 1. Top-Level Financial Loss Metrics

| Financial Metric | Formula / Description | Amount ($ USD) | % of Total Exposure |
| :--- | :--- | :--- | :--- |
| **Total Exposure at Default (EAD)** | $\sum \text{loan\_amnt}$ | **$7,482,334,208.00** | 100.00% |
| **Total Baseline ECL** | $\sum (\text{PD}_{\text{base}} \times 0.50 \times \text{EAD})$ | **$785,231,552.00** | 10.49% |
| **Total Adverse ECL** | $\sum (\text{PD}_{\text{adverse}} \times 0.50 \times \text{EAD})$ | **$716,703,808.00** | 9.58% |
| **Total Severe ECL** | $\sum (\text{PD}_{\text{severe}} \times 0.50 \times \text{EAD})$ | **$650,698,496.00** | 8.70% |

---

## 2. Risk Concentration Matrix (FICO Score Band $\times$ DTI Band)

| FICO Band | DTI Band | Total Loans | Total Exposure ($) | Avg Baseline PD | Avg Severe PD | Total Base ECL ($) | Total Severe ECL ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 660 - 699 (Fair) | 10% - 20% | 124,917 | $1,735,215,250 | 23.21% | 19.33% | $200,808,496.20 | $167,512,948.76 |
| 660 - 699 (Fair) | 20% - 30% | 94,191 | $1,332,400,275 | 28.97% | 22.10% | $192,915,790.44 | $146,782,261.88 |
| 700 - 749 (Good) | 20% - 30% | 50,995 | $797,756,825 | 18.88% | 16.94% | $74,988,056.59 | $66,998,728.74 |
| 660 - 699 (Fair) | 30% - 40% | 30,149 | $417,671,450 | 35.46% | 24.60% | $74,297,530.83 | $51,293,075.70 |
| 700 - 749 (Good) | 10% - 20% | 65,293 | $1,015,918,125 | 14.57% | 13.87% | $73,625,674.40 | $69,965,978.02 |
| 660 - 699 (Fair) | 0% - 10% | 52,016 | $665,549,125 | 18.19% | 16.71% | $60,750,131.59 | $55,696,403.38 |
| 700 - 749 (Good) | 30% - 40% | 16,884 | $253,458,800 | 24.97% | 19.91% | $31,720,276.80 | $25,197,020.07 |
| 700 - 749 (Good) | 0% - 10% | 28,979 | $429,140,425 | 12.57% | 11.95% | $27,059,217.02 | $25,566,196.42 |
| 660 - 699 (Fair) | 40%+ | 3,676 | $59,711,375 | 36.98% | 26.55% | $11,109,033.95 | $7,915,876.94 |
| 750 - 799 (Very Good) | 10% - 20% | 16,475 | $250,663,275 | 8.25% | 7.52% | $10,313,999.80 | $9,373,946.80 |
| 750 - 799 (Very Good) | 20% - 30% | 10,011 | $147,762,400 | 11.54% | 10.31% | $8,427,149.93 | $7,499,291.47 |
| 750 - 799 (Very Good) | 0% - 10% | 11,135 | $169,481,825 | 7.48% | 6.58% | $6,418,431.71 | $5,620,918.63 |
| 700 - 749 (Good) | 40%+ | 2,090 | $38,654,025 | 27.60% | 23.67% | $5,386,223.60 | $4,645,312.54 |
| 750 - 799 (Very Good) | 30% - 40% | 2,801 | $40,187,425 | 15.52% | 13.42% | $3,101,399.00 | $2,668,146.40 |
| 800+ (Exceptional) | 0% - 10% | 2,975 | $49,033,100 | 5.53% | 5.05% | $1,401,151.24 | $1,275,976.26 |
| 800+ (Exceptional) | 10% - 20% | 3,000 | $45,942,275 | 5.47% | 4.97% | $1,266,083.64 | $1,150,508.92 |
| 800+ (Exceptional) | 20% - 30% | 1,476 | $21,432,550 | 7.25% | 6.65% | $758,041.23 | $693,808.00 |
| 750 - 799 (Very Good) | 40%+ | 363 | $6,788,075 | 17.86% | 17.00% | $606,263.66 | $577,699.96 |
| 800+ (Exceptional) | 30% - 40% | 334 | $4,666,775 | 10.08% | 9.56% | $226,848.58 | $213,027.85 |
| 800+ (Exceptional) | 40%+ | 47 | $900,450 | 12.66% | 12.72% | $51,780.61 | $51,380.95 |

---

## 3. Executive Underwriting Policy Recommendation (Phase 5 Verdict)

> [!IMPORTANT]
> **Policy Verdict for Risk Committee:**  
> **"Halt originations for unsecured loans where DTI $\ge$ 25% and FICO $<$ 680 to eliminate $\approx$ $68,484,168.08 in severe scenario default losses (saving $97,503,482.69 in baseline expected credit losses) across $545,325,325.00 of high-risk exposure."**

---

## 4. Next Step: Phase 5 (Power BI Deliverables)
All aggregated datasets are exported and structured for Power BI import:
1. **Card Visuals:** Total Base ECL vs. Total Severe ECL.
2. **Matrix Heatmap Visual:** FICO Band on Rows, DTI Band on Columns, Color-coded by ECL.
3. **Executive Summary Card:** Embedded Underwriting Policy Verdict.
