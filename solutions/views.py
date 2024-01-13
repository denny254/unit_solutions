from .serializers import (
    WriterSerializer,
    TaskSerializer,
    ProjectSerializer,
)
from .models import Writers, Task, Project
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework import status
from app.filters import UserInsightFilter
from solutions.serializers import (
    UserSerializer,
)
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.utils.http import urlsafe_base64_encode
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from solutions.serializers import MyTokenObtainPairSerializer
from solutions.forms import (
    CustomPasswordResetForm,
    PasswordSetForm,
)
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import NewPasswordSerializer
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


User = get_user_model()


# CRUD for writers
@api_view(["POST"])
def create_writer(request):
    serializer = WriterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_writers(request):
    writers = Writers.objects.all()
    serializer = WriterSerializer(writers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_writer(request, writer_id):
    try:
        writer = Writers.objects.get(pk=writer_id)
    except Writers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WriterSerializer(writer)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
def update_writer(request, writer_id):
    try:
        writer = Writers.objects.get(pk=writer_id)
    except Writers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WriterSerializer(
        writer, data=request.data, partial=True if request.method == "PATCH" else False
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_writer(request, writer_id):
    try:
        writer = Writers.objects.get(pk=writer_id)
    except Writers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    writer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for tasks
@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for projects
@api_view(["GET", "POST"])
def project_list(request):
    if request.method == "GET":
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(attachment=request.FILES.get("projects"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            new_attachment = request.data.get("attachment")
            if new_attachment:
                project.attachment.delete()
                project.attachment = new_attachment
            serializer.save(attachment=new_attachment)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
 Full Authentication process 
"""


class CustomUserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    """
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    """


class CustomUserListView(ListAPIView):

    """
    View to list all users.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class FindUserView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserInsightFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomUserRetrieveUpdateDestroyView(RetrieveUpdateAPIView):

    """
     # (RetrieveUpdateDestroyAPIView):
    View to retrieve, update, or delete a single user.
     remove/omit the destroy method to prevent deleting users
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)


def user_details(request, pk):
    """
    View to retrieve a user's profile.
    """
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, safe=False)


class PasswordChangeManager(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password", None)
        new_password1 = request.data.get("new_password1", None)
        new_password2 = request.data.get("new_password2", None)

        if not (old_password and new_password1 and new_password2):
            return Response({"error": "All fields are required."}, status=400)

        if not check_password(old_password, user.password):
            return Response({"error": "Old password is incorrect."}, status=400)

        if new_password1 != new_password2:
            return Response({"error": "Passwords do not match."}, status=400)

        # Update the user's password
        user.set_password(new_password1)
        user.save()

        return Response({"message": "Password reset successful."}, status=200)

    def handle_error(self, error):
        # Handle the error and return an error response
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={"errors": {"detail": "Internal server error"}},
        )


class MyTokenObtainPairView(TokenObtainPairView):  # type: ignore
    serializer_class = MyTokenObtainPairSerializer




