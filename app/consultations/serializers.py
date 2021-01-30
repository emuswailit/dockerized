
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from . import models
from users.models import Dependant
from drugs.models import Preparation, Product
from drugs.serializers import PreparationSerializer
from core.serializers import FacilitySafeSerializerMixin, OwnerSafeSerializerMixin
from datetime import *
from django.db import transaction
from django.contrib.auth import get_user_model
from entities.models import DepartmentalCharges

User = get_user_model()


class SlotSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Slots serializer
    """

    class Meta:
        model = models.Slots
        fields = ('id', 'url',  'employee', 'start', 'end',
                  'is_available', 'owner', 'created', 'updated')

        read_only_fields = ('id', 'url', 'owner', 'is_available',
                            'created', 'updated')

    def create(self, validated_data):
        """
Create slot after validating if time in betweeen in not taken
        """
        start = validated_data.pop('start')
        end = validated_data.pop('end')

        if end.timestamp() <= start.timestamp():
            raise serializers.ValidationError(
                "End time cannot be earlier that start time")

        if start.timestamp() >= end.timestamp():
            raise serializers.ValidationError(
                "Start time cannot be later that end time")

        if start and end:

            if models.Slots.objects.all().count() > 0:
                for slot in models.Slots.objects.all():
                    if start.timestamp() >= slot.start.timestamp() and end.timestamp() <= slot.end.timestamp():
                        raise serializers.ValidationError(
                            f"Slot is not available")
                    else:
                        created = models.Slots.objects.create(
                            start=start, end=end, **validated_data)
            else:
                created = models.Slots.objects.create(
                    start=start, end=end, **validated_data)

        return created


class AppointmentPaymentsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.AppointmentPayments
        fields = ('id', 'url', 'facility', 'dependant', 'slot', 'payment_method',
                  'amount', 'narrative', 'status', 'appointment_created', 'created', 'updated')
        read_only_fields = (
            'owner', 'facility', 'id', 'amount', 'narrative', 'status', 'subscription_created', 'appointment_created',
        )

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        user = User.objects.get(id=user_pk)
        slot = validated_data.pop('slot')
        dependant = validated_data.pop('dependant')
        if dependant and slot and user:
            # Facility has already done a trial plan
            if dependant.owner != user:
                raise serializers.ValidationError(
                    {"response_code":"1", "response_message": f"Selected dependant is not in your list"})

            appointment_payment = None
            today_payment = None

            if models.AppointmentPayments.objects.filter(
                    created__gt=datetime.today(), appointment_created=False).count() > 0:
                today_payment = models.AppointmentPayments.objects.get(
                    created__gt=datetime.today(), appointment_created=False)
            if today_payment:
                appointment_payment = today_payment
            else:
                if DepartmentalCharges.objects.filter(department=slot.employee.department).count() > 0:
                    departmental_charges = DepartmentalCharges.objects.get(
                        department=slot.employee.department)

                    new_appointment_payment = models.AppointmentPayments.objects.create(
                        dependant=dependant,
                        slot=slot,
                        amount=departmental_charges.get_total_departmental_charges(), 
                        narrative="Clinic charges", reference="fgvvvxdvfsgcg", **validated_data)
                    if new_appointment_payment:
                        appointment_payment = new_appointment_payment
                    else:
                        raise serializers.ValidationError(
                            "Appointment payment could not be created")
                    if appointment_payment:

                        created = models.Appointments.objects.create(
                            facility=user.facility,
                            owner=user,
                            appointment_payment=appointment_payment,
                            status="SCHEDULED")

                        if created:
                            # Mark slot as created
                            slot.is_available = False
                            slot.save()

                            appointment_payment.appointment_created = True
                            appointment_payment.save()

                else:
                    raise serializers.ValidationError(
                        f"Required data was not retrieved")
        return appointment_payment


class AppointmentsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Appointments serializer
    """

    class Meta:
        model = models.Appointments
        fields = ('id', 'url',  'facility', 'dependant', 'slot',
                  'status', 'owner', 'created', 'updated')

        read_only_fields = ('id', 'url', 'facility', 'owner', 'status',
                            'created', 'updated')

class AppointmentConsultationsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Appointment Consultations serializer
    """

    class Meta:
        model = models.AppointmentConsultations
        fields = (
            'id', 
            'url',  
            'facility', 
            'appointment', 
            'complaint_duration_length',
            'complaint_duration_unit',
            'location',
            'onset',
            'course',
            'aggravating_factors',
            'previous_treatment',
            'current_medication',
            'uses_alcohol',
            'uses_tobbaco',
            'is_married',
            'current_occupation',
            'allergies',
            'owner', 
            'created', 
            'updated'
            )

        read_only_fields = ('id', 'url', 'facility', 'owner', 'status',
                            'created', 'updated')




class PrescriptionItemSerializer(serializers.HyperlinkedModelSerializer):
    preparation_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.PrescriptionItem
        fields = (
            'id', 'url', 'facility', 'prescription', 'preparation', 'product', 'frequency', 'posology', 'instruction', 'duration', 'owner', 'preparation_details'
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'facility', 'prescription'
        )

    # TODO: Validate foreign key parameters
    def create(self, validated_data):
        try:
            preparation_id = validated_data.pop('preparation').id
            product_id = validated_data.pop('product').id

            preparation = Preparation.objects.get(id=preparation_id)
            product = Product.objects.get(id=product_id)

            if product and preparation:
                if preparation.id != product.preparation_id:
                    raise serializers.ValidationError(
                        f"{product.title} does not contain {preparation.title}")
                else:
                    created = models.PrescriptionItem.objects.create(
                        preparation=preparation, product=product, **validated_data)

        except Preparation.DoesNotExist:
            raise ValidationError('Imaginary preparation not allowed!')
        return created

    def get_preparation_details(self, obj):
        preparation = Preparation.objects.filter(
            id=obj.preparation_id)
        return PreparationSerializer(preparation, context=self.context, many=True).data


class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    prescription_item_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Prescription
        fields = ('id', 'url', 'dependant', 'comment', 'owner',
                  'prescription_item_details', 'is_signed')
        read_only_fields = (
            'created', 'updated', 'owner', 'facility', 'is_signed'
        )

    def get_prescription_item_details(self, obj):
        prescription_item = models.PrescriptionItem.objects.filter(
            prescription=obj)
        return PrescriptionItemSerializer(prescription_item, context=self.context, many=True).data


class PrescriptionUpdateSerializer(serializers.HyperlinkedModelSerializer):
    prescription_item_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Prescription
        fields = ('id', 'url', 'dependant', 'comment',
                  'owner', 'prescription_item_details')
        read_only_fields = ('id', 'url', 'dependant', 'comment',
                            'owner', 'prescription_item_details')

    def get_prescription_item_details(self, obj):
        prescription_item = models.PrescriptionItem.objects.filter(
            prescription=obj)
        return PrescriptionItemSerializer(prescription_item, context=self.context, many=True).data


class DependantSerializer(OwnerSafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    allergy_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = Dependant
        fields = ('id', 'url', 'account', 'owner', 'first_name', 'middle_name',
                  'last_name', 'gender', 'date_of_birth', 'allergy_details', 'created', 'updated')

        read_only_fields = ('id', 'facility', 'url', 'account', 'owner',
                            'created', 'updated')

    def get_allergy_details(self, obj):
        allergy = Allergy.objects.filter(dependant=obj)
        return AllergySerializer(allergy, context=self.context, many=True).data

class AllergySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Allergy
        fields = ('id', 'url', 'title', 'description','allergy_category',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'dependant',
                            'owner', 'created', 'updated')
