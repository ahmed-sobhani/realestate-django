from django.contrib import admin

from . import models


@admin.register(models.KYCFile)
class KYCFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'file_type',)
    ordering = ['-id']
