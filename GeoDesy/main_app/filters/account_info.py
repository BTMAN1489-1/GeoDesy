from .base import FilterField, BaseFilter


class AccountInfoFilter(BaseFilter):
    field_account_number = FilterField('account_number', 'account_number')
    field_type_account = FilterField('type_account', 'type_account')
    field_currency = FilterField('currency', 'currency')

