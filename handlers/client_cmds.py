from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text
from keyboards.client_kb import main_kb, first_or_second_kb, info_kb, promo_kb

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()

    await message.answer(text=f'Привет, <b>{message.from_user.full_name}</b>! Это стоматологическаяL клиника Илфа.',
                         reply_markup=main_kb())


@router.message(Command('help'))
@router.message(Text('Помощь', ignore_case=True))
async def cmd_help(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text='<b>Помощь</b>\n'
                              '/start - перейти на главную страницу\n'
                              '/back или "Назад"- вернуться назад\n'
                              '/help или "Помощь" - оказаться тут\n\n'
                              '<b>Запись</b>\n'
                              '/first - записаться на первичный прием\n'
                              '/doctor - записаться к врачу (для авторизованных пользователей\n\n'
                              '<b>Мой аккаунт</b>\n'
                              '/history - посмотреть историю моих записей\n'
                              '/exit - выйти из аккаунта\n'
                              '/login - пройти аутентификацию\n\n',
                         reply_markup=main_kb())


@router.message(Text('Отмена', ignore_case=True))
@router.message(Command('cancel'))
async def cmd_back(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(text='Нет активных команд для отмены.', reply_markup=main_kb())

    else:
        await message.answer(text='Команда отменена.', reply_markup=main_kb())


@router.message(Text('Запись', ignore_case=True))
async def cmd_registration(message: types.Message):
    await message.answer(text='Вы хотите записаться на первичный прием или на повторный?',
                         reply_markup=first_or_second_kb())


@router.message(Text(['инфо', 'о нас'], ignore_case=True))
async def cmd_info(message: types.Message):
    await message.answer(text='<b>Центр современной стоматологии «IL\'FA»</b>\n\n'
                              'Наша клиника занимает почетное место среди наиболее прогрессивных стоматологических '
                              'центров Москвы. Мы предоставляем стоматологические услуги в соответствии с высокими '
                              'международными стандартами.',
                         reply_markup=info_kb())


@router.message(Text(['промо', 'акции', 'промоакции'], ignore_case=True))
async def cmd_promo(message: types.Message):
    await message.answer(text='Здесь вы можете ознакомиться со всеми промоакциями нашей стоматологической клиники!',
                         reply_markup=promo_kb())
