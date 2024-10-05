from dir_google.google_sheets import get_data_sheet, worksheet1


async def get_lesson_data(index_lesson):
    return worksheet1.row_values(index_lesson)
