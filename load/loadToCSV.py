from pathlib import Path


def load_to_csv(df_to_load):
    filepath = Path('/Users/kubicakacper/PycharmProjects/SetSail_app/csv_files/mergedData.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df_to_load.to_csv(filepath)
