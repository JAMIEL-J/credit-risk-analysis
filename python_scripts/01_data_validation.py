import duckdb

query = """
SELECT 
    loan_amnt, 
    issue_d, 
    dti, 
    fico_range_low, 
    purpose, 
    loan_status
FROM read_csv_auto('data/accepted_2007_to_2018Q4.csv')
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND issue_d IS NOT NULL
"""

df_loans = duckdb.query(query).df()
print(f"Rows loaded: {len(df_loans)}")

import pandas as pd

# 1. Convert Target to Binary (1 = Default, 0 = Paid)
df_loans['target'] = df_loans['loan_status'].apply(lambda x: 1 if x == 'Charged Off' else 0)

# 2. Format Loan Dates ("Dec-2015" -> "2015-12")
df_loans['issue_d'] = pd.to_datetime(df_loans['issue_d'], format='%b-%Y')
df_loans['Year_Month'] = df_loans['issue_d'].dt.to_period('M')

# 3. Load and Format FRED Data
df_unrate = pd.read_csv('data/UNRATE.csv')
df_fed = pd.read_csv('data/FEDFUNDS.csv')

# Merge macro data together, then format date
df_macro = pd.merge(df_unrate, df_fed, on='DATE')
df_macro['DATE'] = pd.to_datetime(df_macro['DATE'])
df_macro['Year_Month'] = df_macro['DATE'].dt.to_period('M')

# 4. Final Merge: Attach Macro to Loans
df_final = pd.merge(df_loans, df_macro[['Year_Month', 'UNRATE', 'FEDFUNDS']], on='Year_Month', how='left')

# Drop any rows where macro data didn't map
df_final = df_final.dropna(subset=['UNRATE', 'FEDFUNDS'])

print(df_final[['issue_d', 'target', 'UNRATE', 'FEDFUNDS']].head())