import pymysql

from extract import FreeWave as efw, Kufner as ek
from transform import prepareFreeWave as pfw, prepareKufner as pk, mergeData as md
from load import loadToAWS_RDS as load
from load import connCredentials as cc



if __name__ == '__main__':

#extract:
    importedYachtsFW = efw.yachts()
    importedYachtsKuf = ek.yachts()
    importedPricelistFW = efw.pricelist()
    importedPricelistKuf = ek.pricelist()

#transform 1:
    preparedYachtsFW = pfw.yachts(importedYachtsFW)
    preparedYachtsKuf = pk.yachts(importedYachtsKuf)
    preparedPricelistFW = pfw.pricelist(importedPricelistFW)
    preparedPricelistKuf = pk.pricelist(importedPricelistKuf)

#transform 2:
    mergedData = md.mergeData(preparedPricelistFW, preparedPricelistKuf, preparedYachtsFW, preparedYachtsKuf)

    # schemaOfYachts = tuple(mergedData.columns.values)
    yachtsTable_listOfLists = mergedData.values  # it is a list of lists

# load:
    db_conn = pymysql.connect(host=cc.ENDPOINT, user=cc.MASTER_USERNAME, password=cc.PASSWORD)

    try:
        with db_conn.cursor() as cursor:

            cursor.execute("USE testDB;")
            load.createYachtsTable(cursor)
            load.populateYachtsTable(cursor, yachtsTable_listOfLists)
            load.queryYachtsTable(cursor)

    finally:
        db_conn.commit()
        db_conn.close()