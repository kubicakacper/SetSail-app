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
                    URL VARCHAR(128), \
                    year_of_built INT, \
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

def truncateYachtsTable(cursor):
    sql = '''
    truncate table Yachts;
    '''
    cursor.execute(sql)

def dropYachtsTable(cursor):
    sql = '''drop table if exists Yachts;'''
    cursor.execute(sql)


