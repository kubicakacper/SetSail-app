import pymysql

from query import readFromAWS_RDS as readRDS
from extract import FreeWave as eFW, Kufner as eK
from transform import prepareFreeWave as pFW, prepareKufner as pK, mergeData as mD
from load import loadToAWS_RDS
from load import connCredentials as cC


# extract:
importedYachtsFW = eFW.yachts()
importedYachtsKuf = eK.yachts()
imported_pricelist_fw = eFW.pricelist()
imported_pricelist_kuf = eK.pricelist()

# transform 1:
preparedYachtsFW = pFW.yachts(importedYachtsFW)
preparedYachtsKuf = pK.yachts(importedYachtsKuf)
preparedPricelistFW = pFW.pricelist(imported_pricelist_fw)
preparedPricelistKuf = pK.pricelist(imported_pricelist_kuf)

# transform 2:
mergedData = mD.merge_data(preparedPricelistFW, preparedPricelistKuf, preparedYachtsFW, preparedYachtsKuf)

# query
db_conn = pymysql.connect(host=cC.ENDPOINT, user=cC.MASTER_USERNAME, password=cC.PASSWORD)

try:
    with db_conn.cursor() as cursor:

        cursor.execute("USE testDB;")

        df_from_rds = readRDS.query_yacht_table_and_read_to_data_frame(cursor)
        difference_df = df_from_rds.compare(mergedData)
        # load
        if not difference_df.empty:
            loadToAWS_RDS.truncate_yachts_table(cursor)
            loadToAWS_RDS.populate_yachts_table(cursor, mergedData.values)

        # test
        print(readRDS.query_yacht_table_and_read_to_data_frame(cursor))

finally:
    db_conn.commit()
    db_conn.close()
