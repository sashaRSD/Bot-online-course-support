from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_google.sheet_myprogress import get_col_authority, get_col_student
from dir_bot.create_bot import bot
from datetime import datetime


async def menu(username, call_menu_user_id, message_id=0):
    authority_tmp = await authority_student(username, call_menu_user_id)
    if authority_tmp:
        button_menu = InlineKeyboardMarkup() \
            .add(InlineKeyboardButton(text='Получить расписание занятий.', callback_data='schedule')) \
            .add(InlineKeyboardButton(text='Получить информацию о занятиях.', callback_data='lessons')) \
            .add(InlineKeyboardButton(text='Получить информацию о домашних заданиях.', callback_data='homeworks')) \
            .add(InlineKeyboardButton(text='Получить статус выполнения домашних заданий.', callback_data='myprogress')) \
            .add(InlineKeyboardButton(text='Поставить отзыв о занятии.', callback_data='feedback'))
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


async def match_datatime(lessons_date, lessons_time):
    len_elements = range(0, len(lessons_date)+1)
    for i in zip(len_elements, lessons_date, lessons_time):
        if datetime.strptime(f"{i[1]} {i[2]}", '%d.%m.%Y %H:%M МСК') > datetime.now():
            return i[0]
    return -1


async def name_button(callback_button, callback_data_button):
    for callback_button1 in callback_button:
        for callback_button2 in callback_button1:
            if callback_data_button in callback_button2.callback_data:
                return callback_button2.text
