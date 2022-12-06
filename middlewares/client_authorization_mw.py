# from aiogram.dispatcher import flags
# from aiogram import BaseMiddleware
# from aiogram import types
# from typing import Callable, Awaitable, Dict, Any
#
#
# class Authorized(BaseMiddleware):
#     async def __call__(self,
#                        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
#                        event: types.Message,
#                        data: Dict[str, Any]) -> Any:
#         __is_authorized = flags.get_flag(data, 'True')
#
#         if not __is_authorized:
#             return await handler(event, data)
#
#
#         async with ChatActionSender(
#                 action=long_operation_type,
#                 chat_id=event.chat.id
#         ):
#             return await handler(event, data)
