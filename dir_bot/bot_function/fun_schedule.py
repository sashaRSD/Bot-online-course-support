from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import menu, google_api_error
from dir_bot.create_bot import bot, dp
from dir_google import sheet_schedule
from aiogram import types
import gspread.exceptions

get_value = 4


@dp.callback_query_handler(lambda fun: fun.data == 'schedule')
async def schedule(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await callback.answer()
    try:
        answer_text = await sheet_schedule.get_schedule(get_value)
        button_schedule_all = (InlineKeyboardMarkup()
                               .add((InlineKeyboardButton(text='Показать всё', callback_data='schedule_all'))))
        if answer_text[1] == get_value:
            await bot.send_message(user_id, f"{answer_text[0]}\n <i>⬇️Ещё⬇️</i>",
                                   parse_mode='HTML', reply_markup=button_schedule_all)
        else:
            await bot.send_message(user_id, f"{answer_text[0]}", parse_mode='HTML')
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await menu(user_id)


@dp.callback_query_handler(text_contains='schedule_all')
async def schedule_all(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    await callback.answer()
    try:
        answer_text = await sheet_schedule.get_schedule()
        button_schedule_mini = (InlineKeyboardMarkup()
                                .add((InlineKeyboardButton(text='Свернуть', callback_data='schedule_mini'))))
        if answer_text[1] > get_value:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                        text=f"{answer_text[0]}\n",
                                        parse_mode='HTML', reply_markup=button_schedule_mini)
        else:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                        text=f"{answer_text[0]}", parse_mode='HTML')
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(text_contains='schedule_mini')
async def schedule_mini(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    await callback.answer()
    try:
        answer_text = await sheet_schedule.get_schedule(get_value)
        button_schedule_all = (InlineKeyboardMarkup()
                               .add((InlineKeyboardButton(text='Показать всё', callback_data='schedule_all'))))
        if answer_text[1] == get_value:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                        text=f"{answer_text[0]}\n <i>⬇️Ещё⬇️</i>",
                                        parse_mode='HTML', reply_markup=button_schedule_all)
        else:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                        text=f"{answer_text[0]}", parse_mode='HTML')
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
