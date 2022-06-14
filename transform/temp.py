from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType

from extract import FreeWave as extractFW
from extract import Kufner as extractKuf
from transform import schemas

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .config("spark.executor.memory", "4gb") \
    .appName("Set Sail") \
    .getOrCreate()

# DEALING WITH PRICELISTS
#
# fwPricelist = spark.createDataFrame(extractFW.pricelist())
#
# fwPricelist.show()
#
# kufPricelist = spark.createDataFrame(extractKuf.pricelist())
#
# kufPricelist.show()

# SCHEMA FOR PRICELIST: MODEL, NAME, YEAR_OF_BUILT, MAX_PAX, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER

# schema = StructType([ \
#     StructField("model", StringType(), True), \
#     StructField("name", StringType(), True), \
#     StructField("year_of_build", StringType(), True), \
#     StructField("max_pax", StringType(), True), \
#     StructField("march", FloatType(), True), \
#     StructField("april", FloatType(), True), \
#     StructField("may", FloatType(), True), \
#     StructField("june", FloatType(), True), \
#     StructField("july", FloatType(), True), \
#     StructField("august", FloatType(), True), \
#     StructField("september", FloatType(), True), \
#     StructField("october", FloatType(), True), \
#     StructField("november", FloatType(), True) \
#     ])


schema = StructType([ \
    StructField(schemas.PRICELIST_SCHEMA[0], StringType(), True), \
    StructField(schemas.PRICELIST_SCHEMA[1], StringType(), True), \
    StructField(schemas.PRICELIST_SCHEMA[2], StringType(), True), \
    StructField(schemas.PRICELIST_SCHEMA[3], StringType(), True), \
    StructField("march", FloatType(), True), \
    StructField("april", FloatType(), True), \
    StructField("may", FloatType(), True), \
    StructField("june", FloatType(), True), \
    StructField("july", FloatType(), True), \
    StructField("august", FloatType(), True), \
    StructField("september", FloatType(), True), \
    StructField("october", FloatType(), True), \
    StructField("november", FloatType(), True) \
    ])

print(schema)

# data = data prepared to ingest to spark.DataFrame => then prepare functions for search anything needed
# SparkSession.createDataFrame(data, schema=None, samplingRatio=None, verifySchema=True)
# Creates a DataFrame from an RDD, a list or a pandas.DataFrame.
# df = spark.createDataFrame(data=data,schema=schema)

# then yachts