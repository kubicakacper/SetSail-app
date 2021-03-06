from pyspark.sql import SparkSession
import pymysql

from query import readFromAWS_RDS as readRDS
from load import connCredentials as cC

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .config("spark.executor.memory", "4gb") \
    .appName("Set Sail") \
    .getOrCreate()

db_conn = pymysql.connect(host=cC.ENDPOINT, user=cC.MASTER_USERNAME, password=cC.PASSWORD)

try:
    with db_conn.cursor() as cursor:

        cursor.execute("USE testDB;")

# search
        yachtsDF = spark.createDataFrame(readRDS.query_yacht_table_and_read_to_data_frame(cursor))
        yachtsDF\
            .filter(yachtsDF.cabins >= 4)\
            .filter(yachtsDF.year_of_built >= 2015)\
            .filter(yachtsDF.september <= 4000)\
            .sort(yachtsDF.september)\
            .select("model", "cabins", "max_pax", "location", "year_of_built", "september")\
            .withColumnRenamed("september", "price")\
            .show(truncate=False)

finally:
    db_conn.commit()
    db_conn.close()
