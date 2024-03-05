from django.urls import path
from user import views
from user.views import (
    CustomUserCreateView,
    CustomUserListView,
    CustomUserRetrieveUpdateDestroyView,
    FindUserView,
    user_details,
    MyTokenObtainPairView,
    PasswordChangeManager,
    EmailActivationManager,
    MyTokenObtainPairView,
    PasswordChangeManager,
    PasswordResetRequestManager,
    confirm_email_address_set_password,
    resend_confirmation_email,
)
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
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
    # clients
    path("clients/", views.client_list, name="client-list"),
    path("clients/<int:pk>/", views.client_detail, name="client-detail"),
    # tasks
    path("tasks/", views.task_list, name="task-list"),
    path("tasks/<int:pk>/", views.task_detail, name="task-detail"),
    path(
        "tasks/user-specific/<str:user_id>/",
        views.user_specific_tasks,
        name="user-specific-tasks",
    ),

    # submitting a task
    path("submit-task/", views.submit_task_list, name="submit_task_list"),
    path("submit-task/<int:pk>/", views.submit_task_detail, name="submit_task_detail"),

    
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
    path(
        "confirm-email/",
        EmailActivationManager.as_view(),
        name="email_confirmation",
    ),
    path(
        "resend-confirmation-email/<uidb64>/",
        resend_confirmation_email,
        name="resend_confirmation_email",
    ),
    path(
        "confirm-email-set-password/<uidb64>/<token>/",
        confirm_email_address_set_password,
        name="confirm_email_address_set_password",
    ),
    path(
        "reset-password/",
        PasswordResetRequestManager.as_view(),
        name="password_reset_request",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="reset-password.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/done/",
        PasswordResetCompleteView.as_view(template_name="password-reset-done.html"),
        name="password_reset_complete",
    ),
]
