from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from datetime import datetime


def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    button_text = ['Консультация 📅', 'Запись 📆', 'О нас ℹ️', 'Администратор 👩🏼‍💻', 'Помощь ❓']
    for text in button_text:
        kb.button(text=text)
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)


def share_contact_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Поделиться контактом', request_contact=True)
    kb.button(text='Отмена ❌')
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Отмена ❌')
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def info_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Наш сайт', url='https://ilfa-dent.ru')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def listed_kb(elements: list[str], col: int = 1) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for element in elements:
        kb.button(text=element)

    kb.button(text='Отмена ❌')

    kb.adjust(col)

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def listed_kb_dates(elements: list[datetime], col: int = 1) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for element in elements:
        element = element.strftime('%d.%m.%y')
        kb.button(text=element)

    kb.button(text='Отмена ❌')

    kb.adjust(col)

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def listed_kb_times(elements: list[datetime], col: int = 1) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for element in elements:
        element = element.strftime('%H:%M')
        kb.button(text=element)

    kb.button(text='Отмена ❌')

    kb.adjust(col)

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def confirm_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Да ✅')
    kb.button(text='Нет 🔄')
    kb.button(text='Отмена ❌')
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def again_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Да ✅')
    kb.button(text='Отмена ❌')
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
