from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error, authority_student, match_datatime
from dir_bot.create_bot import bot, dp
from dir_google.google_sheets import get_modules_name, get_module_inf
from aiogram import types
import gspread.exceptions

max_get_value = 4
message_wait = "⏳ Получаю расписание, подождите пожалуйста ⏳"
button_back = (InlineKeyboardMarkup()
               .add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu'))))


async def module_cul(authority, local_max_value):
    module_name = await get_modules_name()
    data_schedule = []
    lessons_date = []
    lessons_time = []
    lessons_name = []
    schedule_text = " <b>Расписание занятий:"
    for i in range(len(module_name)):
        if authority == -1 or str(i+1) in authority:
            data_schedule.append(await get_module_inf(i))
    for i_module in data_schedule:
        lessons_name += i_module[1]
        lessons_date += i_module[2]
        lessons_time += i_module[3]
    last_lesson = await match_datatime(lessons_date, lessons_time)
    if last_lesson != -1:
        if local_max_value and len(lessons_date) - last_lesson > local_max_value:
            last_element = last_lesson + local_max_value
        else:
            last_element = len(lessons_date)
        for elem in range(last_lesson, last_element):
            schedule_text += (f'\n\n'
                              f'⏰ {lessons_date[elem]} в {lessons_time[elem]}\n'
                              f'📚 {lessons_name[elem][lessons_name[elem].find(".") + 1:]}')
        schedule_text += '</b>'
    else:
        schedule_text = "Занятия закончились 😉"
    return schedule_text


@dp.callback_query_handler(lambda fun: fun.data == 'schedule')
async def schedule(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    wait_message = await bot.send_message(user_id, message_wait)
    # await callback.answer()
    try:
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            schedule_text = await module_cul(authority, max_get_value)

            button_schedule_all = (InlineKeyboardMarkup()
                                   .add((InlineKeyboardButton(text='Показать всё', callback_data='schedule_all')))
                                   .add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu'))))
            if schedule_text.count('⏰') == max_get_value:
                await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                            text= f"{schedule_text}\n\n\n <i>⬇️Ещё⬇️</i>",
                                            parse_mode='HTML', reply_markup=button_schedule_all)
            else:
                await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                            text=f"{schedule_text}", parse_mode='HTML', reply_markup=button_back)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await bot.delete_message(chat_id=user_id, message_id=wait_message.message_id)


@dp.callback_query_handler(text_contains='schedule_all')
async def schedule_all(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    # await callback.answer()
    await bot.edit_message_reply_markup(user_id, message_id)
    wait_message = await bot.send_message(user_id, message_wait)
    try:
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            schedule_text = await module_cul(authority, 0)
            button_schedule_mini = (InlineKeyboardMarkup()
                                    .add((InlineKeyboardButton(text='Свернуть', callback_data='schedule_mini')))
                                    .add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu'))))
            if schedule_text.count('⏰') > max_get_value:
                await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                            text=f"{schedule_text}\n",
                                            parse_mode='HTML', reply_markup=button_schedule_mini)
            else:
                await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                            text=f"{schedule_text}", parse_mode='HTML', reply_markup=button_back)

    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await bot.delete_message(chat_id=user_id, message_id=wait_message.message_id)


@dp.callback_query_handler(text_contains='schedule_mini')
async def schedule_mini(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    message_id = callback.message.message_id
    # await callback.answer()
    await bot.edit_message_reply_markup(user_id, message_id)
    wait_message = await bot.send_message(user_id, message_wait)
    try:
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            schedule_text = await module_cul(authority, max_get_value)
            button_schedule_all = (InlineKeyboardMarkup()
                                   .add((InlineKeyboardButton(text='Показать всё', callback_data='schedule_all')))
                                   .add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu'))))
            if schedule_text.count('⏰') == max_get_value:
                await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                            text=f"{schedule_text}\n\n\n <i>⬇️Ещё⬇️</i>",
                                            parse_mode='HTML', reply_markup=button_schedule_all)
            else:
                await bot.edit_message_text(chat_id=user_id, message_id=message_id,
                                            text=f"{schedule_text}", parse_mode='HTML', reply_markup=button_back)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
    await bot.delete_message(chat_id=user_id, message_id=wait_message.message_id)
