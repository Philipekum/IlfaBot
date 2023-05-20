from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text
from keyboards.client_kb import main_kb, info_kb
import message_text


router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=message_text.start_text.format(message.from_user.full_name),
                         reply_markup=main_kb())


@router.message(Command('help'))
@router.message(Text('Помощь', ignore_case=True))
async def cmd_help(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=message_text.help_text,
                         reply_markup=main_kb())


@router.message(Text('Отмена', ignore_case=True))
@router.message(Command('cancel'))
async def cmd_back(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(text=message_text.no_active_commands_to_cancel, reply_markup=main_kb())

    else:
        await message.answer(text=message_text.commaned_canceled, reply_markup=main_kb())


@router.message(Text(['инфо'], ignore_case=True))
async def cmd_info(message: types.Message):
    await message.answer(text=message_text.info,
                         reply_markup=info_kb())
