import pandas as pd


def query_yacht_table_and_read_to_data_frame(cursor):
    sql = '''select * from Yachts'''
    cursor.execute(sql)

    header = []
    desc = cursor.description
    for column in range(25):
        header.append(desc[column][0])

    data = []
    rows = cursor.fetchall()
    for row in rows:
        row_as_list = []
        for column in range(25):
            row_as_list.append(row[column])
        data.append(row_as_list)
    return pd.DataFrame(data, columns=header)
