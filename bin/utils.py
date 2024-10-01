import os
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import conf
from bin import google_spreadsheets
from bin.logger import get_logger
from bin.states import EnumStates


async def get_and_update_settings(state: FSMContext) -> None:
    settings_values = google_spreadsheets.get_values(
        conf.SHEET_ID,
        conf.SETTING_RANGE,
        major_dimension='COLUMNS',
    )
    if not settings_values:
        logger.info('Settings not found')
    else:
        await update_state_data(state, settings_values)


async def update_state_data(state: FSMContext, values: list) -> None:
    """
    Important!
    Values order depends on Sheet's order
    """
    accounts, outcome_categories, _, income_categories = values
    accounts = tuple(account for account in accounts if account)
    outcome_categories = tuple(
        category for category in outcome_categories if category
    )
    income_categories = tuple(
        category for category in income_categories if category
    )

    await state.update_data(
        {
            EnumStates.ACCOUNTS: accounts,
            EnumStates.OUTCOME_CATEGORIES: outcome_categories,
            EnumStates.INCOME_CATEGORIES: income_categories,
        }
    )

    logger.debug(f'{accounts=}')
    logger.debug(f'{outcome_categories=}')
    logger.debug(f'{income_categories=}')


def get_current_date() -> str:
    return datetime.date(datetime.now()).strftime('%d.%m.%Y')


async def get_message_and_callback_answer(
    callback_query: CallbackQuery,
) -> Message:
    await callback_query.answer()
    return callback_query.message


def get_count_from_message(message: str) -> int:
    """example: "Покажи 5" -> 5"""
    message = message.strip()
    _, count = message.split(' ', 1)
    logger.debug(count)
    if count.isdigit():
        return int(count)
    return 1


def format_sheet_values_to_text(values: list) -> str:
    strings = []
    for string in values:
        strings.append(' | '.join(map(lambda x: x.encode().decode(), string)))
    logger.debug(strings)
    return '\n'.join(strings)


logger = get_logger('utils.log', __name__)
