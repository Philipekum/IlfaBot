from aiogram import Router, types
from keyboards.client_kb import main_kb
from texts import json_reader

router = Router()
text = json_reader.read_json_file('texts/text_client_cmds.json')


@router.message()
async def any_message(message: types.Message):
    await message.answer(text=text['any_message'],
                         reply_markup=main_kb())
