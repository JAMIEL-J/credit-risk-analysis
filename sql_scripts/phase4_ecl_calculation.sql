-- ====================================================================
-- Phase 4: Financial Math & Expected Credit Loss (ECL) Calculation Engine
-- ====================================================================
-- Assumptions:
--   - Loss Given Default (LGD) = 0.50 (50%)
--   - Exposure at Default (EAD) = loan_amnt
--   - ECL = PD * LGD * EAD
-- ====================================================================

-- 1. Loan-Level ECL Calculations & Risk Band Categorization
CREATE OR REPLACE TABLE loan_level_ecl AS
SELECT 
    Year_Month,
    loan_amnt AS ead,
    fico_range_low,
    dti,
    purpose,
    UNRATE,
    FEDFUNDS,
    PD_base,
    PD_adverse,
    PD_severe,
    
    -- Expected Credit Loss (ECL) Formulas
    (PD_base * 0.50 * loan_amnt) AS ecl_base,
    (PD_adverse * 0.50 * loan_amnt) AS ecl_adverse,
    (PD_severe * 0.50 * loan_amnt) AS ecl_severe,
    ((PD_severe * 0.50 * loan_amnt) - (PD_base * 0.50 * loan_amnt)) AS ecl_gap,
    
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

-- 2. Aggregated Risk Matrix (FICO Band x DTI Band) for Power BI Heatmap
CREATE OR REPLACE TABLE ecl_risk_matrix_fico_dti AS
SELECT 
    fico_band,
    dti_band,
    COUNT(*) AS total_loans,
    SUM(ead) AS total_exposure,
    AVG(PD_base) * 100 AS avg_pd_base_pct,
    AVG(PD_severe) * 100 AS avg_pd_severe_pct,
    SUM(ecl_base) AS total_ecl_base,
    SUM(ecl_severe) AS total_ecl_severe,
    SUM(ecl_gap) AS total_ecl_gap,
    (SUM(ecl_gap) / NULLIF(SUM(ead), 0)) * 100 AS ecl_gap_loss_rate_pct
FROM loan_level_ecl
GROUP BY fico_band, dti_band
ORDER BY total_ecl_gap DESC;
