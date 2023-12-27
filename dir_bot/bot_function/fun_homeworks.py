from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import menu, google_api_error
from dir_bot.create_bot import bot, dp
from dir_google import sheet_homeworks
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda homeworks: homeworks.data == 'homeworks')
async def homeworks_name(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await callback.answer()
    try:
        answer_text = await sheet_homeworks.get_name_homeworks()
        button_homeworks = InlineKeyboardMarkup()
        for i, name in enumerate(answer_text, 2):
            button_homeworks.add((InlineKeyboardButton(text=name, callback_data=f'homeworks_name_{i}')))
        await bot.send_message(user_id, '<b>🏠 Информация о домашних занятиях </b>',
                               parse_mode='HTML', reply_markup=button_homeworks)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await menu(user_id)


@dp.callback_query_handler(lambda name: 'homeworks_name' in name.data)
async def homework_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    try:
        answer_text = await sheet_homeworks.get_homeworks(callback.data.split('_')[2])
        button_cansel_homeworks = (InlineKeyboardMarkup()
                                   .add((InlineKeyboardButton(text='Назад', callback_data=f'homeworks_cansel'))))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=answer_text,
                                    parse_mode='HTML', reply_markup=button_cansel_homeworks)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(text_contains='homeworks_cansel')
async def homeworks_name(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    try:
        answer_text = await sheet_homeworks.get_name_homeworks()
        button_homeworks = InlineKeyboardMarkup()
        for i, name in enumerate(answer_text, 2):
            button_homeworks.add((InlineKeyboardButton(text=name, callback_data=f'homeworks_name_{i}')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text='<b>🏠 Информация о домашних занятиях </b>',
                                    parse_mode='HTML', reply_markup=button_homeworks)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
