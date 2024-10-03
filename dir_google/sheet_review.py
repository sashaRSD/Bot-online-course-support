from dir_google.google_sheets import get_data_sheet, worksheet4


async def get_lessons_support():
    lessons_name = list(filter(None, await get_data_sheet('name')))
    lessons_date = [date for date in await get_data_sheet('date') if 'Модуль' not in date]
    lessons_time = list(filter(None, await get_data_sheet('time')))
    return [lessons_name, lessons_date, lessons_time]


async def send_lessons_support(student, lesson, mark, message):
    worksheet4.insert_row([student, lesson, mark, message], 2)
    return True
