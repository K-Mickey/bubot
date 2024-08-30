from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class MainButtons(StrEnum):
    ADD_OUTCOME = 'Добавить расходы'
    ADD_INCOME = 'Добавить доходы'
    SHOW_ACCOUNTS = 'Посмотреть счета'
    SHOW_OUTCOMES = 'Посмотреть расходы'


def get_start_reply_kb() -> ReplyKeyboardMarkup:
    buttons = [button for button in MainButtons]
    return get_reply_kb(buttons, row_width=2)


def create_simple_str_kb_from_list_and_data(
        list_: list, data: CallbackData, row_width: int = 1) -> InlineKeyboardMarkup:
    return get_inline_kb({item: data(value=item) for item in list_}, row_width=row_width)


def get_inline_kb(buttons: dict, row_width: int = 1) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for title, callback_data in buttons.items():
        kb.button(text=title, callback_data=callback_data)
    kb.adjust(row_width)
    return kb.as_markup()


def get_reply_kb(buttons: list, row_width: int = 3) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for title in buttons:
        kb.button(text=title)
    kb.adjust(row_width)
    kb = kb.as_markup()
    kb.resize_keyboard = True
    return kb
