from rest_framework import serializers

from taskite.models import Priority


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["id", "name", "color", "created_at"]
