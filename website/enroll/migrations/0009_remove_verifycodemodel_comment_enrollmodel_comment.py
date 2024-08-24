# Generated by Django 4.2.13 on 2024-08-24 10:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enroll", "0008_alter_enrollmodel_department"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="verifycodemodel",
            name="comment",
        ),
        migrations.AddField(
            model_name="enrollmodel",
            name="comment",
            field=models.TextField(blank=True, verbose_name="备注"),
        ),
    ]
