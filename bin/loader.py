from AiogramStorages.storages import SQLiteStorage
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import conf
from bin.routers import default
from bin.routers.main import handlers as account
from bin.routers.outcome import handlers as outcome
from bin.routers.income import handlers as income
from bin.routers.transfer import handlers as transfer
from bin.utils import get_logger


logger = get_logger('loader.log', __name__)


async def run(token: str) -> None:
    bot = Bot(token)
    storage = get_storage()
    dp = Dispatcher(storage=storage)
    include_routers(dp)

    await set_default_commands(bot)
    await dp.start_polling(bot)
    logger.info('Bot started')


def get_storage() -> MemoryStorage:
    """Place to set storage"""
    logger.debug('Created memory storage')
    return SQLiteStorage(db_path=conf.DB_PATH)


def include_routers(dp: Dispatcher) -> None:
    routers = get_routers()
    dp.include_routers(*routers)
    logger.debug(f'Included routers: {routers}')


def get_routers() -> tuple:
    """Add routers here"""
    return (
        default.router,
        account.router,
        outcome.router,
        income.router,
        transfer.router,
    )


async def set_default_commands(bot: Bot) -> None:
    commands = get_commands()
    await bot.set_my_commands(commands)
    logger.debug(f'Set default commands: {commands}')


def get_commands() -> list:
    """Add default commands here"""
    return [
        BotCommand(command="start", description="Запустить бота"),
    ]
