import unicodedata

import conf
from bin import google_spreadsheets


def get_accounts() -> str:
    values = get_accounts_from_sheet()
    return form_text_from_values(values)


def get_outcomes(is_overspending: bool = False) -> str:
    values = get_outcomes_from_sheet()
    return form_text_from_values(values, is_overspending)


def form_text_from_values(values: list, is_overspending: bool = False) -> str:
    strings = decode_and_join_strings(values, is_overspending)
    set_headings(strings)
    return '\n'.join(strings)


def decode_and_join_strings(
    strings: list, is_overspending: bool = False, sep: str = ' | '
) -> list:
    join_strings = []
    for string in strings:
        if not string or not string[0]:
            continue

        string = list(map(lambda x: unicodedata.normalize('NFKD', x), string))
        if is_overspending:
            highlight_overspending(string)

        join_strings.append(f'{string[0]:<10}{sep}' + sep.join(string[1:]))
    return join_strings


def set_headings(strings: list) -> None:
    if len(strings) > 1:
        strings[0] = f'<u><i>{strings[0]}</i></u>'
        strings[1] = f'<b>{strings[1]}</b>'


def highlight_overspending(string: list) -> None:
    if not string or len(string[0]) < 3:
        print('No values in sheet')
        return

    try:
        if to_float(string[1]) > to_float(string[2]):
            string[0] = f'<u>{string[0]}'
            string[-1] = f'{string[-1]}</u>'
    except ValueError:
        print(f'String {string} is not contains float value')


def to_float(value: str) -> float:
    return float(value.replace(',', '.').replace(' ', ''))


def get_accounts_from_sheet() -> list:
    return google_spreadsheets.get_values(
        conf.SHEET_ID,
        conf.MAIN_ACCOUNT_RANGE,
    )


def get_outcomes_from_sheet() -> list:
    return google_spreadsheets.get_values(
        conf.SHEET_ID,
        conf.MAIN_OUTCOME_RANGE,
    )
