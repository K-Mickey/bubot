from enum import StrEnum

from aiogram.types import InlineKeyboardMarkup

from bin.keyboards import get_inline_kb
from bin.routers.outcome.states import OutcomeData


class OutcomeButtons(StrEnum):
    DATE = 'date'
    CATEGORY = 'category'
    ACCOUNT = 'main'


def get_outcome_kb(date: str, category: str, account: str) -> InlineKeyboardMarkup:
    return get_inline_kb({
        date: OutcomeData(value=OutcomeButtons.DATE),
        category: OutcomeData(value=OutcomeButtons.CATEGORY),
        account: OutcomeData(value=OutcomeButtons.ACCOUNT),
    })

