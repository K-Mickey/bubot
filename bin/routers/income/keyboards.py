from enum import StrEnum

from aiogram.types import InlineKeyboardMarkup

from bin.keyboards import get_inline_kb
from bin.routers.income.states import IncomeData


class IncomeButtons(StrEnum):
    DATE = 'date'
    CATEGORY = 'category'
    ACCOUNT = 'main'


def get_income_kb(date: str, category: str, account: str) -> InlineKeyboardMarkup:
    return get_inline_kb({
        date: IncomeData(value=IncomeButtons.DATE),
        category: IncomeData(value=IncomeButtons.CATEGORY),
        account: IncomeData(value=IncomeButtons.ACCOUNT),
    })
