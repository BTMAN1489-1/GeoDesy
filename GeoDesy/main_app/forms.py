# import decimal
# from django import forms
# from django.db import models
# from django.core.exceptions import ValidationError
# from .models import Account, ATM, User, Card
# import config
#
# __all__ = [
#     "CreateUserForm",
#     "CreateAccountForm",
#     "CreateCardForm"
# ]
#
# currencies = config.allow_currency_name.items()
# payment_systems = [
#     ('', 'Без карты'),
#     *config.allow_payment_system_list]
#
#
# def check_credit_data(form, data):
#     type_account = form.cleaned_data['type_account']
#     if type_account == Account.TypeAccount.CREDIT:
#         if data is not None:
#             return
#
#         error_message = "Счет является кредитным, поэтому необходимо заполнить это поле"
#         raise ValidationError(error_message)
#
#
# class CreateUserForm(forms.ModelForm):
#     type_account = forms.ChoiceField(label="Тип счёта", choices=Account.TypeAccount.choices,
#                                      initial=Account.TypeAccount.DEBIT)
#     currency = forms.ChoiceField(label='Валюта', choices=currencies)
#
#     payment_system = forms.ChoiceField(label='Платежная система', choices=payment_systems, initial=payment_systems[0],
#                                        required=False)
#
#     percent_rate = forms.DecimalField(min_value=0, max_value=100, label="Процентная ставка", required=False)
#
#     grace_period = forms.IntegerField(min_value=0, label='Беспроцентный период (в днях)', required=False)
#
#     max_debt_amount = forms.DecimalField(min_value=0, label="Сумма займа", required=False)
#
#     class Meta:
#         model = User
#         fields = ("first_name", "second_name", "third_name", "sex", "birthday", "phone_number", "email", "type_account",
#                   "currency", "payment_system", "percent_rate", "grace_period", "max_debt_amount")
#
#     def clean_percent_rate(self):
#         check_credit_data(self, self.cleaned_data['percent_rate'])
#
#     def clean_max_debt_amount(self):
#         check_credit_data(self, self.cleaned_data['max_debt_amount'])
#
#     def clean_grace_period(self):
#         check_credit_data(self, self.cleaned_data['grace_period'])
#
#
# class CreateAccountForm(forms.ModelForm):
#     type_account = forms.ChoiceField(label="Тип счёта", choices=Account.TypeAccount.choices,
#                                      initial=Account.TypeAccount.DEBIT)
#     currency = forms.ChoiceField(label='Валюта', choices=currencies)
#
#     payment_system = forms.ChoiceField(label='Платежная система', choices=payment_systems, initial=payment_systems[0],
#                                        required=False)
#
#     percent_rate = forms.DecimalField(min_value=0, max_value=100, label="Процентная ставка", required=False)
#
#     grace_period = forms.IntegerField(min_value=0, label='Беспроцентный период (в днях)', required=False)
#
#     max_debt_amount = forms.DecimalField(min_value=0, label="Сумма займа", required=False)
#
#     class Meta:
#         model = Account
#         fields = (
#             "user", "type_account", "currency", "payment_system", "percent_rate", "grace_period", "max_debt_amount")
#
#     def clean_percent_rate(self):
#         check_credit_data(self, self.cleaned_data['percent_rate'])
#
#     def clean_max_debt_amount(self):
#         check_credit_data(self, self.cleaned_data['max_debt_amount'])
#
#     def clean_grace_period(self):
#         check_credit_data(self, self.cleaned_data['grace_period'])
#
#
# class CreateCardForm(forms.ModelForm):
#     payment_system = forms.ChoiceField(label='Платежная система', choices=payment_systems[1:])
#
#     class Meta:
#         model = Card
#         fields = ("account", "payment_system")
#
#
# class CreateATMForm(forms.ModelForm):
#     class WorkTime(models.TextChoices):
#         DAY_OF = 'Выходной', 'Выходной'
#         WORK_1 = '9:00-17:00', '9:00-17:00'
#         WORK_2 = '8:00-20:00', '8:00-20:00'
#         WORK_3 = '8:00-22:00', '8:00-22:00'
#         WORK_4 = '9:00-23:00', '9:00-23:00'
#         WORK_5 = 'Круглосуточно', 'Круглосуточно'
#
#     address = forms.CharField(label='Адрес')
#     longitude = forms.FloatField(label='Долгота', min_value=-180, max_value=180)
#     latitude = forms.FloatField(label='Широта', min_value=-90, max_value=90)
#     Mon = forms.ChoiceField(choices=WorkTime.choices, initial=WorkTime.WORK_5, label='Понедельник')
#     Tue = forms.ChoiceField(choices=WorkTime.choices, initial=WorkTime.WORK_5, label='Вторник')
#     Wed = forms.ChoiceField(choices=WorkTime.choices, initial=WorkTime.WORK_5, label='Среда')
#     Thu = forms.ChoiceField(choices=WorkTime.choices, initial=WorkTime.WORK_5, label='Четверг')
#     Fri = forms.ChoiceField(choices=WorkTime.choices, initial=WorkTime.WORK_5, label='Пятница')
#     Sat = forms.ChoiceField(choices=WorkTime.choices, initial=WorkTime.DAY_OF, label='Суббота')
#     Sun = forms.ChoiceField(choices=WorkTime.choices, initial=WorkTime.DAY_OF, label='Воскресенье')
#     about = forms.CharField(widget=forms.Textarea(), required=False)
#
#     class Meta:
#         model = ATM
#         fields = (
#             "longitude",
#             "latitude",
#             "address",
#             "Mon",
#             "Tue",
#             "Wed",
#             "Thu",
#             "Fri",
#             "Sat",
#             "Sun",
#             "about"
#         )
