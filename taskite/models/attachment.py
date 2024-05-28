from django.db import models

from taskite.models.base import BaseUUIDTimestampModel


class Attachment(BaseUUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="attachments"
    )
    resource = models.FileField("uploads/tasks/attachments/")

    class Meta:
        db_table = "attachments"

    def __str__(self) -> str:
        return str(self.id)
