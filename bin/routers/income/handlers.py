from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from bin import transaction, utils
from bin.keyboards import MainButtons, create_simple_str_kb_from_list_and_data
from bin.routers.income import utils as in_utils
from bin.routers.income.keyboards import get_income_kb, IncomeButtons
from bin.routers.income.states import IncomeState, IncomeData, IncomeCategoryData, IncomeAccountData
from bin.states import EnumStates

router = Router()


@router.message(F.text == MainButtons.ADD_INCOME)
async def start_income(message: Message, state: FSMContext, edit_last_message: bool = False):
    await state.set_state(IncomeState.active)
    trans = await transaction.get_from_state(type='income', state=state)

    kb = get_income_kb(*trans.get_kb_args())
    text = ('<u>Настройте параметры через <b>клавиатуру</b>.</u>\n\n'
            'Введите <b>сумму доходов</b> и <b>комментарий</b> <i>через пробел</i>.\n'
            'Введите <b>Покажи <i>n</i></b>, для показа последних <i>n</i> расходов.')

    if edit_last_message:
        await message.edit_text(text, reply_markup=kb, parse_mode='HTML')
    else:
        await message.answer(text, reply_markup=kb, parse_mode='HTML')


@router.message(IncomeState.active, F.text.regexp(r'\d+(,\d+)?'))
async def append_income(message: Message, state: FSMContext):
    trans = await transaction.get_from_state('income', state, message.text)
    if trans.is_empty_category_or_account():
        await message.answer('Необходимо выбрать категорию и счёт')
    else:
        answer = in_utils.append_to_sheet(trans.to_list())
        await message.answer(f'Доходы добавлены {answer["updates"]["updatedRange"]}')


@router.message(IncomeState.active, F.text.contains('Покажи'))
async def get_income(message: Message, state: FSMContext):
    count = utils.get_count_from_show_message(message.text)
    text = in_utils.get_last_incomes(count)
    await message.answer(text)


@router.callback_query(IncomeState.active, IncomeData.filter(F.value == IncomeButtons.DATE))
async def choose_date(callback_query: CallbackQuery, state: FSMContext, callback_data: IncomeData):
    message = await utils.get_message_and_answer_query(callback_query)
    await message.edit_text('Выберите дату', reply_markup=await SimpleCalendar().start_calendar())


@router.callback_query(IncomeState.active, IncomeData.filter(F.value == IncomeButtons.CATEGORY))
async def choose_category(callback_query: CallbackQuery, state: FSMContext, callback_data: IncomeData):
    message = await utils.get_message_and_answer_query(callback_query)
    data = await state.get_data()
    income_categories = data.get(EnumStates.INCOME_CATEGORIES, [])

    if not income_categories:
        await message.edit_text('Произошла ошибка. Нет доступных категорий. Выберите команду /start')
        print('No category')
    else:
        kb = create_simple_str_kb_from_list_and_data(income_categories, IncomeCategoryData, row_width=1)
        await message.edit_text('Выберите категорию', reply_markup=kb)


@router.callback_query(IncomeState.active, IncomeData.filter(F.value == IncomeButtons.ACCOUNT))
async def choose_account(callback_query: CallbackQuery, state: FSMContext, callback_data: IncomeData):
    message = await utils.get_message_and_answer_query(callback_query)
    data = await state.get_data()
    income_accounts = data.get(EnumStates.ACCOUNTS, [])

    if not income_accounts:
        await message.edit_text('Произошла ошибка. Нет доступных счетов. Выберите команду /start')
        print('No main')
    else:
        kb = create_simple_str_kb_from_list_and_data(income_accounts, IncomeAccountData, row_width=1)
        await message.edit_text('Выберите счёт', reply_markup=kb)


@router.callback_query(IncomeState.active, SimpleCalendarCallback.filter())
async def process_dialog_calendar(
        callback_query: CallbackQuery, state: FSMContext, callback_data: SimpleCalendarCallback):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    message = await utils.get_message_and_answer_query(callback_query)

    if selected:
        await callback_query.answer(f'{date.strftime("%d/%m/%Y")}')
        await state.update_data({EnumStates.DATE: date.strftime('%d.%m.%Y')})
        await message.delete()
        await start_income(message, state)


@router.callback_query(IncomeState.active, IncomeCategoryData.filter())
async def set_category(callback_query: CallbackQuery, state: FSMContext, callback_data: IncomeCategoryData):
    message = await utils.get_message_and_answer_query(callback_query)
    await state.update_data({EnumStates.IN_CATEGORY: callback_data.value})
    await message.delete()
    await start_income(message, state)


@router.callback_query(IncomeState.active, IncomeAccountData.filter())
async def set_account(callback_query: CallbackQuery, state: FSMContext, callback_data: IncomeAccountData):
    message = await utils.get_message_and_answer_query(callback_query)
    await state.update_data({EnumStates.IN_ACCOUNT: callback_data.value})
    await message.delete()
    await start_income(message, state)
