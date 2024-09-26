from dir_google.google_sheets import worksheet2


async def get_name_homeworks():
    name_homeworks = worksheet2.col_values(2)
    name_homeworks.pop(0)
    return name_homeworks


async def get_num_homeworks():
    num_homeworks = worksheet2.col_values(7)
    num_homeworks.pop(0)
    return num_homeworks


async def get_homeworks(row):
    return worksheet2.row_values(row)


async def get_date_homeworks():
    date_homeworks = worksheet2.col_values(6)
    date_homeworks.pop(0)
    return date_homeworks
