from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save

from taskite.models.base import BaseUUIDTimestampModel


class Task(BaseUUIDTimestampModel):
    class Priority(models.TextChoices):
        URGENT = ("urgent", "Urgent")
        HIGH = ("high", "High")
        MEDIUM = ("medium", "Medium")
        LOW = ("low", "Low")
        NONE = ("none", "None")

    class TaskType(models.TextChoices):
        ISSUE = ("issue", "Issue")
        TASK = ("task", "Task")
        BUG = ("bug", "Bug")
        EPIC = ("epic", "Epic")
        STORY = ("story", "Story")

    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="project_tasks"
    )
    state = models.ForeignKey(
        "State", on_delete=models.CASCADE, related_name="state_tasks"
    )
    task_id = models.CharField(max_length=10, blank=True, editable=False)
    task_type = models.CharField(
        max_length=10, choices=TaskType.choices, default=TaskType.TASK
    )
    name = models.TextField(max_length=512)
    description = models.TextField(blank=True, null=True)
    priority_depr = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.NONE
    )
    priority = models.ForeignKey(
        "Priority", on_delete=models.SET_NULL, null=True, blank=True
    )
    start_date = models.DateField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)
    order = models.FloatField(blank=True, editable=False)
    sequence = models.IntegerField(default=1, blank=True, editable=False)

    archived_at = models.DateTimeField(blank=True, null=True)

    assignees = models.ManyToManyField(
        "User", through="TaskAssignee", related_name="tasks"
    )
    labels = models.ManyToManyField("Label", through="TaskLabel", related_name="tasks")

    class Meta:
        db_table = "tasks"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "task_id"],
                name="unique_project_task_identifier",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} <{self.id}>"

    def save(self, *args, **kwargs):
        if self._state.adding:
            # last_sequence = (
            #     Task.objects.filter(project=self.project)
            #     .aggregate(largest=models.Max("sequence"))
            #     .get("largest")
            # )
            # if last_sequence is not None:
            #     self.sequence = last_sequence + 1
            self.sequence = self.project.next_task_sequence
            self.task_id = f"{self.project.project_id}-{self.sequence}"

            # Increment next task sequence no.
            self.project.next_task_sequence += 1
            self.project.save(update_fields=["next_task_sequence"])

            if not self.order:
                last_order = (
                    Task.objects.filter(project=self.project, state=self.state)
                    .aggregate(largest=models.Max("order"))
                    .get("largest")
                )
                if last_order is not None:
                    self.order = last_order + 10000
                else:
                    self.order = 50000
        return super().save(*args, **kwargs)

    @transaction.atomic
    def update_order(self, index):
        total_index = self.state.state_tasks.all().order_by("order").count() - 1

        if index == 0:
            first_task = self.state.state_tasks.all().order_by("order").only("order")[0]
            self.order = first_task.order / 2
        elif index == total_index:
            last_task = (
                self.state.state_tasks.all()
                .order_by("order")
                .only("order")[total_index]
            )
            self.order = last_task.order + float(10000)
        else:
            previous_task = (
                self.state.state_tasks.all().order_by("order").only("order")[index]
            )
            next_task = (
                self.state.state_tasks.all().order_by("order").only("order")[index + 1]
            )
            self.order = (previous_task.order + next_task.order) / 2

        self.save(update_fields=["order"])


class TaskAssignee(BaseUUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="task_assignees"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_task_assignees"
    )

    class Meta:
        db_table = "task_assignees"
        verbose_name = "Task Assignee"
        verbose_name_plural = "Task Assignees"
        constraints = [
            models.UniqueConstraint(
                fields=["task_id", "user_id"], name="unique_task_assignees"
            )
        ]
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.task.name}"


class TaskLabel(BaseUUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="task_labels"
    )
    label = models.ForeignKey(
        "Label", on_delete=models.CASCADE, related_name="label_task_labels"
    )

    class Meta:
        db_table = "task_labels"
        verbose_name = "Task Label"
        verbose_name_plural = "Task Labels"
        constraints = [
            models.UniqueConstraint(
                fields=["task_id", "label_id"], name="unique_task_label"
            )
        ]

    def __str__(self) -> str:
        return f"{self.label} <{self.id}>"


class TaskAttachment(BaseUUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="attachments"
    )
    resource = models.FileField("uploads/tasks/attachments/")

    class Meta:
        db_table = "task_attachments"

    def __str__(self) -> str:
        return str(self.id)
