from dir_google.google_sheets import worksheet3


async def get_num_student(my_username, my_id):
    username_students = worksheet3.col_values(1)
    for i_student, student in enumerate(username_students, 0):
        if f'@{my_username}' in student or f'id{my_id}' in student:
            return i_student
    return -1


async def get_table_progress():
    return worksheet3.get_all_values()


async def get_authority():
    return worksheet3.col_values(2)
