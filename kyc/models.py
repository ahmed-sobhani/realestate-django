from django.db import models

from account.models import Investor
from .apps import KycConfig as Config
from utils.models import BaseModel


class KYCFile(BaseModel):
    """
    Store Passport & Selfie Picture for each Investor.
    """
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    file_type = models.PositiveSmallIntegerField(choices=Config.FILE_TYPE, default=Config.PASSPORT)
    file = models.FileField(upload_to='KYC_Docs/Files/%Y-%m-%d/')

    class Meta:
        unique_together = (('investor', 'file_type'),)
