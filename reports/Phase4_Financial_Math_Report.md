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
* **Total Baseline Expected Credit Loss (ECL):** **`$937,681,856.00`** (`12.50%` Loss Rate)
* **Total Baseline Risk-Adjusted Net Profit:** **`$103,477,220.91`** (`1.38%` Net Margin)
* **Total Severe Scenario ECL:** **`$694,073,728.00`** (`9.26%` Loss Rate)
* **Total Severe Scenario Net Profit:** **`$347,085,371.84`** (`4.63%` Net Margin)

---

## 3. FICO $\times$ DTI Risk & Net Profit Concentration Matrix
Below is the aggregated performance matrix grouping borrowers by credit score and leverage:

| fico_band             | dti_band   |   total_loans |   total_exposure |   avg_int_rate_pct |   avg_pd_base_pct |   avg_pd_severe_pct |   total_expected_revenue |   total_ecl_base |   total_ecl_severe |     total_ecl_gap |   total_net_profit_base |   total_net_profit_severe |   net_margin_base_pct |   net_margin_severe_pct | risk_adjusted_verdict                   |
|:----------------------|:-----------|--------------:|-----------------:|-------------------:|------------------:|--------------------:|-------------------------:|-----------------:|-------------------:|------------------:|------------------------:|--------------------------:|----------------------:|------------------------:|:----------------------------------------|
| 660 - 699 (Fair)      | 10% - 20%  |        125092 |      1.73799e+09 |           14.1879  |          25.1326  |            18.1002  |              2.57476e+08 |      2.32054e+08 |        1.63056e+08 |      -6.89988e+07 |             2.54221e+07 |               9.44209e+07 |              1.46273  |                 5.43275 | Marginal Margin (<2% Net Return)        |
| 660 - 699 (Fair)      | 20% - 30%  |         94191 |      1.3324e+09  |           15.3681  |          32.1325  |            22.9199  |              2.14608e+08 |      2.28345e+08 |        1.59372e+08 |      -6.89731e+07 |            -1.3737e+07  |               5.52361e+07 |             -1.031    |                 4.14561 | Negative Net Profit (Halt Origination)  |
| 700 - 749 (Good)      | 10% - 20%  |         65438 |      1.01845e+09 |           11.3016  |          16.3443  |            14.0187  |              1.19167e+08 |      8.73316e+07 |        7.26036e+07 |      -1.4728e+07  |             3.18351e+07 |               4.65631e+07 |              3.12585  |                 4.57197 | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 20% - 30%  |         50995 |      7.97757e+08 |           12.5372  |          22.043   |            18.5875  |              1.04243e+08 |      9.33995e+07 |        7.64972e+07 |      -1.69023e+07 |             1.08433e+07 |               2.77456e+07 |              1.35922  |                 3.47795 | Marginal Margin (<2% Net Return)        |
| 660 - 699 (Fair)      | 0% - 10%   |         52018 |      6.65581e+08 |           13.6409  |          21.1598  |            15.3511  |              9.40162e+07 |      7.4388e+07  |        5.24036e+07 |      -2.19844e+07 |             1.96283e+07 |               4.16126e+07 |              2.94904  |                 6.25207 | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 0% - 10%   |         28979 |      4.2914e+08  |           11.1565  |          14.5849  |            12.5787  |              4.93589e+07 |      3.28571e+07 |        2.72731e+07 |      -5.58408e+06 |             1.65018e+07 |               2.20858e+07 |              3.84531  |                 5.14653 | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 30% - 40%  |         30149 |      4.17671e+08 |           17.1592  |          39.9918  |            27.7825  |              7.46809e+07 |      8.85429e+07 |        6.02959e+07 |      -2.82471e+07 |            -1.3862e+07  |               1.43851e+07 |             -3.31888  |                 3.44411 | Negative Net Profit (Halt Origination)  |
| 700 - 749 (Good)      | 30% - 40%  |         16884 |      2.53459e+08 |           14.5894  |          29.9772  |            23.7431  |              3.84292e+07 |      4.03531e+07 |        3.12023e+07 |      -9.15081e+06 |            -1.92394e+06 |               7.22686e+06 |             -0.759075 |                 2.8513  | Negative Net Profit (Halt Origination)  |
| 750 - 799 (Very Good) | 10% - 20%  |         16519 |      2.51612e+08 |            8.80984 |           9.0401  |             8.56221 |              2.30566e+07 |      1.22901e+07 |        1.11011e+07 |      -1.18906e+06 |             1.07665e+07 |               1.19555e+07 |              4.279    |                 4.75158 | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 0% - 10%   |         11135 |      1.69482e+08 |            9.0726  |           8.71615 |             8.19334 |              1.61546e+07 |      8.19835e+06 |        7.29167e+06 | -906681           |             7.9563e+06  |               8.86298e+06 |              4.69448  |                 5.22945 | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 20% - 30%  |         10011 |      1.47762e+08 |            9.75765 |          13.401   |            12.6196  |              1.51879e+07 |      1.09039e+07 |        9.79117e+06 |      -1.11273e+06 |             4.28395e+06 |               5.39668e+06 |              2.89922  |                 3.65227 | Strong Positive Return (>2% Net Margin) |
| 660 - 699 (Fair)      | 40%+       |          3952 |      6.5264e+07  |           18.2738  |          39.628   |            28.7613  |              1.21583e+07 |      1.32232e+07 |        9.46085e+06 |      -3.76234e+06 |            -1.06485e+06 |               2.69749e+06 |             -1.6316   |                 4.1332  | Negative Net Profit (Halt Origination)  |
| 800+ (Exceptional)    | 0% - 10%   |          2975 |      4.90331e+07 |            7.73072 |           5.29406 |             4.96858 |              4.0496e+06  |      1.51632e+06 |        1.3151e+06  | -201225           |             2.53328e+06 |               2.73451e+06 |              5.16647  |                 5.57686 | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 10% - 20%  |          3008 |      4.61207e+07 |            7.68535 |           5.78799 |             5.49736 |              3.78598e+06 |      1.57115e+06 |        1.39559e+06 | -175560           |             2.21484e+06 |               2.3904e+06  |              4.80226  |                 5.18292 | Strong Positive Return (>2% Net Margin) |
| 700 - 749 (Good)      | 40%+       |          2291 |      4.26576e+07 |           15.1042  |          29.0082  |            24.6258  |              6.50924e+06 |      6.30433e+06 |        5.27983e+06 |      -1.0245e+06  |        204906           |               1.22941e+06 |              0.480351 |                 2.88204 | Marginal Margin (<2% Net Return)        |
| 750 - 799 (Very Good) | 30% - 40%  |          2801 |      4.01874e+07 |           11.6966  |          19.633   |            17.9502  |              4.88899e+06 |      4.23009e+06 |        3.72058e+06 | -509509           |        658898           |               1.16841e+06 |              1.63956  |                 2.90739 | Marginal Margin (<2% Net Return)        |
| 800+ (Exceptional)    | 20% - 30%  |          1476 |      2.14326e+07 |            8.30847 |           8.65338 |             8.32985 |              1.94604e+06 |      1.11436e+06 |   994833           | -119526           |        831680           |          951206           |              3.88045  |                 4.43814 | Strong Positive Return (>2% Net Margin) |
| 750 - 799 (Very Good) | 40%+       |           405 |      7.67185e+06 |           11.0819  |          17.0374  |            16.8247  |         872807           | 680238           |   661770           |  -18467.4         |        192569           |          211037           |              2.51007  |                 2.75079 | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 30% - 40%  |           334 |      4.66678e+06 |            9.81012 |          12.7761  |            12.4969  |         479667           | 328608           |   300752           |  -27856.1         |        151059           |          178915           |              3.2369   |                 3.8338  | Strong Positive Return (>2% Net Margin) |
| 800+ (Exceptional)    | 40%+       |            53 |      1.07295e+06 |            8.59528 |           9.75927 |            11.2538  |          90395.2         |  49804.3         |    57679.7         |    7875.4         |         40590.9         |           32715.5         |              3.78311  |                 3.04911 | Strong Positive Return (>2% Net Margin) |

---

## 4. Official Risk Committee Underwriting Verdict (Risk-Adjusted Rule)

> ### 🏛️ Risk Committee Underwriting Policy Rule:
> **"Instead of halting originations blindly based on raw default rate, underwriting policy evaluates Risk-Adjusted Net Return (Revenue - ECL). Halt originations exclusively for segments generating negative net returns (ECL > Revenue), while preserving high-yield segments whose interest rates adequately cover default risk."**

---
*Report generated automatically by Phase 4 Financial Math Engine via DuckDB.*
