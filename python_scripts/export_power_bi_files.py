"""
Organize and export clean CSV files dedicated for Power BI import.
"""
import os
import shutil
import pandas as pd

def organize_power_bi_exports():
    export_dir = "power_bi_exports"
    os.makedirs(export_dir, exist_ok=True)
    
    files_to_copy = [
        ("data/ecl_risk_matrix_fico_dti.csv", f"{export_dir}/ecl_risk_matrix_fico_dti.csv"),
        ("data/ecl_summary_by_purpose.csv", f"{export_dir}/ecl_summary_by_purpose.csv"),
        ("data/stressed_portfolio_phase3.csv", f"{export_dir}/stressed_portfolio_phase3.csv"),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copyfile(src, dst)
            size_mb = os.path.getsize(dst) / (1024 * 1024)
            print(f"Copied {src} -> {dst} ({size_mb:.2f} MB)")
        else:
            print(f"Source file not found: {src}")

if __name__ == "__main__":
    organize_power_bi_exports()
