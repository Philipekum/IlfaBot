from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text
from keyboards.client_kb import main_kb, info_kb, contact_kb
import message_text
from config import config

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=message_text.start_text.format(message.from_user.full_name),
                         reply_markup=main_kb())


@router.message(Command('help'))
@router.message(Text(startswith='Помощь', ignore_case=True))
async def cmd_help(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=message_text.help_text,
                         reply_markup=main_kb())


@router.message(Text(startswith='Отмена', ignore_case=True))
@router.message(Command('cancel'))
async def cmd_back(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(text=message_text.no_active_commands_to_cancel, reply_markup=main_kb())

    else:
        await state.clear()
        await message.answer(text=message_text.commaned_canceled, reply_markup=main_kb())


@router.message(Text(startswith=('Инфо', 'О нас'), ignore_case=True))
async def info_message(message: types.Message):
    await message.answer(text=message_text.info,
                         reply_markup=info_kb())


@router.message(Text(startswith='Администратор', ignore_case=True))
async def admin_message(message: types.Message):
    await message.answer(text=message_text.admin,
                         reply_markup=contact_kb(config.admin_username.get_secret_value()))
