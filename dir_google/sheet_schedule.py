from dir_google.google_sheets import get_lessons_inf
from datetime import datetime


async def get_schedule(last_element=0):
    lessons_name = list(filter(None, await get_lessons_inf('name')))
    lessons_time = list(filter(None, await get_lessons_inf('time')))
    lessons_date = [date for date in await get_lessons_inf('date') if 'Модуль' not in date]
    if len(lessons_name) == len(lessons_time) == len(lessons_date):
        last_lesson = await match_datatime(lessons_date, lessons_time)
        if last_lesson != -1:
            schedule = [" <b>Расписание занятий:"]
            if last_element and (len(lessons_date)-last_lesson > last_element):
                last_element = last_lesson+last_element
            else:
                last_element = len(lessons_date)
            for elem in range(last_lesson, last_element):
                schedule.append(f'⏰ {lessons_date[elem]} в {lessons_time[elem]}\n'
                                f'📚 {lessons_name[elem][lessons_name[elem].find(".")+1:]}')
            schedule.append('</b>')
            return ['\n\n'.join(schedule),  len(schedule)-2]
        else:
            return ["Занятия закончились 😉", 0]
    else:
        return ['❗❗❗\n'
                'Ошибка базы данных!\n'
                'Обратитесь к администратору...', 0]


async def match_datatime(lessons_date, lessons_time):
    len_elements = range(0, len(lessons_date)+1)
    for i in zip(len_elements, lessons_date, lessons_time):
        if datetime.strptime(f"{i[1]} {i[2]}", '%d.%m.%Y %H:%M МСК') > datetime.now():
            return i[0]
    return -1
