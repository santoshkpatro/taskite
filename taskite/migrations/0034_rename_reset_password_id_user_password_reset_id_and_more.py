# Generated by Django 5.1 on 2024-10-23 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0033_user_reset_password_id_user_reset_password_sent_at_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="reset_password_id",
            new_name="password_reset_id",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="reset_password_sent_at",
            new_name="password_reset_sent_at",
        ),
    ]