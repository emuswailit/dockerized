from rest_framework import serializers
from core.serializers import FacilitySafeSerializerMixin
from . import models
from django.db import transaction
from django.contrib.auth import get_user_model


User = get_user_model()


# class ProfessionSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = models.Professions
#         fields = ('id', 'url', 'title', 'description', 'professional_role', 'is_active',
#                   'created', 'updated')

#         read_only_fields = ('id', 'url', 'is_active',
#                             'created', 'updated')


class ProfessionalSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Professionals
        fields = ('id', 'url', 'cadre', 'user', 'certificate', 'national_id', 'is_active', 'is_available', 'owner', 'user',
                  'is_verified', 'created', 'updated')

        read_only_fields = ('id', 'url', 'user', 'owner', 'is_active', 'is_available', 'is_verified',
                            'created', 'updated')
    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        cadre = validated_data.pop('cadre')
        if user_pk:
            # Retrieve user using forwarded ID and set cadre
            user= User.objects.get(id=user_pk)
            user.cadre= cadre
            user.is_professional=True
            user.save()
            created =models.Professionals.objects.create(cadre=cadre, **validated_data)
        else:
            raise serializers.ValidationError(f"Sio professional")

        return created


class ProfessionalUpdateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Professionals
        fields = ('id', 'url', 'cadre', 'user', 'certificate', 'national_id', 'is_active', 'is_available', 'owner', 'user',
                  'is_verified', 'created', 'updated')

        read_only_fields = ('id', 'url', 'user', 'owner', 'cadre', 'certificate', 'national_id', 'is_available',
                            'created', 'updated')


class ProfessionalAvailabilitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Professionals
        fields = ('id', 'url', 'cadre', 'user', 'certificate', 'national_id', 'is_active', 'is_available', 'owner', 'user',
                  'is_verified', 'created', 'updated')

        read_only_fields = ('id', 'url', 'user', 'owner', 'cadre', 'certificate', 'national_id', 'is_active', 'is_verified',
                            'created', 'updated')


class ProfessionalAnnualLicenceSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Professionals
        fields = ('id', 'url', 'facility', 'professional', 'expires_on', 'is_current', 'owner'
                  'created', 'updated')

        read_only_fields = ('id', 'url', 'owner', 'is_current'
                            'created', 'updated')


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Department
        fields = (
            'id',
            'url',
            'title',
            'description',
            'open_monday',
            'open_tuesday',
            'open_wednesday',
            'open_thursday',
            'open_friday',
            'open_saturday',
            'open_sunday',
            'owner',
            'created',
            'updated',)
        read_only_fields = (
            'id', 'owner',
        )






class EmployeesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for employees model

    """
    class Meta:
        model = models.Employees
        fields = ('id', 'url', 'professional','department', 'designation', 'description', 'is_admin', 'is_active', 'is_superintendent', 'owner',
                  'created', 'updated')

        read_only_fields = ('id', 'url', 'owner', 'is_active',
                            'created', 'updated')
    
    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        professional = validated_data.pop('professional')
        if user_pk and professional:
            # Retrieve user using forwarded ID and set cadre
            employee_creator= User.objects.get(id=user_pk)
            professional.user.facility= employee_creator.facility
            created =models.Employees.objects.create(professional=professional, **validated_data)
        else:
            raise serializers.ValidationError(f"Sio professional")

        return created

        