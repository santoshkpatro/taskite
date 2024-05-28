from rest_framework import serializers

from taskite.models import User, Task, State, Priority


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = [
            "id",
            "name",
            "color",
            "created_at"
        ]


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "display_name",
            "email",
            "full_name",
            "avatar",
            "created_at",
        ]


class TaskSerializer(serializers.ModelSerializer):
    assignees = AssigneeSerializer(many=True)
    priority = PrioritySerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "task_id",
            "name",
            "description",
            "priority",
            "order",
            "sequence",
            "created_at",
            "assignees",
        ]


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name", "order", "color", "created_at"]


class StateTaskSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ["id", "name", "order", "color", "tasks", "created_at"]

    def get_tasks(self, obj):
        return TaskSerializer(obj.state_tasks, many=True).data
