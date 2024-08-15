
from django.contrib import admin
from . import models, export

admin.site.register(models.VerifyCodeModel)


@admin.register(models.EnrollModel)
class EnrollAdmin(admin.ModelAdmin):
    list_display = "name", "email", "qq", "department", "status"
    list_editable = "status",

    search_fields = 'name',
    search_help_text = 'Search for name'


admin.site.add_action(export.export_csv)
