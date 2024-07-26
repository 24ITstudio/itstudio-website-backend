

from string import Template
import smtplib  # for error handle
from pathlib import Path
from django.core.mail import send_mail
from .email_livecycle import ALIVE_MINUTES


# use Template over `{}`-format to prevent getting
# confused with JS's block syntax.
MSG = Template("欢迎报名爱特工作室，你的验证码是：$code\n  有效期：$alive_minutes 分钟")
def slurp(fn):
    f = open(fn, encoding="utf-8")
    res = f.read()
    return res

H_MSG = Template(
    slurp(
        Path(__file__).with_name("verify_code.html")
    ))

def substitute(t, code):
    return t.substitute(code=code, alive_minutes=ALIVE_MINUTES)

class Sender:
    def __init__(self, auth_user=None, auth_password=None, from_email=None):
        self.auth_user = auth_user
        self.auth_password = auth_password
        self.from_email = from_email
    def send_code(self, code, emails):
        """returns None is not error (successful).
        If error occurs, returns error message (str).
        """
        num_sent = 0
        err_msg = "success"
        try:
            num_sent = send_mail(
                '报名验证', substitute(MSG, code=code),
                self.from_email, # None means using the value of DEFAULT_FROM_EMAIL setting
                emails,
                html_message=substitute(H_MSG, code=code),
                auth_user=self.auth_user,
                auth_password=self.auth_password
            )
        except smtplib.SMTPServerDisconnected:
            err_msg = "SMTP server disconnected"
        except smtplib.SMTPResponseException as e:
            err_msg = e.smtp_error
            if type(err_msg) is bytes:
                err_msg = err_msg.decode()
        except smtplib.SMTPException as e:
            err_msg = "error"
        if num_sent != 0:
            return None
        return err_msg
