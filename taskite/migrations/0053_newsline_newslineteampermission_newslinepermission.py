# Generated by Django 5.1 on 2024-12-08 05:59

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0052_alter_taskattachment_mime_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Newsline",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=512)),
                ("content", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("published", "Published"),
                            ("draft", "Draft"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                (
                    "visibility",
                    models.CharField(
                        choices=[("public", "Public"), ("restricted", "Restricted")],
                        default="public",
                        max_length=20,
                    ),
                ),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("archived_at", models.DateTimeField(blank=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="author_newslines",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="newslines",
                        to="taskite.workspace",
                    ),
                ),
            ],
            options={
                "db_table": "newslines",
            },
        ),
        migrations.CreateModel(
            name="NewslineTeamPermission",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "newsline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_permissions",
                        to="taskite.newsline",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_newsline_team_permissions",
                        to="taskite.team",
                    ),
                ),
            ],
            options={
                "db_table": "newsline_team_permissions",
            },
        ),
        migrations.CreateModel(
            name="NewslinePermission",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "newsline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="permissions",
                        to="taskite.newsline",
                    ),
                ),
                (
                    "team_membership",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="taskite.teammembership",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_newsline_permissions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "workspace_membership",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="taskite.workspacemembership",
                    ),
                ),
                (
                    "team_permission",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="taskite.newslineteampermission",
                    ),
                ),
            ],
            options={
                "db_table": "newsline_permissions",
            },
        ),
    ]