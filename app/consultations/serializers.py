
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from . import models
from users.models import Dependant, Allergy
from drugs.models import Preparation
from drugs.serializers import PreparationSerializer
from users.serializers import AllergySerializer


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

    def get_preparation_details(self, obj):
        preparation = Preparation.objects.filter(
            id=obj.preparation_id)
        return PreparationSerializer(preparation, context=self.context, many=True).data


class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    prescription_item_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Prescription
        fields = ('id','url','dependant','comment','owner','prescription_item_details')
        read_only_fields = (
            'created', 'updated', 'owner', 'dependant','facility'
        )

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


# class DependantSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = models.Dependant
#         fields = ('id', 'url', 'account', 'owner', 'first_name', 'middle_name',
#                   'last_name', 'gender', 'date_of_birth', 'allergy_details', 'created', 'updated')

#         read_only_fields = ('id', 'url', 'account', 'owner',
#                             'created', 'updated')
