from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
DB_PATH = 'src/bot.sqlite3'
SHEET_ID = env.str('SHEET_ID')
CREDENTIALS_FILE = 'bin/google_creds.json'

LOG_LEVEL = env.str('LOG_LEVEL', 'INFO')
LOG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s - %(filename)s] > %(lineno)d - %(message)s'
LOG_PATH = Path('src/logs')

SETTING_RANGE = 'Настройки!A3:D35'
OUTCOME_APPEND_RANGE = 'Расходы!A1'
OUTCOME_GET_RANGE = 'Расходы!A2:E'
MAIN_ACCOUNT_RANGE = 'Главная!A2:C'
MAIN_OUTCOME_RANGE = 'Главная!D2:G'
INCOME_APPEND_RANGE = 'Доходы!A1'
INCOME_GET_RANGE = 'Доходы!A2:E'
TRANSFER_APPEND_RANGE = 'Переводы!A1'
TRANSFER_GET_RANGE = 'Переводы!A2:E'
