
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from . import models
from users.models import Dependant, Allergy
from drugs.models import Preparation, Product
from drugs.serializers import PreparationSerializer
from users.serializers import AllergySerializer
from core.serializers import FacilitySafeSerializerMixin
from datetime import *


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
                        created = models.Slots.objects.create(start=start, end=end, **validated_data)
            else:
                created = models.Slots.objects.create(start=start, end=end, **validated_data)

        return created

class AppointmentsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Appointments serializer
    """

    class Meta:
        model = models.Appointments
        fields = ('id', 'url',  'facility', 'dependant', 'slot',
                  'status', 'owner', 'created', 'updated')

        read_only_fields = ('id', 'url','facility', 'owner', 'status',
                            'created', 'updated')





class PrescriptionItemSerializer(serializers.HyperlinkedModelSerializer):
    preparation_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.PrescriptionItem
        fields = (
            'id', 'url', 'facility', 'prescription','preparation','product','frequency','posology','instruction','duration','owner','preparation_details'
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
        fields = ('id', 'url', 'dependant', 'comment','owner','prescription_item_details','is_signed')
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
        fields = ('id', 'url', 'dependant', 'comment','owner','prescription_item_details')
        read_only_fields = ('id', 'url', 'dependant', 'comment','owner','prescription_item_details')

    def get_prescription_item_details(self, obj):
        prescription_item = models.PrescriptionItem.objects.filter(
            prescription=obj)
        return PrescriptionItemSerializer(prescription_item, context=self.context, many=True).data


class DependantSerializer(serializers.HyperlinkedModelSerializer):
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
