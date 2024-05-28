import os
import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.conf import settings

from taskite.models.base import BaseUUIDTimestampModel


class Storage(BaseUUIDTimestampModel):
    bucket = models.CharField(max_length=124, blank=True, null=True)
    filename = models.CharField(max_length=225, unique=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "storages"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.filename

    @receiver(post_delete)
    def handle_storage_on_delete(sender, instance, **kwargs):
        for _field in sender._meta.fields:
            if isinstance(_field, models.FileField):
                _file = getattr(instance, _field.name, None)
                if _file:
                    storage = Storage.objects.filter(filename=_file.name).first()
                    if storage:
                        storage.deleted_at = timezone.now()
                        storage.save(update_fields=["deleted_at"])

    @receiver(post_save)
    def handle_storage_on_create(sender, created, instance, **kwargs):
        if created:
            # Add the file to filename
            for _field in sender._meta.fields:
                if isinstance(_field, models.FileField):
                    _file = getattr(instance, _field.name, None)
                    if _file:
                        storage, _ = Storage.objects.get_or_create(
                            filename=_file.name,
                            defaults={"confirmed_at": timezone.now(), "bucket": settings.AWS_BUCKET_NAME},
                        )

    @classmethod
    def get_upload_path(cls, filename):
        basename, extension = os.path.splitext(filename)
        today = timezone.now()
        new_filename = f"uploads/{today.year}/{today.month}/{basename[:20]}_{uuid.uuid4().hex}{extension}"

        storage = cls(filename=new_filename, bucket=settings.AWS_BUCKET_NAME)
        storage.save()

        return new_filename

    @classmethod
    def confirm_upload(cls, file_path):
        storage = cls.objects.filter(filename=file_path).first()
        if storage:
            if not storage.confirmed_at:
                storage.confirmed_at = timezone.now()
                storage.save(update_fields=["confirmed_at"])

    @classmethod
    def delete_upload(cls, filename):
        storage = cls.objects.filter(filename=filename).first()
        if storage:
            storage.deleted_at = timezone.now()
            storage.save(update_fields=["deleted_at"])
