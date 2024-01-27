from django.urls import path
from solutions import views
from solutions.views import (
    CustomUserCreateView,
    CustomUserListView,
    CustomUserRetrieveUpdateDestroyView,
    FindUserView,
    user_details,
    MyTokenObtainPairView,
    PasswordChangeManager,
    PasswordResetManager,
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # authentiaction
    path("user/", FindUserView.as_view()),
    path(
        "user/userList/",
        CustomUserListView.as_view(),
        name="user-list",
    ),
    path(
        "user/get-user/<int:pk>/",
        CustomUserRetrieveUpdateDestroyView.as_view(),
        name="user-detail",
    ),
    path(
        "user/register/",
        CustomUserCreateView.as_view(),
        name="user-create",
    ),
    path("user/details/<str:pk>/", user_details, name="user-detail"),
    # writers
    path("writers/", views.create_writer, name="create_writer"),
    path("writers/all/", views.get_all_writers, name="get_all_writers"),
    path("writers/<int:writer_id>/", views.get_writer, name="get_writer"),
    path("writers/update/<int:writer_id>/", views.update_writer, name="update_writer"),
    path("writers/delete/<int:writer_id>/", views.delete_writer, name="delete_writer"),
    # writers
    path("clients/", views.create_client, name="create_client"),
    path("clients/all/", views.get_all_clients, name="get_all_clients"),
    path("clients/<int:client_id>/", views.get_client, name="get_client"),
    path("clients/update/<int:client_id>/", views.update_client, name="update_client"),
    path("clients/delete/<int:client_id>/", views.delete_client, name="delete_client"),
    # tasks
    path("tasks/", views.task_list, name="task-list"),
    path("tasks/<int:pk>/", views.task_detail, name="task-detail"),
    # projects
    path("projects/", views.project_list, name="project-list"),
    path("projects/<int:pk>/", views.project_detail, name="project-detail"),
    # Signin up the user
    path("user/sign-in/", MyTokenObtainPairView.as_view(), name="sign-in"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "change-password",
        PasswordChangeManager.as_view(),
        name="password_change",
    ),
    path("reset-password", PasswordResetManager.as_view(), name="password_reset"),
]
