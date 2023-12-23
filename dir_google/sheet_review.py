from dir_google.google_sheets import get_lessons_inf, worksheet4


async def get_lessons_support():
    lessons_name = list(filter(None, await get_lessons_inf('name')))
    lessons_date = [date for date in await get_lessons_inf('date') if 'Модуль' not in date]
    if len(lessons_name) == len(lessons_date):
        lessons_support = []
        for i in zip(lessons_name, lessons_date):
            lessons_support.append(f'{i[0]} ({i[1]})')
        return lessons_support
    else:
        return 'Ошибка базы данных! \nОбратитесь к администратору '


async def send_lessons_support(student, lesson, mark, message):
    worksheet4.insert_row([student, lesson, mark, message], 2)
    return True