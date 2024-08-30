import functools

import apiclient
import httplib2
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

import conf


def log_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as error:
            print(f'An error occurred: {error}')

    return wrapper


@log_error
def append_values(sheet_id: str, range_: str, value_input_option: str, values: list) -> dict:
    service = connect()
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_,
        valueInputOption=value_input_option,
        body=body
    ).execute()
    return result


@log_error
def get_values(sheet_id: str, range_: str, major_dimension: str = 'ROWS') -> dict:
    service = connect()
    values = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_,
        majorDimension=major_dimension,
    ).execute()
    return values


def connect() -> apiclient.discovery.Resource:
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        conf.CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
    )
    http_auth = creds.authorize(httplib2.Http())
    return apiclient.discovery.build('sheets', 'v4', http=http_auth)
