from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InvestmentConfig(AppConfig):
    name = 'investment'

    STATUS_NONE = 0
    STATUS_NEW = 1
    STATUS_REJECTED = 2
    STATUS_APPROVED = 3
    STATUS_ACTIVE = 4
    STATUS_COMPLETED = 5
    INVESTMENT_STATUS = (
        (STATUS_NONE, _("None")),
        (STATUS_NEW, _("New")),
        (STATUS_REJECTED, _("Rejected")),
        (STATUS_APPROVED, _("Approved")),
        (STATUS_ACTIVE, _("Active")),
        (STATUS_COMPLETED, _("Completed")),
    )

    TYPE_NONE = 0
    TYPE_IMAGE = 1
    TYPE_PDF = 2
    TYPE_VIDEO = 3
    TYPE_EXCEL = 4
    FILE_TYPE = (
        (TYPE_NONE, _("None")),
        (TYPE_IMAGE, _("Image")),
        (TYPE_PDF, _("PDF")),
        (TYPE_VIDEO, _("Video")),
        (TYPE_EXCEL, _("Excel")),
    )

    ACCOUNT_NONE = 0
    ACCOUNT_GENERAL = 1
    ACCOUNT_CREDIT = 2
    ACCOUNT_INTERMEDIARY = 3
    ACCOUNT_TYPE = (
        (ACCOUNT_NONE, _("None")),
        (ACCOUNT_GENERAL, _("General")),
        (ACCOUNT_CREDIT, _("Credit")),
        (ACCOUNT_INTERMEDIARY, _("Intermediary")),
    )

    # def ready(self):
    #     import investment.signals
