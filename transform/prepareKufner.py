import pandas as pd
from extract import Kufner as kuf
from transform import Calc as c
from transform import schemas


def pricelist(extractedDF):

    print(f'I am in pk.pricelist\n')

    # extractedDF = kuf.pricelist()

    transformedDF = pd.DataFrame(columns=schemas.PRICELIST_SCHEMA)

    for i in range(extractedDF.shape[0]):
        rowToAdd = ['Kufner', extractedDF['MODEL'][i], extractedDF['NAME'][i], \
                    int(extractedDF['BUILT YEAR'][i]), extractedDF['MAX PERSONS'][i], \
                    float(extractedDF['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€')), \
                    float(extractedDF['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€')), \
                    float(extractedDF['27.4. - 25.5. AND 28.9. - 5.10.'][i].lstrip('€')), \
                    float(extractedDF['8.6. - 22.6. AND 14.9. - 21.9.'][i].lstrip('€')), \
                    float(extractedDF['29.6. -27.7. AND 17.8. - 31.8.'][i].lstrip('€')), \
                    float(extractedDF['27.7. - 17.8.'][i].lstrip('€')), \
                    float(extractedDF['22.6. -29.6. AND 31.8. - 14.9.'][i].lstrip('€')), \
                    float(extractedDF['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€')), \
                    float(extractedDF['1.1.- 27.4. AND 5.10. - 31.12.'][i].lstrip('€'))]
        transformedDF.loc[i] = rowToAdd

    return transformedDF


def yachts(extractedDF):

    print(f'I am in pk.yachts\n')

    # extractedDF = kuf.yachts()

    transformedDF = pd.DataFrame(columns=schemas.YACHTS_SCHEMA)

    # DEALING WITH DUPLICATE COLUMNS
    temp = list(extractedDF.columns)
    listOfColumnNames = set()
    for j in range(len(extractedDF.columns)):
        item = extractedDF.columns[j]
        if item in listOfColumnNames:
            temp[j] = str(item + '_2')
            # extractedDF = extractedDF.rename(columns={item : str(item + '_' + str(j))})
        else:
            listOfColumnNames.add(item)
    extractedDF.columns = temp

    for i in range(extractedDF.shape[0]):
        rowToAdd = ['Kufner', extractedDF['MODEL'][i], extractedDF['NAME'][i], \
                    int(extractedDF['CABINS'][i].split('+')[0]), \
                    c.Calc.evaluate(extractedDF['BERTHS_2'][i]), \
                    c.Calc.evaluate(extractedDF['TOILETS/SHOWERS'][i]), \
                    float(extractedDF['LOA'][i].replace(',','.').rstrip('m ')), \
                    float(extractedDF['MAX BEAM'][i].replace(',','.').rstrip('m ')), \
                    float(extractedDF['DRAFT'][i].replace(',','.').rstrip('m ')), \
                    float(extractedDF['MAIN SAIL'][i].split(' ')[0].rstrip('m2'))
                          +float(extractedDF['GENOVA SAIL'][i].split(' ')[0].rstrip('m2')), \
                    extractedDF['ENGINE'][i], \
                    int(extractedDF['WATER CAPACITY(lt)'][i].rstrip('l ')), \
                    int(extractedDF['FUEL CAPACITY(lt)'][i].rstrip('l ')), \
                    extractedDF['LOCATION'][i], \
                    extractedDF['yacht URL'][i], \
                    ]
        transformedDF.loc[i] = rowToAdd

    return transformedDF
