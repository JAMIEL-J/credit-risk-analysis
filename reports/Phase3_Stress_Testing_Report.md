# Phase 3: Macroeconomic Stress Testing Report

**Execution Status:** Completed Successfully  
**Pipeline Script:** `python_scripts/phase3_stress_testing.py`  
**Isolated Portfolio:** 518,706 loans (2016–2018 vintage cohort)  
**Total Portfolio Balance:** $7,499,413,504.00  
**Stressed Export Files:**  
- `data/stressed_portfolio_phase3.csv` (55.64 MB)  
- `data/stressed_portfolio_phase3.parquet` (12.14 MB)  

---

## 1. Scenario Definitions & Macro Shocks

Under standard supervisory stress testing guidelines (e.g. Federal Reserve CCAR / DFAST), macroeconomic shocks simulate portfolio resilience under varying economic environments:

| Scenario | Unemployment Rate Shock ($\Delta \text{UNRATE}$) | Fed Funds Rate Shock ($\Delta \text{FEDFUNDS}$) | Macroeconomic Narrative |
| :--- | :---: | :---: | :--- |
| **Baseline** | $+0.0\%$ | $+0.0\%$ | Prevailing baseline economic conditions |
| **Adverse** | $+1.5\%$ | $+0.5\%$ | Moderate recessionary cycle & interest rate hike |
| **Severe** | $+3.5\%$ | $+1.5\%$ | Severe stagflationary recession & credit crunch |

---

## 2. Multi-Scenario Default Probability (PD) Results

| Scenario | Mean PD | Median PD | 25th Percentile | 75th Percentile | 95th Percentile | Absolute Delta | Relative Shift |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline** | **22.50%** | 18.86% | 10.62% | 30.40% | 54.91% | — | — |
| **Adverse** | **23.69%** | 20.02% | 11.57% | 31.87% | 56.59% | +1.19% | +5.30% |
| **Severe** | **25.21%** | 21.36% | 12.30% | 34.15% | 59.64% | +2.71% | +12.03% |

---

## 3. Risk Sensitivity Takeaways
* **Adverse Macro Sensitivity:** A $+1.5\%$ rise in unemployment combined with a $+0.5\%$ interest rate increase increases the mean default probability from **22.50%** to **23.69%**.
* **Severe Macro Sensitivity:** Under deep recession conditions ($+3.5\%$ unemployment shock), mean default probability reaches **25.21%**.
* **Tail Risk Concentration:** The 95th percentile borrower PD rises to **59.64%** in the severe scenario.

---

## 4. Next Step: Phase 4 Financial Math (SQL Expected Credit Loss)
With individual loan PDs computed under all 3 scenarios, we proceed to Phase 4 to compute Expected Credit Loss (ECL):
$$\text{ECL}_{\text{Base}} = \text{PD}_{\text{base}} \times \text{LGD} \times \text{loan\_amnt}$$
$$\text{ECL}_{\text{Severe}} = \text{PD}_{\text{severe}} \times \text{LGD} \times \text{loan\_amnt}$$
$$\text{ECL Gap} = \text{ECL}_{\text{Severe}} - \text{ECL}_{\text{Base}}$$
*(Assuming $\text{LGD} = 0.50$ per project specification)*.
