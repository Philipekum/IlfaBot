from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text
from CRMRequest import CRMRequest
from keyboards.client_kb import categories_kb, services_kb

router = Router()

req = CRMRequest()


class ClientAction(StatesGroup):
    wait_category = State()
    wait_service = State()
    wait_doctor = State()
    wait_time = State()
    wait_name = State()
    wait_number = State()
    wait_commentary = State()
    wait_confirm = State()


@router.message(Text('Запись', ignore_case=True))
async def reg_start(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_category)
    try:
        await message.answer(text='Выбрать категорию услуг:\n', reply_markup=categories_kb())
    except:
        await state.clear()
        await message.answer(text='Произошла ошибка!')


@router.message(ClientAction.wait_category)
async def got_category(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_service)
    try:
        picked_category = message.text
        await message.answer(text='Выбрать услугу:\n', reply_markup=services_kb(picked_category))
    except:
        await state.clear()
        await message.answer(text='Произошла ошибка!')


@router.message(ClientAction.wait_service)
async def got_service(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_doctor)
    await state.update_data(picked_service=message.text)


    #   вывести список врачей с такой услугой ниже
    await message.answer(text='Выбрать врача:')


@router.message(ClientAction.wait_doctor)
async def got_doctor(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_time)
    #   сохранить врача в память
    #   сделать запрос про доступные даты и время
    await message.answer(text='Выбрать время:')


@router.message(ClientAction.wait_time)
async def got_time(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_name)
    #   занести дату и время в память
    await message.answer(text='Введите Ваше ФИО:')


@router.message(ClientAction.wait_name)
async def got_name(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_number)
    await message.answer(text='Введите Ваш номер телефона в формате +7(xxx)xxx-xx-xx:')


@router.message(ClientAction.wait_number)
async def got_number(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_commentary)
    await message.answer(text='Введите комментарии:')


@router.message(ClientAction.wait_commentary)
async def got_commentary(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_confirm)
    await message.answer(text='Подтвердите правильность введенных данных и подтвердите обработку персональных данных.')
