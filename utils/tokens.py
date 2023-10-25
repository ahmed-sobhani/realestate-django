from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        if user.last_login is None:
            login_timestamp = ''
        else:
            login_timestamp = user.last_login.replace(microsecond=0, tzinfo=None)

        return (
            text_type(user.pk) + user.password +
            text_type(login_timestamp) + text_type(timestamp)
        )


account_activation_token = AccountActivationTokenGenerator()
