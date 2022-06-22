from pyspark.sql import SparkSession
import pymysql

from query import readFromAWS_RDS as readRDS
from load import connCredentials as cc

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .config("spark.executor.memory", "4gb") \
    .appName("Set Sail") \
    .getOrCreate()

db_conn = pymysql.connect(host=cc.ENDPOINT, user=cc.MASTER_USERNAME, password=cc.PASSWORD)

try:
    with db_conn.cursor() as cursor:

        cursor.execute("USE testDB;")

# search
        yachtsDF = spark.createDataFrame(readRDS.queryYachtTableAndReadToDataFrame(cursor))
        yachtsDF\
            .filter(yachtsDF.cabins >= 4)\
            .filter(yachtsDF.year_of_built >= 2015)\
            .filter(yachtsDF.september <= 4000)\
            .show(truncate=False)

finally:
    db_conn.commit()
    db_conn.close()


