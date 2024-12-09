# Generated by Django 5.1 on 2024-10-24 15:01

from django.db import migrations
from django.db.models.functions import Concat
from django.db.models import Value, F, CharField


def backfill_display_name(apps, schema_editor):
    User = apps.get_model("taskite", "User")
    User.objects.update(
        display_name=Concat(
            F("first_name"), Value(" "), F("last_name"), output_field=CharField()
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0037_user_display_name_alter_user_first_name_and_more"),
    ]

    operations = [
        migrations.RunPython(
            backfill_display_name, reverse_code=migrations.RunPython.noop
        )
    ]
