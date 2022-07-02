import pandas as pd


def create_yachts_db(cursor):
    cursor.execute("CREATE DATABASE yachtsDB;")


def create_yachts_table(cursor):
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


def populate_yachts_table(cursor, yachts_table_list_of_lists):
    for rowAsList in yachts_table_list_of_lists:
        # remove NaNs, cause MySQL doesn't accept it:
        for i, cell in enumerate(rowAsList):
            if pd.isna(cell):
                rowAsList[i] = float(-1)
        row_tuple = list(rowAsList)
        sql = '''insert into Yachts values( \
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \
        )'''
        cursor.execute(sql, row_tuple)  # row should be a tuple of 25 elements


def truncate_yachts_table(cursor):
    sql = '''
    truncate table Yachts;
    '''
    cursor.execute(sql)


def drop_yachts_table(cursor):
    sql = '''drop table if exists Yachts;'''
    cursor.execute(sql)
