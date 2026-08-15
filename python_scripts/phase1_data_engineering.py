"""
Phase 1: Data Engineering Pipeline
----------------------------------
1. Load LendingClub dataset via DuckDB (memory-efficient streaming of large 1.67GB CSV).
   Required columns: loan_amnt, issue_d, dti, fico_range_low, purpose, loan_status.
2. Define Binary Target:
   - "Fully Paid" -> 0
   - "Charged Off" -> 1
   - Drop all ongoing/indeterminate loans (Current, Late, In Grace Period).
3. Format Dates: Convert issue_d to Year_Month string (YYYY-MM).
4. Load Macro Indicators:
   - UNRATE (Unemployment Rate from FRED)
   - FEDFUNDS (Effective Federal Funds Rate from FRED)
   - Standardize dates to Year_Month (YYYY-MM).
5. Merge: Left Join macro indicators onto loan data using Year_Month.
6. Data Quality & Validation Checks:
   - Missing value verification
   - Value distribution validation
7. Save cleaned analytical dataset as Parquet for Phase 2 XGBoost modeling.
"""

import os
import duckdb
import pandas as pd
import numpy as np

def run_phase1_pipeline(
    loan_csv_path: str = "data/accepted_2007_to_2018Q4.csv",
    unrate_csv_path: str = "data/UNRATE.csv",
    fedfunds_csv_path: str = "data/FEDFUNDS.csv",
    output_parquet_path: str = "data/cleaned_loans_phase1.parquet",
    output_csv_sample_path: str = "data/cleaned_loans_phase1_sample.csv",
    output_md_report_path: str = "Phase1_Data_Engineering_Report.md"
):
    print("=" * 60)
    print("PHASE 1: DATA ENGINEERING & MACRO INTEGRATION")
    print("=" * 60)

    # 1 & 2. Load & Filter LendingClub data using DuckDB
    print("\n[Step 1 & 2] Loading & filtering LendingClub loans via DuckDB...")
    query = f"""
    SELECT 
        loan_amnt, 
        issue_d, 
        dti, 
        fico_range_low, 
        purpose, 
        loan_status,
        CASE 
            WHEN loan_status = 'Charged Off' THEN 1 
            WHEN loan_status = 'Fully Paid' THEN 0 
            ELSE NULL 
        END AS target
    FROM read_csv_auto('{loan_csv_path}')
    WHERE loan_status IN ('Fully Paid', 'Charged Off')
      AND issue_d IS NOT NULL
      AND loan_amnt IS NOT NULL
      AND fico_range_low IS NOT NULL
    """
    
    con = duckdb.connect()
    df_loans = con.execute(query).df()
    print(f"Loaded {len(df_loans):,} closed/matured loan records.")
    print(f"Target distribution:\n{df_loans['target'].value_counts(normalize=True).round(4) * 100}%")

    # 3. Format Dates to Year_Month
    print("\n[Step 3] Parsing dates and constructing Year_Month keys...")
    df_loans['issue_d_dt'] = pd.to_datetime(df_loans['issue_d'], format='%b-%Y')
    df_loans['Year_Month'] = df_loans['issue_d_dt'].dt.strftime('%Y-%m')

    # 4. Load Macro Indicators
    print("\n[Step 4] Loading and preparing macroeconomic datasets...")
    # Load UNRATE
    df_unrate = pd.read_csv(unrate_csv_path)
    df_unrate['UNRATE_dt'] = pd.to_datetime(df_unrate['DATE'])
    df_unrate['Year_Month'] = df_unrate['UNRATE_dt'].dt.strftime('%Y-%m')
    df_unrate = df_unrate[['Year_Month', 'UNRATE']].drop_duplicates(subset=['Year_Month'])

    # Load FEDFUNDS
    df_fed = pd.read_csv(fedfunds_csv_path)
    date_col = 'observation_date' if 'observation_date' in df_fed.columns else 'DATE'
    df_fed['FED_dt'] = pd.to_datetime(df_fed[date_col])
    df_fed['Year_Month'] = df_fed['FED_dt'].dt.strftime('%Y-%m')
    df_fed = df_fed[['Year_Month', 'FEDFUNDS']].drop_duplicates(subset=['Year_Month'])

    # Merge Macro Indicators together
    df_macro = pd.merge(df_unrate, df_fed, on='Year_Month', how='inner')
    print(f"Macro series synchronized: {len(df_macro)} monthly records ({df_macro['Year_Month'].min()} to {df_macro['Year_Month'].max()})")

    # 5. Merge Loans with Macro Data
    print("\n[Step 5] Merging loans with macroeconomic factors...")
    df_merged = pd.merge(df_loans, df_macro, on='Year_Month', how='left')

    # 6. Data Quality Checks & Cleaning
    print("\n[Step 6] Running Data Quality & Validation Checks...")
    initial_count = len(df_merged)
    
    # Check missing rate
    missing_summary = df_merged.isnull().sum()
    print("Missing values per column before cleaning:")
    for col, null_cnt in missing_summary.items():
        print(f"  - {col}: {null_cnt:,} ({null_cnt/initial_count*100:.2f}%)")

    # Filter out records missing macro data or invalid DTI
    df_clean = df_merged.dropna(subset=['UNRATE', 'FEDFUNDS', 'dti']).copy()
    
    # Filter abnormal/extreme negative or corrupted values
    df_clean = df_clean[df_clean['dti'] >= 0]
    df_clean = df_clean[df_clean['dti'] <= 100]  # Cap standard pre-loan DTI outlier noise
    
    # Reorder columns
    final_cols = [
        'issue_d', 
        'Year_Month', 
        'loan_amnt', 
        'fico_range_low', 
        'dti', 
        'purpose', 
        'UNRATE', 
        'FEDFUNDS', 
        'loan_status', 
        'target'
    ]
    df_clean = df_clean[final_cols]
    
    final_count = len(df_clean)
    print(f"\nFinal cleaned dataset shape: {df_clean.shape}")
    print(f"Retained {final_count:,} of {initial_count:,} loans ({(final_count/initial_count)*100:.2f}%)")
    print(f"Default rate in cleaned dataset: {(df_clean['target'].mean()*100):.2f}%")

    # 7. Save outputs
    print("\n[Step 7] Exporting cleaned dataset and Markdown report...")
    df_clean.to_parquet(output_parquet_path, index=False)
    parquet_size_mb = os.path.getsize(output_parquet_path) / (1024 * 1024)
    print(f"  -> Saved Parquet to: {output_parquet_path} ({parquet_size_mb:.2f} MB)")
    
    # Save a small sample for rapid inspection / SQL testing
    df_clean.head(1000).to_csv(output_csv_sample_path, index=False)
    print(f"  -> Saved 1,000 row preview CSV to: {output_csv_sample_path}")

    # Generate Markdown Report
    target_stats = df_clean['target'].value_counts()
    purpose_stats = df_clean['purpose'].value_counts().head(8)
    
    md_content = f"""# Phase 1: Data Engineering & Macro Integration Report

**Execution Status:** Completed Successfully  
**Pipeline Script:** `python_scripts/phase1_data_engineering.py`  
**Processed Output:** `{output_parquet_path}` ({parquet_size_mb:.2f} MB)  
**Preview Sample:** `{output_csv_sample_path}`

---

## 1. Executive Summary

Phase 1 establishes the consolidated, quality-assured analytical baseline by combining LendingClub closed loan records with historical Federal Reserve macroeconomic series (`UNRATE` and `FEDFUNDS`).

| Metric | Value |
| :--- | :--- |
| **Total Ingested Closed Loans** | {initial_count:,} |
| **Final Retained Quality Records** | {final_count:,} |
| **Data Retention Rate** | {(final_count / initial_count) * 100:.2f}% |
| **Total Features Retained** | {len(final_cols)} |
| **Historical Period Covered** | {df_clean['Year_Month'].min()} to {df_clean['Year_Month'].max()} |

---

## 2. Target Variable Formulation

Loans are categorized based on their terminal resolution:
* **Fully Paid (`target = 0`):** {target_stats.get(0, 0):,} ({target_stats.get(0, 0)/final_count*100:.2f}%)
* **Charged Off / Default (`target = 1`):** {target_stats.get(1, 0):,} ({target_stats.get(1, 0)/final_count*100:.2f}%)
* **Overall Default Rate:** {(df_clean['target'].mean()*100):.2f}%

---

## 3. Macroeconomic Integration

Macro indicators from the Federal Reserve Economic Data (FRED) were synchronized via `Year_Month` timestamp keys:
* **Unemployment Rate (`UNRATE`):** Range [{df_clean['UNRATE'].min():.1f}%, {df_clean['UNRATE'].max():.1f}%], Mean: {df_clean['UNRATE'].mean():.2f}%
* **Federal Funds Rate (`FEDFUNDS`):** Range [{df_clean['FEDFUNDS'].min():.2f}%, {df_clean['FEDFUNDS'].max():.2f}%], Mean: {df_clean['FEDFUNDS'].mean():.2f}%

---

## 4. Key Feature Statistics

| Feature | Min | Median | Mean | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Loan Amount (`loan_amnt`)** | ${df_clean['loan_amnt'].min():,.0f} | ${df_clean['loan_amnt'].median():,.0f} | ${df_clean['loan_amnt'].mean():,.2f} | ${df_clean['loan_amnt'].max():,.0f} |
| **FICO Score (`fico_range_low`)** | {df_clean['fico_range_low'].min():.0f} | {df_clean['fico_range_low'].median():.0f} | {df_clean['fico_range_low'].mean():.2f} | {df_clean['fico_range_low'].max():.0f} |
| **Debt-to-Income (`dti`)** | {df_clean['dti'].min():.2f}% | {df_clean['dti'].median():.2f}% | {df_clean['dti'].mean():.2f}% | {df_clean['dti'].max():.2f}% |
| **Unemployment Rate (`UNRATE`)** | {df_clean['UNRATE'].min():.1f}% | {df_clean['UNRATE'].median():.1f}% | {df_clean['UNRATE'].mean():.2f}% | {df_clean['UNRATE'].max():.1f}% |
| **Federal Funds Rate (`FEDFUNDS`)** | {df_clean['FEDFUNDS'].min():.2f}% | {df_clean['FEDFUNDS'].median():.2f}% | {df_clean['FEDFUNDS'].mean():.2f}% | {df_clean['FEDFUNDS'].max():.2f}% |

### Top Loan Purposes:
{chr(10).join([f"- **{k}**: {v:,} loans ({(v/final_count)*100:.2f}%)" for k, v in purpose_stats.items()])}

---

## 5. Next Steps (Phase 2: ML Engine)
1. **Categorical Encoding:** One-hot / frequency encode `purpose`.
2. **Train/Test Splitting & XGBoost Classifier:** Fit default model on features:
   $$\\mathbf{{X}} = [\\text{{fico\\_range\\_low}}, \\text{{dti}}, \\text{{purpose}}, \\text{{UNRATE}}, \\text{{FEDFUNDS}}]$$
3. **Probability Calibration & Baseline PD Extraction:** Output calibrated default probabilities for stress testing.
"""

    with open(output_md_report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  -> Saved Markdown Report to: {output_md_report_path}")

    print("\n" + "=" * 60)
    print("PHASE 1 COMPLETE: Ready for Phase 2 ML Engine!")
    print("=" * 60)
    print("\nSample Preview:")
    print(df_clean.head(5))

    return df_clean

if __name__ == "__main__":
    run_phase1_pipeline()
