
from django.conf import settings
import warnings
from .verify_code_impl import *

for attr in (
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "DEFAULT_FROM_EMAIL"
):
    globals()[attr] = getattr(settings, attr, None)
del attr

try:
    from ._email_conf import *
except ImportError:
    pass

_ADMINS = getattr(settings, "ADMINS", [])

sender = Sender(
    auth_user=EMAIL_HOST_USER,
    auth_password=EMAIL_HOST_PASSWORD,
    from_email=DEFAULT_FROM_EMAIL,
    admins=_ADMINS)

if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    # overwrite send_code
    Solution = """
        Solution:
        1) set such an environment variable;
        2) modify settings.EMAIL_HOST_PASSWORD to something other than None
"""
    warnings.warn("NO email conf found, `send_code` will raise Error if called" + Solution)
    def send_code(*_a, **_kw):
        raise OSError(
            """EMAIL_HOST_PASSWORD environment variable is not set,
            which is required to send email.

            """ + Solution
        )
    sender._send_code = self.send_code #type: ignore
    sender.send_code = send_code
