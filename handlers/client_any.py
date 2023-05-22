from aiogram import Router, types
import message_text
from keyboards.client_kb import main_kb

router = Router()


@router.message()
async def any_message(message: types.Message):
    await message.answer(text=message_text.any_message,
                         reply_markup=main_kb())
