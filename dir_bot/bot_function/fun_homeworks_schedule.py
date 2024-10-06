from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error, authority_student
from dir_bot.create_bot import bot, dp
from dir_google.sheet_homeworks import get_date_homeworks, get_name_homeworks, get_num_homeworks
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda homeworks: homeworks.data in 'schedule_homeworks')
async def schedule_homeworks(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # await callback.answer()
    try:
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            name_homeworks = await get_name_homeworks()
            date_homeworks = await get_date_homeworks()
            module_num = await get_num_homeworks()
            index = 1
            answer_text = ''
            for i_module_num, i_name_homeworks, i_date_homeworks in zip(module_num, name_homeworks, date_homeworks):
                index += 1
                if authority == -1 or i_module_num in authority:
                    answer_text += (f"\n\n"
                                    f"📗 {i_name_homeworks}\n"
                                    f"⏰ {i_date_homeworks}")
            button_back = (InlineKeyboardMarkup()
                           .add((InlineKeyboardButton(text='⬅️ Назад', callback_data='homeworks'))))
            await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                        text=f'<b>Расписание домашних заданий{answer_text}</b>',
                                        parse_mode='HTML', reply_markup=button_back)

    except gspread.exceptions.APIError:
        await google_api_error(user_id)
