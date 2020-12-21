from rest_framework import serializers
from . import models
from clients.models import ForwardPrescription
from clients.serializers import ForwardPrescriptionSerializer


class QuoteItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.QuoteItem
        fields = "__all__"
        read_only_fields = (
            'owner',  'prescription', 'item_cost', 'quantity_pending'
        )


class PrescriptionQuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_item_details = serializers.SerializerMethodField(
        read_only=True)
    forward_prescription_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.PrescriptionQuote
        fields = "__all__"
        read_only_fields = (
            'owner', 'prescription', 'prescription_cost'
        )

    def get_forward_prescription_details(self, obj):
        prescription = models.ForwardPrescription.objects.filter(
            id=obj.prescription_id)
        return ForwardPrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            id=obj.prescription_id)
        return QuoteItemSerializer(quote_item, context=self.context, many=True).data
