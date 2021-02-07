from consultations.serializers import PrescriptionItemSerializer
from django.db import IntegrityError, transaction
from datetime import date
from consultations.models import PrescriptionItem
# from retailers.models import RetailVariations, RetailProducts
from consultations.models import PrescriptionItem, Prescription
from consultations.serializers import PrescriptionSerializer
from rest_framework import serializers, exceptions
from consultations.serializers import PrescriptionItemSerializer, PrescriptionSerializer
from rest_framework.validators import UniqueTogetherValidator
from retailers.models import PrescriptionQuote
from retailers.models import PrescriptionQuote, QuoteItem
from rest_framework import serializers
from core.serializers import FacilitySafeSerializerMixin
from . import models
from drugs.models import Products
from drugs.serializers import ProductsSerializer
from django.db import transaction
from django.contrib.auth import get_user_model
from users.models import Facility

User = get_user_model()


# TODO : Select only items for a paticular facility

Users = get_user_model()


class ForwardsSerializer(serializers.HyperlinkedModelSerializer):

    prescription_details = serializers.SerializerMethodField(
        read_only=True)

    prescription_quote_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Forwards
        fields = ('id', 'url', 'facility', 'prescription', 'comment',
                  'owner', 'prescription_details', 'prescription_quote_details', 'created', 'updated',)
        read_only_fields = (
            'id', 'owner',
        )

    def get_prescription_details(self, obj):
        prescription = Prescription.objects.filter(
            id=obj.prescription_id)
        return PrescriptionSerializer(prescription, context=self.context, many=True).data

    def get_prescription_quote_details(self, obj):
        """
        Display only quotes which have been confirmed by pharmacist for the client user to confirm and accept
        """
        prescription_quote = PrescriptionQuote.objects.filter(
            forward=obj, pharmacist_confirmed=True)
        return PrescriptionQuoteSerializer(prescription_quote, context=self.context, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)
        prescription = validated_data.pop('prescription')
        facility = validated_data.pop('facility')

        if prescription and user:

            if facility == Facility.objects.default_facility():
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": "You cannot forward a prescription to  this facility "})

            if facility.facility_type != "Pharmacy":
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": "Selected facility is not a pharmacy"})

            if prescription.dependant.owner != user:
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": "Selected prescription does not belong to any of your dependants"})

            if models.Forwards.objects.filter(prescription=prescription, facility=facility).count() > 0:
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": f"Prescription already forwarded to {facility.title}"})
            prescription_items = None

            if PrescriptionItem.objects.filter(prescription=prescription).count() > 0:
                prescription_items = PrescriptionItem.objects.filter(
                    prescription=prescription)

                created = models.Forwards.objects.create(
                    facility=facility, prescription=prescription, **validated_data)

                if created:
                    prescription_quote = PrescriptionQuote.objects.create(
                        facility=facility, forward=created, owner=user)

                    if prescription_quote:
                        pass
                        # for item in prescription_items:
                        #     QuoteItem.objects.create(
                        #         facility=facility, owner=user, prescription_quote=prescription_quote, prescription_item=item)

                    else:
                        raise serializers.ValidationError(
                            {'response_code': 1, "response_message": f"Prescription quote was not created"})

            else:
                raise serializers.ValidationError(
                    {'response_code': 1, "response_message": f"Prescription has no items added"})

            return created


class PharmacySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Facility
        fields = ('id', 'url', 'title', 'town', 'road', 'county', 'town',
                  'building', 'latitude', 'longitude', 'facility_type', 'is_active')


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
            'variation',
            'quantity_required',
            'quantity_pending',
            'quantity_dispensed',
            'pharmacist_instructions',
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
            'quantity_pending',
            'quantity_dispensed',
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
        variation_id = validated_data.pop('variation').id
        quantity_required = int(validated_data.pop('quantity_required'))
        if prescription_quote_item_pk and variation_id:

            prescription_quote_item = models.QuoteItem.objects.get(
                id=prescription_quote_item_pk)

            if prescription_quote_item.prescription_quote.pharmacist_confirmed == True and prescription_quote_item.prescription_quote.client_confirmed == True:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": f"Prescription is already confirmed thus cannot be ammended"})

            variation = RetailProducts.objects.get(id=variation_id)
            if prescription_quote_item and variation:
                if prescription_quote_item.prescription_item.preparation != variation.variation.product.preparation:
                    raise serializers.ValidationError(
                        f"Incorrect selection: the prescribed drug is {prescription_quote_item.prescription_item.preparation.title} but you have selected {variation.variation.product.preparation.title} instead")
                else:

                    # Update the quote item
                    quote_item.variation = variation
                    quote_item.quantity_required = quantity_required
                    quote_item.pharmacist_instructions = validated_data.pop(
                        'pharmacist_instructions')
                    quote_item.dose_divisible = validated_data.pop(
                        'dose_divisible')
                    quote_item.quantity_pending = quantity_required
                    quote_item.save()

                    # Check if user has an existing open order in the facility created today

            else:
                raise serializers.ValidationError(f"Corrupted input")

            # raise serializers.ValidationError(f"Its the fucking {prescription_quote_item_pk} and {variation_id}")
        else:
            raise serializers.ValidationError(
                'Imaginary preparation not allowed!')

        return quote_item


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
            'variation',
            'quantity_required',
            'quantity_pending',
            'quantity_dispensed',
            'pharmacist_instructions',
            'client_comment',
            'created',
            'updated',
            'owner',
            'processed_by',
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
            'client_comment',
            'created',
            'updated',
            'owner',
            'processed_by',
            'item_accepted',
            'prescription_item_details'
        )

    def get_prescription_item_details(self, obj):
        prescription_item = models.PrescriptionItem.objects.filter(
            id=obj.prescription_item_id)
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
            user = Users.objects.get(id=user_pk)

        # Retrieve data items submitted
        variation_id = validated_data.pop('variation').id
        quantity_required = int(validated_data.pop('quantity_required'))
        if prescription_quote_item_pk and variation_id:

            prescription_quote_item = models.QuoteItem.objects.get(
                id=prescription_quote_item_pk)

            if prescription_quote_item.prescription_quote.pharmacist_confirmed == True and prescription_quote_item.prescription_quote.client_confirmed == True:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": f"Prescription is already confirmed thus cannot be ammended"})

            variation = RetailProducts.objects.get(id=variation_id)
            if prescription_quote_item and variation.product:
                if prescription_quote_item.prescription_item.preparation != variation.product.preparation:
                    raise serializers.ValidationError(
                        {"response_code": 1, "response_message": f"Incorrect selection: the prescribed drug is {prescription_quote_item.prescription_item.preparation.title} but you have selected {variation.product.preparation.title} instead"})
                else:

                    # Update the quote item
                    quote_item.variation = variation
                    quote_item.quantity_required = quantity_required
                    quote_item.pharmacist_instructions = validated_data.pop(
                        'pharmacist_instructions')
                    quote_item.dose_divisible = validated_data.pop(
                        'dose_divisible')
                    quote_item.quantity_pending = quantity_required
                    quote_item.processed_by = user
                    quote_item.pharmacist_processing = True
                    quote_item.save()
                    quote_item.prescription_quote.processed_by = user
                    quote_item.prescription_quote.pharmacist_processing = True
                    # Lock prescription quote to user who has quoted item
                    quote_item.prescription_quote.save()

                    # Check if user has an existing open order in the facility created today

            else:
                raise serializers.ValidationError(
                    f"{variation.title} is not in the prescription ")

            # raise serializers.ValidationError(f"Its the fucking {prescription_quote_item_pk} and {variation_id}")
        else:
            raise serializers.ValidationError(
                'Imaginary preparation not allowed!')

        return quote_item


class PrescriptionQuoteSerializer(serializers.HyperlinkedModelSerializer):
    quote_item_details = serializers.SerializerMethodField(
        read_only=True)
    # forward_details = serializers.SerializerMethodField(
    #     read_only=True)

    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'url', 'forward',
                  'client_confirmed',  'pharmacist_confirmed', 'owner', 'processed_by', 'quote_item_details', 'created', 'updated')
        read_only_fields = (
            'owner', 'processed_by', 'facility', 'client_confirmed',
        )

    # def get_forward_details(self, obj):
    #     prescription = models.Forwards.objects.filter(
    #         id=obj.forward_id)
    #     return ForwardsSerializer(prescription, context=self.context, many=True).data

    def get_quote_item_details(self, obj):
        """
        Display only quote items which are not fully dispensed
        """
        quote_item = models.QuoteItem.objects.filter(
            prescription_quote=obj, fully_dispensed=False)
        return PharmacistUpdateQuoteItemSerializer(quote_item, context=self.context, many=True).data


