import conf
from bin import google_spreadsheets, utils


def append_to_sheet(values: list) -> dict:
    return google_spreadsheets.append_values(
        conf.SHEET_ID,
        conf.INCOME_APPEND_RANGE,
        'USER_ENTERED',
        [values],
    )


def get_last_incomes(count: int = 1) -> str:
    values = get_last_values_from_sheet(count)
    return utils.get_text_from_sheet_values(values)


def get_last_values_from_sheet(count: int = 1) -> list:
    values = google_spreadsheets.get_values(
        conf.SHEET_ID,
        conf.INCOME_GET_RANGE,
    ).get('values', [])
    return values[-count:]
