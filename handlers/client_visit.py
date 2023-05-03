from datetime import datetime
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text
from CRMRequest import CRMRequest
from keyboards.client_kb import listed_kb

router = Router()

req = CRMRequest()


class ClientAction(StatesGroup):
    wait_category = State()
    wait_service = State()
    wait_doctor = State()
    wait_date = State()
    wait_time = State()


@router.message(Text('Запись', ignore_case=True))
async def show_categories(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_category)
    await message.answer(text='Выбрать категорию услуг:\n', reply_markup=listed_kb(req.get_categories()))


@router.message(ClientAction.wait_category)
async def show_services(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.wait_service)
    picked_category = message.text
    await message.answer(text='Выбрать услугу:\n', reply_markup=listed_kb(req.get_services(picked_category)))


@router.message(ClientAction.wait_service)
async def show_doctors(message: types.Message, state: FSMContext):
    picked_service = message.text
    await state.update_data(service=picked_service)
    await state.set_state(ClientAction.wait_doctor)
    await message.answer(text='Выбрать врача:\n', reply_markup=listed_kb(req.get_employees(picked_service)))


@router.message(ClientAction.wait_doctor)
async def show_dates(message: types.Message, state: FSMContext):
    picked_doctor = message.text
    await state.update_data(employee=picked_doctor)
    await state.set_state(ClientAction.wait_date)
    await message.answer(text='Выбрать дату:\n', reply_markup=listed_kb(req.get_dates(picked_doctor), col=4))


@router.message(ClientAction.wait_date)
async def show_times(message: types.Message, state: FSMContext):
    picked_date = datetime.strptime(f'{datetime.now().year} {message.text[3:]}', '%Y %d.%m')
    await state.update_data(date=picked_date)
    await state.set_state(ClientAction.wait_time)
    user_data = await state.get_data()
    await message.answer(text='Выбрать время:\n',
                         reply_markup=listed_kb(req.get_times(picked_date, user_data['employee']), col=4))
