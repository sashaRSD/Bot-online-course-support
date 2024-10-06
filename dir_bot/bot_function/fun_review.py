from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
from dir_bot.functions import menu, google_api_error, match_datatime
from dir_bot.create_bot import dp, bot
from dir_google import sheet_review
import gspread.exceptions


class FSMClient(StatesGroup):
    lessons_support = State()
    mark_support = State()
    message_id_review = State()


@dp.callback_query_handler(lambda back: back.data in 'menu', state="*")
async def menu_callback(callback: types.CallbackQuery, state: FSMContext):
    # await callback.answer()
    if await state.get_state():
        await state.finish()
    await menu(callback.message.chat.username, callback.from_user.id, callback.message.message_id)


@dp.callback_query_handler(lambda back: back.data in 'feedback')
async def support(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # await callback.answer()
    try:
        lessons_mass = await sheet_review.get_lessons_support()
        i_last_lesson = await match_datatime(lessons_mass[1], lessons_mass[2])
        if i_last_lesson != 0 and i_last_lesson != -1:
            i_last_lesson -= 1
        button_lessons = InlineKeyboardMarkup()
        button_lessons.add(InlineKeyboardButton(text=f'{lessons_mass[0][i_last_lesson]} '
                                                     f'({lessons_mass[1][i_last_lesson]})',
                                                callback_data=f"LessonNum_{i_last_lesson}"))
        button_lessons.add((InlineKeyboardButton(text='📖 Выбрать урок', callback_data='feedback_all')))
        button_lessons.add((InlineKeyboardButton(text='🏠 В меню', callback_data='menu')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text="Оценить урок?", reply_markup=button_lessons)
    except gspread.exceptions.APIError:
        await bot.delete_message(user_id, callback.message.message_id)
        await google_api_error(user_id)
        await menu(callback.message.chat.username, user_id)


@dp.callback_query_handler(lambda back: back.data in 'feedback_all')
async def support(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # await callback.answer()
    try:
        lessons_mass = await sheet_review.get_lessons_support()
        lessons_support = []
        for i in zip(lessons_mass[0], lessons_mass[1]):
            lessons_support.append(f'{i[0]} ({i[1]})')
        button_lessons = InlineKeyboardMarkup()
        for i, i_lesson in enumerate(lessons_support, 1):
            button_lessons.add(InlineKeyboardButton(text=i_lesson, callback_data=f"LessonNum_{i}"))
        button_lessons.add((InlineKeyboardButton(text='🏠 В меню', callback_data='menu')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text="Выберите урок, который хотите оценить:", reply_markup=button_lessons)
    except gspread.exceptions.APIError:
        await bot.delete_message(user_id, callback.message.message_id)
        await google_api_error(user_id)
        await menu(callback.message.chat.username, user_id)


@dp.callback_query_handler(state="*", text_contains='LessonNum')
async def mark(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    # await callback.answer()
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
    button_mark.add((InlineKeyboardButton(text='🏠 В меню', callback_data='menu')))
    await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                text=f'Урок: {lesson_name} \nПоставьте оценку от 1 до 5:', reply_markup=button_mark)


@dp.callback_query_handler(text_contains='ReviewMark')
async def review(callback: types.CallbackQuery, state: FSMContext):
    lesson_name = callback.message.text
    lesson_name = lesson_name[6:lesson_name.find(" \nПоставьте оценку от 1 до 5:")]
    user_id = callback.from_user.id
    mark_id = callback.data.split('_')[1]
    # await callback.answer()

    button_review = InlineKeyboardMarkup()
    button_review.add((InlineKeyboardButton(text='Отправить без отзыва', callback_data='SendReview')))
    button_review.add((InlineKeyboardButton(text='Изменить оценку', callback_data='LessonNum')))
    button_review.add((InlineKeyboardButton(text='🏠 В меню', callback_data='menu')))
    message_edit = await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                                 text=f"Вы поставили оценку {mark_id} \nНапишите отзыв:",
                                                 reply_markup=button_review)
    await FSMClient.lessons_support.set()
    async with state.proxy() as data:
        data['lessons_support'] = lesson_name
        await FSMClient.next()
        data['mark_support'] = mark_id
        await FSMClient.next()
        data['message_id_review'] = message_edit.message_id


@dp.callback_query_handler(state=FSMClient.message_id_review, text_contains='SendReview')
@dp.message_handler(state=FSMClient.message_id_review)
async def send_review(message, state: FSMContext):
    user_id = message.from_user.id
    if await is_callback('SendReview', message):
        # await message.answer()
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
    await bot.delete_message(chat_id=user_id, message_id=del_message_id_review)
    try:
        await sheet_review.send_lessons_support(username_student, lessons_name, int(mark_id), review_text)
        await bot.send_message(user_id, f"Вы оценили урок <b>{lessons_name}</b> на оценку <b>{mark_id}</b>.\n"
                                        f"Благодарим вас за оставленный отзыв! ❤️",  parse_mode='HTML')
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await menu(message.from_user.username, user_id)


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

