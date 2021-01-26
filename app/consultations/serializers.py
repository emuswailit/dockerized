
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from . import models
from users.models import Dependant, Allergy
from drugs.models import Preparation, Product
from drugs.serializers import PreparationSerializer
from users.serializers import AllergySerializer
from core.serializers import FacilitySafeSerializerMixin


#Slots Serializer
class SlotSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = models.Slots
        fields = ('id', 'url', 'clinic', 'doctor', 'start', 'end',
                  'is_available', 'created', 'updated')

        read_only_fields = ('id', 'url', 
                            'created', 'updated')

    def create(self, validated_data):
         start = validated_data.pop('start')
         if start:
             raise serializers.ValidationError("Date is {start}")




class PrescriptionItemSerializer(serializers.HyperlinkedModelSerializer):
    preparation_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.PrescriptionItem
        fields =(
            'id','url','facility','prescription','preparation','product','frequency','posology','instruction','duration','owner','preparation_details'
        )
        read_only_fields = (
            'created', 'updated', 'owner','facility','prescription'
        )

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=models.PrescriptionItem.objects.all(),
        #         fields=['prescription', 'preparation', 'product']
        #     )
        # ]
    # TODO: Validate foreign key parameters
    def create(self, validated_data):
        try:
            preparation_id = validated_data.pop('preparation').id
            product_id = validated_data.pop('product').id

            preparation = Preparation.objects.get(id=preparation_id)
            product = Product.objects.get(id=product_id)

            if product and preparation:
                if preparation.id !=product.preparation_id:
                    raise serializers.ValidationError(f"{product.title} does not contain {preparation.title}")
                else:
                    created =models.PrescriptionItem.objects.create(preparation=preparation,product=product, **validated_data)
                
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
        fields = ('id','url','dependant','comment','owner','prescription_item_details','is_signed')
        read_only_fields = (
            'created', 'updated', 'owner','facility','is_signed'
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
        fields = ('id','url','dependant','comment','owner','prescription_item_details')
        read_only_fields = ('id','url','dependant','comment','owner','prescription_item_details')
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

        read_only_fields = ('id','facility', 'url', 'account', 'owner',
                            'created', 'updated')

    def get_allergy_details(self, obj):
        allergy = Allergy.objects.filter(dependant=obj)
        return AllergySerializer(allergy, context=self.context, many=True).data


