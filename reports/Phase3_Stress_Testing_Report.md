# Phase 3: Macroeconomic Stress Testing Report

**Execution Status:** Completed Successfully  
**Pipeline Script:** `python_scripts/phase3_stress_testing.py`  
**Isolated Portfolio:** 518,706 loans (2016–2018 vintage cohort)  
**Total Portfolio Balance:** $7,499,413,504.00  
**Stressed Export Files:**  
- `data/stressed_portfolio_phase3.csv` (55.63 MB)  
- `data/stressed_portfolio_phase3.parquet` (12.19 MB)  

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
| **Baseline** | **23.18%** | 19.36% | 11.59% | 31.32% | 55.33% | — | — |
| **Adverse** | **23.53%** | 19.71% | 11.88% | 31.76% | 55.79% | +0.35% | +1.51% |
| **Severe** | **24.14%** | 20.30% | 12.18% | 32.69% | 56.96% | +0.96% | +4.14% |

---

## 3. Risk Sensitivity Takeaways
* **Adverse Macro Sensitivity:** A $+1.5\%$ rise in unemployment combined with a $+0.5\%$ interest rate increase increases the mean default probability from **23.18%** to **23.53%**.
* **Severe Macro Sensitivity:** Under deep recession conditions ($+3.5\%$ unemployment shock), mean default probability reaches **24.14%**.
* **Tail Risk Concentration:** The 95th percentile borrower PD rises to **56.96%** in the severe scenario.

---

## 4. Next Step: Phase 4 Financial Math (SQL Expected Credit Loss)
With individual loan PDs computed under all 3 scenarios, we proceed to Phase 4 to compute Expected Credit Loss (ECL):
$$\text{ECL}_{\text{Base}} = \text{PD}_{\text{base}} \times \text{LGD} \times \text{loan\_amnt}$$
$$\text{ECL}_{\text{Severe}} = \text{PD}_{\text{severe}} \times \text{LGD} \times \text{loan\_amnt}$$
$$\text{ECL Gap} = \text{ECL}_{\text{Severe}} - \text{ECL}_{\text{Base}}$$
*(Assuming $\text{LGD} = 0.50$ per project specification)*.
