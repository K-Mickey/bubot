from datetime import datetime
from typing import Tuple

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import conf
from bin import google_spreadsheets
from bin.states import EnumStates


async def get_and_update_settings(state: FSMContext) -> None:
    settings_values = google_spreadsheets.get_values(
        conf.SHEET_ID,
        conf.SETTING_RANGE,
        major_dimension='COLUMNS',
    )
    if not isinstance(settings_values, dict):
        print('No values in settings sheet')
    else:
        await update_state_data(state, settings_values)


async def update_state_data(state: FSMContext, settings_values: dict) -> None:
    accounts, outcome_categories, _, income_categories = settings_values['values']
    accounts = tuple(account for account in accounts if account)
    outcome_categories = tuple(category for category in outcome_categories if category)
    income_categories = tuple(category for category in income_categories if category)

    await state.update_data({
            EnumStates.ACCOUNTS: accounts,
            EnumStates.OUTCOME_CATEGORIES: outcome_categories,
            EnumStates.INCOME_CATEGORIES: income_categories,
        })


def get_current_date() -> str:
    return datetime.date(datetime.now()).strftime('%d.%m.%Y')


async def get_message_and_answer_query(callback_query: CallbackQuery) -> Message:
    await callback_query.answer()
    return callback_query.message


def get_count_from_show_message(message: str) -> int:
    message = message.strip()
    _, count = message.split(' ', 1)
    if count.isdigit():
        return int(count)
    else:
        return 1


def get_text_from_sheet_values(values: list) -> str:
    strings = []
    for string in values:
        strings.append(' | '.join(map(lambda x: x.encode().decode(), string)))
    return '\n'.join(strings)
