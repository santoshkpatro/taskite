import sentry_sdk
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from taskite.models import Project, ProjectMember, Storage, Task, ProjectInvite
from taskite.permissions import ProjectMemberAPIPermission
from taskite.mixins import ProjectFetchMixin
from taskite.api.projects.serializers import (
    ProjectSerializer,
    MemberSerializer,
    ProjectCreateSerializer,
    ProjectMemberSerializer,
    ProjectMemberUpdateSerializer,
    ProjectUpdateSerializer,
    ProjectMemberInviteSerializer,
    ProjectInviteHomeSerializer,
    ProjectInviteSerializer,
)
from taskite.exceptions import (
    ProjectMemberNotFoundAPIException,
    InvalidRequestBodyAPIException,
    ProjectInviteNotFoundAPIException,
    ProjectPermissionAPIException,
    OperationFailedAPIException,
)


class ProjectListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(
                project_member__user=request.user,
            )
            # public_projects = Project.objects.filter(
            #     visibility=Project.Visibility.PUBLIC
            # )
            # projects = user_projects.union(public_projects, all=False)

        serializer = ProjectSerializer(projects, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)

            return Response(
                data={"detail": "Invalid projected information provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_project_data = serializer.validated_data
        try:
            with transaction.atomic():
                project: Project = Project.objects.create(
                    **new_project_data, created_by=request.user
                )
                if project.visibility == Project.Visibility.PUBLIC:
                    ProjectMember.objects.create(
                        project=project,
                        user=request.user,
                        role=ProjectMember.Role.ADMIN,
                    )
        except Exception as err:
            sentry_sdk.capture_exception(err)
            raise OperationFailedAPIException

        return Response(
            data={
                "detail": "Project has been created successfully.",
                "project": ProjectSerializer(project).data,
            },
            status=status.HTTP_200_OK,
        )


class ProjectDetailUpdateDestroyAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def get(self, request, *args, **kwargs):
        project = request.project
        serializer = ProjectSerializer(project)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        project = request.project
        serializer = ProjectUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise InvalidRequestBodyAPIException

        data = serializer.validated_data
        try:
            with transaction.atomic():
                for attr, value in data.items():
                    prev_value = getattr(project, attr)
                    setattr(project, attr, value)
                    new_value = getattr(project, attr)

                    # Handling File Updates
                    if attr == "cover" and prev_value != new_value:
                        if prev_value:
                            Storage.delete_upload(prev_value)
                        if new_value:
                            Storage.confirm_upload(new_value)

                    # Handling Project ID updates to all tasks
                    if attr == "project_id" and prev_value != new_value:
                        tasks = Task.objects.filter(project=project)
                        for task in tasks:
                            setattr(task, "task_id", f"{new_value}-{task.sequence}")
                        Task.objects.bulk_update(tasks, fields=["task_id"])

                project.save(update_fields=data.keys())
        except Exception as err:
            sentry_sdk.capture_exception(err)
            raise OperationFailedAPIException
        response_data = {
            "detail": "Project details got updated.",
            "project": ProjectSerializer(project).data,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)


class ProjectMembersAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def get(self, request, *args, **kwargs):
        project = request.project
        members = project.members.all().order_by("full_name")
        return Response(
            data=MemberSerializer(members, many=True).data, status=status.HTTP_200_OK
        )


class ProjectMembersListAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def get(self, request, *args, **kwargs):
        project = request.project
        project_members = (
            ProjectMember.objects.filter(project=project)
            .exclude(user=request.user)
            .select_related("user")
        )
        serializer = ProjectMemberSerializer(project_members, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProjectMemberRetrieveUpdateDestroyAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def patch(self, request, *args, **kwargs):
        project = request.project
        project_member = ProjectMember.objects.filter(
            project=project, id=kwargs.get("project_member_id")
        ).first()
        if not project_member:
            raise ProjectMemberNotFoundAPIException

        serializer = ProjectMemberUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise InvalidRequestBodyAPIException

        data = serializer.validated_data
        for attr, value in data.items():
            setattr(project_member, attr, value)
        project_member.save(update_fields=data.keys())

        project_member_serializer = ProjectMemberSerializer(project_member)
        return Response(data=project_member_serializer.data, status=status.HTTP_200_OK)


class ProjectMemberInvitesAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def post(self, request, *args, **kwargs):
        serializer = ProjectMemberInviteSerializer(data=request.data)
        if not serializer.is_valid():
            raise InvalidRequestBodyAPIException

        data = serializer.validated_data
        project = request.project

        existing_invite_emails = list(
            ProjectInvite.objects.filter(
                project=project, email__in=data["emails"], confirmed_at__isnull=True
            ).values_list("email", flat=True)
        )
        existing_member_emails = list(
            project.members.all().values_list("email", flat=True)
        )
        for email in data["emails"]:
            if email in existing_invite_emails:
                continue

            if email in existing_member_emails:
                continue

            try:
                ProjectInvite.objects.create(
                    project=project,
                    role=data["role"],
                    message=data["message"],
                    email=email,
                )
            except Exception:
                print("Failed to invite")

        return Response(
            data={"detail": "Project Invites has been sent!"}, status=status.HTTP_200_OK
        )


class ProjectInviteListAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def get(self, request, *args, **kwargs):
        project_invites = ProjectInvite.objects.filter(
            project=request.project, confirmed_at__isnull=True
        )
        serializer = ProjectInviteSerializer(project_invites, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProjectInviteDestroyAPIView(ProjectFetchMixin, APIView):
    permission_classes = [IsAuthenticated, ProjectMemberAPIPermission]

    def delete(self, request, *args, **kwargs):
        # Ensure only project admin have ability to delete project invites.
        if request.project_role != "admin":
            raise ProjectPermissionAPIException

        project_invite = ProjectInvite.objects.filter(
            project=request.project, id=kwargs.get("project_invite_id")
        ).first()
        if not project_invite:
            raise ProjectInviteNotFoundAPIException

        project_invite.delete()
        return Response(
            data={"detail": "Project invite has been deleted!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProjectInvitesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        project_invites = ProjectInvite.objects.filter(
            email=request.user.email, confirmed_at__isnull=True
        ).select_related("project")
        serializer = ProjectInviteHomeSerializer(project_invites, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
