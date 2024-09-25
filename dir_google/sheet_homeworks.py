from dir_google.google_sheets import worksheet2


async def get_name_homeworks():
    name_homeworks = worksheet2.col_values(2)
    name_homeworks.pop(0)
    homeworks_information = []
    for i_homework in name_homeworks:
        homeworks_information.append(f'📗 {i_homework}')
    return homeworks_information


async def get_homeworks(row):
    row_homework = worksheet2.row_values(row)
    return (f'📗 <b>{row_homework[1]}</b>\n\n'
            f'<i>Дата: {row_homework[5]}\n\n'
            f'Описание: {row_homework[2]}\n\n'
            f'Критерии оценивания:\n {row_homework[3]}</i>')


async def get_date_homeworks():
    date_homeworks = worksheet2.col_values(6)
    date_homeworks.pop(0)
    homeworks_information = []
    for i_date in date_homeworks:
        homeworks_information.append(f'⏰ {i_date}')
    return homeworks_information
