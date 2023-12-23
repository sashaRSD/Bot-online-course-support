from dir_google.google_sheets import get_lessons_inf
from datetime import datetime


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


async def match_datatime(lessons_date, lessons_time):
    len_elements = range(0, len(lessons_date)+1)
    for i in zip(len_elements, lessons_date, lessons_time):
        if datetime.strptime(f"{i[1]} {i[2]}", '%d.%m.%Y %H:%M МСК') > datetime.now():
            return i[0]
    return -1