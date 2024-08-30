from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from bin.keyboards import MainButtons
import bin.routers.main.utils as main_utils


router = Router()


@router.message(StateFilter('*'), F.text == MainButtons.SHOW_ACCOUNTS)
async def show_accounts(message: Message):
    text = main_utils.get_accounts()
    await message.answer(text, parse_mode='HTML')


@router.message(StateFilter('*'), F.text == MainButtons.SHOW_OUTCOMES)
async def show_outcomes(message: Message):
    text = main_utils.get_outcomes(is_overspending=True)
    await message.answer(text, parse_mode='HTML')
