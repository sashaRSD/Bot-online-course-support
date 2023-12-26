from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import menu, google_api_error
from dir_bot.create_bot import bot, dp
from dir_google import sheet_schedule
from aiogram import types
import gspread.exceptions

get_value = 4


@dp.callback_query_handler(lambda fun: fun.data in ['schedule', 'schedule_mini'])
async def schedule_mini(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    await callback.answer()
    try:
        answer_text = await sheet_schedule.get_schedule(get_value)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
        await menu(user_id)
        return

    button_schedule_all = (InlineKeyboardMarkup()
                           .add((InlineKeyboardButton(text='Ещё', callback_data='schedule_all'))))
    if callback.data == 'schedule_mini':
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=answer_text, parse_mode='HTML')
    else:
        await bot.delete_message(chat_id=user_id, message_id=message_id)
        message_id = (await bot.send_message(user_id, answer_text, parse_mode='HTML')).message_id
        await menu(user_id)
    if answer_text.count(sheet_schedule.item_time_lesson) == get_value:
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=button_schedule_all)


@dp.callback_query_handler(text_contains='schedule_all')
async def schedule_all(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    await callback.answer()
    try:
        answer_text = await sheet_schedule.get_schedule()
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
        await menu(user_id)
        return

    button_schedule_mini = (InlineKeyboardMarkup()
                            .add((InlineKeyboardButton(text='Меньше', callback_data='schedule_mini'))))
    await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=answer_text, parse_mode='HTML')
    if answer_text.count(sheet_schedule.item_time_lesson) > get_value:
        await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=button_schedule_mini)
