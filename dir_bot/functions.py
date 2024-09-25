from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_google.sheet_myprogress import get_authority, get_num_student
from dir_bot.create_bot import bot


button_menu = InlineKeyboardMarkup()\
    .add(InlineKeyboardButton(text='Получить расписание занятий.', callback_data='schedule'))\
    .add(InlineKeyboardButton(text='Получить информацию о занятиях.', callback_data='lessons'))\
    .add(InlineKeyboardButton(text='Получить расписание домашних заданий.', callback_data='schedule_homeworks'))\
    .add(InlineKeyboardButton(text='Получить информацию о домашних заданиях.', callback_data='homeworks'))\
    .add(InlineKeyboardButton(text='Получить статус выполнения домашних заданий.', callback_data='myprogress'))\
    .add(InlineKeyboardButton(text='Поставить отзыв о занятии.', callback_data='feedback'))


async def menu(call_menu_user):
    await bot.send_message(call_menu_user, 'Пожалуйста, укажите что вас интересует:', reply_markup=button_menu)


async def authority_student(my_username, my_id):
    num_student = await get_num_student(my_username, my_id)
    if num_student != -1:
        authority = await get_authority()
        if len(authority) >= num_student and authority[num_student]:
            return authority[num_student].split(" ")
        else:
            return -1
    else:
        await bot.send_message(my_id, '❗❗❗\n'
                                      'Ой, а вас нет в ведомости. \n'
                                      'Обратитесь к администратору...')
        return 0


async def student_error(user_id_error):
    await bot.send_message(user_id_error, '❗❗❗\n'
                                          'Ой, а вас нет в ведомости. \n'
                                          'Обратитесь к администратору...')


async def google_api_error(user_id_error):
    await bot.send_message(user_id_error, 'Сервер перегружен! \n'
                                          'Повторите попытку, через минуту 😉\n\n'
                                          'Напишите администратору, если ошибка не уходит!')


async def name_button(callback_button, callback_data_button):
    for callback_button1 in callback_button:
        for callback_button2 in callback_button1:
            if callback_data_button in callback_button2.callback_data:
                return callback_button2.text
