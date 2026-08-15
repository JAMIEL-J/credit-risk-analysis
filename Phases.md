Here are the exact execution steps. Do them in this order.

### Phase 1: Data Engineering (Python)

1. **Load Loan Data:** Import the LendingClub dataset. Keep only: `loan_amnt`, `issue_d`, `dti`, `fico_range_low`, `purpose`, and `loan_status`.
2. **Define Target:** Filter `loan_status` for "Fully Paid" (Target = 0) and "Charged Off" (Target = 1). Drop current/active loans.
3. **Format Dates:** Convert `issue_d` to a `Year_Month` format.
4. **Load Macro Data:** Pull `UNRATE` (Unemployment) and `FEDFUNDS` (Interest Rate) from FRED. Format their dates to `Year_Month`.
5. **Merge:** Perform a Left Join in pandas to map the FRED data onto the LendingClub data using `Year_Month`.

### Phase 2: ML Engine (Python + XGBoost)

1. **Prepare Features:** Your input features (X) are FICO, DTI, Purpose, UNRATE, and FEDFUNDS. Your target (y) is Default (1 or 0).
2. **Train Model:** Train an XGBoost Classifier on the merged dataset.
3. **Extract PD:** Use `.predict_proba()` to get the exact percentage probability of default (PD) for each loan.

### Phase 3: The Stress Test (Python)

1. **Isolate Portfolio:** Take a sample of recent loans to serve as your test portfolio.
2. **Base Scenario:** Run the portfolio through the model using current macro numbers to get Baseline PD.
3. **Adverse Scenario:** Overwrite the macro columns: add +1.5% to UNRATE and +0.5% to FEDFUNDS. Run `.predict_proba()` to get Adverse PD.
4. **Severe Scenario:** Overwrite macro columns again: add +3.5% to UNRATE and +1.5% to FEDFUNDS. Run `.predict_proba()` to get Severe PD.
5. **Export:** Export these 3 DataFrames to a CSV for SQL analysis.

### Phase 4: Financial Math (SQL)

1. **Calculate Base ECL:** Run `PD_base * 0.50 * loan_amnt` for all rows. (0.50 is the assumed Loss Given Default).
2. **Calculate Severe ECL:** Run `PD_severe * 0.50 * loan_amnt`.
3. **Find the Gap:** Subtract Base ECL from Severe ECL to find the exact dollar amount of increased risk.
4. **Isolate Risk:** Group the results by FICO bands and DTI bands. Sort descending by the highest ECL gap. Export this aggregated table.

### Phase 5: The Deliverable (Power BI)

1. **Import:** Load the aggregated SQL table.
2. **KPIs:** Create top-level cards showing the total Base ECL vs. Severe ECL.
3. **Heatmap:** Build a FICO vs. DTI matrix visual. Color-code it by the ECL gap to instantly show the highest risk concentration.
4. **The Verdict:** Add a static text box: "Halt originations for unsecured loans where DTI > [X] and FICO < [Y] to eliminate $[Z] in severe scenario losses."