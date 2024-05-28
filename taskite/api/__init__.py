from django.urls import path

from taskite.api.accounts.views import LoginAPIView, ProfileAPIView, RegisterAPIView
from taskite.api.projects.views import (
    ProjectListCreateAPIView,
    ProjectDetailUpdateDestroyAPIView,
    ProjectMembersAPIView,
    ProjectMembersListAPIView,
    ProjectMemberRetrieveUpdateDestroyAPIView,
    ProjectMemberInvitesAPIView,
    ProjectInvitesAPIView,
    ProjectInviteListAPIView,
    ProjectInviteDestroyAPIView

)
from taskite.api.states.views import StateListCreateAPIView
from taskite.api.tasks.views import (
    TaskListCreateAPIView,
    TaskDetailUpdateDestroyAPIView,
    AttachmentListCreateAPIView,
    CommentListCreateAPIView
)
from taskite.api.labels.views import LabelListCreateAPIView
from taskite.api.priorities.views import PriorityListCreateAPIView
from taskite.api.storages.views import StoragePresignedURLAPIView

# fmt: off
urlpatterns = [
    path("storages/presigned-url/", StoragePresignedURLAPIView.as_view()),
    
    path("accounts/login/", LoginAPIView.as_view()),
    path("accounts/profile/", ProfileAPIView.as_view()),
    path("accounts/register/", RegisterAPIView.as_view()),
        
    path("projects/", ProjectListCreateAPIView.as_view()),
    path("projects/invites/", ProjectInvitesAPIView.as_view()),
    path("projects/<uuid:project_id>/", ProjectDetailUpdateDestroyAPIView.as_view()),
    path("projects/<uuid:project_id>/members/", ProjectMembersAPIView.as_view()),

    path("projects/<uuid:project_id>/project_invites/", ProjectInviteListAPIView.as_view()),
    path("projects/<uuid:project_id>/project_invites/<uuid:project_invite_id>/", ProjectInviteDestroyAPIView.as_view()),
    
    path("projects/<uuid:project_id>/project_members/", ProjectMembersListAPIView.as_view()),
    path("projects/<uuid:project_id>/project_members/invite/", ProjectMemberInvitesAPIView.as_view()),
    path("projects/<uuid:project_id>/project_members/<uuid:project_member_id>/", ProjectMemberRetrieveUpdateDestroyAPIView.as_view()),
    
    path("projects/<uuid:project_id>/states/", StateListCreateAPIView.as_view()),
    
    path("projects/<uuid:project_id>/tasks/", TaskListCreateAPIView.as_view()),
    path("projects/<uuid:project_id>/tasks/<uuid:task_id>/", TaskDetailUpdateDestroyAPIView.as_view()),
    path("projects/<uuid:project_id>/tasks/<uuid:task_id>/attachments/", AttachmentListCreateAPIView.as_view()),
    path("projects/<uuid:project_id>/tasks/<uuid:task_id>/comments/", CommentListCreateAPIView.as_view()),
    
    path("projects/<uuid:project_id>/labels/", LabelListCreateAPIView.as_view()),

    path("projects/<uuid:project_id>/priorities/", PriorityListCreateAPIView.as_view()),
]
