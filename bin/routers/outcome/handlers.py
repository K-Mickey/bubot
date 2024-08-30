from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from bin import utils, transaction
from bin.keyboards import MainButtons, create_simple_str_kb_from_list_and_data
from bin.routers.outcome import utils as out_utils
from bin.routers.outcome.keyboards import get_outcome_kb, OutcomeButtons
from bin.routers.outcome.states import OutcomeState, OutcomeData, OutcomeCategoryData, OutcomeAccountData
from bin.states import EnumStates


router = Router()


@router.message(F.text == MainButtons.ADD_OUTCOME)
async def start_outcome(message: Message, state: FSMContext, edit_last_message: bool = False):
    await state.set_state(OutcomeState.active)
    trans = await transaction.get_from_state('outcome', state)

    kb = get_outcome_kb(*trans.get_kb_args())
    text = ('<u>Настройте параметры через <b>клавиатуру</b>.</u>\n\n'
            'Введите <b>сумму расходов</b> и <b>комментарий</b> <i>через пробел</i>.\n'
            'Введите <b>Покажи <i>n</i></b>, для показа последних <i>n</i> расходов.')

    if edit_last_message:
        await message.edit_text(text, reply_markup=kb, parse_mode='HTML')
    else:
        await message.answer(text, reply_markup=kb, parse_mode='HTML')


@router.message(OutcomeState.active, F.text.regexp(r'\d+(,\d+)?'))
async def append_outcome(message: Message, state: FSMContext):
    trans = await transaction.get_from_state('outcome', state, message.text)
    if trans.is_empty_category_or_account():
        await message.answer('Необходимо выбрать категорию и счёт')
    else:
        answer = out_utils.append_to_sheet(trans.to_list())
        await message.answer(f'Расходы добавлены {answer['updates']['updatedRange']}')


@router.message(OutcomeState.active, F.text.contains('Покажи'))
async def get_outcome(message: Message, state: FSMContext):
    count = utils.get_count_from_show_message(message.text)
    text = out_utils.get_last_outcomes(count)
    await message.answer(text)


@router.callback_query(OutcomeState.active, OutcomeData.filter(F.value == OutcomeButtons.CATEGORY))
async def choose_category(callback_query: CallbackQuery, state: FSMContext, callback_data: OutcomeData):
    message = await utils.get_message_and_answer_query(callback_query)
    data = await state.get_data()
    outcome_categories = data.get(EnumStates.OUTCOME_CATEGORIES, [])

    if not outcome_categories:
        await message.edit_text('Произошла ошибка. Нет доступных категорий. Выберите команду /start')
        print('No category')
    else:
        kb = create_simple_str_kb_from_list_and_data(outcome_categories, OutcomeCategoryData, row_width=2)
        await message.edit_text('Выберите категорию', reply_markup=kb)


@router.callback_query(OutcomeState.active, OutcomeData.filter(F.value == OutcomeButtons.DATE))
async def choose_date(callback_query: CallbackQuery, state: FSMContext, callback_data: OutcomeData):
    message = await utils.get_message_and_answer_query(callback_query)
    await message.edit_text(
        'Выберите дату',
        reply_markup=await SimpleCalendar().start_calendar()
    )


@router.callback_query(OutcomeState.active, SimpleCalendarCallback.filter())
async def process_dialog_calendar(
        callback_query: CallbackQuery, state: FSMContext, callback_data: SimpleCalendarCallback):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    message = await utils.get_message_and_answer_query(callback_query)

    if selected:
        await callback_query.answer(f'{date.strftime("%d/%m/%Y")}')
        await state.update_data({EnumStates.DATE: date.strftime('%d.%m.%Y')})
        await message.delete()
        await start_outcome(message, state)


@router.callback_query(OutcomeState.active, OutcomeData.filter(F.value == OutcomeButtons.ACCOUNT))
async def choose_account(callback_query: CallbackQuery, state: FSMContext, callback_data: OutcomeData):
    message = await utils.get_message_and_answer_query(callback_query)
    data = await state.get_data()
    accounts = data.get(EnumStates.ACCOUNTS, [])

    if not accounts:
        await message.edit_text('Произошла ошибка. Нет доступных счетов. Выберите команду /start')
        print('No accounts')
    else:
        kb = create_simple_str_kb_from_list_and_data(accounts, OutcomeAccountData)
        await message.edit_text('Выберите счёт', reply_markup=kb)


@router.callback_query(OutcomeState.active, OutcomeCategoryData.filter())
async def set_category(callback_query: CallbackQuery, state: FSMContext, callback_data: OutcomeCategoryData):
    message = await utils.get_message_and_answer_query(callback_query)
    await state.update_data({EnumStates.OUT_CATEGORY: callback_data.value})
    await message.delete()
    await start_outcome(message, state)


@router.callback_query(OutcomeState.active, OutcomeAccountData.filter())
async def set_account(callback_query: CallbackQuery, state: FSMContext, callback_data: OutcomeAccountData):
    message = await utils.get_message_and_answer_query(callback_query)
    await state.update_data({EnumStates.OUT_ACCOUNT: callback_data.value})
    await message.delete()
    await start_outcome(message, state)
