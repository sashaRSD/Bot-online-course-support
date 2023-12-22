from aiogram.utils import executor
from dir_bot import create_bot, client


async def on_startup(_):
    print('Start Bot...')


def main():
    executor.start_polling(create_bot.dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
