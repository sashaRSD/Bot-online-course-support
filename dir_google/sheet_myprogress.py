from dir_google.google_sheets import worksheet3


async def get_col_student():
    col_students = worksheet3.col_values(1)
    return col_students


async def get_col_authority():
    return worksheet3.col_values(2)


async def get_table_progress():
    return worksheet3.get_all_values()

