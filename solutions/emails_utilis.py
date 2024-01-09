from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_password_reset_email(user, request):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    url = request.build_absolute_uri(
        reverse("password-reset-confirm", kwargs={"uidb64": uidb64, "token": token})
    )
    subject = "Password Reset Request"
    message = f"Please click the following link to reset your password: {url}"
    send_mail(subject, message, "denniskinanga6@gmail.com", [user.email])
