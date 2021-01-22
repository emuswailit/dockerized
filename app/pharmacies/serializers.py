from rest_framework import serializers
from . import models
from clients.models import ForwardPrescription
from clients.serializers import ForwardPrescriptionSerializer
from consultations.serializers import PrescriptionSerializer
from consultations.models import PrescriptionItem, Prescription
from inventory.models import VariationReceipt
from core.serializers import FacilitySafeSerializerMixin
from consultations.models import PrescriptionItem

#TODO : Select only items for a paticular facility
class QuoteItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.QuoteItem
        fields = "__all__"
        read_only_fields = (
            'owner',  'item_cost', 'quantity_pending', 'facility','prescription_quote','prescription_item'
        )
  
    def update(self, quote_item,validated_data):
        prescription_quote_item_pk = self.context.get("prescription_quote_item_pk")
        variation_item_id = validated_data.pop('variation_item').id
        if prescription_quote_item_pk and variation_item_id:
            prescription_quote_item = models.QuoteItem.objects.get(id=prescription_quote_item_pk)
            variation_item = VariationReceipt.objects.get(id=variation_item_id)

            
            if prescription_quote_item and variation_item:
                if prescription_quote_item.prescription_item.preparation !=variation_item.variation.product.preparation:
                    raise serializers.ValidationError(f"Incorrect selection: the prescribed drug is {prescription_quote_item.prescription_item.preparation.title} but you have selected {variation_item.variation.product.preparation.title} instead")
                else:
                    quote_item.variation_item=variation_item
                    quote_item.quantity_required=validated_data.pop('quantity_required')
                    quote_item.quantity_dispensed=validated_data.pop('quantity_dispensed')
                    quote_item.instructions=validated_data.pop('instructions')
                    quote_item.save()


            else:
                raise serializers.ValidationError(f"Corrupted input")

           
            
            
            # raise serializers.ValidationError(f"Its the fucking {prescription_quote_item_pk} and {variation_item_id}")
        else:
            raise serializers.ValidationError('Imaginary preparation not allowed!')

        return quote_item
    

        #TODO : Finish up this validation later
    # def create(self, validated_data):
    #     try:
    #         prescription_item_id = validated_data.pop('prescription_item').id
    #         quoted_item_id = validated_data.pop('quoted_item').id

    #         prescription_item = PreparationItem.objects.get(id=prescription_item_id)
    #         quoted_item = VariationReceipt.objects.get(id=quoted_item_id)

    #         if prescription_item and quoted_item:
    #             if prescription_item.preparation.id !=quoted_item.variation.product.preparation.id:
    #                 raise serializers.ValidationError(f"Kindly choose item with same preparation as prescribed item")
    #             else:
    #                 created =models.QuoteItem.objects.create(prescription_item=prescription_item,quoted_item=quoted_item, **validated_data)
                
    #     except PrescriptionItem.DoesNotExist:
    #         raise ValidationError('Imaginary preparation not allowed!')
    #     return created


class PrescriptionQuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_item_details = serializers.SerializerMethodField(
        read_only=True)
    forward_prescription_details = serializers.SerializerMethodField(
        read_only=True)
   


    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'forward_prescription', 'prescription_cost','client_confirmed','owner','quote_item_details','forward_prescription_details','created','updated')
        read_only_fields = (
            'owner', 'prescription_cost', 'facility','client_confirmed',
        )

    def get_forward_prescription_details(self, obj):
        prescription = models.ForwardPrescription.objects.filter(
            id=obj.forward_prescription_id)
        return ForwardPrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            prescription_quote=obj)
        return QuoteItemSerializer(quote_item, context=self.context, many=True).data
