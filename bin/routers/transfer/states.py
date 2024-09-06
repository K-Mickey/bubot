from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class TransferState(StatesGroup):
    active = State()


class TransferData(CallbackData, prefix='transfer'):
    value: str


class TransferFromData(CallbackData, prefix='transfer_from'):
    value: str


class TransferToData(CallbackData, prefix='transfer_to'):
    value: str
