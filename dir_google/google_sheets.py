import gspread
from datetime import datetime

gs = gspread.service_account(filename='google_api.json')
sh = gs.open_by_key('1iGTjX-dLFe60cE5i6Asoplk3gahohvfeZrpEGovfjvM')
worksheet1 = sh.sheet1
worksheet2 = sh.get_worksheet(1)
worksheet3 = sh.get_worksheet(2)
worksheet4 = sh.get_worksheet(3)


async def get_lessons_inf(title):
    information = []
    if title == 'date':
        information = worksheet1.col_values(1)
    elif title == 'time':
        information = worksheet1.col_values(2)
    elif title == 'name':
        information = worksheet1.col_values(3)
    information.pop(0)
    return information


async def match_datatime(lessons_date, lessons_time):
    len_elements = range(0, len(lessons_date)+1)
    for i in zip(len_elements, lessons_date, lessons_time):
        if datetime.strptime(f"{i[1]} {i[2]}", '%d.%m.%Y %H:%M МСК') > datetime.now():
            return i[0]
    return -1


async def get_schedule():
    lessons_name = list(filter(None, await get_lessons_inf('name')))
    lessons_time = list(filter(None, await get_lessons_inf('time')))
    lessons_date = [date for date in await get_lessons_inf('date') if 'Модуль' not in date]
    if len(lessons_name) == len(lessons_time) == len(lessons_date):
        last_lesson = await match_datatime(lessons_date, lessons_time)
        if last_lesson != -1:
            schedule = [" <b>Расписание занятий:"]
            for i in zip(lessons_date[last_lesson:], lessons_time[last_lesson:], lessons_name[last_lesson:]):
                schedule.append(f'⏰ {i[0]} в {i[1]}\n📚 {i[2][i[2].find(".")+1:]}')
            schedule.append('</b>')
            return ['\n\n'.join(schedule)]
        else:
            return 'Занятия закончились 😉'
    else:
        return 'Ошибка базы данных! \nОбратитесь к администратору '


async def get_lessons():
    all_table = worksheet1.get_all_values()
    all_table.pop(0)
    lessons_module = await get_lessons_inf('date')
    index_lessons_module = [i for i, i_module in enumerate(lessons_module, 0) if 'Модуль' in i_module]
    index_lessons_module.append(len(lessons_module))
    lessons_information = ['<b>🗂 Информация о занятиях </b>']
    for i_module, module in enumerate(index_lessons_module[:len(index_lessons_module)-1], 0):
        module_lessons_information = [f'<b>{lessons_module[module]}</b>\n']
        for i_lesson in range(module+1, index_lessons_module[i_module+1]):
            module_lessons_information.append(f'📒<b>{all_table[i_lesson][2][all_table[i_lesson][2].find(".")+1:]}</b>\n'
                                              f'<i>Цель: {all_table[i_lesson][3]}\n'
                                              f'Описание: {all_table[i_lesson][4]}\n'
                                              f'Материалы: {all_table[i_lesson][5]}</i>\n')
        lessons_information.append('\n'.join(module_lessons_information))
    return lessons_information


async def get_homeworks():
    all_table = worksheet2.get_all_values()
    all_table.pop(0)
    homeworks_information = ['<b>🏠 Информация о домашних занятиях </b>']
    for i_homework in all_table:
        homeworks_information.append(f'📗 <b>{i_homework[1]}</b>\n\n'
                                              f'<i>Описание: {i_homework[2]}\n\n'
                                              f'Критерии оценивания: {i_homework[3]}</i>')

    return homeworks_information


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
    return 'Ой, а вас нет в ведомости ДЗ. Обратитесь к администратору...'


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
