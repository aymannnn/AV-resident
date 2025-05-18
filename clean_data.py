import pandas as pd
import numpy as np

# import data and quick clean

df = pd.read_csv('input_data/preferences.csv')

# transpose df becaues I'm an idiot

df = df.transpose()
df.columns = df.iloc[0]
df = df[1:]

date_blocks = df.columns
df = df.fillna(0)

# export data

df.to_csv('input_data/preferences_cleaned.csv', index=True)