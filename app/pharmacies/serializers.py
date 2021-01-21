from rest_framework import serializers
from . import models
from clients.models import ForwardPrescription
from clients.serializers import ForwardPrescriptionSerializer
from consultations.serializers import PrescriptionSerializer
from consultations.models import PrescriptionItem, Prescription


class QuoteItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.QuoteItem
        fields = "__all__"
        read_only_fields = (
            'owner',  'item_cost', 'quantity_pending', 'facility'
        )


class PrescriptionQuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_item_details = serializers.SerializerMethodField(
        read_only=True)
    forward_prescription_details = serializers.SerializerMethodField(
        read_only=True)
   

    # def validate_prescription(self, prescription):
    #     if prescription:
    #         prescription_items = PrescriptionItem.objects.get(prescription=prescription)

    #         if prescription_items.count()>0:
    #             pass

    #         else:
    #             raise serializers.ValidationError("There is a prescription")
    #     else:
    #         raise serializers.ValidationError("There is a prescription attached")


    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'prescription', 'prescription_cost','client_confirmed','owner','quote_item_details','forward_prescription_details','created','updated')
        read_only_fields = (
            'owner', 'prescription_cost', 'facility','client_confirmed'
        )

    def get_forward_prescription_details(self, obj):
        prescription = models.ForwardPrescription.objects.filter(
            id=obj.prescription_id)
        return ForwardPrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            id=obj.prescription_id)
        return QuoteItemSerializer(quote_item, context=self.context, many=True).data
