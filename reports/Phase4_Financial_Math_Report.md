# Phase 4: Financial Math & Risk-Adjusted Net Return Report

---

## 1. Executive Summary & Core Financial Formulation
This phase computes regulatory **Expected Credit Loss (ECL)** alongside **Expected Gross Revenue** to determine the **Risk-Adjusted Net Return** across the portfolio:

$$\text{Expected Gross Revenue} = \text{loan\_amnt} \times \left(\frac{\text{int\_rate}}{100}\right)$$

$$\text{Expected Credit Loss (ECL)} = \text{PD} \times \text{LGD (0.50)} \times \text{loan\_amnt}$$

$$\mathbf{\text{Net Profit}} = \mathbf{\text{Expected Gross Revenue}} - \mathbf{\text{Expected Credit Loss (ECL)}}$$

$$\mathbf{\text{Net Profit Margin (\%)}} = \left(\frac{\text{Net Profit}}{\text{loan\_amnt}}\right) \times 100$$

---

## 2. Portfolio-Level Financial Totals (518,706 Loans)
* **Total Portfolio Exposure (EAD):** **`$7,499,413,504.00`**
* **Expected Annual Gross Revenue:** **`$1,041,159,076.60`** (Portfolio Gross Yield: `13.88%`)
* **Total Baseline Expected Credit Loss (ECL):** **`$909,049,024.00`** (`12.12%` Loss Rate)
* **Total Baseline Risk-Adjusted Net Profit:** **`$132,110,032.76`** (`1.76%` Net Margin)
* **Total Severe Scenario ECL:** **`$941,832,960.00`** (`12.56%` Loss Rate)
* **Total Severe Scenario Net Profit:** **`$99,326,110.96`** (`1.32%` Net Margin)

---

## 3. FICO $\times$ DTI Risk & Net Profit Concentration Matrix
Below is the aggregated performance matrix grouping borrowers by credit score and leverage:

