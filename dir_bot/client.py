import aiogram.utils.exceptions
import gspread.exceptions
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram import types
from dir_bot import create_bot
from dir_google import google_sheets
import asyncio

dp = create_bot.dp
bot = create_bot.bot

button_menu = InlineKeyboardMarkup()\
    .add(InlineKeyboardButton(text='Получить расписание занятий.', callback_data='schedule'))\
    .add(InlineKeyboardButton(text='Получить информацию о занятиях.', callback_data='lessons'))\
    .add(InlineKeyboardButton(text='Получить информацию о домашних заданиях.', callback_data='homeworks'))\
    .add(InlineKeyboardButton(text='Получить статус выполнения домашних заданий.', callback_data='myprogress'))\
    .add(InlineKeyboardButton(text='Поставить отзыв о занятии.', callback_data='feedback'))


class FSMClient(StatesGroup):
    lessons_support = State()
    mark_support = State()
    message_id_review = State()


async def menu(call_menu_user):
    await bot.send_message(call_menu_user, f'Пожалуйста, укажите что вас интересует:', reply_markup=button_menu)


@dp.message_handler(commands=['start'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, f'Добрый день, {message.from_user.first_name}! 👋')
        await menu(message.from_user.id)
    except:
        await message.delete()
        await message.reply('Напишите мне в личные сообщения')


@dp.callback_query_handler(state="*", text_contains='menu')
async def menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if await state.get_state():
        await state.finish()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await menu(callback.from_user.id)


@dp.callback_query_handler(lambda enter_callback: enter_callback.data in ['schedule', 'lessons', 'homeworks', 'myprogress'])
async def enter_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    enter_callback = callback.data
    await callback.answer()
    answer_text = ''
    try:
        if enter_callback == 'schedule':
            answer_text = await google_sheets.get_schedule()
        elif enter_callback == 'lessons':
            answer_text = await google_sheets.get_lessons()
        elif enter_callback == 'homeworks':
            answer_text = await google_sheets.get_homeworks()
        elif enter_callback == 'myprogress':
            answer_text = await google_sheets.get_progress(callback.message.chat.username, user_id)
        for i_message in answer_text:
            await bot.send_message(user_id, i_message, parse_mode='HTML', disable_web_page_preview=True)
    except gspread.exceptions.APIError:
        await bot.send_message(user_id, 'Сервер перегружен! \nПовторите попытку позже 😉')
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await menu(user_id)


@dp.callback_query_handler(text_contains='feedback')
async def support(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()

    lessons = await google_sheets.get_lessons_support()
    button_lessons = InlineKeyboardMarkup()
    for i, ilesson in enumerate(lessons, 1):
        button_lessons.add(InlineKeyboardButton(text=ilesson, callback_data=f"LessonNum_{i}"))
    button_lessons.add((InlineKeyboardButton(text='Отмена', callback_data='menu')))
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await bot.send_message(user_id, "Выберите урок, который хотите оценить:", reply_markup=button_lessons)


@dp.callback_query_handler(state="*", text_contains='LessonNum')
async def mark(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.answer()
    if await state.get_state():
        async with state.proxy() as data:
            lesson_name = data['lessons_support']
        await state.finish()
    else:
        lesson_name = await name_button(callback.message.reply_markup.inline_keyboard, callback.data)
        lesson_name = lesson_name[lesson_name.find('.') + 1:]

    button_mark = InlineKeyboardMarkup()
    mark1 = types.InlineKeyboardButton(text='1', callback_data='ReviewMark_1')
    mark2 = types.InlineKeyboardButton(text='2', callback_data='ReviewMark_2')
    mark3 = types.InlineKeyboardButton(text='3', callback_data='ReviewMark_3')
    mark4 = types.InlineKeyboardButton(text='4', callback_data='ReviewMark_4')
    mark5 = types.InlineKeyboardButton(text='5', callback_data='ReviewMark_5')
    button_mark.row(mark1, mark2, mark3, mark4, mark5)
    button_mark.add((InlineKeyboardButton(text='Изменить урок', callback_data='feedback')))
    button_mark.add((InlineKeyboardButton(text='Отмена', callback_data='menu')))
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await bot.send_message(user_id, f'Урок: {lesson_name} \nПоставьте оценку от 1 до 5:', reply_markup=button_mark)


@dp.callback_query_handler(text_contains='ReviewMark')
async def review(callback: types.CallbackQuery, state: FSMContext):
    lesson_name = callback.message.text
    lesson_name = lesson_name[6:lesson_name.find(" \nПоставьте оценку от 1 до 5:")]
    user_id = callback.from_user.id
    mark_id = callback.data.split('_')[1]
    await callback.answer()

    button_review = InlineKeyboardMarkup()
    button_review.add((InlineKeyboardButton(text='Отправить без отзыва', callback_data='SendReview')))
    button_review.add((InlineKeyboardButton(text='Изменить оценку', callback_data='LessonNum')))
    button_review.add((InlineKeyboardButton(text='Отмена', callback_data='menu')))
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    message_delete = await bot.send_message(user_id, f"Вы поставили оценку {mark_id} \nНапишите отзыв:", reply_markup=button_review)
    await FSMClient.lessons_support.set()
    async with state.proxy() as data:
        data['lessons_support'] = lesson_name
        await FSMClient.next()
        data['mark_support'] = mark_id
        await FSMClient.next()
        data['message_id_review'] = message_delete.message_id


@dp.callback_query_handler(state=FSMClient.message_id_review, text_contains='SendReview')
@dp.message_handler(state=FSMClient.message_id_review)
async def send_review(message, state: FSMContext):
    user_id = message.from_user.id
    if await is_callback('SendReview', message):
        await message.answer()
        review_text = '-'
        username_student = f'@{message.message.chat.username} (id{user_id})'
    else:
        review_text = message.text
        username_student = f'@{message.chat.username} (id{user_id})'
    async with state.proxy() as data:
        lessons_name = data['lessons_support']
        mark_id = data['mark_support']
        del_message_id_review = data['message_id_review']
    await state.finish()
    await google_sheets.send_lessons_support(username_student, lessons_name, mark_id, review_text)
    await bot.delete_message(chat_id=user_id, message_id=del_message_id_review)
    await bot.send_message(user_id, f"Вы оценили урок -  {lessons_name} на оценку {mark_id}.\n Благодарим вас за оставленный отзыв!")
    await menu(user_id)


async def is_callback(name_callback, data):
    for item in data:
        if name_callback in item:
            return True
    return False


async def name_button(callback_button, callback_data_button):
    for callback_button1 in callback_button:
        for callback_button2 in callback_button1:
            if callback_data_button in callback_button2.callback_data:
                return callback_button2.text


@dp.message_handler()
async def all_message(message):
    user_id = message.from_user.id
    await message.delete()
    smile = await bot.send_message(user_id, '🗿')
    text = await bot.send_message(user_id, 'Выбери пункт меню.')
    await asyncio.sleep(4)
    await bot.delete_message(chat_id=user_id, message_id=smile.message_id)
    await bot.delete_message(chat_id=user_id, message_id=text.message_id)


@dp.errors_handler(exception=MessageCantBeDeleted)
async def error_delete_2day(update, exception: MessageCantBeDeleted):
    chat_id = update['callback_query']['from']['id']
    message_id = update['callback_query']['message']['message_id']
    await bot.edit_message_text(text='<< Меню обновлено >>', chat_id=chat_id, message_id=message_id)
    await bot.send_message(chat_id, f'Пожалуйста, укажите что вас интересует:', reply_markup=button_menu)
    return True

