from django.core import exceptions
from django.shortcuts import get_object_or_404
from users.models import Facility
from rest_framework.exceptions import NotFound


class FacilitySafeViewMixin:
    """
    Mixin to be used with views that ensures that models are related to the company during creation and are querysets
    are filtered for read operations
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:

            facility_id = self.request.user.facility_id
            return queryset.filter(facility_id=facility_id,)
        else:
            raise NotFound("Please log in")

    def perform_create(self, serializer):
        facility_id = self.request.user.facility_id
        serializer.save(facility_id=facility_id)
