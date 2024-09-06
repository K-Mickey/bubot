from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bin.routers import default
from bin.routers.main import handlers as account
from bin.routers.outcome import handlers as outcome
from bin.routers.income import handlers as income
from bin.routers.transfer import handlers as transfer


async def run(token: str) -> None:
    bot = Bot(token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        default.router,
        account.router,
        outcome.router,
        income.router,
        transfer.router,
    )

    await set_default_commands(bot)
    await dp.start_polling(bot)


async def set_default_commands(bot: Bot) -> None:
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
    ])
