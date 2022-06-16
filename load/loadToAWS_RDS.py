master_username = 'kakubica'
password = 'Kr0wu1ec'
endpoint = 'setsail-app.cq6kprgd8h6c.eu-central-1.rds.amazonaws.com'

from transform import mergeData as md
import pymysql
import pandas as pd

def createTestDB():
    cursor.execute("CREATE DATABASE testDB;")

def createYachtsDB():
    cursor.execute("CREATE DATABASE yachtsDB;")

schemaOfYachts = tuple(md.mergeData().columns.values)
# print(f'{schemaOfYachts}')
yachtsTable_listOfLists = md.mergeData().values # it is a list of lists

def createTestTable():
    sql = '''drop table if exists testTable;'''
    cursor.execute(sql)
    sql = '''create table testTable( \
    raz VARCHAR(32), \
    dwa INT \
    );'''
    cursor.execute(sql)


# name,charterer,model,cabins,max_pax,toilets,length,beam,draft,sail_area,engine,water_tank,fuel_tank,location,URL,year_of_built,march,april,may,june,july,august,september,october,november

def createYachtsTable():
    sql = '''drop table if exists Yachts;'''
    cursor.execute(sql)
    sql = '''CREATE TABLE Yachts( \
                    name VARCHAR(32), \
                    charterer VARCHAR(32), \
                    model VARCHAR(32), \
                    cabins INT, \
                    max_pax INT, \
                    toilets INT, \
                    length FLOAT, \
                    beam FLOAT, \
                    draft FLOAT, \
                    sail_area FLOAT, \
                    engine VARCHAR(32), \
                    water_tank INT, \
                    fuel_tank INT, \
                    location VARCHAR(32), \
                    URL VARCHAR(32), \
                    year_of_built FLOAT, \
                    march FLOAT, \
                    april FLOAT, \
                    may FLOAT, \
                    june FLOAT, \
                    july FLOAT, \
                    august FLOAT, \
                    september FLOAT, \
                    october FLOAT, \
                    november FLOAT \
                    );'''
    cursor.execute(sql)


def populateTestTable():
    col1 = 'col1'
    col2 = 2
    sql = '''insert into testTable values(%s, %s)'''
    cursor.execute(sql, (col1, col2))

def populateYachtsTable():
    for rowAsList in yachtsTable_listOfLists:
        rowTuple = tuple(rowAsList)
        sql = '''insert into Yachts values( \
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \
        )'''
        cursor.execute(sql, rowTuple) # row should be a tuple of 25 elements

def queryTestTable():
    sql = '''select * from testTable'''
    cursor.execute(sql)
    desc = cursor.description
    print(f'{desc[0][0]:<8} {desc[1][0]:<8}')
    rows = cursor.fetchall()
    for row in rows:
        print(f'{row[0]:<8} {row[1]:<8}')

def queryYachtsTable():
    sql = '''select * from Yachts'''
    cursor.execute(sql)
    desc = cursor.description
    # headersAsString - create a loop to build a string of {desc[0][0]:<8} {desc[1][0]:<8}....
    # print(f'{desc[0][0]:<8} {desc[1][0]:<8}')
    rows = cursor.fetchall()
    # for row in rows:
    #     print(f'{row[0]:<8} {row[1]:<8}')
    print(f'{desc}\n{rows}')

def dropTestTable():
    sql = '''drop table if exists testTable;'''
    cursor.execute(sql)

def dropTestTable():
    sql = '''drop table if exists Yachts;'''
    cursor.execute(sql)

db_conn = pymysql.connect(host=endpoint, user=master_username, password=password)

try:
    with db_conn.cursor() as cursor:

# cursor.execute("select version()")
# data = cursor.fetchall()
# print(data)

        cursor.execute("USE testDB;")
        # createTestTable()
        # populateTestTable()
        # populateTestTable()
        # populateTestTable()
        # dropTestTable()
        # queryTestTable()
        # createYachtsTable()
        # populateYachtsTable()
        queryYachtsTable()

# cursor.execute(" \
# DROP TABLE IF EXISTS cities; \
# CREATE TABLE cities(id INT PRIMARY_KEY AUTO_INCREMENT, name VARCHAR(255), population INT); \
# INSERT INTO cities(name, population) VALUES('Bratislava', 432000); \
# INSERT INTO cities(name, population) VALUES('Budapest', 1759000); \
# INSERT INTO cities(name, population) VALUES('Prague', 1280000); \
# INSERT INTO cities(name, population) VALUES('Warsaw', 1748000); \
# INSERT INTO cities(name, population) VALUES('Los Angeles', 3971000); \
# INSERT INTO cities(name, population) VALUES('New York', 8550000); \
# INSERT INTO cities(name, population) VALUES('Edinburgh', 464000); \
# INSERT INTO cities(name, population) VALUES('Berlin', 3671000); \
# ")

# cursor.execute("CREATE TABLE Wines(fixed_acidity FLOAT, volatile_acidity FLOAT, \
#                    citric_acid FLOAT, residual_sugar FLOAT, chlorides FLOAT, \
#                    free_so2 FLOAT, total_so2 FLOAT, density FLOAT, pH FLOAT, \
#                    sulphates FLOAT, alcohol FLOAT, quality INT, is_red INT);")
#
# red_wines = pd.read_csv("winequality-red.csv", sep=";")
# red_wines["is_red"] = 1
# white_wines = pd.read_csv("winequality-white.csv", sep=";")
# white_wines["is_red"] = 0
# all_wines = pd.concat([red_wines, white_wines])
# all_wines

# ------------------------------------------------------------
#     string.join(iterable)
#
# text = ['Python', 'is', 'a', 'fun', 'programming', 'language']
#
# # join elements of text with space
# print(' '.join(text))
#
# # Output: Python is a fun programming language
# -------------------------------------------------------------

# wine_tuples = list(all_wines.itertuples(index=False, name=None))
# wine_tuples_string = ",".join(["(" + ",".join([str(w) for w in wt]) + ")" for wt in wine_tuples])
#
# cursor.execute("INSERT INTO Wines(fixed_acidity, volatile_acidity, citric_acid,\
#                    residual_sugar, chlorides, free_so2, total_so2, density, pH,\
#                    sulphates, alcohol, quality, is_red) VALUES " + wine_tuples_string + ";")
# cursor.execute("FLUSH TABLES;")
#
# cursor.connection.commit()

# disconnect from server

finally:
    db_conn.commit()
    db_conn.close()
