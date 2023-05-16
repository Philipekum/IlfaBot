from datetime import datetime
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text
from CrmRequest import CrmRequest
from keyboards.client_kb import listed_kb, listed_kb_dates, listed_kb_times

router = Router()


class ClientAction(StatesGroup):
    choose_category = State()
    choose_service = State()
    choose_doctor = State()
    choose_date = State()
    ask_name = State()
    ask_phone = State()
    ask_comment = State()
    confirm_data = State()
    end = State()


async def get_crm_and_data(state: FSMContext):
    """Returns CrmRequest instance and user_data of state. Just to avoid repeated code"""
    user_data = await state.get_data()
    crm = user_data['crm']
    return crm, user_data


@router.message(Text('Запись', ignore_case=True))
async def show_categories(message: types.Message, state: FSMContext):
    crm = CrmRequest()
    await state.update_data(crm=crm)

    await state.set_state(ClientAction.choose_category)
    await message.answer(text='Выбрать категорию услуг:\n', reply_markup=listed_kb(crm.get_categories()))


@router.message(ClientAction.choose_category)
async def show_services(message: types.Message, state: FSMContext):
    picked_category = message.text

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.choose_service)
    await message.answer(text='Выбрать услугу:\n', reply_markup=listed_kb(crm.get_services(picked_category)))


@router.message(ClientAction.choose_service)
async def show_doctors(message: types.Message, state: FSMContext):
    picked_service = message.text
    await state.update_data(picked_service=picked_service)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.choose_doctor)
    await message.answer(text='Выбрать врача:\n', reply_markup=listed_kb(crm.get_employees(picked_service)))


@router.message(ClientAction.choose_doctor)
async def show_dates(message: types.Message, state: FSMContext):
    picked_employee = message.text
    await state.update_data(picked_employee=picked_employee)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.choose_date)
    await message.answer(text='Выбрать дату:\n', reply_markup=listed_kb_dates(crm.get_dates(picked_employee), col=3))


@router.message(ClientAction.choose_date)
async def show_times(message: types.Message, state: FSMContext):
    picked_date = datetime.strptime(message.text, '%d.%m.%y')
    await state.update_data(picked_date=picked_date)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.ask_name)
    await message.answer(text='Выбрать время:\n',
                         reply_markup=listed_kb_times(crm.get_times(picked_date, user_data['picked_employee']), col=4))


@router.message(ClientAction.ask_name)
async def ask_name(message: types.Message, state: FSMContext):
    picked_time = datetime.strptime(message.text, '%H:%M')
    await state.update_data(picked_time=picked_time)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.ask_phone)
    await message.answer(text='Введите ФИО:\n')


@router.message(ClientAction.ask_phone)
async def ask_phone(message: types.Message, state: FSMContext):
    user_name = message.text.title()
    await state.update_data(user_name=user_name)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.ask_comment)
    await message.answer(text='Введите номер телефона:\n')


@router.message(ClientAction.ask_comment)
async def ask_comment(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.confirm_data)
    await message.answer(text=f'Введите комментарий:\n')


@router.message(ClientAction.confirm_data)
async def confirm_visit(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ClientAction.end)
    await message.answer(text=f'Проверьте данные:\n'
                              f'Выбранная услуга - {user_data["picked_service"]}\n'
                              f'Выбранный врач - {user_data["picked_employee"]}\n'
                              f'Выбранная дата - {datetime.strftime(user_data["picked_date"], "%d.%m.%Y")}\n'
                              f'Выбранное время - {datetime.strftime(user_data["picked_time"], "%H:%M")}\n'
                              f'Ваше ФИО - {user_data["user_name"]}\n'
                              f'Ваш номер телефона - {user_data["phone_number"]}\n'
                              f'Ваш комментарий - {user_data["comment"]}')


@router.message(ClientAction.end)
async def end(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Ура!')
