from aiogram.dispatcher import flags
from aiogram import BaseMiddleware, types
from aiogram.utils.chat_action import ChatActionSender
from typing import Callable, Awaitable, Dict, Any


class BotTyping(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
                       event: types.Message,
                       data: Dict[str, Any]) -> Any:

        typing = flags.get_flag(data, 'typing')

        if not typing:
            return await handler(event, data)

        async with ChatActionSender(
                action=typing,
                chat_id=event.chat.id
        ):
            return await handler(event, data)
