from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.utils import executor
from aiogram import types
from dir_bot.functions import menu, google_api_error
from dir_bot.create_bot import dp, bot
from dir_google.sheet_myprogress import get_table_progress
from dir_bot.bot_function import *
import asyncio


@dp.message_handler(commands=['start'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.chat.id, f'Добрый день, {message.from_user.first_name}! 👋')
        await menu(message.from_user.username, message.from_user.id)
    except:
        await google_api_error(message.from_user.id)


@dp.message_handler(commands=['lesson_push'])
async def commands_start(message: types.Message):
    user_id = message.from_user.id
    if len(message.text.split(" ")) == 3:
        authority = str(message.text.split(" ")[1])
        url = message.text.split(" ")[2]
        table_student = await get_table_progress()
        list_user_id = []
        lost_user_id = []
        send_score = 0
        for i_mass_student in table_student:
            if (not i_mass_student[1]) or (authority in i_mass_student[1]):
                student = i_mass_student[0].split(" ")
                for id_in_name in student:
                    if 'id' in id_in_name:
                        list_user_id.append(id_in_name[2:])
        for i_user_id in list_user_id:
            try:
                await bot.send_message(i_user_id, f'Урок начнется через 5 минут!\n'
                                                  f'{url}')
                send_score += 1
            except:
                lost_user_id.append(i_user_id)
        if lost_user_id:
            await bot.send_message(user_id, f'Найдено учеников: {len(list_user_id)}\n'
                                            f'Сообщение отправлено {send_score} раз!\n\n'
                                            f'Не отправлено: {lost_user_id}')
        else:
            await bot.send_message(user_id, f'Найдено учеников: {len(list_user_id)}\n'
                                            f'Сообщение отправлено всем!')
    else:
        await bot.send_message(user_id, f'Команда оформлена неверно!\n'
                                        f'Сообщение не отправлено...')


@dp.message_handler()
async def all_message(message):
    user_id = message.from_user.id
    await message.delete()
    smile = await bot.send_message(user_id, '🗿')
    text = await bot.send_message(user_id, 'Выбери пункт меню')
    await asyncio.sleep(4)
    await bot.delete_message(chat_id=user_id, message_id=smile.message_id)
    await bot.delete_message(chat_id=user_id, message_id=text.message_id)


@dp.callback_query_handler(lambda back: back.data in 'back_to_menu')
async def menu_callback_all(callback: types.CallbackQuery):
    await menu(callback.message.chat.username, callback.from_user.id, callback.message.message_id)


@dp.errors_handler(exception=MessageCantBeDeleted)
async def error_delete_2day(update, exception: MessageCantBeDeleted):
    print(update)
    chat_id = update['callback_query']['from']['id']
    message_id = update['callback_query']['message']['message_id']
    await bot.edit_message_text(text='<< Меню обновлено >>', chat_id=chat_id, message_id=message_id)
    username = update['callback_query']['message']['chat']['username']
    await menu(username, chat_id)
    return True


async def on_startup(_):
    print('Start Bot...')


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
