from transform import Calc as c
import pandas as pd
from extract import FreeWave as fw
from transform import schemas

def pricelist():

    extractedDF = fw.pricelist()

    transformedDF = pd.DataFrame(columns=schemas.PRICELIST_SCHEMA)
    model_column = []
    name_column = []

    for row in extractedDF['Segelyachten']:
        model, name = str(row).split(' ‚')
        model_column.append(model)
        name_column.append(name.rstrip('‘'))

    for i in range(len(model_column)):
        rowToAdd = [model_column[i], name_column[i], int(extractedDF['Baujahr'][i+1]), \
                    c.Calc.evaluate(extractedDF['Kojen'][i+1]), \
                    1000*float(extractedDF['19.03. 09.04.'][i+1]), 1000*float(extractedDF['09.04. 30.04.'][i+1]), \
                    1000*float(extractedDF['14.05. 28.05.'][i+1]), 1000*float(extractedDF['11.06. 25.06.'][i+1]), \
                    1000*float(extractedDF['09.07. 23.07.'][i+1]), 1000*float(extractedDF['13.08. 27.08.'][i+1]), \
                    1000*float(extractedDF['10.09. 24.09.'][i+1]), 1000*float(extractedDF['08.10. 22.10.'][i+1]), \
                    1000*float(extractedDF['22.10. 05.11.'][i+1])]
        transformedDF.loc[i] = rowToAdd

    return transformedDF


def yachts():

    extractedDF = fw.yachts()

    transformedDF = pd.DataFrame(columns=schemas.YACHTS_SCHEMA)

    model_column = []
    name_column = []

    for row in extractedDF['NAME']:
        model, name = str(row).replace(' „',' ‚').replace(' “',' ‚').split(' ‚')
        model_column.append(model)
        name_column.append(name.rstrip('‘,“”'))

    for i in range(len(model_column)):
        rowToAdd = [model_column[i], name_column[i], int(extractedDF['Cabins:'][i].split('+')[0]), \
                    c.Calc.evaluate(extractedDF['Berths:'][i]), \
                    c.Calc.evaluate(extractedDF['Toilets:'][i]), \
                    float(extractedDF['LOA = Overall length (m):'][i].replace(',','.')), \
                    float(extractedDF['Max. beam (m):'][i].replace(',','.')), \
                    float(extractedDF['Draft (m):'][i].replace(',','.')), \
                    float(extractedDF['Canvas size(m2):'][i].replace(',','.')) \
                         if extractedDF['Canvas size(m2):'][i] != 'Unknown' else float('nan'), \
                    extractedDF['Engine:'][i], \
                    int(extractedDF['Water tank (l):'][i]), \
                    int(extractedDF['Fuel tank (l):'][i]), \
                    extractedDF['Location'][i], \
                    extractedDF['yacht URL'][i], \
                    ]
        transformedDF.loc[i] = rowToAdd

    return transformedDF


print(pricelist())