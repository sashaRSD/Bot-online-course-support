from dir_bot.functions import menu, google_api_error, authority_student, student_error
from dir_bot.create_bot import bot, dp
from dir_google.sheet_myprogress import get_num_student, get_table_progress
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(text_contains='myprogress')
async def my_progress_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await callback.answer()
    try:
        num_student = await get_num_student(callback.message.chat.username, user_id)
        if num_student != -1:
            my_progress = await get_table_progress()
            progress_information = '<b>📈 Статистика ваших дз: </b>\n\n'
            for num_homework in range(2, len(my_progress[0])):
                mark_homework = my_progress[num_student][num_homework]
                if mark_homework.lstrip("-").isnumeric():
                    mark_homework = int(mark_homework)
                else:
                    mark_homework = 0
                if mark_homework > 0:
                    progress_information += '✅'
                else:
                    progress_information += '❌'
                progress_information += f' {my_progress[0][num_homework]}: {abs(mark_homework)}/10\n'
            await bot.send_message(user_id, progress_information, parse_mode='HTML')
        else:
            await student_error(user_id)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await menu(callback.message.chat.username, user_id)
