from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from taskite.permissions import ProjectMemberAPIPermission
from taskite.mixins import ProjectFetchMixin
from taskite.api.priorities.serializers import PrioritySerializer


class PriorityListCreateAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def get(self, request, *args, **kwargs):
        project = request.project
        labels = project.priorities.all()
        return Response(
            data=PrioritySerializer(labels, many=True).data, status=status.HTTP_200_OK
        )
