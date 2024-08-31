
from django.contrib import admin
from . import models, export

@admin.register(models.VerifyCodeModel)
class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = "email", "send_time"
    # send_time is marked as `auto_now=True`, so not editable
    #list_editable = "send_time",

@admin.register(models.EnrollModel)
class EnrollAdmin(admin.ModelAdmin):
    list_display = "name", "email", "qq", "department", "status", "comment"
    list_editable = "status", "comment"

    search_fields = 'name',
    search_help_text = 'Search for name'
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for i in 'qq', 'content':
            form.base_fields[i].required = False
        return form


admin.site.add_action(export.export_csv)
