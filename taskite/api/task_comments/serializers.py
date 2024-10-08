from rest_framework import serializers

from taskite.models import TaskComment, User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "avatar"]


class TaskCommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = TaskComment
        fields = ["id", "content", "author", "created_at"]
