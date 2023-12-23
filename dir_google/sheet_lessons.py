from dir_google.google_sheets import get_lessons_inf, worksheet1

async def get_lessons():
    all_table = worksheet1.get_all_values()
    all_table.pop(0)
    lessons_module = await get_lessons_inf('date')
    index_lessons_module = [i for i, i_module in enumerate(lessons_module, 0) if 'Модуль' in i_module]
    index_lessons_module.append(len(lessons_module))
    lessons_information = ['<b>🗂 Информация о занятиях </b>']
    for i_module, module in enumerate(index_lessons_module[:len(index_lessons_module)-1], 0):
        module_lessons_information = [f'<b>{lessons_module[module]}</b>\n']
        for i_lesson in range(module+1, index_lessons_module[i_module+1]):
            module_lessons_information.append(f'📒<b>{all_table[i_lesson][2][all_table[i_lesson][2].find(".")+1:]}</b>\n'
                                              f'<i>Цель: {all_table[i_lesson][3]}\n'
                                              f'Описание: {all_table[i_lesson][4]}\n'
                                              f'Материалы: {all_table[i_lesson][5]}</i>\n')
        lessons_information.append('\n'.join(module_lessons_information))
    return lessons_information