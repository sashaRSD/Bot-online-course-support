from dir_google.google_sheets import worksheet2


async def get_homeworks():
    all_table = worksheet2.get_all_values()
    all_table.pop(0)
    homeworks_information = ['<b>🏠 Информация о домашних занятиях </b>']
    for i_homework in all_table:
        homeworks_information.append(f'📗 <b>{i_homework[1]}</b>\n\n'
                                     f'<i>Описание: {i_homework[2]}\n\n'
                                     f'Критерии оценивания: {i_homework[3]}</i>')

    return homeworks_information
