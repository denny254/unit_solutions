from typing import Any

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters



User = get_user_model()


class UserInsightFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )

    order_by = filters.OrderingFilter(fields=(("first_name", "first_name"),))

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]


# class MailFilters(filters.FilterSet):  # type: ignore[no-any-unimported]
#     inquiry_no = filters.CharFilter(
#         field_name="inquiry_no", lookup_expr="icontains"
#     )
#     email_type = filters.CharFilter(
#         field_name="email_type", lookup_expr="icontains"
#     )
#     subject = filters.CharFilter(field_name="subject", lookup_expr="icontains")
#     sender = filters.CharFilter(field_name="sender", lookup_expr="icontains")
#     recipients = filters.CharFilter(
#         field_name="recipients", lookup_expr="icontains"
#     )
#     cc = filters.CharFilter(field_name="cc", lookup_expr="icontains")
#     bcc = filters.CharFilter(field_name="bcc", lookup_expr="icontains")
#     reply_to = filters.CharFilter(
#         field_name="reply_to", lookup_expr="icontains"
#     )
#     date_received = filters.DateFilter(
#         field_name="date_received", lookup_expr="icontains"
#     )
#     is_draft = filters.CharFilter(
#         field_name="is_draft", lookup_expr="icontains"
#     )
#     is_archived = filters.CharFilter(
#         field_name="is_archived", lookup_expr="icontains"
#     )
#     inquiry_value = filters.CharFilter(
#         field_name="inquiry_value", lookup_expr="icontains"
#     )
#     inquiry_status = filters.CharFilter(
#         field_name="inquiry_status", lookup_expr="icontains"
#     )
  