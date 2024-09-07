from abc import abstractmethod
from typing import Tuple

from bin.states import EnumStates
from bin.utils import get_current_date


class Transaction:
    """Base class for all transactions"""
    def __init__(self, data: dict, message: str = ''):
        """
        :param data: dict with date key
        :param message: message from user
        """
        amount, comment = self._parse_message(message)
        self.date = data.get(EnumStates.DATE, get_current_date())
        self.amount = amount
        self.comment = comment

    @abstractmethod
    def get_kb_args(self):
        """Data for keyboard"""
        pass

    @abstractmethod
    def to_list(self):
        """All data in one list. Order is important for sheet"""
        pass

    @abstractmethod
    def is_empty(self):
        """Check if transaction is empty"""
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
