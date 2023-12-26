from dir_google.google_sheets import get_lessons_inf, worksheet1


async def get_module_lesson():
    lessons_module = await get_lessons_inf('date')
    return [module for module in lessons_module if 'Модуль' in module]


async def get_lesson_name(name_module):
    name_lessons = await get_lessons_inf('name')
    lessons_module = await get_lessons_inf('date')
    index_lessons_module = [[i, module] for i, module in enumerate(lessons_module, 0) if 'Модуль' in module]
    index_lessons_module.append([len(lessons_module), ''])

    index_lesson_name = [i for i, module in enumerate(index_lessons_module, 0) if module[1] == name_module][0]
    index_start = index_lessons_module[index_lesson_name][0]
    index_stop = index_lessons_module[index_lesson_name+1][0]
    lessons_information = []
    for i_lesson in range(int(index_start)+1, int(index_stop)):
        lessons_information.append(name_lessons[i_lesson][name_lessons[i_lesson].find(".")+1:])
    return lessons_information


async def get_lesson(name_lesson):
    name_lessons = await get_lessons_inf('name')
    index_lesson = [i for i, name in enumerate(name_lessons, 2) if name_lesson in name][0]
    row_lesson = worksheet1.row_values(index_lesson)
    return (f'<b>{name_lesson}</b>\n\n'
            f'<i>Цель: {row_lesson[3]}\n'
            f'Описание: {row_lesson[4]}\n'
            f'Материалы: {row_lesson[5]}</i>\n')
