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
from django.contrib.auth import get_user_model

# TODO : Select only items for a paticular facility

User = get_user_model()


class PharmacistUpdateQuoteItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
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
            'quoted_by',
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
            'quoted_by',
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
        user_pk = self.context.get(
            "user_pk")
        if user_pk:
            user = User.objects.get(id=user_pk)

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
                    quote_item.quoted_by = user
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
                  'client_confirmed',  'pharmacist_confirmed', 'owner', 'quoted_by', 'quote_item_details', 'created', 'updated')
        read_only_fields = (
            'owner', 'quoted_by', 'facility', 'client_confirmed',
        )

    # def get_forward_prescription_details(self, obj):
    #     prescription = models.ForwardPrescription.objects.filter(
    #         id=obj.forward_prescription_id)
    #     return ForwardPrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            prescription_quote=obj)
        return PharmacistUpdateQuoteItemSerializer(quote_item, context=self.context, many=True).data


class PharmacistConfirmPrescriptionQuoteSerializer(serializers.HyperlinkedModelSerializer):

    # forward_prescription_details = serializers.SerializerMethodField(
    #     read_only=True)

    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'url', 'forward_prescription', 'get_total_quote_cost',
                  'client_confirmed',  'pharmacist_confirmed', 'owner', 'quoted_by', 'created', 'updated')
        read_only_fields = (
            'owner', 'quoted_by', 'facility', 'client_confirmed',         'forward_prescription'
        )

    def update(self, prescription_quote, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve user from context

        user_pk = self.context.get(
            "user_pk")

        # Update quoted by
        if user_pk:
            user = User.objects.get(id=user_pk)
            prescription_quote.quoted_by_id = user_pk
            prescription_quote.save()
        return prescription_quote


class ClientConfirmQuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_item_details = serializers.SerializerMethodField(
        read_only=True)
    # forward_prescription_details = serializers.SerializerMethodField(
    #     read_only=True)

    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'url', 'forward_prescription', 'get_total_quote_cost', 'payment_method',
                  'client_confirmed',  'pharmacist_confirmed', 'owner', 'quote_item_details', 'created', 'updated')
        read_only_fields = (
            'owner',  'facility', 'pharmacist_confirmed', 'forward_prescription'
        )

    # def get_forward_prescription_details(self, obj):
    #     prescription = models.ForwardPrescription.objects.filter(
    #         id=obj.forward_prescription_id)
    #     return ForwardPrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        quote_item = models.QuoteItem.objects.filter(
            prescription_quote=obj)
        return PharmacistUpdateQuoteItemSerializer(quote_item, context=self.context, many=True).data

    @transaction.atomic
    def update(self, prescription_quote, validated_data):
        """
        Cilent confirms prescription quote, creates payment

        """

        user_id = self.context.get("user")

        # Retrieve data items submitted

        client_confirmed = validated_data.pop('client_confirmed')
        payment_method = validated_data.pop('payment_method')

        if client_confirmed == True:
            prescription_quote.client_confirmed = client_confirmed
            prescription_quote.save()

            # Client confirms that he/she is ok with order and order
            if models.Order.objects.filter(prescription_quote=prescription_quote).count() > 0:
                order = models.Order.objects.get(
                    prescription_quote=prescription_quote)
                order.client_confirmed = client_confirmed
                order.save()

                order_items = models.OrderItem.objects.filter(order=order)
                if order_items.count() > 0:
                    for item in order_items:
                        item.client_confirmed = client_confirmed
                        item.save()

                if models.PharmacyPayments.objects.filter(order=order).count() > 0:
                    payment = models.PharmacyPayments.objects.get(order=order)
                else:
                    payment = models.PharmacyPayments.objects.create(
                        facility=prescription_quote.facility, owner=prescription_quote.owner, order=order, payment_method=payment_method)
        else:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "You have rejected the offer"})
        return prescription_quote


class ClientQuoteItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializer for a client to edit a quote item offer. Client can also reduce quantity if it is permissible for the drug
    """
    prescription_item_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.QuoteItem
        fields = (
            'owner',
            'quoted_by',
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
            'get_pending_items_cost', 'quoted_by',  'quantity_pending', 'facility', 'prescription_quote', 'prescription_item', 'instructions', 'quantity_required', 'variation_item', 'dose_divisible', 'fully_dispensed', 'prescription_item_details',
        )

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
                                                          created=today, client_confirmed=True, owner=quote_item.prescription_quote.forward_prescription.owner)
        if obj:
            order = obj
            # raise serializers.ValidationError("Retrieved very well")
        elif created:
            order = created

        if prescription_quote_item_pk:
            quote_item = models.QuoteItem.objects.get(
                id=prescription_quote_item_pk)
            if quote_item and quantity_dispensed and item_accepted:
                if quote_item.quantity_pending < 1:
                    quote_item.fully_dispensed = True
                    quote_item.save()
                    raise serializers.ValidationError(
                        {"message": f"Prescription item is fully dispensed {quote_item.quantity_pending}"})

                # # Dispended  item quantity  must be equal to or less than pending quantity
                if quantity_dispensed > quote_item.quantity_pending and quantity_dispensed > 0:
                    raise serializers.ValidationError(
                        {"message": f"You can only requisition quantity {quote_item.quantity_pending} or less"})

                #     # Update the quote item
                quote_item.quantity_dispensed = quote_item.quantity_dispensed+quantity_dispensed
                quote_item.quantity_pending = quote_item.quantity_pending - quantity_dispensed
                quote_item.item_accepted = item_accepted
                quote_item.client_comment = client_comment
                quote_item.save()

                # Check if item is already added to order. If added, update quantity or else create new order item
                if models.OrderItem.objects.filter(quote_item=quote_item, created=date.today()).count() > 0:
                    order_item = models.OrderItem.objects.get(
                        quote_item=quote_item)
                    order_item.quantity += quantity_dispensed
                    order_item.save()
                else:
                    order_item = models.OrderItem.objects.create(
                        order=order,
                        facility=quote_item.facility,
                        quote_item=quote_item,
                        quantity=quantity_dispensed,
                        owner=quote_item.prescription_quote.forward_prescription.owner)

            else:
                raise serializers.ValidationError(
                    f"Check your quantity and also if you have accepted the offer")

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
        fields = ('id', 'url', 'facility', 'prescription_quote', 'client_confirmed',
                  'owner', 'get_total_price', 'order_items_details', 'created', 'updated')
        read_only_fields = (
            'owner',  'facility', 'prescription_quote', 'get_total_price'
        )

    def get_order_items_details(self, obj):
        order_item = models.OrderItem.objects.filter(
            order=obj)
        return OrderItemSerializer(order_item, context=self.context, many=True).data

    @ transaction.atomic
    def update(self, order, validated_data):
        client_confirmed = validated_data.pop('client_confirmed')

        if client_confirmed:
            payment = None

            if order:
                # Create or retrieve transaction
                obj, created = models.Payment.objects.get_or_create(
                    facility=order.facility, order=order, owner=order.owner)

                if obj:
                    order.client_confirmed = client_confirmed
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


class PharmacyPaymentsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.PharmacyPayments
        fields = ('id', 'url', 'facility', 'order', 'reference', 'status', 'get_amount',
                  'owner', 'created', 'updated')
        read_only_fields = (
            'owner',  'facility', 'order',
        )

    def get_amount(self):
        return self.order.get_total_price()
