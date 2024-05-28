from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from taskite.models.base import BaseUUIDTimestampModel
from taskite.models.project import Project


class Priority(BaseUUIDTimestampModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="priorities"
    )
    name = models.CharField(max_length=124)
    color = models.CharField(max_length=10, default="#33cc33")

    class Meta:
        db_table = "priorities"
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "name"], name="unique_project_priority_name"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} <{self.id}>"

    @receiver(post_save, sender=Project)
    def add_default_project_priorities(sender, created, instance, **kwargs):
        if created:
            Priority.objects.bulk_create(
                [
                    Priority(project=instance, name="Urgent", color="#ff0000"),
                    Priority(project=instance, name="High", color="#ed5934"),
                    Priority(project=instance, name="Medium", color="#ffff00"),
                    Priority(project=instance, name="Low", color="#00ff00"),
                ]
            )