from asyncio import run
from aiogram import Dispatcher, Bot
from config import config
from handlers import client_cmds, client_first_visit, client_second_visit, client_authorization, client_visit
from aiogram.types import BotCommand

import logging


async def set_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Главное меню'),
            BotCommand(command='help', description='Помощь'),
        ]
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(config.bot_token.get_secret_value(), parse_mode='html')
    dp = Dispatcher()
    # for file in [client_cmds, client_first_visit, client_second_visit, client_authorization]:
    #     dp.include_router(file.router)
    dp.include_router(client_visit.router)

    await set_commands(bot)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    run(main())