class PharmacistConfirmPrescriptionQuoteSerializer(serializers.HyperlinkedModelSerializer):

    # forward_details = serializers.SerializerMethodField(
    #     read_only=True)

    class Meta:
        model = models.PrescriptionQuote
        fields = ('id', 'url', 'forward',
                  'client_confirmed',  'pharmacist_confirmed', 'owner', 'processed_by', 'created', 'updated')
        read_only_fields = (
            'owner', 'processed_by', 'facility', 'client_confirmed',         'forward'
        )

    def update(self, prescription_quote, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve user from context

        user_pk = self.context.get(
            "user_pk")

        quantity_dispensed = int(validated_data.pop('quantity_dispensed'))
        item_accepted = validated_data.pop('item_accepted')
        client_comment = validated_data.pop('client_comment')

        # Update quoted by
        if user_pk:
            # raise serializers.ValidationError(f"{user_pk}")
            user = Users.objects.get(id=user_pk)
            if QuoteItem.objects.filter(prescription_quote=prescription_quote).count() > 0:
                quote_items = QuoteItem.objects.filter(
                    prescription_quote=prescription_quote)
                for item in quote_items:
                    if item.quantity_required < 1:
                        prescription_quote.pharmacist_confirmed = False
                        item.pharmacist_confirmed = False
                        raise serializers.ValidationError(
                            {"response_code": 1, "response_message": f"Enter required quantity for {item.variation.title}"})
                    else:
                        item.pharmacist_confirmed = True
                        item.save()

                prescription_quote.processed_by = user
                prescription_quote.pharmacist_confirmed = True
                prescription_quote.save()
            else:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": f"Prescription quote has no items"})

        return prescription_quote


# class ClientConfirmQuoteSerializer(serializers.HyperlinkedModelSerializer):
#     quote_item_details = serializers.SerializerMethodField(
#         read_only=True)
#     # forward_details = serializers.SerializerMethodField(
#     #     read_only=True)

#     class Meta:
#         model = models.PrescriptionQuote
#         fields = ('id', 'url', 'forward', 'payment_method',
#                   'client_confirmed',  'pharmacist_confirmed', 'owner', 'quote_item_details', 'created', 'updated')
#         read_only_fields = (
#             'owner',  'facility', 'pharmacist_confirmed', 'forward'
#         )

#     # def get_forward_details(self, obj):
#     #     prescription = models.Forwards.objects.filter(
#     #         id=obj.forward_id)
#     #     return ForwardsSerializer(prescription, context=self.context, many=True).data

#     def get_quote_item_details(self, obj):
#         quote_item = models.QuoteItem.objects.filter(
#             prescription_quote=obj)
#         return PharmacistUpdateQuoteItemSerializer(quote_item, context=self.context, many=True).data

#     @transaction.atomic
#     def update(self, prescription_quote, validated_data):
#         """
#         Cilent confirms prescription quote, creates payment

#         """

#         user_id = self.context.get("user")

#         # Retrieve data items submitted

#         client_confirmed = validated_data.pop('client_confirmed')
#         payment_method = validated_data.pop('payment_method')

#         if not payment_method:
#             raise serializers.ValidationError(
#                 {"response_code": 1, "response_message": "Please select payment method"})

#         if client_confirmed == True and payment_method:
#             prescription_quote.client_confirmed = client_confirmed
#             prescription_quote.payment_method = payment_method
#             prescription_quote.save()

#             # Client confirms that he/she is ok with order and order
#             if models.Order.objects.filter(prescription_quote=prescription_quote).count() > 0:
#                 # raise serializers.ValidationError(
#                 #     {"response_code": 1, "response_message": "There is an order"})
#                 order = models.Order.objects.get(
#                     prescription_quote=prescription_quote)
#                 order.client_confirmed = client_confirmed
#                 order.save()

#                 order_items = models.OrderItem.objects.filter(order=order)
#                 if order_items.count() > 0:
#                     for item in order_items:
#                         item.client_confirmed = client_confirmed
#                         item.save()

#                 if models.PharmacyPayments.objects.filter(order=order).count() > 0:
#                     payment = models.PharmacyPayments.objects.get(order=order)
#                 else:
#                     payment = models.PharmacyPayments.objects.create(
#                         facility=prescription_quote.facility, owner=prescription_quote.owner, order=order, payment_method=payment_method)
#             else:
#                 raise serializers.ValidationError(
#                     {"response_code": 1, "response_message": "There was no order created for this quote"})

#         else:
#             raise serializers.ValidationError(
#                 {"response_code": 1, "response_message": "Please accept offer or enter payment method"})
#         return prescription_quote


class ClientAcceptQuoteItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializer for a client to edit a quote item offer. Client can also reduce quantity if it is permissible for the drug
    """
    prescription_item_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.QuoteItem
        fields = (
            'id',
            'url',
            'facility',
            'owner',
            'processed_by',
            'quantity_required',
            'quantity_dispensed',
            'quantity_pending',
            'dose_divisible',
            'fully_dispensed',
            'prescription_quote',
            'prescription_item',
            'client_comment',
            'client_confirmed',
            'item_accepted',
            'client_confirmed',
            'pharmacist_confirmed',
            'pharmacist_instructions',
            'prescription_item_details'

        )
        read_only_fields = (
            'owner',
            'get_dispensed_items_cost',
            'get_pending_items_cost', 'processed_by',  'quantity_pending', 'facility', 'prescription_quote', 'prescription_item', 'pharmacist_instructions', 'quantity_required', 'variation', 'dose_divisible', 'fully_dispensed', 'prescription_item_details',
        )

    def get_prescription_item_details(self, obj):
        prescription_item = models.PrescriptionItem.objects.filter(
            id=obj.prescription_item.id)
        return PrescriptionItemSerializer(prescription_item, context=self.context, many=True).data

    @transaction.atomic
    def update(self, quote_item, validated_data):
        """s
        This method updates the prescription quote item

        """
        user_id = self.context.get("user_id")
        user = Users.objects.get(id=user_id)

        quantity_dispensed = int(validated_data.pop('quantity_dispensed'))
        item_accepted = validated_data.pop('item_accepted')
        client_comment = validated_data.pop('client_comment')
        order = None

        # If item is fully dispensed
        if quote_item.quantity_dispensed == quote_item.quantity_required and quote_item.quantity_pending == 0:
            quote_item.fully_dispensed = True
            quote_item.save()
            # raise serializers.ValidationError(
            #     {"message": f"Prescription item is fully dispensed {quote_item.quantity_pending}"})
        else:

            if models.Order.objects.filter(facility=quote_item.facility, prescription_quote=quote_item.prescription_quote, client_confirmed=False).count() > 0:
                order = models.Order.objects.get(
                    facility=quote_item.facility, prescription_quote=quote_item.prescription_quote, client_confirmed=False)
            else:
                order = models.Order.objects.create(
                    facility=quote_item.facility, owner=quote_item.owner, prescription_quote=quote_item.prescription_quote)
            if quote_item and user and order:
                # # Dispended  item quantity  must be equal to or less than pending quantity
                if quantity_dispensed > quote_item.quantity_pending and quantity_dispensed > 0:
                    raise serializers.ValidationError(
                        {"message": f"You can only requisition quantity {quote_item.quantity_pending} or less"})

                # Update the quote item
                quote_item.quantity_dispensed = quote_item.quantity_dispensed+quantity_dispensed
                quote_item.quantity_pending = quote_item.quantity_pending - quantity_dispensed

                quote_item.item_accepted = item_accepted
                quote_item.client_comment = client_comment
                quote_item.save()

                if quote_item.quantity_pending == 0:
                    quote_item.fully_dispensed = True
                    quote_item.save()

                # Check if order item is already added to order. If added, update quantity or else create new order item
                if models.OrderItem.objects.filter(facility=quote_item.facility, quote_item=quote_item, order=order, client_confirmed=False).count() > 0:

                    order_item = models.OrderItem.objects.get(
                        facility=quote_item.facility, quote_item=quote_item, order=order, client_confirmed=False)
                    order_item.quantity += quantity_dispensed
                    order_item.save()
                else:
                    order_item = models.OrderItem.objects.create(
                        order=order,
                        facility=quote_item.facility,
                        quote_item=quote_item,
                        quantity=quantity_dispensed,
                        owner=quote_item.prescription_quote.forward.owner)

            else:
                raise serializers.ValidationError(
                    f"Check your quantity and also if you have accepted the offer")

        return quote_item


class OrderSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    order_items_details = serializers.SerializerMethodField(
        read_only=True)

    pharmacy_payment = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Order
        fields = (
            'id',
            'url', 'facility', 'prescription_quote', 'client_confirmed', 'payment_method', 'pharmacy_payment',
            'owner', 'order_items_details', 'created', 'updated')
        read_only_fields = (
            'owner',  'facility', 'prescription_quote',
        )

    def get_order_items_details(self, obj):
        order_item = models.OrderItem.objects.filter(
            order=obj)
        return OrderItemSerializer(order_item, context=self.context, many=True).data

    def get_pharmacy_payment(self, obj):
        payment = models.PharmacyPayments.objects.filter(
            order=obj)
        return PharmacyPaymentsSerializer(payment, context=self.context, many=True).data

    @ transaction.atomic
    def update(self, order, validated_data):

        if order.client_confirmed:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Order is already confirmed"})

        client_confirmed = validated_data.pop('client_confirmed')
        payment_method = validated_data.pop('payment_method')

        if not payment_method:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Please select payment method"})

        if client_confirmed == True:
            order.client_confirmed = client_confirmed
            order.save()
        else:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Order is already confirmed"})

        if models.PharmacyPayments.objects.filter(order=order).count() > 0:
            payment = models.PharmacyPayments.objects.get(order=order)
        else:
            payment = models.PharmacyPayments.objects.create(
                facility=order.facility, owner=order.owner, order=order, payment_method=payment_method)

        return order


class OrderItemSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = ('id', 'url', 'facility', 'quote_item',
                  'order', )
        read_only_fields = (
            'owner',  'facility', 'quote_item', 'quantity'
        )


class PharmacyPaymentsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.PharmacyPayments
        fields = ('id', 'url', 'facility', 'order', 'reference', 'status',
                  'owner', 'created', 'updated')
        read_only_fields = (
            'owner',  'facility', 'order',
        )

    def get_amount(self):
        return self.order.get_total_price()


class RetailProductPhotosSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RetailProductPhotos
        fields = "__all__"
        read_only_fields = (
            'variation', 'owner'
        )


class RetailVariationsDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RetailVariations
        fields = (
            ('id', 'url', 'unit_quantity', 'pack_buying_price',
             'pack_selling_price', 'manufacture_date', 'expiry_date')
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'is_active', 'unit_quantity', 'unit_buying_price', 'unit_selling_price', 'variations', 'facility'
        )

# Not using FacilitySafeSerializerMixin to allow global view of products


class RetailProductsSerializer(serializers.HyperlinkedModelSerializer):
    # variation_images = RetailProductPhotosSerializer(many=True, read_only=True)
    product_details = serializers.SerializerMethodField(read_only=True)
    variations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.RetailProducts
        fields = (
            'id',  'facility', 'url', 'product', 'get_available_units', 'get_available_packs', 'product_details', 'variations',
            'created', 'updated', 'owner', 'is_active',
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'facility', 'is_active'
        )

    def get_product_details(self, obj):
        if obj.product:
            product = Products.objects.get_by_id(id=obj.product.id)
            return ProductsSerializer(product, context=self.context).data

    def get_variations(self, obj):

        items = models.RetailVariations.objects.filter(retail_product=obj)
        return RetailVariationsDisplaySerializer(items, context=self.context, many=True).data

    @transaction.atomic
    def create(self, validated_data):

        user_pk = self.context.get("user_pk")

        user = User.objects.get(id=user_pk)
        # title = validated_data.pop('title')
        product = validated_data.pop('product')
        # category = validated_data.pop('category')

        if user.facility == Facility.objects.default_facility():
            raise serializers.ValidationError(
                f"You are not allowed to create inventory in this facility")
        if product:
            if models.RetailProducts.objects.filter(product=product, facility=user.facility).count() > 0:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": f"{product.title} already added to facility"})

            else:
                created = models.RetailProducts.objects.create(
                    product=product, **validated_data)

        return created


class RetailVariationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RetailVariations
        fields = (
            "__all__"
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'is_active', 'unit_quantity', 'unit_buying_price', 'unit_selling_price', 'facility', 'wholesale_product',
        )


class RetailProductsUpdateSerializer(serializers.HyperlinkedModelSerializer):
    variation_images = RetailProductPhotosSerializer(many=True, read_only=True)
    product_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.RetailProducts
        fields = (
            'id',  'facility', 'url',
            'created', 'updated', 'owner', 'product', 'is_active', 'variation_images', 'product_details',
        )
        read_only_fields = (
            'created', 'updated', 'owner',  'is_active', 'facility', 'product',
        )

    def get_product_details(self, obj):
        if obj.product:
            product = Products.objects.get_by_id(id=obj.product.id)
            return ProductsSerializer(product, context=self.context).data

    def delete(self):
        raise serializers.ValidationError(
            {"response_code": 1, "response_message": "Item cannot be deleted"})
