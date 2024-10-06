from dir_google.google_sheets import worksheet1, get_data_sheet


async def get_lesson_data(index_lesson):
    return worksheet1.row_values(index_lesson)


async def get_lessons_datatime(index_authority_lesson):
    lessons_date = await get_data_sheet('date')
    authority_lessons_date = [date for i, date in enumerate(lessons_date, 2) if i in index_authority_lesson]
    lessons_time = await get_data_sheet('time')
    authority_lessons_time = [time for i, time in enumerate(lessons_time, 2) if i in index_authority_lesson]
    return [authority_lessons_date, authority_lessons_time]
