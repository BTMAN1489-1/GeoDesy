from .base import FilterField, BaseFilter
from .validators import clean_uuid, clean_boolean


class CardInfoFilter(BaseFilter):
    field_token_card = FilterField('token_card', 'token_card', validators=(clean_uuid,))
    field_is_activated = FilterField('is_activated', 'is_activated', validators=(clean_boolean,))
    field_payment_system = FilterField('payment_system', 'payment_system')
    field_account_number = FilterField('account_number', 'account__account_number')
    field_type_account = FilterField('type_account', 'account__type_account')
    field_currency = FilterField('currency', 'account__currency')

