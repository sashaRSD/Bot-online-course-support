from dir_google.google_sheets import worksheet5


async def get_materials_link():
    key = worksheet5.col_values(1)
    value = worksheet5.col_values(2)
    for i in zip(key, value):
        if i[0] == 'materials_link':
            return i[1]
    return 0
