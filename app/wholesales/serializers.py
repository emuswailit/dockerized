
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
        fields = ('id', 'url', 'facility',  'product', 'available_packs_quantity',   'is_active',
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
            'is_active',
            'pack_quantity',
            'pack_buying_price',
            'pack_selling_price',
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

    @transaction.atomic
    def create(self, validated_data):
        """
        Adding a wholesale product and variation to requisition and subsequently to despatch
        """
        selected_payment_terms = None
        despatch = None
        variations = None
        new_requisition_item = None
        retailer_account = None
        despatch_item = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        quantity_required = int(validated_data.pop('quantity_required'))
        wholesale_product = validated_data.pop('wholesale_product')
        requisition = validated_data.pop('requisition')

        # Is item in stock
        if wholesale_product.available_packs_quantity() <= 0:
            raise serializers.ValidationError(
                f"Item is not in stock")
        else:
            limit = 0
            if models.WholesaleVariations.objects.filter(wholesale_product=wholesale_product, pack_quantity__gte=0).count() > 0:
                variations = models.WholesaleVariations.objects.filter(
                    wholesale_product=wholesale_product).order_by('-created')
            else:
                raise serializers.ValidationError(
                    f"{wholesale_product.product.title}: {wholesale_product.id} has no variations")

        # Quantity must be equal or less than available
        if quantity_required > wholesale_product.available_packs_quantity():
            raise serializers.ValidationError(
                f"Only {wholesale_product.available_packs_quantity()} available")

        # Quantity must be 1 or more
        if quantity_required <= 0:
            raise serializers.ValidationError(
                f"Please enter quantity")

        # Requisition must be open for editing
        if requisition.status != "PENDING":
            raise serializers.ValidationError(
                f"Requistion is closed and cannot be edited further")

        # Requisition item should be unique
        if models.RequisitionItems.objects.filter(facility=user.facility, requisition=requisition, wholesale_product=wholesale_product).count() > 0:
            new_requisition_item = models.RequisitionItems.objects.get(
                facility=user.facility, requisition=requisition, wholesale_product=wholesale_product)
        else:
            # Create requisition item if all is well
            new_requisition_item = models.RequisitionItems.objects.create(
                requisition=requisition, wholesale_product=wholesale_product, quantity_required=quantity_required, **validated_data)
        if new_requisition_item:
            if models.Despatches.objects.filter(requisition=requisition, status="PENDING", facility=user.facility,).count() > 0:
                despatch = models.Despatches.objects.get(
                    requisition=requisition, status="PENDING", facility=user.facility)

            else:
                despatch = models.Despatches.objects.create(
                    requisition=requisition, facility=user.facility, owner=user)

            # # Retrieve all wholesale variations for this product ordered by expiry date
            # # Check quantity for each variation against required quantity
            # # If variation quantity for earliest expiring product is greater than quantity required then sell it
            # # If  quantity of earliest expiring variation is less than quantity required then sell whole balance and then top balance up with next expiring variation

            for item in variations:
                if models.DespatchItems.objects.filter(wholesale_variation=item, requisition_item=new_requisition_item).count() > 0:
                    # Item is in the despatch and will be retrieved
                    despatch_item = models.DespatchItems.objects.filter(
                        wholesale_variation=item, requisition_item=new_requisition_item)
                    source = "Retrieved"

                else:
                    # Item is not in the despatch and shall be created afresh
                    despatch_item = models.DespatchItems.objects.create(
                        facility=user.facility, owner=user, wholesale_variation=item, despatch=despatch, requisition_item=new_requisition_item)
                    source = "Created"

                if despatch_item:
                    if item.pack_quantity >= quantity_required:
                        despatch_item.quantity_issued = quantity_required
                        despatch_item.save()
                        item.pack_quantity -= quantity_required
                        item.save()
                        break
                    else:
                        despatch_item.quantity_issued = item.pack_quantity
                        despatch_item.save()
                        quantity_required -= despatch_item.quantity_issued
                        item.pack_quantity -= despatch_item.quantity_issued
                        item.save()

                    # raise serializers.ValidationError(f"{despatch_item.id}")
        return new_requisition_item


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
