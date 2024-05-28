from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from taskite.models import State, Task
from taskite.mixins import ProjectFetchMixin
from taskite.permissions import ProjectMemberAPIPermission
from taskite.api.states.serializers import (
    StateTaskSerializer,
    StateSerializer,
)


class StateListCreateAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def get(self, request, *args, **kwargs):
        project = request.project
        include = request.query_params.get("include", None)
        if include == "tasks":
            # For Sending All states along with tasks and it's members
            task_queryset = (
                Task.objects.order_by("order")
                .prefetch_related("assignees")
                .prefetch_related("labels")
                .select_related("priority")
            )
            priorities = request.query_params.getlist("priorities[]")
            assignees = request.query_params.getlist("assignees[]")
            labels = request.query_params.getlist("labels[]")
            if len(priorities) > 0:
                task_queryset = task_queryset.filter(priority__in=priorities)

            if len(assignees) > 0:
                task_queryset = task_queryset.filter(task_assignees__user__in=assignees)

            if len(labels) > 0:
                task_queryset = task_queryset.filter(task_labels__label__in=labels)

            states = (
                State.objects.filter(project=project)
                .prefetch_related(
                    Prefetch(
                        "state_tasks",
                        queryset=task_queryset,
                    )
                )
                .order_by("order")
            )
            return Response(
                data=StateTaskSerializer(states, many=True).data,
                status=status.HTTP_200_OK,
            )

        states = State.objects.filter(project=project).order_by("order")
        return Response(
            data=StateSerializer(states, many=True).data, status=status.HTTP_200_OK
        )
