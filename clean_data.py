import pandas as pd
import numpy as np

# 1. Simulate "Messy" Enterprise Data (Like an Appian Export)
data = {
    'Project_ID': [101, 102, 103, 104],
    'Client_Name': ['iShift', 'Federal_Agency_A', 'iShift', 'Federal_Agency_B'],
    'Budget_Status': ['Over', 'Under', 'Over', 'Pending'],
    'Margin_Value': [0.15, -0.05, 0.22, np.nan] # np.nan is a "null" value
}

# 2. Create a "DataFrame" (Think of this as an Appian CDT or a Table)
df = pd.DataFrame(data)

print("--- Original Data ---")
print(df)

# 3. Data Transformation (Logic)
# Let's say we only care about 'iShift' projects with a valid margin.
cleaned_df = df[df['Client_Name'] == 'iShift'].copy()

# Fill the missing margin with the average (a very common AI prep step)
avg_margin = df['Margin_Value'].mean()
df['Margin_Value'] = df['Margin_Value'].fillna(avg_margin)

print("\n--- Processed Data (Ready for AI) ---")
print(df)