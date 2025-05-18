import pandas as pd
import numpy as np

# import data and quick clean

df = pd.read_csv('input_data/preferences.csv')

# transpose df becaues I'm an idiot

df = df.transpose()
df.columns = df.iloc[0]
df = df[1:]

date_blocks = df.columns

def fill_missing_with_unique_random(df, min_val=1, max_val=len(date_blocks)):
    for idx, row in df.iterrows():
        missing = row.isnull()
        n_missing = missing.sum()
        if n_missing > 0:
            existing = set(pd.to_numeric(row.dropna(), errors='coerce').astype(int))
            possible = [x for x in range(min_val, max_val + 1) if x not in existing]
            if len(possible) < n_missing:
                raise ValueError(f"Not enough unique values to fill missing for row {idx}")
            fill_values = np.random.choice(possible, size=n_missing, replace=False)
            row[missing] = fill_values
            df.loc[idx] = row
    return df

df = fill_missing_with_unique_random(df)

# now do a check to make sure that each row has all values from 1 to 18

def check_rows_have_all_unique_values(df, min_val=1, max_val=len(date_blocks)):
    for idx, row in df.iterrows():
        values = pd.to_numeric(row, errors='coerce').astype(int)
        unique_values = set(values)
        expected_values = set(range(min_val, max_val + 1))
        if unique_values != expected_values:
            print(f"Row {idx} does not contain all unique values from {min_val} to {max_val}.")
            return False
    print("All rows contain unique values from 1 to n_blocks.")
    return True

check_rows_have_all_unique_values(df)

# export data

df.to_csv('input_data/preferences_cleaned.csv', index=True)