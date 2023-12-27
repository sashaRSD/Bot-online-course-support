from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import menu, google_api_error, name_button
from dir_bot.create_bot import bot, dp
from dir_google import sheet_lessons
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda lessons: lessons.data == 'lessons')
async def menu_module(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await callback.answer()
    try:
        answer_text = await sheet_lessons.get_module_lesson()
        button_module = InlineKeyboardMarkup()
        for i, name in enumerate(answer_text, 1):
            button_module.add((InlineKeyboardButton(text=name, callback_data=f'lessons_module_{i}')))
        await bot.send_message(user_id, '<b>🗂 Информация о занятиях </b>',
                               parse_mode='HTML', reply_markup=button_module)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await menu(user_id)


@dp.callback_query_handler(lambda name: 'lessons_module' in name.data)
async def menu_lessons(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    module_name = await name_button(callback.message.reply_markup.inline_keyboard, callback.data)
    await callback.answer()
    try:
        answer_text = await sheet_lessons.get_lesson_name(module_name)
        button_lessons = InlineKeyboardMarkup()
        for i, name in enumerate(answer_text, 1):
            button_lessons.add((InlineKeyboardButton(text=name, callback_data=f'lessons_name_{i}')))
        button_lessons.add((InlineKeyboardButton(text='Назад', callback_data=f'lessons_cansel')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text=f'📒<b>{module_name}</b>', parse_mode='HTML', reply_markup=button_lessons)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: 'lessons_name' in name.data)
async def get_lesson(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lesson_name = await name_button(callback.message.reply_markup.inline_keyboard, callback.data)
    await callback.answer()
    try:
        answer_text = await sheet_lessons.get_lesson(lesson_name)
        menu_cansel = (InlineKeyboardMarkup()
                       .add((InlineKeyboardButton(text='Другой урок', callback_data=f'lessons_cansel'))))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text=f"<b>{callback.message.text}</b>\n{answer_text}",
                                    parse_mode='HTML', disable_web_page_preview=True, reply_markup=menu_cansel)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: 'lessons_cansel' in name.data)
async def menu_module_cansel(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    try:
        answer_text = await sheet_lessons.get_module_lesson()
        button_module = InlineKeyboardMarkup()
        for i, name in enumerate(answer_text, 1):
            button_module.add((InlineKeyboardButton(text=name, callback_data=f'lessons_module_{i}')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text='<b>🗂 Информация о занятиях </b>',
                                    parse_mode='HTML', reply_markup=button_module)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)

