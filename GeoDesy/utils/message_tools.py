from django.template import loader
from django.utils.html import strip_tags, escape
from django.core.mail import send_mail


class Message:
    def __init__(self, user):
        self.user = user

    def send(self):
        raise NotImplementedError()

    def init_confirm_code(self, confirm_code):
        raise NotImplementedError()


class EmailMessage(Message):

    def __init__(self, user):
        super().__init__(user)
        self.html_message = None
        self.subject = None
        self.plain_message = None

    def send(self):
        send_mail(self.subject, self.plain_message, from_email=None, recipient_list=(self.user.email,),
                  html_message=self.html_message)

    def init_confirm_code(self, confirm_code):
        username = f"{self.user.second_name.capitalize()}  {self.user.first_name.capitalize()} {self.user.third_name.capitalize()}"
        self.subject = 'Код подверждения'
        self.html_message = loader.render_to_string(
            "email/confirm_code.html", {
                "title": self.subject,
                "username": username,
                "confirm_code": confirm_code
            })
        self.plain_message = strip_tags(escape(self.html_message))

# def send_welcome_message(user, account):
#     to = user.email
#     username = f"{user.second_name.capitalize()}  {user.first_name.capitalize()} {user.third_name.capitalize()}"
#     subject = 'Добро пожаловать'
#     html_message = loader.render_to_string("email/welcome.html",
#                                            {
#                                                "title": subject,
#                                                "username": username,
#                                                "account": account.account_number
#                                            })
#     plain_message = strip_tags(escape(html_message))
#     send_message(subject, plain_message, None, [to], html_message)
