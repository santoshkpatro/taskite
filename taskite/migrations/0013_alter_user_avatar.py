# Generated by Django 5.0.4 on 2024-05-06 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0012_alter_project_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/users/avatars/"
            ),
        ),
    ]
