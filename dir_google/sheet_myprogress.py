from dir_google.google_sheets import worksheet3


async def get_progress(my_username, my_id):
    username_students = worksheet3.col_values(1)
    for i_student, student in enumerate(username_students, 0):
        if f'@{my_username}' in student or f'id{my_id}' in student:
            all_table = worksheet3.get_all_values()
            progress_information = ['<b>📈 Статистика ваших дз: </b>\n\n']
            for num_homework in range(1, len(all_table[0])):
                mark_homework = all_table[i_student][num_homework]
                if mark_homework:
                    mark_homework = int(mark_homework)
                else:
                    mark_homework = 0
                if mark_homework > 0:
                    progress_information.append('✅')
                else:
                    progress_information.append('❌')
                progress_information.append(f' {all_table[0][num_homework]}: {abs(mark_homework)}/10\n')
            return [' '.join(progress_information)]
    return ['Ой, а вас нет в ведомости ДЗ. Обратитесь к администратору...']
