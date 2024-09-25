from dir_bot.functions import menu, google_api_error
from dir_bot.create_bot import bot, dp
from dir_google import sheet_myprogress
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(text_contains='myprogress')
async def my_progress_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await callback.answer()
    try:
        answer_text = await sheet_myprogress.get_progress(callback.message.chat.username, user_id)
        await bot.send_message(user_id, answer_text, parse_mode='HTML', disable_web_page_preview=True)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await menu(user_id)
