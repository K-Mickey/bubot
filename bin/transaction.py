from abc import abstractmethod
from dataclasses import dataclass
from typing import Tuple

from aiogram.fsm.context import FSMContext

from bin.states import EnumStates
from bin.utils import get_current_date


class Transaction:
    def __init__(self, data: dict, message: str = ''):
        """type = 'outcome' or 'income'"""
        amount, comment = self._parse_message(message)
        self.date = data.get(EnumStates.DATE, get_current_date())
        self.amount = amount
        self.comment = comment

    @abstractmethod
    def get_kb_args(self):
        pass

    @abstractmethod
    def to_list(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @staticmethod
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
