-- ====================================================================
-- Phase 4: Financial Math, Expected Credit Loss & Risk-Adjusted Net Return Engine
-- ====================================================================
-- Formulations:
--   - Expected Revenue = loan_amnt * (int_rate / 100)
--   - ECL = PD * LGD (0.50) * loan_amnt
--   - Net Profit = Expected Revenue - ECL
--   - Net Margin % = (Net Profit / loan_amnt) * 100
-- ====================================================================

-- 1. Loan-Level Financial Calculations & Risk Band Categorization
CREATE OR REPLACE TABLE loan_level_ecl AS
SELECT 
    Year_Month,
    loan_amnt AS ead,
    int_rate,
    annual_inc,
    fico_range_low,
    dti,
    revol_util,
    delinq_2yrs,
    inq_last_6mths,
    purpose,
    UNRATE,
    FEDFUNDS,
    PD_base,
    PD_adverse,
    PD_severe,
    
    -- 1. Expected Gross Revenue (Interest Income)
    (loan_amnt * (int_rate / 100.0)) AS expected_revenue,
    
    -- 2. Expected Credit Loss (ECL = PD * LGD * EAD)
    (PD_base * 0.50 * loan_amnt) AS ecl_base,
    (PD_adverse * 0.50 * loan_amnt) AS ecl_adverse,
    (PD_severe * 0.50 * loan_amnt) AS ecl_severe,
    ((PD_severe * 0.50 * loan_amnt) - (PD_base * 0.50 * loan_amnt)) AS ecl_gap,
    
    -- 3. Risk-Adjusted Net Profit (Revenue - ECL)
    ((loan_amnt * (int_rate / 100.0)) - (PD_base * 0.50 * loan_amnt)) AS net_profit_base,
    ((loan_amnt * (int_rate / 100.0)) - (PD_adverse * 0.50 * loan_amnt)) AS net_profit_adverse,
    ((loan_amnt * (int_rate / 100.0)) - (PD_severe * 0.50 * loan_amnt)) AS net_profit_severe,
    
    -- FICO Credit Score Bands
    CASE 
        WHEN fico_range_low < 660 THEN '< 660 (Subprime)'
        WHEN fico_range_low BETWEEN 660 AND 699 THEN '660 - 699 (Fair)'
        WHEN fico_range_low BETWEEN 700 AND 749 THEN '700 - 749 (Good)'
        WHEN fico_range_low BETWEEN 750 AND 799 THEN '750 - 799 (Very Good)'
        WHEN fico_range_low >= 800 THEN '800+ (Exceptional)'
        ELSE 'Unknown'
    END AS fico_band,
    
    -- DTI (Debt-to-Income) Risk Bands
    CASE 
        WHEN dti < 10.0 THEN '0% - 10%'
        WHEN dti BETWEEN 10.0 AND 19.99 THEN '10% - 20%'
        WHEN dti BETWEEN 20.0 AND 29.99 THEN '20% - 30%'
        WHEN dti BETWEEN 30.0 AND 39.99 THEN '30% - 40%'
        WHEN dti >= 40.0 THEN '40%+'
        ELSE 'Unknown'
    END AS dti_band
FROM read_parquet('data/stressed_portfolio_phase3.parquet');

-- 2. Aggregated Risk & Net Profit Matrix (FICO Band x DTI Band) for Heatmaps & Decisioning
CREATE OR REPLACE TABLE ecl_risk_matrix_fico_dti AS
SELECT 
    fico_band,
    dti_band,
    COUNT(*) AS total_loans,
    SUM(ead) AS total_exposure,
    AVG(int_rate) AS avg_int_rate_pct,
    AVG(PD_base) * 100 AS avg_pd_base_pct,
    AVG(PD_severe) * 100 AS avg_pd_severe_pct,
    SUM(expected_revenue) AS total_expected_revenue,
    SUM(ecl_base) AS total_ecl_base,
    SUM(ecl_severe) AS total_ecl_severe,
    SUM(ecl_gap) AS total_ecl_gap,
    SUM(net_profit_base) AS total_net_profit_base,
    SUM(net_profit_severe) AS total_net_profit_severe,
    (SUM(net_profit_base) / NULLIF(SUM(ead), 0)) * 100 AS net_margin_base_pct,
    (SUM(net_profit_severe) / NULLIF(SUM(ead), 0)) * 100 AS net_margin_severe_pct,
    CASE 
        WHEN SUM(net_profit_base) < 0 THEN 'Negative Net Profit (Halt Origination)'
        WHEN (SUM(net_profit_base) / NULLIF(SUM(ead), 0)) * 100 < 2.0 THEN 'Marginal Margin (<2% Net Return)'
        ELSE 'Strong Positive Return (>2% Net Margin)'
    END AS risk_adjusted_verdict
FROM loan_level_ecl
GROUP BY fico_band, dti_band
ORDER BY total_exposure DESC;

-- 3. Aggregated Summary by Purpose
CREATE OR REPLACE TABLE ecl_summary_by_purpose AS
SELECT 
    purpose,
    COUNT(*) AS total_loans,
    SUM(ead) AS total_exposure,
    AVG(int_rate) AS avg_int_rate,
    AVG(PD_base) * 100 AS avg_pd_base_pct,
    SUM(expected_revenue) AS total_expected_revenue,
    SUM(ecl_base) AS total_ecl_base,
    SUM(net_profit_base) AS total_net_profit_base,
    (SUM(net_profit_base) / NULLIF(SUM(ead), 0)) * 100 AS net_margin_base_pct
FROM loan_level_ecl
GROUP BY purpose
ORDER BY total_exposure DESC;
