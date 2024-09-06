from enum import StrEnum

from aiogram.types import InlineKeyboardMarkup

from bin.keyboards import get_inline_kb
from bin.routers.transfer.states import TransferData


class TransferButtons(StrEnum):
    DATE = 'date'
    ACCOUNT_FROM = 'account_from'
    ACCOUNT_TO = 'account_to'


def get_transfer_kb(date: str, account_from: str, account_to: str) -> InlineKeyboardMarkup:
    return get_inline_kb({
        date: TransferData(value=TransferButtons.DATE),
        account_from: TransferData(value=TransferButtons.ACCOUNT_FROM),
        account_to: TransferData(value=TransferButtons.ACCOUNT_TO),
    })
