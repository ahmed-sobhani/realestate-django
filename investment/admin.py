from django.contrib import admin

from . import models


@admin.register(models.Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'opportunity', 'status', 'amount', 'deleted',)
    ordering = ['-id']


@admin.register(models.InvestmentDocument)
class InvestmentDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'investment', 'title', 'deleted',)
    ordering = ['-id']


@admin.register(models.InvestingEntity)
class InvestingEntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'deleted',)
    ordering = ['-id']


@admin.register(models.AccountIndividual)
class AccountIndividualAdmin(admin.ModelAdmin):
    list_display = ('id', 'deleted',)
    ordering = ['-id']


@admin.register(models.AccountEntity)
class AccountEntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'country', 'deleted',)
    ordering = ['-id']


@admin.register(models.BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_type', 'country', 'deleted',)
    ordering = ['-id']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'deleted',)
    ordering = ['-id']
