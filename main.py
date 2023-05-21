from asyncio import run
from aiogram import Dispatcher, Bot
from config import config
from handlers import client_cmds, client_visit, client_consultation
from aiogram.types import BotCommand
from aiogram.utils.chat_action import ChatActionMiddleware
import logging


async def set_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Главное меню'),
            BotCommand(command='help', description='Помощь'),
            BotCommand(command='cancel', description='Отмена действия')
        ]
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(config.bot_token.get_secret_value(), parse_mode='Markdown')
    dp = Dispatcher()
    for file in [client_cmds, client_visit, client_consultation]:
        dp.include_router(file.router)

    dp.message.middleware(ChatActionMiddleware())
    await set_commands(bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
