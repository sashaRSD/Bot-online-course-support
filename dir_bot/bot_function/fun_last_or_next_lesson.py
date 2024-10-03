from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error
from dir_google.sheet_last_or_next_lesson import get_lesson_data
from dir_bot.create_bot import bot, dp
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda name: 'lessons_num_' in name.data)
async def get_lesson_num(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lesson_num = callback.data.split("_")[2]
    # await callback.answer()
    try:
        row_lesson = await get_lesson_data(lesson_num)
        if len(row_lesson) >= 8 and row_lesson[7]:
            teacher = row_lesson[7]
        else:
            teacher = 'Игорь Гулькин'
        data_lesson = (f'<b>📒 {row_lesson[2]}</b>\n\n'
                       f'<i>Дата: {row_lesson[0]}, {row_lesson[1]}\n'
                       f'Преподаватель: {teacher}\n'
                       f'Цель: {row_lesson[3]}\n\n'
                       f'Описание:\n\n {row_lesson[4]}\n\n'
                       f'Материалы: {row_lesson[5]}</i>\n')
        menu_cansel = InlineKeyboardMarkup().add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text=f"{data_lesson}",
                                    parse_mode='HTML', disable_web_page_preview=True, reply_markup=menu_cansel)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)