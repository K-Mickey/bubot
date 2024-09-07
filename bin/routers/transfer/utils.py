import conf
from bin import google_spreadsheets, utils
from bin.states import EnumStates
from bin.transaction import Transaction


class Transfer(Transaction):
    def __init__(self, data: dict, message: str = ''):
        super().__init__(data, message)
        self.account_from = data.get(EnumStates.TRANSFER_FROM, 'Счёт списания')
        self.account_to = data.get(EnumStates.TRANSFER_TO, 'Счёт пополнения')

    def get_kb_args(self):
        return self.date, self.account_from, self.account_to

    def to_list(self):
        return [self.date, self.account_from, self.account_to, self.amount, self.comment]

    def is_empty(self):
        return 'Счёт списания' in self.account_from and 'Счёт пополнения' in self.account_to


def append_to_sheet(values: list) -> dict:
    return google_spreadsheets.append_values(
        conf.SHEET_ID,
        conf.TRANSFER_APPEND_RANGE,
        'USER_ENTERED',
        [values],
    )


def get_last_transactions(count: int = 1) -> str:
    values = get_last_values_from_sheet(count)
    return utils.format_sheet_values_to_text(values)


def get_last_values_from_sheet(count: int = 1) -> list:
    values = google_spreadsheets.get_values(
        conf.SHEET_ID,
        conf.TRANSFER_GET_RANGE,
    ).get('values', [])
    return values[-count:]
