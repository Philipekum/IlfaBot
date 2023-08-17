from datetime import datetime
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text
from exceptions import ElementNotFoundError
from CrmRequest import CrmRequest
from keyboards.client_kb import listed_kb, listed_kb_dates, listed_kb_times, share_contact_kb, cancel_kb, confirm_kb, \
    main_kb
import asyncio
from handlers.client_visit import get_crm_and_data
from texts import json_reader

router = Router()
text = json_reader.read_json_file('texts/text_client_visit.json')


class ConsultationProcess(StatesGroup):
    choose_doctor = State()
    choose_date = State()
    choose_time = State()
    ask_name = State()
    ask_phone = State()
    ask_comment = State()
    confirm_data = State()
    end = State()
    again = State()


@router.message(Text(startswith='Консультация', ignore_case=True))
async def show_employees(message: types.Message, state: FSMContext):
    crm = CrmRequest()
    picked_service = 'Прием (осмотр, консультация) врача-стоматолога первичный'
    await state.update_data(crm=crm)
    await state.update_data(picked_service=picked_service)

    await state.set_state(ConsultationProcess.choose_doctor)
    await asyncio.sleep(0.5)

    await message.answer(text=text['choose_doctor'], reply_markup=listed_kb(crm.get_employees(picked_service)))


@router.message(ConsultationProcess.choose_doctor)
async def show_dates(message: types.Message, state: FSMContext):
    picked_employee = message.text
    await state.update_data(picked_employee=picked_employee)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ConsultationProcess.choose_date)
    await asyncio.sleep(0.5)

    await message.answer(text=text['choose_date'],
                         reply_markup=listed_kb_dates(crm.get_dates(picked_employee), col=3))


@router.message(ConsultationProcess.choose_date)
async def show_times(message: types.Message, state: FSMContext):
    picked_date = datetime.strptime(message.text, '%d.%m.%y')
    await state.update_data(picked_date=picked_date)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ConsultationProcess.choose_time)
    await asyncio.sleep(0.5)

    await message.answer(text=text['choose_time'],
                         reply_markup=listed_kb_times(crm.get_times(picked_date, user_data['picked_employee']), col=4))


@router.message(ConsultationProcess.choose_time)
async def ask_name(message: types.Message, state: FSMContext):
    picked_time = datetime.strptime(message.text, '%H:%M')
    await state.update_data(picked_time=picked_time)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ConsultationProcess.ask_name)
    await asyncio.sleep(0.5)

    await message.answer(text=text['ask_name'])


@router.message(ConsultationProcess.ask_name)
async def ask_phone(message: types.Message, state: FSMContext):
    user_name = message.text.title()
    await state.update_data(user_name=user_name)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ConsultationProcess.ask_phone)
    await asyncio.sleep(0.5)

    await message.answer(text=text['ask_phone'], reply_markup=share_contact_kb())


@router.message(ConsultationProcess.ask_phone)
async def ask_comment(message: types.Message, state: FSMContext):
    crm, user_data = await get_crm_and_data(state)

    try:
        if hasattr(message.contact, 'phone_number'):
            user_number = crm.format_phone_number(message.contact.phone_number)

        else:
            user_number = crm.format_phone_number(message.text)

    except ElementNotFoundError:
        await message.answer(text=text['wrong_number'], reply_markup=share_contact_kb())
        await state.set_state(ConsultationProcess.ask_phone)

    else:
        await state.update_data(user_number=user_number)

        await state.set_state(ConsultationProcess.ask_comment)
        await asyncio.sleep(0.5)

        await message.answer(text=text['ask_comment'], reply_markup=cancel_kb())


@router.message(ConsultationProcess.ask_comment)
async def confirm_visit(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)

    crm, user_data = await get_crm_and_data(state)

    await state.set_state(ConsultationProcess.confirm_data)
    await asyncio.sleep(0.5)

    await message.answer(text=text['confirm_data'].format(user_data["picked_service"],
                                                          user_data["picked_employee"],
                                                          datetime.strftime(user_data["picked_date"], "%d.%m.%Y"),
                                                          datetime.strftime(user_data["picked_time"], "%H:%M"),
                                                          user_data["user_name"],
                                                          user_data["user_number"],
                                                          user_data["comment"]),
                         reply_markup=confirm_kb(no_required=True))


@router.message(ConsultationProcess.confirm_data)
async def visit_confirmed(message: types.Message, state: FSMContext):
    if 'Да' in message.text:
        await state.clear()
        await asyncio.sleep(0.5)

        await message.answer(text=text['confirmed'],
                             reply_markup=main_kb())

    elif 'Нет' in message.text:
        await state.set_state(ConsultationProcess.again)
        await asyncio.sleep(0.5)

        await message.answer(text=text['again'], reply_markup=confirm_kb())


@router.message(ConsultationProcess.again)
async def end(message: types.Message, state: FSMContext):
    if 'Да' in message.text:
        await state.set_state(ConsultationProcess.choose_doctor)
        crm, user_data = await get_crm_and_data(state)
        await asyncio.sleep(0.5)

        await message.answer(text=text['choose_doctor'], reply_markup=listed_kb(crm.get_employees()))
