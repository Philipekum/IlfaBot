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
    wait_time = State()
    wait_name = State()
    wait_number = State()
    wait_commentary = State()
    wait_confirm = State()


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
    await state.set_state(ClientAction.wait_time)
    await message.answer(text='Выбрать дату:\n', reply_markup=listed_kb(req.get_dates(picked_doctor)))
