from django.db import models

from taskite.models.base import BaseUUIDTimestampModel


class Comment(BaseUUIDTimestampModel):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        related_name="user_comments",
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)

    class Meta:
        db_table = "comments"

    def __str__(self) -> str:
        return str(self.id)
