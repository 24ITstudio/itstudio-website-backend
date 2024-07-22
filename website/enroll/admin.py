
from django.contrib import admin
from . import models

admin.site.register(models.VerifyCodeModel)


@admin.register(models.EnrollModel)
class EnrollAdmin(admin.ModelAdmin):
    list_display = "name", "email", "qq", "status"
    list_editable = "status",

    search_fields = 'name',
    search_help_text = 'Search for name'

