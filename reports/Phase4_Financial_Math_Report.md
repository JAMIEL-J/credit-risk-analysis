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
* **Total Baseline Expected Credit Loss (ECL):** **`$883,979,072.00`** (`11.79%` Loss Rate)
* **Total Baseline Risk-Adjusted Net Profit:** **`$157,179,984.55`** (`2.10%` Net Margin)
* **Total Severe Scenario ECL:** **`$980,823,680.00`** (`13.08%` Loss Rate)
* **Total Severe Scenario Net Profit:** **`$60,335,412.59`** (`0.80%` Net Margin)

---

## 3. FICO $\times$ DTI Risk & Net Profit Concentration Matrix
Below is the aggregated performance matrix grouping borrowers by credit score and leverage:

| fico_band             | dti_band   |   total_loans |   total_exposure |   avg_int_rate_pct |   avg_pd_base_pct |   avg_pd_severe_pct |   total_expected_revenue |   total_ecl_base |   total_ecl_severe |    total_ecl_gap |   total_net_profit_base |   total_net_profit_severe |   net_margin_base_pct |   net_margin_severe_pct | risk_adjusted_verdict                   |
|:----------------------|:-----------|--------------:|-----------------:|-------------------:|------------------:|--------------------:|-------------------------:|-----------------:|-------------------:|-----------------:|------------------------:|--------------------------:|----------------------:|------------------------:|:----------------------------------------|
| 660 - 699 (Fair)      | 10% - 20%  |        125092 |      1.73799e+09 |           14.1879  |          24.0273  |            26.7059  |              2.57476e+08 |      2.21266e+08 |        2.43346e+08 |      2.20799e+07 |             3.62107e+07 |               1.41308e+07 |             2.08348   |                0.813052 | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 20% - 30%  |         94191 |      1.3324e+09  |           15.3681  |          31.6249  |            34.6821  |              2.14608e+08 |      2.23787e+08 |        2.42909e+08 |      1.91219e+07 |            -9.17954e+06 |              -2.83015e+07 |            -0.688947  |               -2.1241   | Negative Net Profit (Halt Origination)  |
| 700 - 749 (Good)      | 10% - 20%  |         65438 |      1.01845e+09 |           11.3016  |          14.4016  |            16.7169  |              1.19167e+08 |      7.70043e+07 |        8.82278e+07 |      1.12235e+07 |             4.21624e+07 |               3.09389e+07 |             4.13987   |                3.03785  | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 20% - 30%  |         50995 |      7.97757e+08 |           12.5372  |          20.0057  |            22.7879  |              1.04243e+08 |      8.47925e+07 |        9.53679e+07 |      1.05753e+07 |             1.94502e+07 |               8.8749e+06  |             2.43812   |                1.11248  | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 0% - 10%   |         52018 |      6.65581e+08 |           13.6409  |          19.4448  |            22.2152  |              9.40162e+07 |      6.79292e+07 |        7.69062e+07 |      8.97705e+06 |             2.60871e+07 |               1.711e+07   |             3.91944   |                2.57069  | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 0% - 10%   |         28979 |      4.2914e+08  |           11.1565  |          12.2079  |            14.5447  |              4.93589e+07 |      2.72989e+07 |        3.21648e+07 |      4.86592e+06 |             2.206e+07   |               1.71941e+07 |             5.14051   |                4.00663  | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 30% - 40%  |         30149 |      4.17671e+08 |           17.1592  |          40.6798  |            43.8348  |              7.46809e+07 |      8.90945e+07 |        9.52527e+07 |      6.15814e+06 |            -1.44136e+07 |              -2.05718e+07 |            -3.45095   |               -4.92535  | Negative Net Profit (Halt Origination)  |
| 700 - 749 (Good)      | 30% - 40%  |         16884 |      2.53459e+08 |           14.5894  |          27.3945  |            30.6191  |              3.84292e+07 |      3.66575e+07 |        4.0577e+07  |      3.91958e+06 |             1.7717e+06  |              -2.14789e+06 |             0.699008  |               -0.84743  | Marginal Margin (<2% Net Return)        |
| 750 - 799 (Very Good) | 10% - 20%  |         16519 |      2.51612e+08 |            8.80984 |           7.56483 |             9.50461 |              2.30566e+07 |      1.01838e+07 |        1.25894e+07 |      2.40556e+06 |             1.28728e+07 |               1.04672e+07 |             5.11614   |                4.16008  | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 0% - 10%   |         11135 |      1.69482e+08 |            9.0726  |           6.96856 |             8.83627 |              1.61546e+07 |      6.43863e+06 |        8.0441e+06  |      1.60546e+06 |             9.71601e+06 |               8.11055e+06 |             5.73277   |                4.7855   | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 20% - 30%  |         10011 |      1.47762e+08 |            9.75765 |          11.5188  |            14.1635  |              1.51879e+07 |      9.33926e+06 |        1.12986e+07 |      1.95934e+06 |             5.84859e+06 |               3.88925e+06 |             3.95811   |                2.6321   | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 40%+       |          3952 |      6.5264e+07  |           18.2738  |          46.4607  |            50.2309  |              1.21583e+07 |      1.54487e+07 |        1.66985e+07 |      1.24983e+06 |            -3.29035e+06 |              -4.54019e+06 |            -5.04161   |               -6.95665  | Negative Net Profit (Halt Origination)  |
| 800+ (Exceptional)    | 0% - 10%   |          2975 |      4.90331e+07 |            7.73072 |           4.11627 |             5.34016 |              4.0496e+06  |      1.16303e+06 |        1.48366e+06 | 320634           |             2.88658e+06 |               2.56594e+06 |             5.88699   |                5.23308  | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 10% - 20%  |          3008 |      4.61207e+07 |            7.68535 |           4.87082 |             6.34678 |              3.78598e+06 |      1.29956e+06 |        1.66291e+06 | 363349           |             2.48643e+06 |               2.12308e+06 |             5.39112   |                4.6033   | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 40%+       |          2291 |      4.26576e+07 |           15.1042  |          30.3644  |            34.3361  |              6.50924e+06 |      6.54015e+06 |        7.40084e+06 | 860692           |        -30912.1         |         -891604           |            -0.0724655 |               -2.09014  | Negative Net Profit (Halt Origination)  |
| 750 - 799 (Very Good) | 30% - 40%  |          2801 |      4.01874e+07 |           11.6966  |          17.4835  |            20.8728  |              4.88899e+06 |      3.74781e+06 |        4.42499e+06 | 677179           |             1.14119e+06 |          464007           |             2.83966   |                1.15461  | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 20% - 30%  |          1476 |      2.14326e+07 |            8.30847 |           7.48609 |             9.60635 |              1.94604e+06 | 963414           |        1.2079e+06  | 244488           |        982625           |          738138           |             4.58473   |                3.444    | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 40%+       |           405 |      7.67185e+06 |           11.0819  |          17.0413  |            20.868   |         872807           | 681426           |   834366           | 152939           |        191381           |           38441.2         |             2.49458   |                0.501068 | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 30% - 40%  |           334 |      4.66678e+06 |            9.81012 |          11.5833  |            14.5074  |         479667           | 296291           |   363851           |  67560.3         |        183376           |          115816           |             3.9294    |                2.48171  | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 40%+       |            53 |      1.07295e+06 |            8.59528 |           9.02869 |            12.1479  |          90395.2         |  47081.1         |    63167.8         |  16086.7         |         43314.1         |           27227.4         |             4.03692   |                2.53762  | Strong Positive Return (>2% Net Margin) |

---

## 4. Official Risk Committee Underwriting Verdict (Risk-Adjusted Rule)

> ### 🏛️ Risk Committee Underwriting Policy Rule:
> **"Instead of halting originations blindly based on raw default rate, underwriting policy evaluates Risk-Adjusted Net Return (Revenue - ECL). Halt originations exclusively for segments generating negative net returns (ECL > Revenue), while preserving high-yield segments whose interest rates adequately cover default risk."**

---
*Report generated automatically by Phase 4 Financial Math Engine via DuckDB.*
