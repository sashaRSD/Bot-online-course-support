from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error, authority_student
from dir_bot.create_bot import bot, dp
from dir_google.sheet_homeworks import get_homeworks, get_name_homeworks, get_num_homeworks
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda homeworks: homeworks.data in 'homeworks')
async def homeworks_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # await callback.answer()
    try:
        button_homeworks = InlineKeyboardMarkup()
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            module_num = await get_num_homeworks()
            name_homeworks = await get_name_homeworks()
            index = 1
            for i_module_num, i_name_homeworks in zip(module_num, name_homeworks):
                index += 1
                if authority == -1 or i_module_num in authority:
                    button_homeworks.add((InlineKeyboardButton(text=f'{index-1}. {i_name_homeworks}',
                                                               callback_data=f'homeworks_name_{index}')))
            button_homeworks.add((InlineKeyboardButton(text="⏰ Расписание домашних заданий",
                                                       callback_data=f'schedule_homeworks')))
            button_homeworks.add((InlineKeyboardButton(text='🏠 В меню', callback_data='back_to_menu')))
            await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                        text='<b>🏠 Информация о домашних занятиях </b>',
                                        parse_mode='HTML', reply_markup=button_homeworks)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: 'homeworks_name' in name.data)
async def homework_name(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # await callback.answer()
    try:
        row_homework = await get_homeworks(callback.data.split('_')[2])
        homeworks_inf = (f'📗 <b>{row_homework[1]}</b>\n\n'
                         f'<i>Дата: {row_homework[5]}\n\n'
                         f'Описание: {row_homework[2]}\n\n'
                         f'Критерии оценивания:\n {row_homework[3]}</i>')
        button_cansel_homeworks = (InlineKeyboardMarkup()
                                   .add((InlineKeyboardButton(text='⬅️ Назад', callback_data=f'homeworks')))
                                   .add((InlineKeyboardButton(text='🏠 В меню', callback_data='back_to_menu'))))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=homeworks_inf,
                                    parse_mode='HTML', reply_markup=button_cansel_homeworks)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
