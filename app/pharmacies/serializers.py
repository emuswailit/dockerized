from rest_framework import serializers, exceptions
from . import models
from clients.models import ForwardPrescription
from consultations.serializers import PrescriptionSerializer
from consultations.models import PrescriptionItem, Prescription
from inventory.models import VariationReceipt
from core.serializers import FacilitySafeSerializerMixin
from consultations.models import PrescriptionItem
# from clients.serializers import ForwardPrescriptionSerializer
from datetime import date
from django.db import IntegrityError, transaction
from consultations.serializers import PrescriptionItemSerializer

# TODO : Select only items for a paticular facility


class QuoteItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    prescription_item_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.QuoteItem
        fields = (
            'id',
            'url',
            'facility',
            'prescription_quote',
            'prescription_item',
            'dose_divisible',
            'variation_item',
            'quantity_required',
            'quantity_pending',
            'quantity_dispensed',
            'get_total_items_cost',
            'get_dispensed_items_cost',
            'get_pending_items_cost',
            'instructions',
            'client_comment',
            'created',
            'updated',
            'owner',
            'item_accepted',
            'prescription_item_details'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'prescription_quote',
            'prescription_item',
            'quantity_pending',
            'quantity_dispensed',
            'get_total_items_cost',
            'get_dispensed_items_cost',
            'get_pending_items_cost',
            'client_comment',
            'created',
            'updated',
            'owner',
            'item_accepted',
            'prescription_item_details'
        )

    def get_prescription_item_details(self, obj):
        prescription_item = models.PrescriptionItem.objects.filter(
            id=obj.prescription_item.id)
        return PrescriptionItemSerializer(prescription_item, context=self.context, many=True).data

    def update(self, quote_item, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        prescription_quote_item_pk = self.context.get(
            "prescription_quote_item_pk")

        # Retrieve data items submitted
        variation_item_id = validated_data.pop('variation_item').id
        quantity_required = int(validated_data.pop('quantity_required'))
        if prescription_quote_item_pk and variation_item_id:

            prescription_quote_item = models.QuoteItem.objects.get(
                id=prescription_quote_item_pk)

            if prescription_quote_item.prescription_quote.pharmacist_confirmed == True and prescription_quote_item.prescription_quote.client_confirmed == True:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": f"Prescription is already confirmed thus cannot be ammended"})

            variation_item = VariationReceipt.objects.get(id=variation_item_id)
            if prescription_quote_item and variation_item:
                if prescription_quote_item.prescription_item.preparation != variation_item.variation.product.preparation:
                    raise serializers.ValidationError(
                        f"Incorrect selection: the prescribed drug is {prescription_quote_item.prescription_item.preparation.title} but you have selected {variation_item.variation.product.preparation.title} instead")
                else:

                    # Update the quote item
                    quote_item.variation_item = variation_item
                    quote_item.quantity_required = quantity_required
                    quote_item.instructions = validated_data.pop(
                        'instructions')
                    quote_item.dose_divisible = validated_data.pop(
                        'dose_divisible')
                    quote_item.quantity_pending = quantity_required
                    quote_item.save()

                    # Check if user has an existing open order in the facility created today

            else:
                raise serializers.ValidationError(f"Corrupted input")

            # raise serializers.ValidationError(f"Its the fucking {prescription_quote_item_pk} and {variation_item_id}")
        else:
            raise serializers.ValidationError(
                'Imaginary preparation not allowed!')

        return quote_item


class PrescriptionQuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_item_details = serializers.SerializerMethodField(
        read_only=True)
    # forward_prescription_details = serializers.SerializerMethodField(
    #     read_only=True)

    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'url', 'forward_prescription', 'get_total_quote_cost',
                  'client_confirmed',  'pharmacist_confirmed', 'owner', 'quote_item_details', 'created', 'updated')
        read_only_fields = (
            'owner', 'prescription_cost', 'facility', 'client_confirmed',
        )

    # def get_forward_prescription_details(self, obj):
    #     prescription = models.ForwardPrescription.objects.filter(
    #         id=obj.forward_prescription_id)
    #     return ForwardPrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            prescription_quote=obj)
        return QuoteItemSerializer(quote_item, context=self.context, many=True).data


class PharmacistConfirmQuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_item_details = serializers.SerializerMethodField(
        read_only=True)
    # forward_prescription_details = serializers.SerializerMethodField(
    #     read_only=True)

    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'url', 'forward_prescription', 'prescription_cost',
                  'client_confirmed',  'pharmacist_confirmed', 'owner', 'quote_item_details', 'created', 'updated')
        read_only_fields = (
            'owner', 'prescription_cost', 'facility', 'client_confirmed',         'forward_prescription'
        )

    # def get_forward_prescription_details(self, obj):
    #     prescription = models.ForwardPrescription.objects.filter(
    #         id=obj.forward_prescription_id)
    #     return ForwardPrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            prescription_quote=obj)
        return QuoteItemSerializer(quote_item, context=self.context, many=True).data


class ClientQuoteItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    prescription_item_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.QuoteItem
        fields = (
            'owner',
            'get_total_items_cost',
            'get_dispensed_items_cost',
            'get_pending_items_cost',
            'quantity_pending',
            'facility',
            'prescription_quote',
            'prescription_item',
            'quantity_dispensed',
            'client_comment',
            'item_accepted',
            'prescription_item_details'
        )
        read_only_fields = (
            'owner',  'get_total_items_cost',
            'get_dispensed_items_cost',
            'get_pending_items_cost',  'quantity_pending', 'facility', 'prescription_quote', 'prescription_item', 'instructions', 'quantity_required', 'variation_item', 'dose_divisible', 'fully_dispensed', 'prescription_item_details',
        )

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            prescription_quote=obj)
        return QuoteItemSerializer(quote_item, context=self.context, many=True).data

    def get_prescription_item_details(self, obj):
        prescription_item = models.PrescriptionItem.objects.filter(
            id=obj.prescription_item.id)
        return PrescriptionItemSerializer(prescription_item, context=self.context, many=True).data

    @transaction.atomic
    def update(self, quote_item, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        prescription_quote_item_pk = self.context.get(
            "prescription_quote_item_pk")
        user_id = self.context.get("user")

        # Retrieve data items submitted

        quantity_dispensed = int(validated_data.pop('quantity_dispensed'))
        item_accepted = validated_data.pop('item_accepted')
        client_comment = validated_data.pop('client_comment')

        order = None

        today = date.today()
        obj, created = models.Order.objects.get_or_create(facility=quote_item.facility, prescription_quote=quote_item.prescription_quote,
                                                          created=today, is_open=True, owner=quote_item.prescription_quote.forward_prescription.owner)
        if obj:
            order = obj
            # raise serializers.ValidationError("Retrieved very well")
        elif created:
            order = created
            # raise serializers.ValidationError("Created very well")

        if prescription_quote_item_pk:

            prescription_quote_item = models.QuoteItem.objects.get(
                id=prescription_quote_item_pk)
            if prescription_quote_item:

                # Update the quote item
                quote_item.quantity_dispensed = quote_item.quantity_dispensed+quantity_dispensed
                quote_item.quantity_pending = quote_item.quantity_pending - quantity_dispensed
                quote_item.save()

                try:
                    if quote_item.quantity_pending < 1:
                        quote_item.fully_dispensed = True
                        quote_item.save()
                        raise serializers.ValidationError(
                            {"message": f"Prescription item is fully dispensed"})

                    if quantity_dispensed > quote_item.quantity_pending and quantity_dispensed > 0:
                        raise serializers.ValidationError(
                            {"message": f"You can only requisition quantity {quote_item.quantity_pending} or less"})

                    quote_item.item_accepted = item_accepted
                    quote_item.client_comment = client_comment

                    order_item = models.OrderItem.objects.create(
                        facility=quote_item.facility, quote_item=quote_item, quantity=quantity_dispensed, owner=quote_item.prescription_quote.forward_prescription.owner)
                    order.items.add(order_item)
                    order.save()
                except IntegrityError as e:
                    raise exceptions.NotAcceptable(
                        {"detail": ["Order item must be to be unique. Similar item is already added!", ]})

            else:
                raise serializers.ValidationError(f"Corrupted input")

            # raise serializers.ValidationError(f"Its the fucking {prescription_quote_item_pk} and {variation_item_id}")
        else:
            raise serializers.ValidationError(
                'Imaginary preparation not allowed!')

        return quote_item


class OrderSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    order_items_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Order
        fields = ('id', 'url', 'facility', 'prescription_quote', 'is_confirmed', 'payment_method',
                  'owner', 'get_total_price', 'order_items_details', 'created', 'updated')
        read_only_fields = (
            'owner',  'facility', 'prescription_quote', 'get_total_price'
        )

    def get_order_items_details(self, obj):
        order_item = models.OrderItem.objects.filter(
            order=obj)
        return OrderItemSerializer(order_item, context=self.context, many=True).data

    @transaction.atomic
    def update(self, order, validated_data):
        is_confirmed = validated_data.pop('is_confirmed')
        payment_method = validated_data.pop('payment_method')

        if is_confirmed:
            payment = None

            if order:
                # Create or retrieve transaction
                obj, created = models.Payment.objects.get_or_create(
                    facility=order.facility, order=order, owner=order.owner)

                if obj:
                    order.is_confirmed = is_confirmed
                    order.payment_method = payment_method
                    order.save()

                    # TODO : Process payment based on selected payment method

        return order


class OrderItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ('id', 'url', 'facility', 'quote_item',
                  'order', 'get_total_item_price')
        read_only_fields = (
            'owner',  'facility', 'quote_item', 'quantity'
        )
