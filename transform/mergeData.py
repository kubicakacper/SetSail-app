import pandas as pd
from transform import schemas


def merge_data(pricelist1, pricelist2, yachts1, yachts2):
    print(f'I am in md.merge_data\n')

    merged_pricelist = pd.DataFrame(columns=schemas.PRICELIST_SCHEMA)
    merged_pricelist = pd.concat([merged_pricelist, pricelist1], ignore_index=True, axis=0)
    merged_pricelist = pd.concat([merged_pricelist, pricelist2], ignore_index=True, axis=0)

    merged_yachts = pd.DataFrame(columns=schemas.YACHTS_SCHEMA)
    merged_yachts = pd.concat([merged_yachts, yachts1], ignore_index=True, axis=0)
    merged_yachts = pd.concat([merged_yachts, yachts2], ignore_index=True, axis=0)

    all_data_table = merged_yachts.set_index(['name', 'charterer']) \
        .join(merged_pricelist.set_index(['name', 'charterer']), rsuffix='_p', how='outer') \
        .sort_values(by=['name', 'charterer'])
    all_data_table = all_data_table.drop(['max_pax_p', 'model_p'], axis=1)
    all_data_table.reset_index(inplace=True)

    return all_data_table
