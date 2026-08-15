# Phase 1: Data Engineering & Macro Integration Report

**Execution Status:** Completed Successfully  
**Pipeline Script:** `python_scripts/phase1_data_engineering.py`  
**Processed Output:** `data/cleaned_loans_phase1.parquet` (6.20 MB)  
**Preview Sample:** `data/cleaned_loans_phase1_sample.csv`

---

## 1. Executive Summary

Phase 1 establishes the consolidated, quality-assured analytical baseline by combining LendingClub closed loan records with historical Federal Reserve macroeconomic series (`UNRATE` and `FEDFUNDS`).

| Metric | Value |
| :--- | :--- |
| **Total Ingested Closed Loans** | 1,345,310 |
| **Final Retained Quality Records** | 1,344,401 |
| **Data Retention Rate** | 99.93% |
| **Total Features Retained** | 10 |
| **Historical Period Covered** | 2007-06 to 2018-12 |

---

## 2. Target Variable Formulation

Loans are categorized based on their terminal resolution:
* **Fully Paid (`target = 0`):** 1,076,056 (80.04%)
* **Charged Off / Default (`target = 1`):** 268,345 (19.96%)
* **Overall Default Rate:** 19.96%

---

## 3. Macroeconomic Integration

Macro indicators from the Federal Reserve Economic Data (FRED) were synchronized via `Year_Month` timestamp keys:
* **Unemployment Rate (`UNRATE`):** Range [3.7%, 10.0%], Mean: 5.58%
* **Federal Funds Rate (`FEDFUNDS`):** Range [0.07%, 5.26%], Mean: 0.35%

---

## 4. Key Feature Statistics

| Feature | Min | Median | Mean | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Loan Amount (`loan_amnt`)** | $500 | $12,000 | $14,416.92 | $40,000 |
| **FICO Score (`fico_range_low`)** | 625 | 690 | 696.18 | 845 |
| **Debt-to-Income (`dti`)** | 0.00% | 17.61% | 18.18% | 100.00% |
| **Unemployment Rate (`UNRATE`)** | 3.7% | 5.1% | 5.58% | 10.0% |
| **Federal Funds Rate (`FEDFUNDS`)** | 0.07% | 0.14% | 0.35% | 5.26% |

### Top Loan Purposes:
- **debt_consolidation**: 779,781 loans (58.00%)
- **credit_card**: 295,119 loans (21.95%)
- **home_improvement**: 87,423 loans (6.50%)
- **other**: 77,806 loans (5.79%)
- **major_purchase**: 29,411 loans (2.19%)
- **medical**: 15,543 loans (1.16%)
- **small_business**: 15,409 loans (1.15%)
- **car**: 14,581 loans (1.08%)

---

## 5. Next Steps (Phase 2: ML Engine)
1. **Categorical Encoding:** One-hot / frequency encode `purpose`.
2. **Train/Test Splitting & XGBoost Classifier:** Fit default model on features:
   $$\mathbf{X} = [\text{fico\_range\_low}, \text{dti}, \text{purpose}, \text{UNRATE}, \text{FEDFUNDS}]$$
3. **Probability Calibration & Baseline PD Extraction:** Output calibrated default probabilities for stress testing.
