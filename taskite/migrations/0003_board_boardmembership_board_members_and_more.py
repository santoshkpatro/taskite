# Generated by Django 5.1 on 2024-08-17 03:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0002_alter_user_avatar_organization_organizationuser"),
    ]

    operations = [
        migrations.CreateModel(
            name="Board",
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
                ("name", models.CharField(max_length=124)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "visibility",
                    models.CharField(
                        choices=[("public", "Public"), ("private", "Private")],
                        default="private",
                        max_length=10,
                    ),
                ),
                (
                    "cover",
                    models.ImageField(
                        blank=True, null=True, upload_to="boards/covers/"
                    ),
                ),
                ("task_sequence_counter", models.IntegerField(default=1)),
                ("task_prefix", models.CharField(blank=True, max_length=5)),
                ("tasks_count", models.IntegerField(default=0)),
                ("members_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("archived_at", models.DateTimeField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="boards",
                        to="taskite.organization",
                    ),
                ),
            ],
            options={
                "db_table": "boards",
            },
        ),
        migrations.CreateModel(
            name="BoardMembership",
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
                (
                    "role",
                    models.CharField(
                        choices=[("admin", "Admin"), ("staff", "Staff")],
                        default="staff",
                        max_length=10,
                    ),
                ),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="taskite.board",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="board_memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "board_memberships",
            },
        ),
        migrations.AddField(
            model_name="board",
            name="members",
            field=models.ManyToManyField(
                related_name="boards",
                through="taskite.BoardMembership",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="boardmembership",
            constraint=models.UniqueConstraint(
                fields=("board", "user"), name="unique_member_per_board"
            ),
        ),
    ]
