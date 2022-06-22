import pandas as pd

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


# def queryYachtsTableAndPrint(cursor):
#     sql = '''select * from Yachts'''
#     cursor.execute(sql)
#
#     header = []
#     desc = cursor.description
#     for column in range(25):
#         header.append(desc[column][0])
#     # headersAsString - create a loop to build a string of {desc[0][0]:<8} {desc[1][0]:<8}....
#     str_ = ''
#     for column in range(25):
#         str_ = str_ + desc[column][0] + ' '
#     # print(f'{str_}\n\n')
#     # # print(f'{desc[0][0]:<8} {desc[1][0]:<8} {desc[2][0]:<8} {desc[3][0]:<8} {desc[4][0]:<8} ' \
#     # # f'{desc[5][0]:<8} {desc[6][0]:<8} {desc[7][0]:<8} {desc[8][0]:<8} {desc[9][0]:<8} ' \
#     # # f'{desc[10][0]:<8} {desc[11][0]:<8} {desc[12][0]:<8} {desc[13][0]:<8} {desc[14][0]:<8} ' \
#     # # f'{desc[15][0]:<8} {desc[16][0]:<8} {desc[17][0]:<8} {desc[18][0]:<8} {desc[19][0]:<8} ' \
#     # # f'{desc[20][0]:<8} {desc[21][0]:<8} {desc[22][0]:<8} {desc[23][0]:<8} {desc[24][0]:<8}')
#     str_ = ''
#     rows = cursor.fetchall()
#     for row in rows:
#         for column in range(25):
#             str_ = str_ + str(row[column]) + ' '
#         print(f'{str_}\n')
#         str_ = ''
