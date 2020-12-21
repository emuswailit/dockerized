from rest_framework import serializers
from . import models

from consultations.serializers import PrescriptionItemSerializer, PrescriptionSerializer
from consultations.models import PrescriptionItem, Prescription
from rest_framework.validators import UniqueTogetherValidator

from users.models import Facility


class ForwardPrescriptionSerializer(serializers.HyperlinkedModelSerializer):

    prescription_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.ForwardPrescription
        fields = "__all__"
        read_only_fields = (
            'owner', 'prescription'
        )

    def get_prescription_details(self, obj):
        prescription = Prescription.objects.filter(
            id=obj.prescription_id)
        return PrescriptionSerializer(prescription, context=self.context, many=True).data


class PharmacySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Facility
        fields = ('id', 'url', 'title', 'town', 'road',
                  'building', 'latitude', 'longitude')
