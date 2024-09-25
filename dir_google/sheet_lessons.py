from dir_google.google_sheets import get_data_sheet, worksheet1, get_module_inf, get_module_name


async def get_lesson_data(name_lesson):
    all_name_lessons = await get_data_sheet('name')
    index_lesson = [i for i, name in enumerate(all_name_lessons, 2) if name_lesson in name][0]
    row_lesson = worksheet1.row_values(index_lesson)
    return row_lesson
