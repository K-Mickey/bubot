from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class OutcomeData(CallbackData, prefix='outcome'):
    value: str


class OutcomeCategoryData(CallbackData, prefix='outcome_category'):
    value: str


class OutcomeAccountData(CallbackData, prefix='outcome_account'):
    value: str


class OutcomeState(StatesGroup):
    active = State()
