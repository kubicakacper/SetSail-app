from load import connCredentials as cc

from transform import mergeData as md
import pymysql
import pandas as pd

def createYachtsDB(cursor):
    cursor.execute("CREATE DATABASE yachtsDB;")

# name,charterer,model,cabins,max_pax,toilets,length,beam,draft,sail_area,engine,water_tank,fuel_tank,location,URL,year_of_built,march,april,may,june,july,august,september,october,november

def createYachtsTable(cursor):
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


def populateYachtsTable(cursor, yachtsTable_listOfLists):
    for rowAsList in yachtsTable_listOfLists:
        # remove NaNs, cause MySQL doesn't accept it:
        for i, cell in enumerate(rowAsList):
            if pd.isna(cell):
                rowAsList[i] = float(-1)
        rowTuple = list(rowAsList)
        sql = '''insert into Yachts values( \
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \
        )'''
        cursor.execute(sql, rowTuple) # row should be a tuple of 25 elements

def queryTestTable(cursor):
    sql = '''select * from testTable'''
    cursor.execute(sql)
    desc = cursor.description
    print(f'{desc[0][0]:<8} {desc[1][0]:<8}')
    rows = cursor.fetchall()
    for row in rows:
        print(f'{row[0]:<8} {row[1]:<8}')

def queryYachtsTable(cursor):
    sql = '''select * from Yachts'''
    cursor.execute(sql)
    desc = cursor.description
    # headersAsString - create a loop to build a string of {desc[0][0]:<8} {desc[1][0]:<8}....
    str_ = ''
    for column in range(25):
        str_ = str_ + desc[column][0] + ' '
    # print(f'{str_}\n\n')
    # # print(f'{desc[0][0]:<8} {desc[1][0]:<8} {desc[2][0]:<8} {desc[3][0]:<8} {desc[4][0]:<8} ' \
    # # f'{desc[5][0]:<8} {desc[6][0]:<8} {desc[7][0]:<8} {desc[8][0]:<8} {desc[9][0]:<8} ' \
    # # f'{desc[10][0]:<8} {desc[11][0]:<8} {desc[12][0]:<8} {desc[13][0]:<8} {desc[14][0]:<8} ' \
    # # f'{desc[15][0]:<8} {desc[16][0]:<8} {desc[17][0]:<8} {desc[18][0]:<8} {desc[19][0]:<8} ' \
    # # f'{desc[20][0]:<8} {desc[21][0]:<8} {desc[22][0]:<8} {desc[23][0]:<8} {desc[24][0]:<8}')
    str_ = ''
    rows = cursor.fetchall()
    for row in rows:
        for column in range(25):
            str_ = str_ + str(row[column]) + ' '
        print(f'{str_}\n')
        str_ = ''
    # print(f'{desc}\n\n{rows}')

def queryYachtTableAndReadToDataFrame(cursor):
    sql = '''select * from Yachts'''
    cursor.execute(sql)

    header = []
    desc = cursor.description
    for column in range(25):
        header.append(desc[column][0])

    data = []
    rows = cursor.fetchall()
    for row in rows:
        rowAsList = []
        for column in range(25):
            rowAsList.append(row[column])
        data.append(rowAsList)
    return pd.DataFrame(data, columns=header)

def dropTestTable(cursor):
    sql = '''drop table if exists testTable;'''
    cursor.execute(sql)

def dropYachtsTable(cursor):
    sql = '''drop table if exists Yachts;'''
    cursor.execute(sql)


