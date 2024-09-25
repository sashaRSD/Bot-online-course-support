from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error, name_button, authority_student
from dir_bot.create_bot import bot, dp
from dir_google.sheet_lessons import get_lesson_data, get_module_inf, get_module_name
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda lessons: lessons.data in ['lessons', 'lessons_cansel'])
async def menu_module(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    try:
        module_name = await get_module_name()
        button_module = InlineKeyboardMarkup()
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            for i, name in enumerate(module_name, 1):
                if authority == -1 or str(i) in authority:
                    button_module.add((InlineKeyboardButton(text=name, callback_data=f'lessons_module_{i - 1}')))
            if callback.data == 'lessons':
                await bot.send_message(user_id, '<b>🗂 Информация о занятиях </b>',
                                       parse_mode='HTML', reply_markup=button_module)
            elif callback.data == 'lessons_cansel':
                await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                            text='<b>🗂 Информация о занятиях </b>',
                                            parse_mode='HTML', reply_markup=button_module)

    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: 'lessons_module' in name.data)
async def menu_lessons(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    index_module_name = int(callback.data.split("_")[2])
    await callback.answer()
    try:
        module_inf = await get_module_inf(index_module_name)
        button_lessons = InlineKeyboardMarkup()
        for i, name in enumerate(module_inf[1]):
            button_lessons.add((InlineKeyboardButton(text=name, callback_data=f'lessons_name_{index_module_name}_{i}')))
        button_lessons.add((InlineKeyboardButton(text='Назад', callback_data=f'lessons_cansel')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text=f'📂 <b>{module_inf[0]}</b>', parse_mode='HTML', reply_markup=button_lessons)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: 'lessons_name' in name.data)
async def get_lesson(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    index_module_name = callback.data.split("_")[2]
    lesson_name = await name_button(callback.message.reply_markup.inline_keyboard, callback.data)
    await callback.answer()
    try:
        row_lesson = await get_lesson_data(lesson_name)
        if len(row_lesson) >= 8 and row_lesson[7]:
            teacher = row_lesson[7]
        else:
            teacher = 'Игорь Гулькин'
        data_lesson = (f'<b>📒 {lesson_name}</b>\n\n'
                       f'<i>Дата: {row_lesson[0]}, {row_lesson[1]}\n'
                       f'Преподаватель: {teacher}\n'
                       f'Цель: {row_lesson[3]}\n\n'
                       f'Описание:\n\n {row_lesson[4]}\n\n'
                       f'Материалы: {row_lesson[5]}</i>\n')
        menu_cansel = (InlineKeyboardMarkup()
                       .add((InlineKeyboardButton(text='Другой урок',
                                                  callback_data=f'lessons_module_{index_module_name}')))
                       .add((InlineKeyboardButton(text='Другой модуль', callback_data=f'lessons_cansel'))))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text=f"{data_lesson}",
                                    parse_mode='HTML', disable_web_page_preview=True, reply_markup=menu_cansel)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)

