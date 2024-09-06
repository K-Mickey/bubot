from enum import StrEnum


class EnumStates(StrEnum):
    ACCOUNTS = 'accounts'
    OUTCOME_CATEGORIES = 'outcome_categories'
    INCOME_CATEGORIES = 'income_categories'
    DATE = 'date'
    OUT_CATEGORY = 'outcome_category'
    OUT_ACCOUNT = 'outcome_account'
    IN_CATEGORY = 'income_category'
    IN_ACCOUNT = 'income_account'
    TRANSFER_FROM = 'transfer_from'
    TRANSFER_TO = 'transfer_to'
