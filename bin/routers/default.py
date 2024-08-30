from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bin.keyboards import get_start_reply_kb
from bin.utils import get_and_update_settings

router = Router()


@router.message(StateFilter('*'), CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await get_and_update_settings(state)
    kb = get_start_reply_kb()
    await message.answer('Здравствуйте! Данные, обновлены.', reply_markup=kb)
