
import csv
from typing import Callable
from django.http import HttpResponse
from django.db.models import Model
from django.contrib.admin import ModelAdmin

def export_csv(self: ModelAdmin, request, queryset) -> HttpResponse:

    meta = self.model._meta
    field_names = list(field.name for field in meta.fields)
    try: field_names.remove("id")
    except ValueError: pass

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow(
            getattr(obj, field) for field in field_names
        )

    return response

export_csv.short_description = "Export Selected as csv"

class ExportCsvMixin:
    '''to be inherited by AdminModel'''
    model: Model
    export_csv: Callable
ExportCsvMixin.export_csv = export_csv

