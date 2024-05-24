# from django.contrib import admin, messages
# from django.db import transaction
# from django.forms import ValidationError
# from . import forms
# from utils import algorithms, message_tools
# from .models import Account, ATM, Card, Contract, User
#
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     form = forms.CreateUserForm
#     search_fields = ("first_name", "second_name", "third_name")
#     list_display = ("first_name", "second_name", "third_name", "sex", "birthday", "phone_number", "email")
#     save_on_top = True
#
#     def save_model(self, request, obj, form, change):
#         if not change:
#             type_account = form.data["type_account"]
#             currency = form.data["currency"]
#             payment_system = form.data["payment_system"]
#             percent_rate = form.data["percent_rate"]
#             grace_period = form.data["grace_period"]
#             max_debt_amount = form.data["max_debt_amount"]
#             with transaction.atomic():
#                 obj.other_info = {"passport_scans": ""}
#                 obj.save()
#                 account = Account.create_account(type_account=type_account, currency=currency, user=obj)
#                 account.save()
#
#                 contract = Contract.create_contract(account, percent_rate=percent_rate, grace_period=grace_period,
#                                                     max_debt_amount=max_debt_amount)
#
#                 contract.save()
#                 if payment_system:
#                     card = Card.create_card(account, payment_system=payment_system)
#                     card.save()
#                 message_tools.send_welcome_message(obj, account)
#
#     def response_change(self, request, obj):
#         self.message_user(request, "Данные клиентов запрещено изменять", messages.ERROR)
#         return self.response_post_save_change(request, obj)
#
#
# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     form = forms.CreateAccountForm
#
#     list_display = ("type_account", "account_number", "currency", "balance", "owner", "contract_ref")
#     search_fields = ("account_number",)
#
#     @admin.display(description='Владелец счета')
#     def owner(self, account: Account):
#         return f"{account.user.second_name.capitalize()} {account.user.first_name.capitalize()} {account.user.third_name.capitalize()}"
#
#     @admin.display(description='Номер договора')
#     def contract_ref(self, account: Account):
#         return f"{account.contract.contract_number}"
#
#     def save_model(self, request, obj, form, change):
#         if not change:
#             currency = form.data["currency"]
#             payment_system = form.data["payment_system"]
#             percent_rate = form.data["percent_rate"]
#             grace_period = form.data["grace_period"]
#             max_debt_amount = form.data["max_debt_amount"]
#             with transaction.atomic():
#                 obj.account_number = algorithms.create_new_account(currency)
#                 obj.save()
#                 contract = Contract.create_contract(obj, percent_rate=percent_rate, grace_period=grace_period,
#                                                     max_debt_amount=max_debt_amount)
#                 contract.save()
#                 if payment_system:
#                     card = Card.create_card(obj, payment_system=payment_system)
#                     card.save()
#
#     def response_change(self, request, obj):
#         self.message_user(request, "Платежные данные клиентов запрещено изменять", messages.ERROR)
#         return self.response_post_save_change(request, obj)
#
#
# @admin.register(Card)
# class CardAdmin(admin.ModelAdmin):
#     form = forms.CreateCardForm
#     list_display = ("card_number", "end_date", "is_activated", "payment_system", "account_ref")
#     search_fields = ("card_number",)
#
#     @admin.display(description='Клиент/Номер счета')
#     def account_ref(self, contract: Contract):
#         return str(contract.account)
#
#     def save_model(self, request, obj, form, change):
#         if not change:
#             payment_system = form.data["payment_system"]
#             with transaction.atomic():
#                 obj.card_number = algorithms.create_new_card(payment_system)
#                 obj.end_date = algorithms.get_end_date_for_card()
#                 obj.cvc_hash = algorithms.create_cvc_code()
#                 obj.save()
#
#     def response_change(self, request, obj):
#         self.message_user(request, "Платежные данные клиентов запрещено изменять", messages.ERROR)
#         return self.response_post_save_change(request, obj)
#
#
#
# @admin.register(ATM)
# class ATMAdmin(admin.ModelAdmin):
#     form = forms.CreateATMForm
#     save_on_top = True
#
#     def save_model(self, request, obj, form, change):
#         with transaction.atomic():
#             obj.description = {
#                 "address": form.data["address"],
#                 "url_photo": [],
#                 "schedule": {
#                     "Mon": form.data["Mon"],
#                     "Tue": form.data["Tue"],
#                     "Wed": form.data["Wed"],
#                     "Thu": form.data["Thu"],
#                     "Fri": form.data["Fri"],
#                     "Sat": form.data["Sat"],
#                     "Sun": form.data["Sun"]
#                 },
#                 "about": form.data["about"]
#             }
#             obj.save()
