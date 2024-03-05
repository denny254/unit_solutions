from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from user.serializers import (
    WriterSerializer,
    TaskSerializer,
    ProjectSerializer,
    ClientSerializer,
    UserSerializer,
    MyTokenObtainPairSerializer,
    SubmitTaskSerializer,
)
from .models import Writer, Task, Project, Client, User, SubmitTask
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from user.filters import UserInsightFilter
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .email_confirmation import (
    EmailActivationTokenGenerator,
    send_email_confirmation_email,
)
from .forms import (
    CustomPasswordResetForm,
    PasswordSetForm,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


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
    writers = Writer.objects.all()
    serializer = WriterSerializer(writers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_writer(request, writer_id):
    try:
        writer = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WriterSerializer(writer)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
def update_writer(request, writer_id):
    try:
        writer = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
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
        writer = Writer.objects.get(pk=writer_id)
    except Writer.DoesNotExist:
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
            writer_full_name = serializer.validated_data.pop('writer')
            # Find the corresponding user object based on the full name
            try:
                writer = User.objects.get(first_name=writer_full_name.first_name, last_name=writer_full_name.last_name)
            except User.DoesNotExist:
                return Response({"writer": ["User with the provided full name does not exist."]}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(writer=writer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def user_specific_tasks(request, user_id):
    try:
        tasks = Task.objects.filter(writer_id=user_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response({"message": "Tasks not found for the specified user"}, status=404)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = TaskSerializer(
            task, data=request.data, partial=request.method == "PATCH"
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for clients
@api_view(["GET", "POST"])
def client_list(request):
    if request.method == "GET":
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        client.delete()
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
            serializer.save()
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

    elif request.method in ["PUT", "PATCH"]:
        serializer = ProjectSerializer(
            project, data=request.data, partial=request.method == "PATCH"
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for SubmitTask
@api_view(["GET", "POST"])
def submit_task_list(request):
    if request.method == "GET":
        submit_tasks = SubmitTask.objects.all()
        serializer = SubmitTaskSerializer(submit_tasks, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SubmitTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def submit_task_detail(request, pk):
    try:
        submit_task = SubmitTask.objects.get(pk=pk)
    except SubmitTask.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SubmitTaskSerializer(submit_task)
        return Response(serializer.data)
    elif request.method in ["PUT", "PATCH"]:
        serializer = SubmitTaskSerializer(
            submit_task, data=request.data, partial=request.method == "PATCH"
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        submit_task.delete()
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


class CustomUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

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


def delete(self, request, *args, **kwargs):
    instance = self.get_object()

    if instance != request.user:
            raise PermissionDenied("You don't have permission to delete this user.")
        
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


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


class MyTokenObtainPairView(TokenObtainPairView):  
    serializer_class = MyTokenObtainPairSerializer

def resend_confirmation_email(request, uidb64):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(), id=uid)

    if send_email_confirmation_email(
        request=request,
        user=user,
        receiver_email=user.email,
        receiver_name=f"{user.first_name} {user.last_name}",
        app_name="Unitsolutions App",
    ):
        context = {
            "page_title": "Confirmation email",
            "message_title": "Success!!",
            "message_content": "A confirmation email has been sent.",
        }

    else:
        context = {
            "page_title": "Confirmation email",
            "message_title": "Oops!!",
            "message_content": "Sorry we were unable to send confirmation"
            "email.",
        }

    return render(request, "message-page.html", context)


class EmailActivationManager(APIView):
    def get(self, request):
        uidb64 = request.GET.get("uidb64")
        token = request.GET.get("token")

        if uidb64 is None or token is None:
            context = {
                "status": "error",
                "page_title": "Invalid link",
                "message_title": "Oops!!",
                "message_content": "The link you clicked is invalid.",
            }

            return render(request, "message-page.html", context)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(get_user_model(), id=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
            Exception,
        ):
            context = {
                "status": "error",
                "page_title": "Invalid link",
                "message_title": "Oops!!",
                "message_content": "The link you clicked is invalid.",
            }

            return render(request, "message-page.html", context)
        confirmed = False

        if EmailActivationTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            confirmed = True

        context = {
            "is_active": user.is_active,
            "uidb64": uidb64,
            "confirmed": confirmed,
        }
        return render(
            request,
            "email-activation-result.html",
            context,
        )

    def post(self, request):
        try:
            errors = {}

            action = request.data.get("action")
            if action is None or action == "":
                errors = {**errors, "action": ["This value is required"]}

            uidb64 = request.data.get("uidb64")
            if uidb64 is None or uidb64 == "":
                errors = {**errors, "uidb64": ["This value is required"]}

            token = request.data.get("token")
            if token is None or token == "":
                errors = {**errors, "token": ["This value is required"]}

            if len(errors) > 0:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data={"errors": errors}
                )

            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=uid)

            if action == "confirm":
                if EmailActivationTokenGenerator().check_token(user, token):
                    user.is_active = True
                    user.save()
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            "messages": {
                                "detail": "Email address confirmed "
                                "successfully"
                            }
                        },
                    )

                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            "errors": {
                                "detail": "Invalid link, It could be that "
                                "the confirmation link has already "
                                "make been used or the link has expired."
                            },
                            "data": {
                                "uidb64": uidb64,
                                "user_account_active": user.is_active,
                            },
                        },
                    )

            elif action == "resend-email":
                if send_email_confirmation_email(
                    request=request,
                    user=user,
                    receiver_email=user.email,
                    receiver_name=f"{user.first_name} {user.last_name}",
                    app_name="App in App",
                ):
                    return Response(
                        status=status.HTTP_200_OK,
                        data={
                            "messages": {
                                "detail": "Confirmation email sent "
                                "successfully"
                            }
                        },
                    )

                else:
                    return Response(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={
                            "errors": {
                                "detail": "Confirmation email sending failed"
                            }
                        },
                    )

            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"errors": {"action": "Invalid action"}},
                )

        except get_user_model().DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "errors": {
                        "uidb64": "User with the given id does not exist"
                    }
                },
            )

        except Exception as e:
            return self.handle_error(e)

    def handle_error(self, error):
        # Handle the error and return an error response
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={"errors": {"detail": "Internal server error"}},
        )


