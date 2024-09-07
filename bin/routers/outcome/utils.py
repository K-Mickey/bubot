import conf
from bin import google_spreadsheets, utils
from bin.states import EnumStates
from bin.transaction import Transaction


class Outcome(Transaction):
    def __init__(self, data: dict, message: str = ''):
        super().__init__(data, message)
        self.category = data.get(EnumStates.OUT_CATEGORY, 'Категория')
        self.account = data.get(EnumStates.OUT_ACCOUNT, 'Счёт')

    def get_kb_args(self):
        return self.date, self.category, self.account

    def to_list(self):
        return [self.date, self.category, self.amount, self.account, self.comment]

    def is_empty(self):
        return 'Категория' in self.category or 'Счёт' in self.account


def get_last_outcomes(count: int = 1) -> str:
    values = get_last_values_from_sheet(count)
    return utils.format_sheet_values_to_text(values)


def get_last_values_from_sheet(count: int = 1) -> list:
    values = google_spreadsheets.get_values(
        conf.SHEET_ID,
        conf.OUTCOME_GET_RANGE,
    ).get('values', [])
    return values[-count:]


def append_to_sheet(values: list) -> dict:
    return google_spreadsheets.append_values(
        conf.SHEET_ID,
        conf.OUTCOME_APPEND_RANGE,
        'USER_ENTERED',
        [values],
    )
