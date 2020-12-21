from rest_framework import serializers
from users.models import Facility


class FacilitySafeRelatedField(serializers.HyperlinkedRelatedField):
    """
    Ensures that the queryset only returns values for the facility
    """

    def get_queryset(self):

        request = self.context['request']
        if request.user.is_authenticated:
            facility_id = request.user.facility_id
            return super().get_queryset().filter(facility_id=facility_id)


class FacilitySafeSerializerMixin(object):
    """
    Mixin to be used with HyperlinkedModelSerializer to ensure that only facility values are returned
    """
    serializer_related_field = FacilitySafeRelatedField
