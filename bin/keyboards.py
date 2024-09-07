from enum import StrEnum
from typing import Type

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bin.utils import get_logger


logger = get_logger('keyboards.log', __name__)


class MainButtons(StrEnum):
    """Buttons in main reply keyboard"""
    ADD_OUTCOME = 'Добавить расходы'
    ADD_INCOME = 'Добавить доходы'
    SHOW_OUTCOMES = 'Посмотреть расходы'
    SHOW_ACCOUNTS = 'Посмотреть счета'
    ADD_TRANSACTION = 'Добавить транзакцию'


def get_main_reply_kb() -> ReplyKeyboardMarkup:
    buttons = [button for button in MainButtons]
    return get_reply_kb(buttons, row_width=2)


def get_inline_kb_from_list(list_: list, data: Type[CallbackData], row_width: int = 1) -> InlineKeyboardMarkup:
    buttons = {item: data(value=item) for item in list_}
    return get_inline_kb(buttons, row_width=row_width)


def get_inline_kb(buttons: dict, row_width: int = 1) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for title, callback_data in buttons.items():
        kb.button(text=title, callback_data=callback_data)
    kb.adjust(row_width)
    logger.debug(f'Created inline keyboard with {buttons}')
    return kb.as_markup()


def get_reply_kb(buttons: list, row_width: int = 3) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for title in buttons:
        kb.button(text=title)
    kb.adjust(row_width)
    kb = kb.as_markup()
    kb.resize_keyboard = True
    logger.debug(f'Created reply keyboard with {buttons}')
    return kb