def confirm_email_address_set_password(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(), id=uid)

    if PasswordResetTokenGenerator().check_token(user, token):
        if request.method == "GET":
            form = PasswordSetForm()

            context = {
                "form": form,
                "title": "Set a new password",
            }
            return render(request, "password-set.html", context)

        elif request.method == "POST":
            filled_form = PasswordSetForm(request.POST)

            if filled_form.is_valid():
                user.set_password(filled_form.cleaned_data["password"])
                user.is_active = True
                user.save()

                context = {
                    "page_title": "Set password",
                    "message_title": "Success!!",
                    "message_content": "Your password has been set "
                    "successfully, you can now log in to "
                    "your account.",
                }

                return render(
                    request,
                    "message-page.html",
                    context,
                )

            else:
                form = filled_form
                context = {
                    "form": form,
                    "title": "Set a new password",
                }

                return render(
                    request,
                    "set-password.html",
                    context,
                )

    context = {
        "page_title": "Set password",
        "message_title": "Oops!!",
        "message_content": "The link you clicked is invalid, it may be that "
        "the link has already been used or has"
        "expired. Please contact your admin to resend an activation link",
    }

    return render(request, "message-page.html", context)


class PasswordResetRequestManager(APIView):
    def post(self, request):
        try:
            form = CustomPasswordResetForm(request.data)
            if form.is_valid():
                form.save(
                    domain_override=get_current_site(request).domain,
                    app_name="unity-solutions.app",
                )

                return Response(
                    {
                        "messages": {
                            "detail": "If an account with that email exists, you will receive an "
                            "email with further instructions to reset your password"
                        }
                    }
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"errors": form.errors},
                )

        except Exception as e:
            return self.handle_error(e)

    def handle_error(self, error):
        # Handle the error and return an error response
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={"errors": {"detail": "Internal server error"}},
        )
