# Generated by Django 5.1 on 2024-12-18 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0063_alter_board_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="is_from_template",
            field=models.BooleanField(
                default=False,
                help_text="Indicates if this board was created from a template",
            ),
        ),
        migrations.AddField(
            model_name="board",
            name="template",
            field=models.ForeignKey(
                blank=True,
                help_text="If this board was created from a template, reference to the template board",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="copies",
                to="taskite.board",
            ),
        ),
        migrations.AlterField(
            model_name="board",
            name="is_template",
            field=models.BooleanField(
                default=False,
                help_text="WARN: Enabling this would make board public for other people to copy as template",
            ),
        ),
    ]
