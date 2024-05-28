from rest_framework import serializers

from taskite.models import Task, User, Label, Priority, Attachment, Comment


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["id", "name", "color", "created_at"]


class TaskUpdateSerializer(serializers.Serializer):
    state_id = serializers.UUIDField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    priority_id = serializers.UUIDField(required=False)
    order = serializers.FloatField(required=False)
    task_type = serializers.ChoiceField(choices=Task.TaskType.choices, required=False)
    assignee_ids = serializers.ListSerializer(
        required=False, child=serializers.UUIDField()
    )


class TaskSerializer(serializers.ModelSerializer):
    priority = PrioritySerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "task_id",
            "name",
            "task_type",
            "description",
            "priority",
            "order",
            "sequence",
            "created_at",
        ]


class TaskCreateSerializer(serializers.Serializer):
    state_id = serializers.UUIDField()
    name = serializers.CharField()
    priority = serializers.CharField(required=False)
    order = serializers.FloatField(required=False)
    description = serializers.CharField(required=False)
    task_type = serializers.CharField(required=False)


class TaskAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "full_name", "display_name", "created_at"]


class TaskLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "color", "created_at"]


class TaskDetailSerializer(serializers.ModelSerializer):
    assignees = TaskAssigneeSerializer(many=True)
    labels = TaskLabelSerializer(many=True)
    priority = PrioritySerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "task_id",
            "task_type",
            "name",
            "description",
            "priority",
            "start_date",
            "target_date",
            "order",
            "sequence",
            "assignees",
            "labels",
            "created_at",
        ]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "resource", "created_at"]


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "full_name", "avatar", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()

    class Meta:
        model = Comment
        fields = ["id", "user", "description", "created_at"]