| fico_band             | dti_band   |   total_loans |   total_exposure |   avg_int_rate_pct |   avg_pd_base_pct |   avg_pd_severe_pct |   total_expected_revenue |   total_ecl_base |   total_ecl_severe |    total_ecl_gap |   total_net_profit_base |   total_net_profit_severe |   net_margin_base_pct |   net_margin_severe_pct | risk_adjusted_verdict                   |
|:----------------------|:-----------|--------------:|-----------------:|-------------------:|------------------:|--------------------:|-------------------------:|-----------------:|-------------------:|-----------------:|------------------------:|--------------------------:|----------------------:|------------------------:|:----------------------------------------|
| 660 - 699 (Fair)      | 10% - 20%  |        125092 |      1.73799e+09 |           14.1879  |          24.5347  |            25.494   |              2.57476e+08 |      2.25312e+08 |        2.32803e+08 |      7.49005e+06 |             3.2164e+07  |               2.4674e+07  |              1.85064  |                1.41968  | Marginal Margin (<2% Net Return)        |
| 660 - 699 (Fair)      | 20% - 30%  |         94191 |      1.3324e+09  |           15.3681  |          32.0604  |            33.0699  |              2.14608e+08 |      2.26509e+08 |        2.32264e+08 |      5.75473e+06 |            -1.19012e+07 |              -1.76559e+07 |             -0.893212 |               -1.32512  | Negative Net Profit (Halt Origination)  |
| 700 - 749 (Good)      | 10% - 20%  |         65438 |      1.01845e+09 |           11.3016  |          15.1743  |            16.0437  |              1.19167e+08 |      8.08195e+07 |        8.48925e+07 |      4.073e+06   |             3.83472e+07 |               3.42742e+07 |              3.76526  |                3.36534  | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 20% - 30%  |         50995 |      7.97757e+08 |           12.5372  |          21.0159  |            21.9592  |              1.04243e+08 |      8.87276e+07 |        9.20719e+07 |      3.3443e+06  |             1.55151e+07 |               1.21708e+07 |              1.94484  |                1.52563  | Marginal Margin (<2% Net Return)        |
| 660 - 699 (Fair)      | 0% - 10%   |         52018 |      6.65581e+08 |           13.6409  |          20.229   |            21.2412  |              9.40162e+07 |      7.04384e+07 |        7.37417e+07 |      3.30333e+06 |             2.35779e+07 |               2.02745e+07 |              3.54245  |                3.04614  | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 0% - 10%   |         28979 |      4.2914e+08  |           11.1565  |          12.9374  |            13.8603  |              4.93589e+07 |      2.87534e+07 |        3.07258e+07 |      1.97248e+06 |             2.06055e+07 |               1.86331e+07 |              4.80159  |                4.34195  | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 30% - 40%  |         30149 |      4.17671e+08 |           17.1592  |          40.909   |            41.9429  |              7.46809e+07 |      8.96075e+07 |        9.14028e+07 |      1.79536e+06 |            -1.49266e+07 |              -1.67219e+07 |             -3.57376  |               -4.00361  | Negative Net Profit (Halt Origination)  |
| 700 - 749 (Good)      | 30% - 40%  |         16884 |      2.53459e+08 |           14.5894  |          29.0633  |            30.1287  |              3.84292e+07 |      3.87907e+07 |        3.99749e+07 |      1.18416e+06 |       -361556           |              -1.54572e+06 |             -0.142649 |               -0.609849 | Negative Net Profit (Halt Origination)  |
| 750 - 799 (Very Good) | 10% - 20%  |         16519 |      2.51612e+08 |            8.80984 |           8.57388 |             9.34942 |              2.30566e+07 |      1.14509e+07 |        1.24291e+07 | 978181           |             1.16056e+07 |               1.06275e+07 |              4.61252  |                4.22376  | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 0% - 10%   |         11135 |      1.69482e+08 |            9.0726  |           7.83219 |             8.62844 |              1.61546e+07 |      7.1612e+06  |        7.87688e+06 | 715678           |             8.99345e+06 |               8.27777e+06 |              5.30644  |                4.88416  | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 20% - 30%  |         10011 |      1.47762e+08 |            9.75765 |          12.5948  |            13.576   |              1.51879e+07 |      1.01403e+07 |        1.08601e+07 | 719799           |             5.04754e+06 |               4.32774e+06 |              3.41598  |                2.92885  | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 40%+       |          3952 |      6.5264e+07  |           18.2738  |          46.2315  |            47.5787  |              1.21583e+07 |      1.53836e+07 |        1.57929e+07 | 409252           |            -3.22529e+06 |              -3.63454e+06 |             -4.94192  |               -5.56899  | Negative Net Profit (Halt Origination)  |
| 800+ (Exceptional)    | 0% - 10%   |          2975 |      4.90331e+07 |            7.73072 |           4.72976 |             5.29656 |              4.0496e+06  |      1.31767e+06 |        1.47918e+06 | 161510           |             2.73194e+06 |               2.57043e+06 |              5.57162  |                5.24223  | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 10% - 20%  |          3008 |      4.61207e+07 |            7.68535 |           5.62179 |             6.25309 |              3.78598e+06 |      1.47835e+06 |        1.64308e+06 | 164728           |             2.30764e+06 |               2.14291e+06 |              5.00347  |                4.6463   | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 40%+       |          2291 |      4.26576e+07 |           15.1042  |          31.9555  |            33.4043  |              6.50924e+06 |      6.88563e+06 |        7.17403e+06 | 288403           |       -376387           |         -664790           |             -0.882345 |               -1.55843  | Negative Net Profit (Halt Origination)  |
| 750 - 799 (Very Good) | 30% - 40%  |          2801 |      4.01874e+07 |           11.6966  |          19.1877  |            20.4613  |              4.88899e+06 |      4.09926e+06 |        4.34147e+06 | 242210           |        789733           |          547523           |              1.96512  |                1.36242  | Marginal Margin (<2% Net Return)        |
| 800+ (Exceptional)    | 20% - 30%  |          1476 |      2.14326e+07 |            8.30847 |           8.30732 |             9.13165 |              1.94604e+06 |      1.05675e+06 |        1.15212e+06 |  95371.6         |        889291           |          793920           |              4.14926  |                3.70427  | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 40%+       |           405 |      7.67185e+06 |           11.0819  |          18.5608  |            20.0146  |         872807           | 740373           |   797232           |  56858.8         |        132434           |           75574.7         |              1.72623  |                0.985091 | Marginal Margin (<2% Net Return)        |
| 800+ (Exceptional)    | 30% - 40%  |           334 |      4.66678e+06 |            9.81012 |          12.8169  |            14.0288  |         479667           | 324153           |   352371           |  28217.7         |        155514           |          127296           |              3.33237  |                2.72772  | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 40%+       |            53 |      1.07295e+06 |            8.59528 |          10.052   |            11.1911  |          90395.2         |  52327.9         |    58629.3         |   6301.41        |         38067.3         |           31765.9         |              3.54791  |                2.96061  | Strong Positive Return (>2% Net Margin) |

---

## 4. Official Risk Committee Underwriting Verdict (Risk-Adjusted Rule)

> ### 🏛️ Risk Committee Underwriting Policy Rule:
> **"Instead of halting originations blindly based on raw default rate, underwriting policy evaluates Risk-Adjusted Net Return (Revenue - ECL). Halt originations exclusively for segments generating negative net returns (ECL > Revenue), while preserving high-yield segments whose interest rates adequately cover default risk."**

---
*Report generated automatically by Phase 4 Financial Math Engine via DuckDB.*
