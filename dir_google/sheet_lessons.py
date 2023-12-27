from dir_google.google_sheets import get_lessons_inf, worksheet1


async def get_module_lesson():
    lessons_module = await get_lessons_inf('date')
    return [module for module in lessons_module if 'Модуль' in module]


async def get_lesson_name(index_module):
    name_lessons = await get_lessons_inf('name')
    name_module = await get_lessons_inf('date')
    index_lessons_module = [i for i, module in enumerate(name_module, 0) if 'Модуль' in module]
    index_lessons_module.append(len(name_module))

    lessons_name = []
    for i_lesson in range(index_lessons_module[index_module] + 1, index_lessons_module[index_module+1]):
        lessons_name.append(name_lessons[i_lesson][name_lessons[i_lesson].find(".")+1:])
    return [lessons_name, name_module[index_lessons_module[index_module]]]


async def get_lesson(name_lesson):
    name_lessons = await get_lessons_inf('name')
    index_lesson = [i for i, name in enumerate(name_lessons, 2) if name_lesson in name][0]
    row_lesson = worksheet1.row_values(index_lesson)
    return (f'<b>📒 {name_lesson}</b>\n\n'
            f'<i>Цель: {row_lesson[3]}\n\n'
            f'Описание: {row_lesson[4]}\n\n'
            f'Материалы: {row_lesson[5]}</i>\n')
