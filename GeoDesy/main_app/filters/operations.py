from .base import FilterField, BaseFilter
from .validators import clean_uuid


class OperationInfoFilter(BaseFilter):
    field_account_number = FilterField('account_number', 'account_number', required=True)
    field_token_card = FilterField('token_card', 'token_card', validators=(clean_uuid,))
    field_status_operation = FilterField('status_operation', 'status_operation')
    field_currency = FilterField('description__currency', 'currency')

