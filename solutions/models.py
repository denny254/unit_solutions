from django.db import models

# Create your models here.
from django.db import models
import os

from typing import Any
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from app.abstracts import (
    IntegerIDModel,
    TimeStampedModel,
)
from app.constant import UserGroup


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **kwargs: Any) -> Any:
        if not email:
            raise ValueError("Email must be set!")
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **kwargs: Any) -> Any:
        """Creates a regular user with a given email address and password."""
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)
        try:
            self.model(email=email)
        except ValidationError:
            raise ValueError("Invalid email address")
        user = self._create_user(email=email, password=password, **kwargs)
        return user

    def create_superuser(self, email: str, password: str, **kwargs: Any) -> Any:
        """creates a superuser with a given email address and password"""
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        try:
            self.model(email=email)
        except ValidationError:
            raise ValueError("Invalid email address")
        superuser = self._create_user(email=email, password=password, **kwargs)

        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, IntegerIDModel):
    """
    Custom user model to replace the default Django User model.
    """

    username = models.CharField(
        verbose_name=_("Display Name"),
        unique=True,
        blank=True,
        max_length=40,
        null=True,
    )
    first_name = models.CharField(
        verbose_name=_("First Name"), max_length=30, blank=False
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"), max_length=30, blank=False
    )
    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    phone = models.CharField(max_length=12, blank=True)
    alternate_phone = models.CharField(max_length=12, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    user_group = models.PositiveIntegerField(
        verbose_name=_("User Group"),
        choices=UserGroup.choices,
        default=UserGroup.CONSULTANT,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs) -> None:
        if not self.username:
            username = self.email.split("@")[0]
            self.username = username
        super(User, self).save(*args, **kwargs)

    def get_short_name(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]


        

#writers model for writers
class Writers(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    date = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        ("New", "New"),
        ("Approved", "Approved"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
        ("Revision", "Revision"),
        ("Resubmission", "Resubmission"),
        ("Pending", "Pending"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    writer = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    book_balance = models.CharField(max_length=255)
    deadline = models.DateField()

    def __str__(self):
        return f"{self.status} - {self.writer} - {self.client}"


class Project(models.Model):
    STATUS_CHOICES = (
        ("New", "New"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
        ("Revision", "Revision"),
        ("Resubmission", "Resubmission"),
        ("Pending", "Pending"),
    )
    title = models.CharField(max_length=255)
    deadline = models.DateField()
    writer_assigned = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    attachment = models.FileField(
        blank=True, null=True, upload_to="images", default="avator.png"
    )

    def __str__(self):
        return self.title

    def delete_old_file(self):
        if self.attachment:
            old_file = self.attachment.path

            if os.path.isfile(old_file):
                print(f"Deleting old file {old_file}")
                os.remove(old_file)

    def save(self, *args, **kwargs):
        self.delete_old_file()
        super().save(*args, **kwargs)
        print("New file saved")

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
