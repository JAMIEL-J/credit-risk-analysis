"""
Organize all generated project reports into the reports/ folder.
"""
import os
import shutil

def organize_reports():
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    report_files = [
        "Phase1_Data_Engineering_Report.md",
        "Phase2_Model_Evaluation_Report.md",
        "Phase3_Stress_Testing_Report.md",
        "Phase4_Financial_Math_Report.md",
        "Phase5_Power_BI_Deliverable_Guide.md"
    ]
    
    for filename in report_files:
        if os.path.exists(filename):
            dst = os.path.join(reports_dir, filename)
            shutil.copyfile(filename, dst)
            print(f"Copied {filename} -> {dst}")

if __name__ == "__main__":
    organize_reports()
