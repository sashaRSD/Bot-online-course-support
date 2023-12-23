from dir_bot.functions import menu, name_button, google_api_error
from dir_bot.create_bot import bot, dp
from dir_google import google_sheets
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(text_contains='myprogress')
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
        await google_api_error(user_id)
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await menu(user_id)
