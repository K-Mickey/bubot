from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup


class IncomeState(StatesGroup):
    active = State()


class IncomeData(CallbackData, prefix='income'):
    value: str


class IncomeCategoryData(CallbackData, prefix='income_category'):
    value: str


class IncomeAccountData(CallbackData, prefix='income_account'):
    value: str
