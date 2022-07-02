import pandas as pd
from transform import Calc
from transform import schemas


def pricelist(extracted_df):
    print(f'I am in pk.pricelist\n')

    transformed_df = pd.DataFrame(columns=schemas.PRICELIST_SCHEMA)

    for i in range(extracted_df.shape[0]):
        row_to_add = ['Kufner', extracted_df['MODEL'][i], extracted_df['NAME'][i],
                      int(extracted_df['BUILT YEAR'][i]), extracted_df['MAX PERSONS'][i],
                      float(extracted_df['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€')),
                      float(extracted_df['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€')),
                      float(extracted_df['27.4. - 25.5. AND 28.9. - 5.10.'][i].lstrip('€')),
                      float(extracted_df['8.6. - 22.6. AND 14.9. - 21.9.'][i].lstrip('€')),
                      float(extracted_df['29.6. -27.7. AND 17.8. - 31.8.'][i].lstrip('€')),
                      float(extracted_df['27.7. - 17.8.'][i].lstrip('€')),
                      float(extracted_df['22.6. -29.6. AND 31.8. - 14.9.'][i].lstrip('€')),
                      float(extracted_df['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€')),
                      float(extracted_df['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€'))]
        transformed_df.loc[i] = row_to_add

    return transformed_df


def yachts(extracted_df):
    print(f'I am in pk.yachts\n')

    transformed_df = pd.DataFrame(columns=schemas.YACHTS_SCHEMA)

    # dealing with duplicates columns:
    temp = list(extracted_df.columns)
    list_of_column_names = set()
    for j in range(len(extracted_df.columns)):
        item = extracted_df.columns[j]
        if item in list_of_column_names:
            temp[j] = str(item + '_2')
        else:
            list_of_column_names.add(item)
    extracted_df.columns = temp

    for i in range(extracted_df.shape[0]):
        row_to_add = ['Kufner', extracted_df['MODEL'][i], extracted_df['NAME'][i],
                      int(extracted_df['CABINS'][i].split('+')[0]),
                      Calc.Calc.evaluate(extracted_df['BERTHS_2'][i]),
                      Calc.Calc.evaluate(extracted_df['TOILETS/SHOWERS'][i]),
                      float(extracted_df['LOA'][i].replace(',', '.').rstrip('m ')),
                      float(extracted_df['MAX BEAM'][i].replace(',', '.').rstrip('m ')),
                      float(extracted_df['DRAFT'][i].replace(',', '.').rstrip('m ')),
                      float(extracted_df['MAIN SAIL'][i].split(' ')[0].rstrip('m2'))
                      + float(extracted_df['GENOVA SAIL'][i].split(' ')[0].rstrip('m2')),
                      extracted_df['ENGINE'][i],
                      int(extracted_df['WATER CAPACITY(lt)'][i].rstrip('l ')),
                      int(extracted_df['FUEL CAPACITY(lt)'][i].rstrip('l ')),
                      extracted_df['LOCATION'][i],
                      extracted_df['yacht URL'][i],
                      ]
        transformed_df.loc[i] = row_to_add

    return transformed_df
