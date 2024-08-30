from dataclasses import dataclass
from typing import Tuple

from aiogram.fsm.context import FSMContext

from bin.states import EnumStates
from bin.utils import get_current_date


@dataclass
class Transaction:
    def __init__(self, type: str, data: dict, amount: str = '', comment: str = ''):
        """type = 'outcome' or 'income'"""
        self.date = data.get(EnumStates.DATE, get_current_date())
        if type == 'outcome':
            self.category = data.get(EnumStates.OUT_CATEGORY, 'Категория')
            self.account = data.get(EnumStates.OUT_ACCOUNT, 'Счёт')
        elif type == 'income':
            self.category = data.get(EnumStates.IN_CATEGORY, 'Категория')
            self.account = data.get(EnumStates.IN_ACCOUNT, 'Счёт')
        else:
            raise ValueError(f'Unknown type: {type}')
        self.amount = amount
        self.comment = comment

    def get_kb_args(self):
        return self.date, self.category, self.account

    def to_list(self):
        return [self.date, self.category, self.amount, self.account, self.comment]

    def is_empty_category_or_account(self):
        return 'Категория' in self.category or 'Счёт' in self.account


async def get_from_state(type: str, state: FSMContext, message: str = '') -> Transaction:
    data = await state.get_data()
    amount, comment = _parse_message(message)
    return Transaction(type, data, amount=amount, comment=comment)


def _parse_message(text: str) -> Tuple[str, str]:
    text = text.strip()
    amount = comment = ''
    for i in range(len(text)):
        char = text[i]
        if char.isdigit() or char in '=+-,':
            amount += char
        elif char == '.':
            amount += ','
        elif char == ' ':
            pass
        else:
            comment = text[i:]
            break
    return amount, comment
