from rest_framework import serializers

from taskite.models.team import Team
from taskite.models.user import User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        ]


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "members",
            "created_at",
        ]