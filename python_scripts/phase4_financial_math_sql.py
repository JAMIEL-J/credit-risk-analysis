"""
Phase 4: Financial Math, Expected Credit Loss & Risk-Adjusted Net Profit Pipeline
---------------------------------------------------------------------------------
1. Executes SQL engine to calculate loan-level ECL and Expected Revenue.
   Formulas:
     - Expected Gross Revenue = loan_amnt * (int_rate / 100)
     - Expected Credit Loss (ECL) = PD * LGD (0.50) * loan_amnt
     - Net Profit = Expected Gross Revenue - ECL
     - Net Margin % = (Net Profit / loan_amnt) * 100
2. Groups portfolio by FICO Bands x DTI Bands to calculate Net Return matrix.
3. Formulates the Risk Committee Underwriting Decision based on Net Profit maximization.
4. Exports aggregated tables for Power BI and generates Phase4_Financial_Math_Report.md.
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
    print("PHASE 4: FINANCIAL MATH, EXPECTED LOSS & RISK-ADJUSTED RETURN ENGINE")
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
    print("\n[Step 3] Fetching FICO x DTI Risk & Net Profit Matrix...")
    df_matrix = con.execute("SELECT * FROM ecl_risk_matrix_fico_dti ORDER BY total_exposure DESC").df()
    df_matrix.to_csv(output_matrix_csv, index=False)
    print(f"  -> Saved FICO x DTI Matrix to {output_matrix_csv}")

    # 3. Purpose Breakdown
    print("\n[Step 4] Computing Purpose Breakdown...")
    df_purpose = con.execute("SELECT * FROM ecl_summary_by_purpose").df()
    df_purpose.to_csv(output_purpose_csv, index=False)
    print(f"  -> Saved Purpose Breakdown to {output_purpose_csv}")

    # Portfolio Top-Level KPIs
    tot_exposure = df_loan_level['ead'].sum()
    tot_revenue = df_loan_level['expected_revenue'].sum()
    tot_ecl_base = df_loan_level['ecl_base'].sum()
    tot_ecl_adv = df_loan_level['ecl_adverse'].sum()
    tot_ecl_sev = df_loan_level['ecl_severe'].sum()
    tot_ecl_gap = df_loan_level['ecl_gap'].sum()
    tot_net_profit_base = df_loan_level['net_profit_base'].sum()
    tot_net_profit_sev = df_loan_level['net_profit_severe'].sum()
    
    ecl_base_rate = (tot_ecl_base / tot_exposure) * 100
    ecl_sev_rate = (tot_ecl_sev / tot_exposure) * 100
    net_margin_base = (tot_net_profit_base / tot_exposure) * 100
    net_margin_sev = (tot_net_profit_sev / tot_exposure) * 100

    print("\n" + "=" * 70)
    print("PORTFOLIO LEVEL FINANCIAL & RISK-ADJUSTED RETURN SUMMARY:")
    print("=" * 70)
    print(f"Total Portfolio Exposure (EAD):     ${tot_exposure:,.2f}")
    print(f"Total Expected Gross Revenue:       ${tot_revenue:,.2f} ({(tot_revenue/tot_exposure)*100:.2f}% Yield)")
    print(f"Total Base Expected Credit Loss:    ${tot_ecl_base:,.2f} ({ecl_base_rate:.2f}% Loss Rate)")
    print(f"Total Baseline Net Profit:          ${tot_net_profit_base:,.2f} ({net_margin_base:.2f}% Net Margin)")
    print(f"Total Severe Expected Credit Loss:  ${tot_ecl_sev:,.2f} ({ecl_sev_rate:.2f}% Loss Rate)")
    print(f"Total Severe Net Profit:            ${tot_net_profit_sev:,.2f} ({net_margin_sev:.2f}% Net Margin)")

    # 4. Generate Markdown Financial Math Report
    md_content = f"""# Phase 4: Financial Math & Risk-Adjusted Net Return Report

---

## 1. Executive Summary & Core Financial Formulation
This phase computes regulatory **Expected Credit Loss (ECL)** alongside **Expected Gross Revenue** to determine the **Risk-Adjusted Net Return** across the portfolio:

$$\\text{{Expected Gross Revenue}} = \\text{{loan\\_amnt}} \\times \\left(\\frac{{\\text{{int\\_rate}}}}{{100}}\\right)$$

$$\\text{{Expected Credit Loss (ECL)}} = \\text{{PD}} \\times \\text{{LGD (0.50)}} \\times \\text{{loan\\_amnt}}$$

$$\\mathbf{{\\text{{Net Profit}}}} = \\mathbf{{\\text{{Expected Gross Revenue}}}} - \\mathbf{{\\text{{Expected Credit Loss (ECL)}}}}$$

$$\\mathbf{{\\text{{Net Profit Margin (\\%)}}}} = \\left(\\frac{{\\text{{Net Profit}}}}{{\\text{{loan\\_amnt}}}}\\right) \\times 100$$

---

## 2. Portfolio-Level Financial Totals ({len(df_loan_level):,} Loans)
* **Total Portfolio Exposure (EAD):** **`${tot_exposure:,.2f}`**
* **Expected Annual Gross Revenue:** **`${tot_revenue:,.2f}`** (Portfolio Gross Yield: `{(tot_revenue/tot_exposure)*100:.2f}%`)
* **Total Baseline Expected Credit Loss (ECL):** **`${tot_ecl_base:,.2f}`** (`{ecl_base_rate:.2f}%` Loss Rate)
* **Total Baseline Risk-Adjusted Net Profit:** **`${tot_net_profit_base:,.2f}`** (`{net_margin_base:.2f}%` Net Margin)
* **Total Severe Scenario ECL:** **`${tot_ecl_sev:,.2f}`** (`{ecl_sev_rate:.2f}%` Loss Rate)
* **Total Severe Scenario Net Profit:** **`${tot_net_profit_sev:,.2f}`** (`{net_margin_sev:.2f}%` Net Margin)

---

## 3. FICO $\\times$ DTI Risk & Net Profit Concentration Matrix
Below is the aggregated performance matrix grouping borrowers by credit score and leverage:

{df_matrix.to_markdown(index=False)}

---

## 4. Official Risk Committee Underwriting Verdict (Risk-Adjusted Rule)

> ### 🏛️ Risk Committee Underwriting Policy Rule:
> **"Instead of halting originations blindly based on raw default rate, underwriting policy evaluates Risk-Adjusted Net Return (Revenue - ECL). Halt originations exclusively for segments generating negative net returns (ECL > Revenue), while preserving high-yield segments whose interest rates adequately cover default risk."**

---
*Report generated automatically by Phase 4 Financial Math Engine via DuckDB.*
"""
    with open(output_md_report_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n[Step 5] Saved Phase 4 Financial Math Report to: {output_md_report_path}")
    print("=" * 70)
    print("PHASE 4 COMPLETE: Ready for Phase 5 Dashboard & Deliverables!")
    print("=" * 70)

if __name__ == "__main__":
    run_phase4_pipeline()
