from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error, authority_student, get_num_student
from dir_bot.create_bot import bot, dp
from dir_google.sheet_myprogress import get_table_progress
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(text_contains='myprogress')
async def my_progress_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # await callback.answer()
    try:
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            my_progress = await get_table_progress()
            num_student = await get_num_student(callback.message.chat.username, user_id)
            progress_information = '<b>📈 Статистика ваших дз: </b>\n\n'
            for num_homework in range(2, len(my_progress[0])):
                if authority == -1 or my_progress[0][num_homework][1:2] in authority:
                    mark_homework = my_progress[num_student][num_homework]
                    if mark_homework.lstrip("-").isnumeric():
                        mark_homework = int(mark_homework)
                    else:
                        mark_homework = 0
                    if mark_homework > 0:
                        progress_information += '✅'
                    else:
                        progress_information += '❌'
                    progress_information += (f' {my_progress[0][num_homework][my_progress[0][num_homework].find(":")+1:]}:'
                                             f' {abs(mark_homework)}/10\n')
            button_back = (InlineKeyboardMarkup()
                           .add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu'))))
            await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                        text=progress_information,
                                        parse_mode='HTML', reply_markup=button_back)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
