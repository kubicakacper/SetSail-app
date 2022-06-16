from pathlib import Path
from transform import mergeData as md

DFtoLoad = md.mergeData()

filepath = Path('/Users/kubicakacper/PycharmProjects/SetSail_app/csv_files/mergedData.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
DFtoLoad.to_csv(filepath)

