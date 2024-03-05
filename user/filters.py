from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters



User = get_user_model()
#

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


