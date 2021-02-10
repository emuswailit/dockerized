
from users.models import Facility
from rest_framework import serializers
from . import models
from django.db import transaction
from django.contrib.auth import get_user_model
from drugs.models import Products
from drugs.serializers import ProductsSerializer
from users.serializers import FacilitySerializer


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

    def update(self, wholesale_product, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        user_pk = self.context.get(
            "user_pk")
        if user_pk:
            user = Users.objects.get(id=user_pk)

        # Update price
        trade_price = float(validated_data.pop('trade_price'))
        total_quantity = int(validated_data.pop('total_quantity'))
        if trade_price == 0.00:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Price cannot be zero"})
        else:

            wholesale_product.trade_price = trade_price
            wholesale_product.total_quantity = total_quantity
            wholesale_product.save()

        return wholesale_product


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
    payment = serializers.SerializerMethodField(
        read_only=True)
    wholesale_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Requisitions
        fields = ('id', 'url', 'facility',  'wholesale', 'retailer_account', 'status', 'retailer_confirmed', 'wholesaler_confirmed', 'payment_terms', 'priority',
                  'is_closed',  'owner', 'created', 'updated', 'items', 'payment', 'wholesale_details')
        read_only_fields = ('id', 'url', 'facility', 'retailer_account',  'status',  'is_active', 'retailer_confirmed', 'wholesaler_confirmed',

                            'is_closed',   'owner', 'created', 'updated', 'items', 'wholesale_details')

    def get_items(self, obj):
        items = models.RequisitionItems.objects.filter(requisition=obj)
        return RequisitionItemsSerializer(items, context=self.context, many=True).data

    def get_payment(self, obj):
        payment = {}
        if models.RequisitionPayments.objects.filter(requisition=obj).count() > 0:
            payment = models.RequisitionPayments.objects.get(requisition=obj)
            return RequisitionPaymentsSerializer(payment, context=self.context).data

    def get_wholesale_details(self, obj):
        wholesale = {}
        if Facility.objects.filter(id=obj.wholesale.id).count() > 0:
            wholesale = Facility.objects.get(
                id=obj.wholesale.id)
            return FacilitySerializer(wholesale, context=self.context).data

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


class RequisitionsRetailerConfirmSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.SerializerMethodField(
        read_only=True)
    payment = serializers.SerializerMethodField(
        read_only=True)
    wholesale_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Requisitions
        fields = ('id',
                  'url',
                  'facility',
                  'wholesale',
                  'retailer_account',
                  'status',
                  'retailer_confirmed',
                  'wholesaler_confirmed',
                  'payment_method',
                  'payment_terms',
                  'priority',
                  'is_closed',
                  'owner',
                  'created',
                  'updated',
                  'items',
                  'payment',
                  'wholesale_details'

                  )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'retailer_account',
            'status',
            'is_active',
            'wholesale',
            'priority',
            'is_closed',
            'wholesaler_confirmed',
            'owner',
            'created',
            'updated')

    def get_items(self, obj):
        items = models.RequisitionItems.objects.filter(requisition=obj)
        return RequisitionItemsSerializer(items, context=self.context, many=True).data

    def get_payment(self, obj):
        payment = {}
        if models.RequisitionPayments.objects.filter(requisition=obj).count() > 0:
            payment = models.RequisitionPayments.objects.get(requisition=obj)
            return RequisitionPaymentsSerializer(payment, context=self.context).data

    def get_wholesale_details(self, obj):
        wholesale = {}
        if Facility.objects.filter(id=obj.wholesale.id).count() > 0:
            wholesale = Facility.objects.get(
                id=obj.wholesale.id)
            return FacilitySerializer(wholesale, context=self.context).data

    @transaction.atomic
    def update(self, requisition, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        user_pk = self.context.get(
            "user_pk")
        user = Users.objects.get(id=user_pk)

        payment_terms = validated_data.pop('payment_terms')
        payment_method = validated_data.pop('payment_method')
        selected_payment_terms = None
        requisition_items = None

        if models.RequisitionItems.objects.filter(requisition=requisition).count() > 0:
            requisition_items = models.RequisitionItems.objects.filter(
                requisition=requisition)
        else:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Requisition has no items added into it"})

        # Enforce cash terms for retaailers with no accounts
        if models.RetailerAccounts.objects.filter(retailer=user.facility).count() > 0:

            selected_payment_terms = payment_terms
            requisition.save()
            retailer_account = models.RetailerAccounts.objects.get(
                retailer=user.facility)
            if not retailer_account.credit_allowed and payment_terms == "CREDIT":
                """
                Credit not allowed for this facility
                """
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": "Credit terms not yet authorized. Please select different terms of payment"})

            if not retailer_account.placement_allowed and payment_terms == "PLACEMENT":
                """
                Placement not allowed for this facility
                """
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": "Placement terms not yet authorized. Please select different terms of payment"})
        else:
            if payment_method:
                selected_payment_terms = 'CASH'
                requisition.payment_terms = selected_payment_terms
                requisition.save()
                requisition.retailer_confirmed = True
                requisition.payment_method = payment_method
                requisition.status = "RETAILER_CONFIRMED"
                requisition.save()
            else:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": "Select payment method"})
        # Create or update the payment
        if requisition_items:
            amount = 0.00
            for item in requisition_items:
                amount += float(item.quantity_issued) * \
                    float(item.wholesale_product.trade_price)
            if amount > 0.00:
                if models.RequisitionPayments.objects.filter(requisition=requisition).count() > 0:
                    requisition_payment = models.RequisitionPayments.objects.get(
                        requisition=requisition)
                else:
                    requisition_payment = models.RequisitionPayments.objects.create(facility=user.facility, owner=user,
                                                                                    requisition=requisition, payment_method=payment_method, payment_terms=payment_terms, amount=amount)
        return requisition


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
        despatch = None
        variations = None
        new_requisition_item = None
        retailer_account = None
        despatch_item = None
        quantity_issued = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        quantity_required = int(validated_data.pop('quantity_required'))
        wholesale_product = validated_data.pop('wholesale_product')
        requisition = validated_data.pop('requisition')

        # Check if requisition is still open for editing
        if requisition.is_closed:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Requisition is no longer open for editing"})

        # Quantity should not be zero
        if quantity_required <= 0:
            raise serializers.ValidationError(
                "Quantity required cannot be zero")

        # Item should be in stock
        if models.WholesaleProducts.objects.get(id=wholesale_product.id).total_quantity == 0:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Item is out of stock"})

        # Required quantity is less than available quantity
        if models.WholesaleProducts.objects.get(id=wholesale_product.id).total_quantity < quantity_required:
            quantity = models.WholesaleProducts.objects.get(
                id=wholesale_product.id).total_quantity

            # Set the available quantity as quantity required, entire quantity required cannot be availed
            quantity_issued = quantity
            # raise serializers.ValidationError(
            #     {"response_code": 1, "response_message": f"Available quantity: {quantity}"})
        else:
            quantity_issued = quantity_required
        # Requisition item should be unique
        if models.RequisitionItems.objects.filter(
                facility=user.facility, requisition=requisition, wholesale_product=wholesale_product).count() > 0:
            new_requisition_item = models.RequisitionItems.objects.get(
                facility=user.facility, requisition=requisition, wholesale_product=wholesale_product)

            # Update retrieved requisition item with the new entered required quantity

            new_requisition_item.quantity_required = quantity_required
            new_requisition_item.quantity_issued = quantity_issued
            new_requisition_item.save()
        else:
            # Create requisition item if all is well
            if quantity_required > 0:
                new_requisition_item = models.RequisitionItems.objects.create(
                    requisition=requisition,
                    wholesale_product=wholesale_product,
                    quantity_required=quantity_required,
                    quantity_issued=quantity_issued,
                    **validated_data)

        return new_requisition_item

    @transaction.atomic
    def update(self, requisition_item, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        if requisition_item.retailer_confirmed:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Item is closed for editing. You can only delete it"})


class DespatchesSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)

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
            'updated',
            'items'
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
            'updated',
            'items'
        )

    def get_items(self, obj):
        items = models.DespatchItems.objects.filter(
            despatch=obj)
        return DespatchItemsSerializer(items, context=self.context, many=True).data


class DespatchesWholesaleUpdateSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)

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
            'updated',
            'items'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'receipt_confirmed',
            'courier_confirmed',
            'despatch_confirmed_by',
            'receipt_confirmed_by',
            'courier_confirmed_by',
            'priority',
            'owner',
            'created',
            'updated',
            'items'
        )

    def get_items(self, obj):
        items = models.DespatchItems.objects.filter(
            despatch=obj)
        return DespatchItemsSerializer(items, context=self.context, many=True).data


class DespatchesRetailUpdateSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)

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
            'updated',
            'items'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'despatch_confirmed',
            'courier_confirmed',
            'despatch_confirmed_by',
            'receipt_confirmed_by',
            'courier_confirmed_by',
            'courier',
            'priority',
            'owner',
            'created',
            'updated',
            'items'
        )

    def get_items(self, obj):
        items = models.DespatchItems.objects.filter(
            despatch=obj)
        return DespatchItemsSerializer(items, context=self.context, many=True).data


class DespatchItemsSerializer(serializers.HyperlinkedModelSerializer):
    requisition_item = serializers.SerializerMethodField(read_only=True)

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

    def get_requisition_item(self, obj):
        item = {}
        item = models.RequisitionItems.objects.get(
            id=obj.requisition_item.id)
        return RequisitionItemsSerializer(item, context=self.context).data


class RequisitionPaymentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RequisitionPayments
        fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'status',
            'amount',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'amount',
            'owner',
            'created',
            'updated'
        )

    @ transaction.atomic
    def update(self, requisition_payment, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        user_pk = self.context.get(
            "user_pk")
        user = Users.objects.get(id=user_pk)
        status = validated_data.pop('status')

        if requisition_payment.requisition.is_closed and requisition_payment.status == "SUCCESS":
            raise serializers.ValidationError(
                {"response_code": 1,
                 "response_message": f"Requisition is already paid for and closed"})

        if status == "SUCCESS":
            # Update payment status and close the requisition
            requisition_payment.status = status
            requisition_payment.save()

            requisition_payment.requisition.is_closed = True
            requisition_payment.requisition.save()

            # Create a despatch for the requisition
            despatch = models.Despatches.objects.create(
                facility=user.facility, owner=user, requisition=requisition_payment.requisition)

            # Update inventory
            if models.RequisitionPayments.objects.filter(requisition=requisition_payment.requisition).count() > 0:
                requisition_items = models.RequisitionItems.objects.filter(
                    requisition=requisition_payment.requisition)
                for item in requisition_items:
                    if item.wholesale_product.total_quantity >= item.quantity_issued:
                        # Deduct sold quantity from inventory if quantity is still sufficient
                        item.wholesale_product.total_quantity -= item.quantity_issued
                        item.wholesale_product.save()

                        # Add item to despatch
                        despatch_item = models.DespatchItems.objects.create(
                            facility=user.facility, owner=user, requisition_item=item, despatch=despatch)
                    else:
                        raise serializers.ValidationError(
                            {"response_code": 1,
                             "response_message": f"Quantity available  now is  {item.wholesale_product.quantity}"})

            else:
                raise serializers.ValidationError(
                    {"response_code": 1,
                     "response_message": f"Requisition has no items added to it"})

        else:
            raise serializers.ValidationError(
                {"response_code": 1,
                 "response_message": f"Check if your payment was succesfully processed"})

        return requisition_payment
