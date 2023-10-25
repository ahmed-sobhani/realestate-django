from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KycConfig(AppConfig):
    name = 'kyc'

    PASSPORT = 1
    PHOTO = 2
    FILE_TYPE = (
        (PASSPORT, _("Passport")),
        (PHOTO, _("Selfie Photo")),
    )
