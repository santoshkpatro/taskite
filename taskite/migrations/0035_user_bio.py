# Generated by Django 5.1 on 2024-10-23 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0034_rename_reset_password_id_user_password_reset_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
    ]
