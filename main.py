if __name__ == '__main__':

    # from transform import mergeData as md
    # FULL_SCHEMA = md.mergeData().columns.values.tolist()
    # print(FULL_SCHEMA)
    from transform import mergeData as md
    yachtsTable = md.mergeData()
    print(yachtsTable)
    print('\n\n')
    print(yachtsTable.values)
