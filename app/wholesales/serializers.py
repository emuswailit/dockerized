
from users.models import Facility
from rest_framework import serializers
from . import models
from django.db import transaction
from django.contrib.auth import get_user_model
from drugs.models import Products
from drugs.serializers import ProductsSerializer

Users = get_user_model()


class RetailerAccountsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RetailerAccounts
        fields = (
            'id',
            'url',
            'facility',
            'retailer',
            'is_active',
            'credit_limit',
            'credit_allowed',
            'placement_allowed',
            'account_manager',
            'account_contact',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')


class WholesaleProductsSerializer(serializers.HyperlinkedModelSerializer):
    product_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.WholesaleProducts
        fields = ('id', 'url', 'facility',  'product', 'total_quantity', 'trade_price',  'is_active',
                  'owner', 'created', 'updated', 'product_details')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')

    def get_product_details(self, obj):
        product = Products.objects.filter(
            id=obj.product.id)
        return ProductsSerializer(product, context=self.context, many=True).data


class WholesaleVariationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.WholesaleVariations
        fields = (
            'id',
            'url',
            'facility',
            'wholesale_product',
            'batch',
            'is_active',
            'quantity',
            'buying_price',
            'selling_price',
            'manufacture_date',
            'expiry_date',
            'source',
            'comment',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        selected_payment_terms = None
        retailer_account = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        quantity = int(validated_data.pop('quantity'))
        wholesale_product = validated_data.pop('wholesale_product')
        selling_price = validated_data.pop('selling_price')

        if selling_price <= 0:
            raise serializers.ValidationError("Selling price cannot be zero")

        if quantity <= 0:
            raise serializers.ValidationError("Quantity cannot be zero")

        created = models.WholesaleVariations.objects.create(
            is_active=True,
            wholesale_product=wholesale_product,
            quantity=quantity, **validated_data)

        if created:
            # Update quantity
            wholesale_product.total_quantity += quantity
            wholesale_product.save()

            # Update trade price
            if selling_price > wholesale_product.trade_price:
                wholesale_product.trade_price = selling_price
                wholesale_product.save()

        return created

    @transaction.atomic
    def update(self, wholesale_variation, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        user_pk = self.context.get(
            "user_pk")
        if user_pk:
            user = Users.objects.get(id=user_pk)

        # Update price
        selling_price = float(validated_data.pop('selling_price'))
        if selling_price == 0.00:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Price cannot be zero"})
        else:
            wholesale_variation.wholesale_product.trade_price = selling_price
            wholesale_variation.wholesale_product.save()
            wholesale_variation.selling_price = selling_price
            wholesale_variation.save()

        return wholesale_variation


class BonusesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bonuses
        fields = ('id', 'url', 'facility',  'wholesale_variation', 'title', 'description', 'start_date', 'end_date', 'for_every', 'get_free',  'is_active',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')


class DiscountsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Discounts
        fields = ('id', 'url', 'facility',  'wholesale_variation', 'title', 'description', 'start_date', 'end_date', 'percentage',   'is_active',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')


class RequisitionsSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Requisitions
        fields = ('id', 'url', 'facility',  'wholesale', 'retailer_account', 'status', 'retailer_confirmed', 'wholesaler_confirmed', 'payment_terms', 'priority',
                  'owner', 'created', 'updated', 'items')
        read_only_fields = ('id', 'url', 'facility', 'retailer_account', 'status',  'is_active', 'retailer_confirmed', 'wholesaler_confirmed',

                            'owner', 'created', 'updated', 'items')

    def get_items(self, obj):
        items = models.RequisitionItems.objects.filter(requisition=obj)
        return RequisitionItemsSerializer(items, context=self.context, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        selected_payment_terms = None
        retailer_account = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        wholesale = validated_data.pop('wholesale')
        payment_terms = validated_data.pop('payment_terms')

        # Ensure this is done only in a bulk pharmacy
        if wholesale.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                f"Selected facility is not a wholesale pharmacy ")
        # Retrieve retail account
        if models.RetailerAccounts.objects.filter(retailer=user.facility, facility=wholesale).exists():

            selected_payment_terms = payment_terms,
            # Retrieve the account
            retailer_account = models.RetailerAccounts.objects.filter(
                retailer=user.facility, facility=wholesale)
        else:
            # Enforce cash as payment terms
            selected_payment_terms = "CASH"

        # Check if a retail facility has an open order in the target wholesale already
        if models.Requisitions.objects.filter(facility=user.facility, wholesale=wholesale, status="PENDING").count() > 0:
            raise serializers.ValidationError(
                f"You already have an open requisition at {wholesale.title}. Please edit that one")

        else:
            # If no existing requisition then create a new one
            created = models.Requisitions.objects.create(wholesale=wholesale,
                                                         payment_terms=selected_payment_terms, retailer_account=retailer_account, **validated_data)

        return created


class RequisitionItemsSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.RequisitionItems
        fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'wholesale_product',
            'wholesaler_confirmed',
            'retailer_confirmed',
            'quantity_required',
            'quantity_issued',
            'quantity_pending',
            'quantity_paid',
            'quantity_unpaid',
            'owner',
            'wholesaler_confirmed_by',
            'created',
            'updated',
            'product'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'is_active',
            'retailer_confirmed',
            'wholesaler_confirmed',
            'quantity_issued',
            'quantity_pending',
            'quantity_paid',
            'quantity_unpaid',
            'wholesaler_confirmed_by',
            'owner',
            'created',
            'updated'
        )

    def get_product(self, obj):
        product = models.WholesaleProducts.objects.filter(
            id=obj.wholesale_product.id)
        return WholesaleProductsSerializer(product, context=self.context, many=True).data

    # @transaction.atomic
    # def create(self, validated_data):
    #     """
    #     Adding a wholesale product and variation to requisition and subsequently to despatch
    #     """
    #     selected_payment_terms = None
    #     despatch = None
    #     variations = None
    #     new_requisition_item = None
    #     retailer_account = None
    #     despatch_item = None
    #     user_pk = self.context.get("user_pk")
    #     user = Users.objects.get(id=user_pk)

    #     quantity_required = int(validated_data.pop('quantity_required'))
    #     wholesale_product = validated_data.pop('wholesale_product')
    #     requisition = validated_data.pop('requisition')

    #     return new_requisition_item


class DespatchesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Despatches
        fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'despatch_confirmed',
            'receipt_confirmed',
            'courier_confirmed',
            'despatch_confirmed_by',
            'receipt_confirmed_by',
            'courier_confirmed_by',
            'get_total_quantity_issued',
            'courier',
            'priority',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'despatch_confirmed',
            'receipt_confirmed',
            'courier_confirmed',
            'despatch_confirmed_by',
            'receipt_confirmed_by',
            'courier_confirmed_by',
            'get_total_quantity_issued',
            'courier',
            'priority',
            'owner',
            'created',
            'updated'
        )


class DespatchItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DespatchItems
        fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )


class DespatchPaymentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DespatchPayments
        fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )
