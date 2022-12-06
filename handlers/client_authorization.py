from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text

router = Router()


# registration - /reg вместо /appointment

class Authorization(StatesGroup):
    await_username = State()
    await_password = State()
    authorized = State()


accounts = {
    'username': 'password',
    'admin': '1234',
    'test_user': '1'
}


# Условие если пользователь не авторизован
@router.message(Text('Повторный', ignore_case=True))
async def second_reg_start(message: types.Message, state: FSMContext):
    await state.set_state(Authorization.await_username)
    # await message.from_user.id
    await message.answer(text='Чтобы записаться на повторный прием, вам нужно авторизироваться.\n'
                              'Пожалуйста введите логин учетной записи:')


@router.message(Authorization.await_username)
async def got_username(message: types.Message, state: FSMContext):
    if message.text in accounts:
        await state.update_data(username=message.text)
        await state.set_state(Authorization.await_password)
        await message.answer(text='Пожалуйста введите, пароль от учетной записи:')

    else:
        await state.clear()
        await message.answer(text='Аккаунт не найден!')


@router.message(Authorization.await_password)
async def got_password(message: types.Message, state: FSMContext):
    if message.text in accounts.values():
        await state.update_data(password=message.text)
        await message.answer(text='Вы авторизованы!')

    else:
        await state.set_state(Authorization.await_username)
        await message.answer(text='Неправильный пароль, попробуйте еще раз!')
