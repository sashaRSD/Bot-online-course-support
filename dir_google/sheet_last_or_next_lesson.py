from dir_google.google_sheets import get_data_sheet, worksheet1


async def get_lessons_inf():
    lessons_name_all = await get_data_sheet('name')
    lessons_name = list(filter(None, lessons_name_all))
    lessons_date = [date for date in await get_data_sheet('date') if 'Модуль' not in date]
    lessons_time = list(filter(None, await get_data_sheet('time')))
    return [lessons_name, lessons_date, lessons_time, lessons_name_all]


async def get_lesson_data(num_lesson):
    row_lesson = worksheet1.row_values(num_lesson)
    return row_lesson
