# Generated by Django 5.1 on 2024-09-29 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0014_purgedasset_unusedasset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unusedasset",
            name="key",
            field=models.CharField(max_length=225, unique=True),
        ),
    ]