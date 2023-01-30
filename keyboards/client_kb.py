from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from CRMRequest import CRMRequest

req = CRMRequest()


def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    button_text = ['Запись', 'Мой аккаунт', 'Акции', 'О нас', 'Помощь']
    for text in button_text:
        kb.button(text=text)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def first_or_second_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Первичный')
    kb.button(text='Повторный')
    kb.button(text='Отмена')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def share_contact_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Поделиться контактом', request_contact=True)
    kb.button(text='Отмена')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def yes_or_no_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='✅', callback_data='yes')
    kb.button(text='❌', callback_data='no')
    kb.adjust(2)
    return kb.as_markup()


def info_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Наш сайт', url='https://ilfa-dent.ru')
    return kb.as_markup(resize_keyboard=True)


def promo_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Об акциях', url='https://ilfa-dent.ru/aktsii')
    return kb.as_markup(resize_keyboard=True)


def categories_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    categories = req.categories
    for category in categories:
        kb.button(text=category)

    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def services_kb(category: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    service_names = req.get_service_names(category)
    for name in service_names:
        kb.button(text=name)

    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)
