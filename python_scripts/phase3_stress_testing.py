"""
Phase 3: Macroeconomic Stress Testing Pipeline
-----------------------------------------------
1. Isolate Portfolio: Load recent test loans (2016–2018 cohort).
2. Base Scenario: Predict baseline default probability (PD_base).
3. Adverse Scenario: Apply macro shock (+1.5% UNRATE, +0.5% FEDFUNDS) -> PD_adverse.
4. Severe Scenario: Apply extreme macro shock (+3.5% UNRATE, +1.5% FEDFUNDS) -> PD_severe.
5. Export: Save stressed portfolio to CSV and Parquet for Phase 4 SQL ECL calculations.
6. Documentation: Generate Phase3_Stress_Testing_Report.md.
"""

import os
import time
import joblib
import numpy as np
import pandas as pd

def run_phase3_pipeline(
    portfolio_parquet_path: str = "data/test_portfolio_with_pd.parquet",
    model_path: str = "models/champion_pd_model.joblib",
    output_parquet_path: str = "data/stressed_portfolio_phase3.parquet",
    output_csv_path: str = "data/stressed_portfolio_phase3.csv",
    output_md_report_path: str = "Phase3_Stress_Testing_Report.md"
):
    print("=" * 70)
    print("PHASE 3: MACROECONOMIC STRESS TESTING PIPELINE")
    print("=" * 70)

    # 1. Load Portfolio & Model
    print(f"\n[Step 1] Loading test portfolio from {portfolio_parquet_path}...")
    df_portfolio = pd.read_parquet(portfolio_parquet_path)
    total_loans = len(df_portfolio)
    total_principal = df_portfolio['loan_amnt'].sum()
    print(f"Isolated Test Portfolio: {total_loans:,} loans | Total Principal: ${total_principal:,.2f}")

    print(f"Loading champion model pipeline from {model_path}...")
    pipeline = joblib.load(model_path)

    # 2. Base Scenario PD
    print("\n[Step 2] Calculating Baseline PD (PD_base)...")
    features = ['fico_range_low', 'dti', 'purpose', 'UNRATE', 'FEDFUNDS']
    X_base = df_portfolio[features].copy()
    
    t0 = time.time()
    df_portfolio['PD_base'] = pipeline.predict_proba(X_base)[:, 1].astype(np.float32)
    print(f"  -> Baseline PD calculated in {time.time() - t0:.2f}s | Mean PD_base: {df_portfolio['PD_base'].mean()*100:.2f}%")

    # 3. Adverse Scenario (+1.5% UNRATE, +0.5% FEDFUNDS)
    print("\n[Step 3] Applying Adverse Scenario (+1.5% UNRATE, +0.5% FEDFUNDS)...")
    X_adverse = df_portfolio[features].copy()
    X_adverse['UNRATE'] = X_adverse['UNRATE'] + 1.5
    X_adverse['FEDFUNDS'] = X_adverse['FEDFUNDS'] + 0.5

    t0 = time.time()
    df_portfolio['PD_adverse'] = pipeline.predict_proba(X_adverse)[:, 1].astype(np.float32)
    print(f"  -> Adverse PD calculated in {time.time() - t0:.2f}s | Mean PD_adverse: {df_portfolio['PD_adverse'].mean()*100:.2f}%")

    # 4. Severe Scenario (+3.5% UNRATE, +1.5% FEDFUNDS)
    print("\n[Step 4] Applying Severe Scenario (+3.5% UNRATE, +1.5% FEDFUNDS)...")
    X_severe = df_portfolio[features].copy()
    X_severe['UNRATE'] = X_severe['UNRATE'] + 3.5
    X_severe['FEDFUNDS'] = X_severe['FEDFUNDS'] + 1.5

    t0 = time.time()
    df_portfolio['PD_severe'] = pipeline.predict_proba(X_severe)[:, 1].astype(np.float32)
    print(f"  -> Severe PD calculated in {time.time() - t0:.2f}s | Mean PD_severe: {df_portfolio['PD_severe'].mean()*100:.2f}%")

    # 5. Export Datasets for Phase 4
    print("\n[Step 5] Exporting Stressed Datasets for SQL Financial Math...")
    sql_cols = [
        'Year_Month', 
        'loan_amnt', 
        'fico_range_low', 
        'dti', 
        'purpose', 
        'UNRATE', 
        'FEDFUNDS', 
        'PD_base', 
        'PD_adverse', 
        'PD_severe'
    ]
    df_export = df_portfolio[sql_cols].copy()
    
    df_export.to_parquet(output_parquet_path, index=False)
    df_export.to_csv(output_csv_path, index=False)
    
    parquet_size = os.path.getsize(output_parquet_path) / (1024 * 1024)
    csv_size = os.path.getsize(output_csv_path) / (1024 * 1024)
    print(f"  -> Saved Stressed Parquet: {output_parquet_path} ({parquet_size:.2f} MB)")
    print(f"  -> Saved Stressed CSV: {output_csv_path} ({csv_size:.2f} MB)")

    # 6. Generate Markdown Stress Testing Report
    mean_base = df_portfolio['PD_base'].mean() * 100
    mean_adv = df_portfolio['PD_adverse'].mean() * 100
    mean_sev = df_portfolio['PD_severe'].mean() * 100

    delta_adv = mean_adv - mean_base
    delta_sev = mean_sev - mean_base

    md_content = f"""# Phase 3: Macroeconomic Stress Testing Report

**Execution Status:** Completed Successfully  
**Pipeline Script:** `python_scripts/phase3_stress_testing.py`  
**Isolated Portfolio:** {total_loans:,} loans (2016–2018 vintage cohort)  
**Total Portfolio Balance:** ${total_principal:,.2f}  
**Stressed Export Files:**  
- `{output_csv_path}` ({csv_size:.2f} MB)  
- `{output_parquet_path}` ({parquet_size:.2f} MB)  

---

## 1. Scenario Definitions & Macro Shocks

Under standard supervisory stress testing guidelines (e.g. Federal Reserve CCAR / DFAST), macroeconomic shocks simulate portfolio resilience under varying economic environments:

| Scenario | Unemployment Rate Shock ($\\Delta \\text{{UNRATE}}$) | Fed Funds Rate Shock ($\\Delta \\text{{FEDFUNDS}}$) | Macroeconomic Narrative |
| :--- | :---: | :---: | :--- |
| **Baseline** | $+0.0\\%$ | $+0.0\\%$ | Prevailing baseline economic conditions |
| **Adverse** | $+1.5\\%$ | $+0.5\\%$ | Moderate recessionary cycle & interest rate hike |
| **Severe** | $+3.5\\%$ | $+1.5\\%$ | Severe stagflationary recession & credit crunch |

---

## 2. Multi-Scenario Default Probability (PD) Results

| Scenario | Mean PD | Median PD | 25th Percentile | 75th Percentile | 95th Percentile | Absolute Delta | Relative Shift |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline** | **{mean_base:.2f}%** | {df_portfolio['PD_base'].median()*100:.2f}% | {df_portfolio['PD_base'].quantile(0.25)*100:.2f}% | {df_portfolio['PD_base'].quantile(0.75)*100:.2f}% | {df_portfolio['PD_base'].quantile(0.95)*100:.2f}% | — | — |
| **Adverse** | **{mean_adv:.2f}%** | {df_portfolio['PD_adverse'].median()*100:.2f}% | {df_portfolio['PD_adverse'].quantile(0.25)*100:.2f}% | {df_portfolio['PD_adverse'].quantile(0.75)*100:.2f}% | {df_portfolio['PD_adverse'].quantile(0.95)*100:.2f}% | +{delta_adv:.2f}% | +{(delta_adv/mean_base)*100:.2f}% |
| **Severe** | **{mean_sev:.2f}%** | {df_portfolio['PD_severe'].median()*100:.2f}% | {df_portfolio['PD_severe'].quantile(0.25)*100:.2f}% | {df_portfolio['PD_severe'].quantile(0.75)*100:.2f}% | {df_portfolio['PD_severe'].quantile(0.95)*100:.2f}% | +{delta_sev:.2f}% | +{(delta_sev/mean_base)*100:.2f}% |

---

## 3. Risk Sensitivity Takeaways
* **Adverse Macro Sensitivity:** A $+1.5\\%$ rise in unemployment combined with a $+0.5\\%$ interest rate increase increases the mean default probability from **{mean_base:.2f}%** to **{mean_adv:.2f}%**.
* **Severe Macro Sensitivity:** Under deep recession conditions ($+3.5\\%$ unemployment shock), mean default probability reaches **{mean_sev:.2f}%**.
* **Tail Risk Concentration:** The 95th percentile borrower PD rises to **{df_portfolio['PD_severe'].quantile(0.95)*100:.2f}%** in the severe scenario.

---

## 4. Next Step: Phase 4 Financial Math (SQL Expected Credit Loss)
With individual loan PDs computed under all 3 scenarios, we proceed to Phase 4 to compute Expected Credit Loss (ECL):
$$\\text{{ECL}}_{{\\text{{Base}}}} = \\text{{PD}}_{{\\text{{base}}}} \\times \\text{{LGD}} \\times \\text{{loan\\_amnt}}$$
$$\\text{{ECL}}_{{\\text{{Severe}}}} = \\text{{PD}}_{{\\text{{severe}}}} \\times \\text{{LGD}} \\times \\text{{loan\\_amnt}}$$
$$\\text{{ECL Gap}} = \\text{{ECL}}_{{\\text{{Severe}}}} - \\text{{ECL}}_{{\\text{{Base}}}}$$
*(Assuming $\\text{{LGD}} = 0.50$ per project specification)*.
"""

    with open(output_md_report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  -> Saved Stress Testing Report: {output_md_report_path}")

    print("\n" + "=" * 70)
    print("PHASE 3 COMPLETE: Ready for Phase 4 Financial Math & SQL Analysis!")
    print("=" * 70)

    return df_portfolio

if __name__ == "__main__":
    run_phase3_pipeline()
