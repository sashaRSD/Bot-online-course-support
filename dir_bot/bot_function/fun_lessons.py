from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dir_bot.functions import google_api_error, authority_student
from dir_bot.create_bot import bot, dp
from dir_google.sheet_lessons import get_lesson_data
from dir_google.google_sheets import get_module_inf, get_modules_name, get_modules_index
from aiogram import types
import gspread.exceptions


@dp.callback_query_handler(lambda lessons: lessons.data in 'lessons')
async def menu_module(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # await callback.answer()
    try:
        authority = await authority_student(callback.message.chat.username, user_id)
        if authority:
            module_name = await get_modules_name()
            button_module = InlineKeyboardMarkup()
            for i, name in enumerate(module_name, 1):
                if authority == -1 or str(i) in authority:
                    button_module.add((InlineKeyboardButton(text=name, callback_data=f'lesson_module_{i - 1}')))
            button_module.add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu')))
            await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                        text='<b>🗂 Информация о занятиях </b>',
                                        parse_mode='HTML', reply_markup=button_module)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: 'lesson_module' in name.data)
async def menu_lessons(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    index_module = int(callback.data.split("_")[2])
    # await callback.answer()
    try:
        module_inf = await get_module_inf(index_module)
        button_lessons = InlineKeyboardMarkup()
        lesson_in_module = len(module_inf[1])
        for i, name in enumerate(module_inf[1], 1):
            button_lessons.add((InlineKeyboardButton(text=f'{i}. {name}',
                                                     callback_data=f'lesson_num_{index_module}_{lesson_in_module}_{i}')))
        button_lessons.add((InlineKeyboardButton(text='Назад', callback_data=f'lessons')))
        button_lessons.add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text=f'📂 <b>{module_inf[0]}</b>', parse_mode='HTML', reply_markup=button_lessons)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)


@dp.callback_query_handler(lambda name: ('lesson_num' in name.data) or 'lesson_index' in name.data)
async def get_lesson(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    menu_cansel = InlineKeyboardMarkup()
    index_modules_global = await get_modules_index()
    if "lesson_num" in callback.data:
        index_module = int(callback.data.split("_")[2])
        lesson_in_module = int(callback.data.split("_")[3])
        index_lesson = int(callback.data.split("_")[4])
        index_lesson_global = index_modules_global[index_module]+index_lesson+2
        if index_lesson != lesson_in_module:
            menu_cansel.add((InlineKeyboardButton(text='Следующий урок',
                                                  callback_data=f'lesson_num_{index_module}_{lesson_in_module}_{index_lesson+1}')))
        if index_lesson != 1:
            menu_cansel.add((InlineKeyboardButton(text='Предыдущий урок',
                                                  callback_data=f'lesson_num_{index_module}_{lesson_in_module}_{index_lesson-1}')))
        menu_cansel.add((InlineKeyboardButton(text='Назад', callback_data=f'lesson_module_{index_module}')))
        menu_cansel.add((InlineKeyboardButton(text='В модули', callback_data=f'lessons')))
    else:
        index_lesson_global = int(callback.data.split("_")[2])
    # await callback.answer()
    try:
        row_lesson = await get_lesson_data(index_lesson_global)
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
        menu_cansel.add((InlineKeyboardButton(text='В меню', callback_data='back_to_menu')))
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id,
                                    text=f"{data_lesson}",
                                    parse_mode='HTML', disable_web_page_preview=True, reply_markup=menu_cansel)
    except gspread.exceptions.APIError:
        await google_api_error(user_id)
