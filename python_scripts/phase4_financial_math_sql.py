"""
Phase 4: Financial Math & SQL Expected Credit Loss (ECL) Pipeline
-----------------------------------------------------------------
1. Executes SQL engine to calculate loan-level ECL under Base, Adverse, and Severe scenarios.
   Formula: ECL = PD * LGD (0.50) * Exposure (loan_amnt)
2. Calculates ECL Gap = ECL_Severe - ECL_Base.
3. Groups portfolio by FICO Bands x DTI Bands to isolate risk concentrations.
4. Derives the precise Power BI underwriting cutoffs.
5. Exports aggregated tables for Power BI and generates Phase4_Financial_Math_Report.md.
"""

import os
import duckdb
import pandas as pd

def run_phase4_pipeline(
    input_parquet_path: str = "data/stressed_portfolio_phase3.parquet",
    sql_script_path: str = "sql_scripts/phase4_ecl_calculation.sql",
    output_loan_level_parquet: str = "data/loan_level_ecl_results.parquet",
    output_matrix_csv: str = "data/ecl_risk_matrix_fico_dti.csv",
    output_purpose_csv: str = "data/ecl_summary_by_purpose.csv",
    output_md_report_path: str = "Phase4_Financial_Math_Report.md"
):
    print("=" * 70)
    print("PHASE 4: FINANCIAL MATH & SQL EXPECTED CREDIT LOSS (ECL) ENGINE")
    print("=" * 70)

    con = duckdb.connect()

    # Read and execute SQL script
    print(f"\n[Step 1] Executing SQL calculations from {sql_script_path}...")
    with open(sql_script_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    con.execute(sql_content)

    # 1. Export Loan-Level ECL
    print("\n[Step 2] Fetching loan-level results and exporting Parquet...")
    df_loan_level = con.execute("SELECT * FROM loan_level_ecl").df()
    df_loan_level.to_parquet(output_loan_level_parquet, index=False)
    print(f"  -> Saved {len(df_loan_level):,} loan-level ECL records to {output_loan_level_parquet}")

    # 2. Export FICO x DTI Risk Matrix (For Power BI)
    print("\n[Step 3] Fetching FICO x DTI Risk Matrix for Power BI...")
    df_matrix = con.execute("SELECT * FROM ecl_risk_matrix_fico_dti ORDER BY total_ecl_base DESC").df()
    df_matrix.to_csv(output_matrix_csv, index=False)
    print(f"  -> Saved FICO x DTI Risk Matrix to {output_matrix_csv}")

    # 3. Purpose Breakdown
    print("\n[Step 4] Computing Purpose Breakdown...")
    df_purpose = con.execute("""
    SELECT 
        purpose,
        COUNT(*) AS total_loans,
        SUM(ead) AS total_exposure,
        AVG(PD_base) * 100 AS avg_pd_base_pct,
        AVG(PD_severe) * 100 AS avg_pd_severe_pct,
        SUM(ecl_base) AS total_ecl_base,
        SUM(ecl_severe) AS total_ecl_severe,
        SUM(ecl_gap) AS total_ecl_gap
    FROM loan_level_ecl
    GROUP BY purpose
    ORDER BY total_ecl_base DESC
    """).df()
    df_purpose.to_csv(output_purpose_csv, index=False)
    print(f"  -> Saved Purpose Breakdown to {output_purpose_csv}")

    # Portfolio Top-Level KPIs
    tot_exposure = df_loan_level['ead'].sum()
    tot_ecl_base = df_loan_level['ecl_base'].sum()
    tot_ecl_adv = df_loan_level['ecl_adverse'].sum()
    tot_ecl_sev = df_loan_level['ecl_severe'].sum()
    tot_ecl_gap = df_loan_level['ecl_gap'].sum()
    
    ecl_base_rate = (tot_ecl_base / tot_exposure) * 100
    ecl_sev_rate = (tot_ecl_sev / tot_exposure) * 100

    print("\n" + "=" * 70)
    print("PORTFOLIO LEVEL EXPECTED CREDIT LOSS (ECL) SUMMARY:")
    print("=" * 70)
    print(f"Total Portfolio Exposure (EAD): ${tot_exposure:,.2f}")
    print(f"Total Base ECL:                 ${tot_ecl_base:,.2f} ({ecl_base_rate:.2f}% loss rate)")
    print(f"Total Adverse ECL:              ${tot_ecl_adv:,.2f}")
    print(f"Total Severe ECL:               ${tot_ecl_sev:,.2f} ({ecl_sev_rate:.2f}% loss rate)")
    print(f"Total Severe ECL Gap:           ${tot_ecl_gap:,.2f}")

    # Identify Highest Risk Segment for the Underwriting Verdict
    high_risk_segment = con.execute("""
    SELECT 
        fico_band, 
        dti_band, 
        COUNT(*) as loans, 
        SUM(ead) as exposure, 
        SUM(ecl_base) as ecl_base, 
        SUM(ecl_severe) as ecl_severe
    FROM loan_level_ecl
    WHERE (fico_range_low < 680 AND dti >= 25.0)
    GROUP BY fico_band, dti_band
    """).df()
    
    elim_exposure = high_risk_segment['exposure'].sum()
    elim_ecl_base = high_risk_segment['ecl_base'].sum()
    elim_ecl_sev = high_risk_segment['ecl_severe'].sum()

    # Generate Markdown Report
    md_content = f"""# Phase 4: Financial Math & SQL Expected Credit Loss (ECL) Report

**Execution Status:** Completed Successfully  
**SQL Engine:** DuckDB High-Performance SQL Engine  
**Portfolio Scope:** {len(df_loan_level):,} Loans (2016–2018 Vintage Cohort)  
**Assumed LGD (Loss Given Default):** 50.0%  
**Export Files Generated:**  
- `data/ecl_risk_matrix_fico_dti.csv` (Power BI Heatmap Matrix)  
- `data/ecl_summary_by_purpose.csv` (Purpose Breakdown)  
- `data/loan_level_ecl_results.parquet` (Complete Loan-Level Audit Table)  

---

## 1. Top-Level Financial Loss Metrics

| Financial Metric | Formula / Description | Amount ($ USD) | % of Total Exposure |
| :--- | :--- | :--- | :--- |
| **Total Exposure at Default (EAD)** | $\\sum \\text{{loan\\_amnt}}$ | **${tot_exposure:,.2f}** | 100.00% |
| **Total Baseline ECL** | $\\sum (\\text{{PD}}_{{\\text{{base}}}} \\times 0.50 \\times \\text{{EAD}})$ | **${tot_ecl_base:,.2f}** | {ecl_base_rate:.2f}% |
| **Total Adverse ECL** | $\\sum (\\text{{PD}}_{{\\text{{adverse}}}} \\times 0.50 \\times \\text{{EAD}})$ | **${tot_ecl_adv:,.2f}** | {(tot_ecl_adv/tot_exposure)*100:.2f}% |
| **Total Severe ECL** | $\\sum (\\text{{PD}}_{{\\text{{severe}}}} \\times 0.50 \\times \\text{{EAD}})$ | **${tot_ecl_sev:,.2f}** | {ecl_sev_rate:.2f}% |

---

## 2. Risk Concentration Matrix (FICO Score Band $\\times$ DTI Band)

| FICO Band | DTI Band | Total Loans | Total Exposure ($) | Avg Baseline PD | Avg Severe PD | Total Base ECL ($) | Total Severe ECL ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for _, r in df_matrix.iterrows():
        md_content += f"| {r['fico_band']} | {r['dti_band']} | {r['total_loans']:,} | ${r['total_exposure']:,.0f} | {r['avg_pd_base_pct']:.2f}% | {r['avg_pd_severe_pct']:.2f}% | ${r['total_ecl_base']:,.2f} | ${r['total_ecl_severe']:,.2f} |\n"

    md_content += f"""
---

## 3. Executive Underwriting Policy Recommendation (Phase 5 Verdict)

> [!IMPORTANT]
> **Policy Verdict for Risk Committee:**  
> **"Halt originations for unsecured loans where DTI $\\ge$ 25% and FICO $<$ 680 to eliminate $\\approx$ ${elim_ecl_sev:,.2f} in severe scenario default losses (saving ${elim_ecl_base:,.2f} in baseline expected credit losses) across ${elim_exposure:,.2f} of high-risk exposure."**

---

## 4. Next Step: Phase 5 (Power BI Deliverables)
All aggregated datasets are exported and structured for Power BI import:
1. **Card Visuals:** Total Base ECL vs. Total Severe ECL.
2. **Matrix Heatmap Visual:** FICO Band on Rows, DTI Band on Columns, Color-coded by ECL.
3. **Executive Summary Card:** Embedded Underwriting Policy Verdict.
"""

    with open(output_md_report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\nSaved Financial Math Report to: {output_md_report_path}")

    print("\n" + "=" * 70)
    print("PHASE 4 COMPLETE: Ready for Phase 5 Power BI Deliverables!")
    print("=" * 70)

    return df_matrix

if __name__ == "__main__":
    run_phase4_pipeline()
