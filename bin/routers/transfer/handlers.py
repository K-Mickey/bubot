from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from bin import utils
from bin.keyboards import MainButtons, get_inline_kb_from_list
from bin.routers.transfer import utils as tr_utils
from bin.routers.transfer.keyboards import get_transfer_kb, TransferButtons
from bin.routers.transfer.states import TransferState, TransferData, TransferFromData, TransferToData
from bin.states import EnumStates

router = Router()


@router.message(F.text == MainButtons.ADD_TRANSACTION)
async def start_transfer(message: Message, state: FSMContext, edit_last_message: bool = False):
    await state.set_state(TransferState.active)
    data = await state.get_data()
    transaction = tr_utils.Transfer(data)

    kb = get_transfer_kb(*transaction.get_kb_args())
    text = ('<u>Настройте параметры через <b>клавиатуру</b>.</u>\n\n'
            'Введите <b>сумму перевода</b> и <b>комментарий</b> <i>через пробел</i>.\n'
            'Введите <b>Покажи <i>n</i></b>, для показа последних <i>n</i> переводов.')

    if edit_last_message:
        await message.edit_text(text, reply_markup=kb, parse_mode='HTML')
    else:
        await message.answer(text, reply_markup=kb, parse_mode='HTML')


@router.message(TransferState.active, F.text.regexp(r'\d+(,\d+)?'))
async def append_transfer(message: Message, state: FSMContext):
    data = await state.get_data()
    transaction = tr_utils.Transfer(data, message.text)
    if transaction.is_empty():
        await message.answer('Необходимо выбрать хоть один счёт')
    else:
        answer = tr_utils.append_to_sheet(transaction.to_list())
        await message.answer(f'Перевод добавлен {answer["updates"]["updatedRange"]}')


@router.message(TransferState.active, F.text.contains('Покажи'))
async def get_transfer(message: Message, state: FSMContext):
    count = utils.get_count_from_message(message.text)
    text = tr_utils.get_last_transactions(count)
    await message.answer(text)


@router.callback_query(TransferState.active, TransferData.filter(F.value == TransferButtons.DATE))
async def choose_date(callback_query: CallbackQuery, state: FSMContext):
    message = await utils.get_message_and_callback_answer(callback_query)
    await message.edit_text('Выберите дату', reply_markup=await SimpleCalendar().start_calendar())


@router.callback_query(TransferState.active, TransferData.filter(F.value == TransferButtons.ACCOUNT_FROM))
async def choose_account_from(callback_query: CallbackQuery, state: FSMContext):
    message = await utils.get_message_and_callback_answer(callback_query)
    data = await state.get_data()
    accounts = data.get(EnumStates.ACCOUNTS)

    if not accounts:
        text = 'Произошла ошибка. Нет доступных счетов. Выберите команду /start'
        await message.edit_text(text)
        print('No accounts')
    else:
        text = 'Выберите счёт'
        kb = get_inline_kb_from_list(accounts, TransferFromData)
        await message.edit_text(text, reply_markup=kb)


@router.callback_query(TransferState.active, TransferData.filter(F.value == TransferButtons.ACCOUNT_TO))
async def choose_account_to(callback_query: CallbackQuery, state: FSMContext):
    message = await utils.get_message_and_callback_answer(callback_query)
    data = await state.get_data()
    accounts = data.get(EnumStates.ACCOUNTS)

    if not accounts:
        text = 'Произошла ошибка. Нет доступных счетов. Выберите команду /start'
        await message.edit_text(text)
        print('No accounts')
    else:
        text = 'Выберите счёт'
        kb = get_inline_kb_from_list(accounts, TransferToData)
        await message.edit_text(text, reply_markup=kb)


@router.callback_query(TransferState.active, SimpleCalendarCallback.filter())
async def process_dialog_calendar(
        callback_query: CallbackQuery, state: FSMContext, callback_data: SimpleCalendarCallback):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    message = await utils.get_message_and_callback_answer(callback_query)

    if selected:
        await callback_query.answer(f'{date.strftime("%d/%m/%Y")}')
        await state.update_data({EnumStates.DATE: date.strftime('%d.%m.%Y')})
        await message.delete()
        await start_transfer(message, state)


@router.callback_query(TransferState.active, TransferFromData.filter())
async def set_transfer_from(callback_query: CallbackQuery, state: FSMContext, callback_data: TransferFromData):
    message = await utils.get_message_and_callback_answer(callback_query)
    await state.update_data({EnumStates.TRANSFER_FROM: callback_data.value})
    await message.delete()
    await start_transfer(message, state)


@router.callback_query(TransferState.active, TransferToData.filter())
async def set_transfer_to(callback_query: CallbackQuery, state: FSMContext, callback_data: TransferToData):
    message = await utils.get_message_and_callback_answer(callback_query)
    await state.update_data({EnumStates.TRANSFER_TO: callback_data.value})
    await message.delete()
    await start_transfer(message, state)
