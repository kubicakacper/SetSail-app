from transform import Calc
import pandas as pd
from transform import schemas


def pricelist(extracted_df):
    print(f'I am in pfw.pricelist\n')

    transformed_df = pd.DataFrame(columns=schemas.PRICELIST_SCHEMA)
    model_column = []
    name_column = []

    for row in extracted_df['Segelyachten']:
        model, name = str(row).split(' ‚')
        model_column.append(model)
        name_column.append(name.rstrip('‘'))

    for i in range(len(model_column)):
        row_to_add = ['Free-Wave', model_column[i], name_column[i], int(extracted_df['Baujahr'][i + 1]),
                      Calc.Calc.evaluate(extracted_df['Kojen'][i + 1]),
                      1000 * float(extracted_df['19.03. 09.04.'][i + 1]),
                      1000 * float(extracted_df['09.04. 30.04.'][i + 1]),
                      1000 * float(extracted_df['14.05. 28.05.'][i + 1]),
                      1000 * float(extracted_df['11.06. 25.06.'][i + 1]),
                      1000 * float(extracted_df['09.07. 23.07.'][i + 1]),
                      1000 * float(extracted_df['13.08. 27.08.'][i + 1]),
                      1000 * float(extracted_df['10.09. 24.09.'][i + 1]),
                      1000 * float(extracted_df['08.10. 22.10.'][i + 1]),
                      1000 * float(extracted_df['22.10. 05.11.'][i + 1])]
        transformed_df.loc[i] = row_to_add

    return transformed_df


def yachts(extracted_df):
    print(f'I am in pfw.yachts\n')

    transformed_df = pd.DataFrame(columns=schemas.YACHTS_SCHEMA)

    model_column = []
    name_column = []

    for row in extracted_df['NAME']:
        model, name = str(row).replace(' „', ' ‚').replace(' “', ' ‚').split(' ‚')
        model_column.append(model)
        name_column.append(name.rstrip('‘,“”'))

    for i in range(len(model_column)):
        row_to_add = ['Free-Wave', model_column[i], name_column[i], int(extracted_df['Cabins:'][i].split('+')[0]),
                      Calc.Calc.evaluate(extracted_df['Berths:'][i]),
                      Calc.Calc.evaluate(extracted_df['Toilets:'][i]),
                      float(extracted_df['LOA = Overall length (m):'][i].replace(',', '.')),
                      float(extracted_df['Max. beam (m):'][i].replace(',', '.')),
                      float(extracted_df['Draft (m):'][i].replace(',', '.')),
                      float(extracted_df['Canvas size(m2):'][i].replace(',', '.'))
                      if extracted_df['Canvas size(m2):'][i] != 'Unknown' else float(-1),
                      extracted_df['Engine:'][i],
                      int(extracted_df['Water tank (l):'][i]),
                      int(extracted_df['Fuel tank (l):'][i]),
                      extracted_df['Location'][i],
                      extracted_df['yacht URL'][i]
                      ]  # regarding "float(-1)": I would use NaN, but MyQSL does not support it
        transformed_df.loc[i] = row_to_add

    return transformed_df
