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
    choose_category = State()
    choose_service = State()
    choose_doctor = State()
    choose_date = State()
    ask_name = State()
    ask_phone = State()
    ask_comment = State()
    confirm_data = State()
    end = State()


@router.message(Text('Запись', ignore_case=True))
async def show_categories(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.choose_category)
    await message.answer(text='Выбрать категорию услуг:\n', reply_markup=listed_kb(req.get_categories()))


@router.message(ClientAction.choose_category)
async def show_services(message: types.Message, state: FSMContext):
    await state.set_state(ClientAction.choose_service)
    picked_category = message.text
    await message.answer(text='Выбрать услугу:\n', reply_markup=listed_kb(req.get_services(picked_category)))


@router.message(ClientAction.choose_service)
async def show_doctors(message: types.Message, state: FSMContext):
    picked_service = message.text
    await state.update_data(service=picked_service)
    await state.set_state(ClientAction.choose_doctor)
    await message.answer(text='Выбрать врача:\n', reply_markup=listed_kb(req.get_employees(picked_service)))


@router.message(ClientAction.choose_doctor)
async def show_dates(message: types.Message, state: FSMContext):
    picked_doctor = message.text
    await state.update_data(employee=picked_doctor)
    await state.set_state(ClientAction.choose_date)
    await message.answer(text='Выбрать дату:\n', reply_markup=listed_kb(req.get_dates(picked_doctor), col=4))


@router.message(ClientAction.choose_date)
async def show_times(message: types.Message, state: FSMContext):
    picked_date = datetime.strptime(f'{datetime.now().year} {message.text[3:]}', '%Y %d.%m')
    await state.update_data(date=picked_date)
    await state.set_state(ClientAction.ask_name)
    user_data = await state.get_data()
    await message.answer(text='Выбрать время:\n',
                         reply_markup=listed_kb(req.get_times(picked_date, user_data['employee']), col=4))


@router.message(ClientAction.ask_name)
async def ask_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    picked_datetime = datetime.combine(user_data['date'], datetime.strptime(message.text, '%H:%M').time())
    await state.update_data(datetime=picked_datetime)
    await state.set_state(ClientAction.ask_phone)
    await message.answer(text='Введите ФИО:\n')


@router.message(ClientAction.ask_phone)
async def ask_phone(message: types.Message, state: FSMContext):
    user_name = message.text.title()
    await state.update_data(user_name=user_name)
    await state.set_state(ClientAction.ask_comment)
    await message.answer(text='Введите номер телефона:\n')


@router.message(ClientAction.ask_comment)
async def ask_comment(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await state.set_state(ClientAction.confirm_data)
    await message.answer(text=f'Введите комментарий:\n')


@router.message(ClientAction.confirm_data)
async def confirm_visit(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)
    user_data = await state.get_data()
    await state.set_state(ClientAction.end)
    await message.answer(text=f'Проверьте данные:\n'
                              f'- {user_data["service"]}\n'
                              f'- {user_data["employee"]}\n'
                              f'- {datetime.strftime(user_data["datetime"], "%d.%m.%Y %H:%M")}\n'
                              f'- {user_data["user_name"]}\n'
                              f'- {user_data["phone_number"]}\n'
                              f'- {user_data["comment"]}')


@router.message(ClientAction.end)
async def end(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Ура!')
