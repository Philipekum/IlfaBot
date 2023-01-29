import re
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text
from keyboards.client_kb import share_contact_kb, yes_or_no_kb
from crm_connection import CRMRequest
from config import config

router = Router()

req = CRMRequest.CRMRequest(url=config.url.get_secret_value(),
                            token=config.crm_token.get_secret_value())


class ClientVisit(StatesGroup):
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
    await state.set_state(ClientVisit.wait_category)
    #   сделать запрос getServices
    req.get_command('getEmployees')
    # сохранить в память
    #   найти категории и перечислить ниже
    await message.answer(text='Выбрать категорию услуг:\n')


@router.message(ClientVisit.wait_category)
async def got_category(message: types.Message, state: FSMContext):
    await state.set_state(ClientVisit.wait_service)
    #   соотнести ответ пользователя и категории услуг из памяти
    #   вывести список услуг ниже
    await message.answer(text='Выбрать услугу:')


@router.message(ClientVisit.wait_service)
async def got_service(message: types.Message, state: FSMContext):
    await state.set_state(ClientVisit.wait_doctor)
    #   сохранить услугу в память
    #   сделать запрос getEmployees
    #   сохранить в память
    #   вывести список врачей с такой услугой ниже
    await message.answer(text='Выбрать врача:')


@router.message(ClientVisit.wait_doctor)
async def got_doctor(message: types.Message, state: FSMContext):
    await state.set_state(ClientVisit.wait_time)
    #   сохранить врача в память
    #   сделать запрос про доступные даты и время
    await message.answer(text='Выбрать время:')


@router.message(ClientVisit.wait_time)
async def got_time(message: types.Message, state: FSMContext):
    await state.set_state(ClientVisit.wait_name)
    #   занести дату и время в память
    await message.answer(text='Введите Ваше ФИО:')


@router.message(ClientVisit.wait_name)
async def got_name(message: types.Message, state: FSMContext):
    await state.set_state(ClientVisit.wait_number)
    await message.answer(text='Введите Ваш номер телефона в формате +7(xxx)xxx-xx-xx:')


@router.message(ClientVisit.wait_number)
async def got_number(message: types.Message, state: FSMContext):
    await state.set_state(ClientVisit.wait_commentary)
    await message.answer(text='Введите комментарии:')


@router.message(ClientVisit.wait_commentary)
async def got_commentary(message: types.Message, state: FSMContext):
    await state.set_state(ClientVisit.wait_confirm)
    await message.answer(text='Подтвердите правильность введенных данных и подтвердите обработку персональных данных.')
