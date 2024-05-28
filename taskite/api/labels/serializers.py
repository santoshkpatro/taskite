from rest_framework import serializers

from taskite.models import Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "color", "created_at"]
