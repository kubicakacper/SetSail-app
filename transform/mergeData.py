import pandas as pd
from transform import prepareFreeWave as fw
from transform import prepareKufner as kuf
from transform import schemas

def mergeData():

    mergedPricelist = pd.DataFrame(columns=schemas.PRICELIST_SCHEMA)
    mergedPricelist = pd.concat([mergedPricelist, kuf.pricelist()], ignore_index=True, axis=0)
    mergedPricelist = pd.concat([mergedPricelist, fw.pricelist()], ignore_index=True, axis=0)
    # print(f'{mergedPricelist}\n\n')

    mergedYachts = pd.DataFrame(columns=schemas.YACHTS_SCHEMA)
    mergedYachts = pd.concat([mergedYachts, kuf.yachts()], ignore_index=True, axis=0)
    mergedYachts = pd.concat([mergedYachts, fw.yachts()], ignore_index=True, axis=0)
    # print(f'{mergedYachts}\n\n')

    allDataTable = mergedYachts.set_index(['name', 'charterer']).join(mergedPricelist.set_index(['name', 'charterer']), rsuffix='_p', how='outer').sort_values(by=['name', 'charterer'])
    allDataTable = allDataTable.drop(['max_pax_p', 'model_p'], axis=1)
    allDataTable.reset_index(inplace=True)
    # print(allDataTable.columns)

    return allDataTable

# print(mergeData())