from django.db import models

from .apps import InvestmentConfig as Config
from utils.models import BaseModel


class Investment(BaseModel):
    investing_entity = models.ForeignKey(
        'InvestingEntity',
        on_delete=models.CASCADE, related_name="investment_entity", null=True, blank=True)
    opportunity = models.ForeignKey(
        'opportunity.Opportunity',
        on_delete=models.CASCADE, related_name="investment_opportunity", null=True, blank=True)
    amount = models.IntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=Config.INVESTMENT_STATUS, default=Config.STATUS_NEW)
    description = models.TextField(null=True, blank=True)
    price_per_share = models.FloatField(default=0)
    electronic_notice = models.BooleanField(default=False)
    signature_text = models.CharField(max_length=125, null=True, blank=True)


class InvestmentDocument(BaseModel):
    investment = models.ForeignKey(
        Investment, on_delete=models.CASCADE, related_name="document", null=True, blank=True)
    opportunity_document = models.ForeignKey(
        'opportunity.OpportunityDocument',
        on_delete=models.CASCADE, related_name="opportunity_document", null=True, blank=True)
    title = models.CharField(max_length=125, null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=Config.FILE_TYPE, default=Config.TYPE_NONE)
    file = models.FileField(upload_to='Investment_Docs/Files/%Y-%m-%d/', null=True, blank=True)
    signature = models.ImageField(upload_to='Investment_Docs/Signatures/%Y-%m-%d/', null=True, blank=True)
    signature_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class InvestingEntity(BaseModel):
    user = models.ForeignKey(
        'account.CustomUser', on_delete=models.CASCADE, related_name="investor_entity", null=True, blank=True)
    account_individual = models.ForeignKey(
        'AccountIndividual',
        on_delete=models.RESTRICT, related_name="account_individual", null=True, blank=True)  # LIMIT 1
    account_entity = models.ForeignKey(
        'AccountEntity', on_delete=models.RESTRICT, related_name="account_entity", null=True, blank=True)
    questionnaire = models.JSONField(blank=True, null=True)
    has_future_credit_account = models.BooleanField(default=False)
    has_intermediary_account = models.BooleanField(default=False)


class AccountIndividual(BaseModel):
    birthday = models.DateField(null=True, blank=True)
    citizenship = models.ForeignKey('opportunity.Country', on_delete=models.RESTRICT, null=True, blank=True)
    tax_id = models.CharField(max_length=125, null=True, blank=True)


class AccountEntity(BaseModel):
    company = models.CharField(max_length=125, null=True, blank=True)
    tax_id = models.CharField(max_length=125, null=True, blank=True)
    country = models.ForeignKey('opportunity.Country', on_delete=models.RESTRICT, null=True, blank=True)
    state = models.CharField(max_length=125, null=True, blank=True)
    questionnaire = models.JSONField(blank=True, null=True)


class BankAccount(BaseModel):
    investing_entity = models.ForeignKey(
        'InvestingEntity', on_delete=models.CASCADE, related_name="bank_investment", null=True, blank=True)
    account_type = models.PositiveSmallIntegerField(
        choices=Config.ACCOUNT_TYPE, default=Config.ACCOUNT_GENERAL)
    country = models.ForeignKey('opportunity.Country', on_delete=models.RESTRICT, null=True, blank=True)
    name = models.CharField(max_length=125, null=True, blank=True)
    wire = models.CharField(max_length=125, null=True, blank=True)
    account_name = models.CharField(max_length=125, null=True, blank=True)
    account_number = models.CharField(max_length=125, null=True, blank=True)


class Address(BaseModel):
    investing_entity = models.ForeignKey(
        'InvestingEntity', on_delete=models.CASCADE, related_name="address_investment", null=True, blank=True)
    country = models.ForeignKey('opportunity.Country', on_delete=models.RESTRICT, null=True, blank=True)
    street1 = models.CharField(max_length=125, null=True, blank=True)
    street2 = models.CharField(max_length=125, null=True, blank=True)
    city = models.CharField(max_length=125, null=True, blank=True)
    state = models.CharField(max_length=125, null=True, blank=True)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
