from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_google.sheet_myprogress import get_col_authority, get_col_student
from dir_google.sheet_lessons import get_lessons_datatime
from dir_google.google_sheets import get_modules_index
from dir_bot.create_bot import bot
from datetime import datetime


async def menu(username, call_menu_user_id, message_id=0):
    authority_tmp = await authority_student(username, call_menu_user_id)
    if authority_tmp:
        button_menu = InlineKeyboardMarkup()
        i_lesson = await button_lesson_index(authority_tmp)
        if i_lesson[1] != -1:
            button_menu.add(InlineKeyboardButton(text='Следующий урок.', callback_data=f'lesson_index_{i_lesson[1]}'))
        if i_lesson[0] != -1:
            button_menu.add(InlineKeyboardButton(text='Предыдущий урок.', callback_data=f'lesson_index_{i_lesson[0]}'))
        button_menu.add(InlineKeyboardButton(text='Получить расписание занятий.', callback_data='schedule'))
        button_menu.add(InlineKeyboardButton(text='Получить информацию о занятиях.', callback_data='lessons'))
        button_menu.add(InlineKeyboardButton(text='Получить информацию о домашних заданиях.', callback_data='homeworks'))
        button_menu.add(InlineKeyboardButton(text='Получить статус выполнения домашних заданий.', callback_data='myprogress'))
        button_menu.add(InlineKeyboardButton(text='Поставить отзыв о занятии.', callback_data='feedback'))
        if authority_tmp == -1:
            button_menu.add(InlineKeyboardButton(text='Перейти к материалам.',
                                                 url='https://disk.yandex.ru/d/355CI_7ELLCBsQ'))

        if message_id:
            await bot.edit_message_text(chat_id=call_menu_user_id, message_id=message_id,
                                        text='Пожалуйста, укажите что вас интересует:', reply_markup=button_menu)
        else:
            await bot.send_message(call_menu_user_id, 'Пожалуйста, укажите что вас интересует:', reply_markup=button_menu)


async def authority_student(my_username, my_id):
    num_student = await get_num_student(my_username, my_id)
    if num_student != -1:
        authority = await get_col_authority()
        # if 460325052 == my_id:
        #     return -1
        if len(authority)-1 >= num_student and authority[num_student]:
            return authority[num_student].split(" ")
        else:
            return -1
    else:
        await bot.send_message(my_id, '❗❗❗\n'
                                      'Ой, а вас нет в ведомости. \n'
                                      'Обратитесь к администратору...')
        return 0


async def get_num_student(my_username, my_id):
    username_students = await get_col_student()
    for i_student, student in enumerate(username_students, 0):
        if my_username in student or f"{my_id}" in student:
            return i_student
    return -1


async def google_api_error(user_id_error):
    await bot.send_message(user_id_error, 'Сервер перегружен! \n'
                                          'Повторите попытку, через минуту 😉\n\n'
                                          'Напишите администратору, если ошибка не уходит!')


async def button_lesson_index(authority):
    i_mass_authority_lesson = []
    all_modules_index = await get_modules_index()
    for i_module in range(len(all_modules_index)-1):
        if authority == -1 or str(i_module+1) in authority:
            for i_lesson in range(all_modules_index[i_module]+1, all_modules_index[i_module+1]):
                i_lesson_global = i_lesson + 2
                i_mass_authority_lesson.append(i_lesson_global)
    lessons_datatime = await get_lessons_datatime(i_mass_authority_lesson)
    index_lesson_authority = await match_datatime(lessons_datatime[0], lessons_datatime[1])
    if index_lesson_authority == -1:
        i_last_lesson_global = i_mass_authority_lesson[-1]
        i_next_lesson_global = -1
    elif index_lesson_authority == 0:
        i_last_lesson_global = -1
        i_next_lesson_global = i_mass_authority_lesson[0]
    else:
        i_last_lesson_global = i_mass_authority_lesson[index_lesson_authority-1]
        i_next_lesson_global = i_mass_authority_lesson[index_lesson_authority]
    return [i_last_lesson_global, i_next_lesson_global]


async def match_datatime(lessons_date, lessons_time):
    len_elements = range(0, len(lessons_date)+1)
    for i in zip(len_elements, lessons_date, lessons_time):
        if datetime.strptime(f"{i[1]} {i[2]}", '%d.%m.%Y %H:%M МСК') > datetime.now():
            return i[0]
    return -1
