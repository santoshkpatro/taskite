# Generated by Django 5.1 on 2024-09-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0012_upload"),
    ]

    operations = [
        migrations.AddField(
            model_name="upload",
            name="bucket",
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
        migrations.AddField(
            model_name="upload",
            name="uploaded_by_email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
