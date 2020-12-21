from rest_framework import serializers
from core.serializers import FacilitySafeSerializerMixin
from . import models


class PharmacistSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Pharmacist
        fields = (
            'id',
            'url',
            'facility',
            'cadre',
            'board_number',
            'certificate',
            'is_active',
            'is_available',
            'is_verified',
            'owner',
            'created',
            'updated'
        )

        read_only_fields = ('is_active', 'is_available', 'facility',
                            'is_verified', 'owner')


class CourierSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Courier
        fields = (
            'id',
            'url',
            'facility',
            'vehicle',
            'vehicle_number',
            'permit_number',
            'licence',
            'is_available',
            'is_verified',
            'is_active',
            'owner',
            'created',
            'updated'
        )

        read_only_fields = ('is_active', 'is_available',
                            'is_verified', 'owner')


class PrescriberSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Prescriber
        fields = (
            'id',
            'url',
            'salutation',
            'cadre',
            'board_number',
            'certificate',
            'is_available',
            'is_verified',
            'is_active',
            'owner',
            'created',
            'updated'
        )

        read_only_fields = ('is_active', 'is_available',
                            'is_verified', 'owner')


class PharmacistPhotoSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PharmacistPhoto
        fields = (
            'id',
            'url',
            'facility_id',
            'pharmacist',
            'photo',

            'owner',
            'created',
            'updated'
        )
        read_only_fields = ('owner', 'pharmacist')


class CourierPhotoSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CourierPhoto
        fields = (
            'id',
            'url',
            'facility_id',
            'courier',
            'photo',

            'owner',
            'created',
            'updated'
        )
        read_only_fields = ('owner', 'courier')


class PrescriberPhotoSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PrescriberPhoto
        fields = (
            'id',
            'url',
            'facility_id',
            'prescriber',
            'photo',

            'owner',
            'created',
            'updated'
        )
        read_only_fields = ('owner', 'prescriber')

# Not using FaciliySafeSerializerMixin in order to view all pharmacists


class FacilityPharmacistSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.FacilityPharmacist
        fields = (
            'id',
            'url',

            'pharmacist',
            'is_active',
            'is_superintendent',
            'owner',
            'created',
            'updated'
        )

        read_only_fields = ('pharmacist', 'owner')


class FacilityPrescriberSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.FacilityPrescriber
        fields = (
            'id',
            'url',

            'prescriber',
            'is_active',
            'is_superintendent',
            'owner',
            'created',
            'updated'
        )

        read_only_fields = ('prescriber', 'owner',)


class FacilityCourierSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.FacilityCourier
        fields = (
            'id',
            'url',
            'facility',
            'courier',
            'is_active',
            'owner',
            'created',
            'updated'
        )

        read_only_fields = ('pharmacist', 'courier', 'owner')
