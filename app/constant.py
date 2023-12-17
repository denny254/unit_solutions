from django.db import models
from django.utils.translation import gettext_lazy as _


class UserGroup(models.IntegerChoices):
    CONSULTANT = 100, _("Consultant")
    ADMIN = 200, _("Admin")
    SUPERADMIN = 300, _("SuperAdmin")


class InquiryStatus(models.TextChoices):
    INQUIRY = "Inquiry", _("Inquiry")
    PROVISIONAL = "Provisional", _("Provisional")
    CONFIRMED = "Confirmed", _("Confirmed")
    LOST = "Lost", _("Lost")
