import re
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Text
from keyboards.client_kb import share_contact_kb

router = Router()


class FirstVisit(StatesGroup):
    waiting_for_name = State()
    waiting_for_birthday = State()
    waiting_for_number = State()


@router.message(Text('Первичный', ignore_case=True))
async def first_reg_start(message: types.Message, state: FSMContext):
    await state.set_state(FirstVisit.waiting_for_name)
    await message.answer(text='Регистрация на первичный прием:\nВведите Ваше ФИО:')


@router.message(FirstVisit.waiting_for_name)
async def got_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text.title().split())
    user_data = await state.get_data()
    await state.set_state(FirstVisit.waiting_for_birthday)
    await message.answer(
        text=f'<i>Отлично, вот ваши данные:</i>\n'
             f'<b>ФИО</b>: <u>{" ".join(map(str, user_data["user_name"]))}</u>\n\n'
             f'<i>Теперь введите Вашу дату рождения в формате ДД.ММ.ГГГГ:</i>')


@router.message(FirstVisit.waiting_for_birthday)
async def got_birthday(message: types.Message, state: FSMContext):
    user_input = re.search(r'^\d{2}\.\d{2}\.\d{4}$', message.text)
    if user_input is None:
        await message.answer(
            text='Неверный ввод данных!\n'
                 '<i>Введите данные в формате ДД.ММ.ГГГГ:</i>')
        await state.set_state(FirstVisit.waiting_for_birthday)
        return
    else:
        await state.update_data(user_birthday=user_input.group())

    user_data = await state.get_data()
    await state.set_state(FirstVisit.waiting_for_number)
    await message.answer(
        text=f'<i>Отлично, вот ваши данные:</i>\n'
             f'<b>ФИО</b>: <u>{" ".join(map(str, user_data["user_name"]))}</u>\n'
             f'<b>Дата рождения</b>: <u>{user_data["user_birthday"]}</u>\n\n'
             f'<i>Теперь, пожалуйста, поделитесь номером телефона или вбейте его вручную:</i>',
        reply_markup=share_contact_kb())


@router.message(FirstVisit.waiting_for_number)
async def got_number(message: types.Message, state: FSMContext):
    if hasattr(message.contact, 'phone_number'):
        await state.update_data(user_number=message.contact.phone_number)
    else:
        user_input = re.search(r'^\+?\d?\D?(\D?\d\D?\D?){10}$', message.text)
        if user_input is None:
            await message.answer(text='Неправильный номер телефона!\nПопробуйте еще раз!')
            await state.set_state(FirstVisit.waiting_for_number)
        else:
            await state.update_data(user_number=message.text)

    user_data = await state.get_data()
    await message.answer(
        text=f'<i>Отлично, вот ваши данные:</i>\n'
             f'<b>ФИО</b>: <u>{" ".join(map(str, user_data["user_name"]))}</u>\n'
             f'<b>Дата рождения</b>: <u>{user_data["user_birthday"]}</u>\n'
             f'<b>Номер телефона</b>: <u>{user_data["user_number"]}</u>\n\n'
             f'<i>Все верно?</i>')


@router.callback_query(Text(text='yes'))
async def inl_success(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text='Вы зарегистрированы!', reply_markup=None)
    await state.clear()
    await callback_query.answer()


@router.callback_query(Text(text='no'))
async def inl_denied(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text='Регистрация не пройдена, попробуйте еще раз!', reply_markup=None)
    await state.clear()
    await callback_query.answer()
