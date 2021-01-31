from rest_framework import serializers
from core.serializers import FacilitySafeSerializerMixin
from . import models
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotAcceptable
from users.models import Facility


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
        fields = ('id', 'url', 'facility', 'cadre', 'user', 'certificate', 'national_id', 'is_active', 'is_available', 'owner', 'user',
                  'is_verified', 'created', 'updated')

        read_only_fields = ('id', 'url', 'facility', 'user', 'owner', 'is_active', 'is_available', 'is_verified',
                            'created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        cadre = validated_data.pop('cadre')
        if user_pk:
            # Retrieve user using forwarded ID and set cadre
            user = User.objects.get(id=user_pk)
            if models.Professionals.objects.filter(owner=user).count() == 1:
                raise serializers.ValidationError(
                    "You are already registered as a professional")
            else:
                user.cadre = cadre
                user.is_professional = True
                user.save()
                created = models.Professionals.objects.create(
                    cadre=cadre, **validated_data)
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
        fields = ('id', 'url', 'facility', 'cadre', 'user', 'certificate', 'national_id', 'is_active', 'is_available', 'owner', 'user',
                  'is_verified', 'created', 'updated')

        read_only_fields = ('id', 'facility', 'url', 'user', 'owner', 'cadre', 'certificate', 'national_id', 'is_active', 'is_verified',
                            'created', 'updated')

    @transaction.atomic
    def update(self, instance, validated_data):
        updated = super().update(instance, validated_data)
        default_facility = Facility.objects.default_facility()

        user_pk = self.context.get("user_pk")
        user = User.objects.get(id=user_pk)

        # Administrator cannot change away fro a facility he/she created
        if user.is_administrator:
            raise NotAcceptable(
                {"response_code": 1, "response_message": f"You cannot change your facility from {user.facility.title} because you created it"})

        # Take the professional back to default facility and make use visible to facilities for recruitment
        if 'is_available' in validated_data:
            availability_status = validated_data['is_available']
            if availability_status == True:
                user.facility = default_facility
                user.save()
                updated.is_available = availability_status
                updated.facility = default_facility
                updated.save()
            else:
                raise NotAcceptable({"response_message": f"Not acceptable"})

        return updated


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
        fields = ('id', 'url', 'professional', 'department', 'job', 'is_admin', 'is_active', 'is_superintendent', 'owner',
                  'created', 'updated')

        read_only_fields = ('id', 'url', 'owner', 'is_active',
                            'created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        professional = validated_data.pop('professional')
        job = validated_data.pop('job')

        if job.cadre != professional.cadre:
            raise NotAcceptable(
                {"response_code": 1, "response_message": f"{professional.cadre.title} cannot be employed as {job.cadre}. Please select correct job for the selected professional"})
        i
        if user_pk and professional:
            # Retrieve user using forwarded ID and set cadre
            employee_creator = User.objects.get(id=user_pk)
            if employee_creator.facility.title == "Mobipharma":
                raise NotAcceptable(
                    {"response_code": 1, "response_message": f"You cannot create employees at {employee_creator.facility.title}"})
            else:
                professional.user.facility = employee_creator.facility
                created = models.Employees.objects.create(
                    professional=professional, job=job, **validated_data)
        else:
            raise serializers.ValidationError(
                f"You may not be registered in the system as a professional")

        return created


class JobsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Jobs
        fields = ('id', 'url', 'facility', 'title', 'description', 'cadre', 'is_active', 'maximum_positions', 'filled_positions', 'advertised_positions', 'is_advertised', 'owner',
                  'created', 'updated')

        read_only_fields = ('id', 'url', 'facility',  'owner',
                            'created', 'updated')
