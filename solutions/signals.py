from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs
):

    frontend_url = "https://www.unitysolutionstutors.com/reset-password"

   
    reset_password_url = f"{frontend_url}?token={reset_password_token.key}"

    
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "reset_password_url": reset_password_url,  # This URL is used in your email template
    }

    email_html_message = render_to_string("email/password_reset_email.html", context)
    email_plaintext_message = render_to_string(
        "email/password_reset_email.txt", context
    )

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Your Website Title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@yourdomain.com",
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
