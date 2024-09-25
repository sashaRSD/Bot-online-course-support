from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error
from dir_bot.create_bot import bot, dp
from dir_google.sheet_homeworks import get_homeworks, get_name_homeworks
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda homeworks: homeworks.data in 'homeworks')
async def homeworks_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    try:
        answer_text = await get_name_homeworks()
        button_homeworks = InlineKeyboardMarkup()
        button_homeworks.add((InlineKeyboardButton(text="⏰ Получить расписание домашних заданий.",
                                                   callback_data=f'schedule_homeworks')))
        for i, name in enumerate(answer_text, 2):
            button_homeworks.add((InlineKeyboardButton(text=name, callback_data=f'homeworks_name_{i}')))
        button_homeworks.add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text='<b>🏠 Информация о домашних занятиях </b>',
                                    parse_mode='HTML', reply_markup=button_homeworks)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: 'homeworks_name' in name.data)
async def homework_name(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    try:
        answer_text = await get_homeworks(callback.data.split('_')[2])
        button_cansel_homeworks = (InlineKeyboardMarkup()
                                   .add((InlineKeyboardButton(text='Назад', callback_data=f'homeworks')))
                                   .add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu'))))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=answer_text,
                                    parse_mode='HTML', reply_markup=button_cansel_homeworks)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
