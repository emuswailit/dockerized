from rest_framework import serializers
from . import models

from consultations.serializers import PrescriptionItemSerializer, PrescriptionSerializer
from consultations.models import PrescriptionItem, Prescription
from rest_framework.validators import UniqueTogetherValidator

from users.models import Facility
from pharmacies.models import PrescriptionQuote
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


class ForwardPrescriptionSerializer(serializers.HyperlinkedModelSerializer):

    prescription_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.ForwardPrescription
        fields = ('id', 'url', 'facility', 'prescription', 'comment',
                  'owner', 'prescription_details', 'created', 'updated',)
        read_only_fields = (
            'id', 'owner',
        )

    def get_prescription_details(self, obj):
        prescription = Prescription.objects.filter(
            id=obj.prescription_id)
        return PrescriptionSerializer(prescription, context=self.context, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        user = User.objects.get(id=user_pk)
        prescription = validated_data.pop('prescription')
        facility = validated_data.pop('facility')

        if prescription and user:

            if facility == Facility.objects.default_facility():
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": "Selected facility is not a pharmacy"})

            if prescription.dependant.owner != user:
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": "Selected prescription does not belong to any of your dependants"})

            if models.ForwardPrescription.objects.filter(prescription=prescription, facility=facility).count() > 0:
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": f"Prescription already forwarded to {facility.title}"})


class PharmacySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Facility
        fields = ('id', 'url', 'title', 'town', 'road', 'county', 'town',
                  'building', 'latitude', 'longitude', 'facility_type', 'is_active')
