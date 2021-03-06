import pandas as pd
from pathlib import Path

filepath = Path('/Users/kubicakacper/PycharmProjects/SetSail_app/csv_files/mergedData.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)

df_from_csv = pd.read_csv(filepath)
pd.set_option('display.max_columns', None)
print(df_from_csv.head())

print(df_from_csv.columns.values.tolist())
