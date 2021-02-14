
from users.models import Facility
from rest_framework import serializers
from . import models
from django.db import transaction
from django.contrib.auth import get_user_model
from drugs.models import Products
from drugs.serializers import ProductsSerializer
from users.serializers import FacilitySerializer
from retailers.models import RetailVariations, RetailProducts
from core.serializers import FacilitySafeSerializerMixin


Users = get_user_model()


class RetailerAccountsSerializer(serializers.HyperlinkedModelSerializer):
    retailer_details = serializers.SerializerMethodField(
        read_only=True)
    wholesaler_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.RetailerAccounts
        fields = (
            'id',
            'url',
            'facility',
            'wholesale',
            'is_active',
            'credit_limit',
            'retailer_verified',
            'credit_allowed',
            'placement_allowed',
            'wholesaler_contact',
            'retailer_contact',
            'owner',
            'created',
            'updated',
            'retailer_details',
            'wholesaler_details',
        )
        read_only_fields = ('id', 'url', 'facility', 'credit_limit', 'credit_allowed', 'retailer_verified', 'wholesaler_contact', 'placement_allowed',  'is_active',
                            'owner', 'created', 'updated')

    def get_retailer_details(self, obj):
        facility = None

        if models.Facility.objects.filter(id=obj.facility_id).count() > 0:

            retailer = models.Facility.objects.get(
                id=obj.facility_id)
        return FacilitySerializer(retailer, context=self.context).data

    def get_wholesaler_details(self, obj):
        wholesaler = None

        if models.Facility.objects.filter(id=obj.facility_id).count() > 0:

            wholesaler = models.Facility.objects.get(
                id=obj.wholesale_id)
        return FacilitySerializer(wholesaler, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):
        selected_payment_terms = None
        retailer_account = None
        # Retrieve logged on user from context
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        # Retrieve user entered data
        retailer_contact = validated_data.pop('retailer_contact')
        wholesale = validated_data.pop('wholesale')

        # Create account only in a wholesale pharmacy
        if wholesale.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"{wholesale.title} is not a wholesale"})

        # If account contact is not specified then the creator becomes account contact
        if not retailer_contact:
            retailer_contact = user

        if models.RetailerAccounts.objects.filter(facility=user.facility, wholesale=wholesale).count() > 0:
            """
            Check if account exists

            """
            retailer_account = models.RetailerAccounts.objects.get(
                facility=user.facility, wholesale=wholesale)
        else:
            # Create ne account
            retailer_account = models.RetailerAccounts.objects.create(
                wholesale=wholesale, retailer_contact=retailer_contact, **validated_data)

        return retailer_account

    def update(self, retailer_account, validated_data):
        """
        This method updates the prescription quote item

        """
        # Retrieve quote item ID from context as it was passed in url
        user_pk = self.context.get(
            "user_pk")
        if user_pk:
            user = Users.objects.get(id=user_pk)

        if retailer_account.wholesale != user.facility:
            raise serilaizers.ValidationError(
                {"response_code": 1, "response_message": "You are not authorized"})


class RetailerAccountsUpdateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for wholesalers to update retailer accounts
    """
    class Meta:
        model = models.RetailerAccounts
        fields = (
            'id',
            'url',
            'facility',
            'wholesale',
            'is_active',
            'credit_limit',
            'placement_limit',
            'retailer_verified',
            'credit_allowed',
            'placement_allowed',
            'wholesaler_contact',
            'retailer_contact',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = ('id', 'url', 'facility',  'wholesaler_contact', 'retailer_contact', 'wholesale',
                            'owner', 'created', 'updated')


# class WholesaleProductsSerializerForRetailer(serializers.HyperlinkedModelSerializer):
#     product_details = serializers.SerializerMethodField(
#         read_only=True)

#     class Meta:
#         model = models.WholesaleProducts
#         fields = ('id', 'url', 'facility',  'product', 'available_quantity',  'is_active',
#                   'owner', 'created', 'updated', 'product_details')
#         read_only_fields = ('id', 'url', 'facility',  'is_active',
#                             'owner', 'created', 'updated')

#     def get_product_details(self, obj):
#         product = Products.objects.filter(
#             id=obj.product.id)
#         return ProductsSerializer(product, context=self.context, many=True).data


# class WholesaleProductsSerializer(serializers.HyperlinkedModelSerializer):
#     product_details = serializers.SerializerMethodField(
#         read_only=True)

#     class Meta:
#         model = models.WholesaleProducts
#         fields = ('id', 'url', 'facility',  'product', 'is_active',
#                   'owner', 'created', 'updated', 'product_details')
#         read_only_fields = ('id', 'url', 'facility',  'is_active',
#                             'owner', 'created', 'updated')

#     def get_product_details(self, obj):
#         product = Products.objects.filter(
#             id=obj.product.id)
#         return ProductsSerializer(product, context=self.context, many=True).data

    # def update(self, wholesale_product, validated_data):
    #     """
    #     This method updates the prescription quote item

    #     """
    #     # Retrieve quote item ID from context as it was passed in url
    #     user_pk = self.context.get(
    #         "user_pk")
    #     if user_pk:
    #         user = Users.objects.get(id=user_pk)

    #     # Update price
    #     trade_price = float(validated_data.pop('trade_price'))
    #     available_quantity = int(validated_data.pop('available_quantity'))
    #     if trade_price == 0.00:
    #         raise serializers.ValidationError(
    #             {"response_code": 1, "response_message": "Price cannot be zero"})
    #     else:

    #         wholesale_product.trade_price = trade_price
    #         wholesale_product.available_quantity = available_quantity
    #         wholesale_product.save()

    #     return wholesale_product


class WholesaleVariationsSerializerForRetailer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    product_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.WholesaleVariations
        fields = (
            'id',
            'url',
            'facility',
            'product',
            'batch',
            'is_active',
            'available_quantity',
            'buying_price',
            'selling_price',
            'manufacture_date',
            'get_final_price',
            'expiry_date',
            'source',
            'comment',
            'owner',
            'created',
            'updated', 'product_details'
        )
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')

    def get_product_details(self, obj):
        product = None

        if models.WholesaleProducts.objects.filter(id=obj.wholesale_product_id).count() > 0:

            product = models.WholesaleProducts.objects.get(
                id=obj.wholesale_product_id)
        return WholesaleProductsSerializer(product, context=self.context).data


class WholesaleVariationsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Remove FacilitySafeSerializerMixin in order to access sources and products created at drugs app by admin
    """
    product_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.WholesaleVariations
        fields = (
            'id',
            'url',
            'facility',
            'product',
            'batch',
            'is_active',
            'quantity_received',
            'quantity_issued',
            'quantity_available',
            'buying_price',
            'selling_price',
            'manufacture_date',
            'get_final_price',
            'expiry_date',
            'source',
            'comment',
            'owner',
            'created',
            'updated', 'product_details'
        )
        read_only_fields = ('id', 'url', 'facility', 'quantity_issued',
                            'quantity_available',  'is_active',
                            'owner', 'created', 'updated')

    def get_product_details(self, obj):
        product = None

        if Products.objects.filter(id=obj.product_id).count() > 0:

            product = models.Products.objects.get(
                id=obj.product_id)
        return ProductsSerializer(product, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):
        selected_payment_terms = None
        retailer_account = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        if user.facility.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Selling price cannot be zero"})

        quantity_received = int(validated_data.pop('quantity_received'))
        product = validated_data.pop('product')
        selling_price = validated_data.pop('selling_price')

        if selling_price <= 0:
            raise serializers.ValidationError("Selling price cannot be zero")

        if quantity_received <= 0:
            raise serializers.ValidationError("Quantity cannot be zero")

        created = models.WholesaleVariations.objects.create(
            is_active=True,
            product=product,
            quantity_received=quantity_received, quantity_available=quantity_received, **validated_data)

        return created

    @transaction.atomic
    def update(self, wholesale_variation, validated_data):
        """
        This method updates the prescription quote item

        """
        user = None
        # Retrieve quote item ID from context as it was passed in url
        user_pk = self.context.get(
            "user_pk")
        if user_pk:
            user = Users.objects.get(id=user_pk)

        if user.facility.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Selling price cannot be zero"})
        # Update price
        selling_price = float(validated_data.pop('selling_price'))
        # TODO : Remove this later to avoid abuse
        quantity_received = float(validated_data.pop('quantity_received'))
        batch = validated_data.pop('batch')
        comment = validated_data.pop('comment')
        manufacture_date = validated_data.pop('manufacture_date')
        expiry_date = validated_data.pop('expiry_date')
        if selling_price == 0.00:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Price cannot be zero"})
        else:
            wholesale_variation.product.trade_price = selling_price
            wholesale_variation.quantity_received = quantity_received
            wholesale_variation.batch = batch
            wholesale_variation.comment = comment
            wholesale_variation.expiry_date = expiry_date
            wholesale_variation.manufacture_date = manufacture_date
            wholesale_variation.product.save()
            wholesale_variation.selling_price = selling_price
            wholesale_variation.save()

        return wholesale_variation


class BonusesSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bonuses
        fields = ('id', 'url', 'facility',  'wholesale_variation', 'title', 'description', 'start_date', 'end_date', 'lowest_limit', 'highest_limit', 'bonus_quantity',  'is_active',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        selected_payment_terms = None
        retailer_account = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)
        created = None

        if user.facility.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Bonus cannot be created on the default facility"})

        wholesale_variation = validated_data.pop('wholesale_variation')

        # User must be set to a wholesale to create a bonus
        if user.facility.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Discount cannot be created on the default facility"})

        # Selected variation item must not be out of stock
        if wholesale_variation.quantity_available <= 0:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Selected item is out of stock"})
        created = models.Bonuses.objects.create(
            wholesale_variation=wholesale_variation, **validated_data)

        return created


class DiscountsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Discounts
        fields = ('id', 'url', 'facility',  'wholesale_variation', 'title', 'description', 'start_date', 'end_date', 'percentage',   'is_active',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')

    @transaction.atomic
    def create(self, validated_data):
        selected_payment_terms = None
        retailer_account = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        wholesale_variation = validated_data.pop('wholesale_variation')
        percentage = validated_data.pop('percentage')

        if user.facility.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Selling price cannot be zero"})

         # Selected variation item must not be out of stock
        if wholesale_variation.quantity_available <= 0:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Selected item is out of stock"})

        # Discount percentage should not be too abnormal
        if percentage >= 20:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"{percentage}% discount seems to be very generous! Please confirm!"})

        created = models.Discounts.objects.create(
            wholesale_variation=wholesale_variation, percentage=percentage, **validated_data)

        return created


class RequisitionsSerializer(serializers.HyperlinkedModelSerializer):

    items = serializers.SerializerMethodField(
        read_only=True)
    payment = serializers.SerializerMethodField(
        read_only=True)
    wholesale_details = serializers.SerializerMethodField(
        read_only=True)
    invoice = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = models.Requisitions
        fields = (
            'id',
            'url',
            'facility',
            'wholesale',
            'retailer_account',
            'status',
            'total_amount',
            'retailer_confirmed',
            'wholesaler_confirmed',
            'payment_terms',
            'priority',
            'is_closed',
            'owner',
            'created',
            'updated', 'items', 'payment', 'wholesale_details', 'invoice')
        read_only_fields = (
            'id',
            'url',
            'facility',
            'retailer_account',  'status', 'total_amount',  'is_active', 'retailer_confirmed', 'wholesaler_confirmed',

            'is_closed', 'payment_terms', 'owner', 'created', 'updated', 'items', 'wholesale_details')

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

    def get_invoice(self, obj):
        invoice = {}
        if models.Invoices.objects.filter(requisition=obj).count() > 0:
            invoice = models.Invoices.objects.get(requisition=obj)
            return InvoicesSerializer(invoice, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):
        selected_payment_terms = None
        retailer_account = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        wholesale = validated_data.pop('wholesale')

        # Ensure this is done only in a bulk pharmacy
        if wholesale.facility_type != "BulkPharmacy":
            raise serializers.ValidationError(
                f"Selected facility is not a wholesale pharmacy ")

        # Check if a retail facility has an open order in the target wholesale already
        if models.Requisitions.objects.filter(facility=user.facility, wholesale=wholesale, status="PENDING").count() > 0:
            raise serializers.ValidationError(
                f"You already have an open requisition at {wholesale.title}. Please edit that one")

        else:
            # If no existing requisition then create a new one
            created = models.Requisitions.objects.create(wholesale=wholesale,
                                                         retailer_account=retailer_account, **validated_data)

        return created


class RequisitionsRetailerConfirmSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
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
                  'total_amount',
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
            'total_amount',
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
        requisition_payment = None
        amount = 0.00
        retailer_account = None
        invoice = None
        invoice_item = None

        if requisition.is_closed:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Requisition is already closed"})

        if models.RetailerAccounts.objects.filter(facility=user.facility, wholesale=requisition.wholesale).count() > 0:
            retailer_account = models.RetailerAccounts.objects.get(
                facility=user.facility, wholesale=requisition.wholesale)
        else:
            pass

        if models.RequisitionItems.objects.filter(requisition=requisition).count() > 0:
            requisition_items = models.RequisitionItems.objects.filter(
                requisition=requisition)

            for item in requisition_items:
                amount += float(item.quantity_invoiced) * \
                    float(item.wholesale_variation.get_final_price())
        else:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Requisition has no items added into it"})

        if payment_terms == "CASH":

            # Create or retrieve an invoice for the cash payment
            if models.Invoices.objects.filter(facility=user.facility, requisition=requisition, retailer_account=retailer_account).count() > 0:
                invoice = models.Invoices.objects.get(
                    facility=user.facility, requisition=requisition, retailer_account=retailer_account)
            else:
                invoice = models.Invoices.objects.create(
                    facility=user.facility, owner=user, requisition=requisition, retailer_account=retailer_account, invoice_type=payment_terms, total_amount=amount)
            if invoice and requisition_items:
                for item in requisition_items:
                    if models.InvoiceItems.objects.filter(invoice=invoice, requisition_item=item).count() > 0:
                        invoice_item = models.InvoiceItems.objects.get(
                            invoice=invoice, requisition_item=item)
                        invoice_item.bonus_quantity = item.bonus_quantity
                        invoice_item.quantity_invoiced = item.quantity_invoiced
                        invoice_item.price = item.wholesale_variation.get_final_price()
                        invoice_item.save()
                    else:
                        invoice_item = models.InvoiceItems.objects.create(
                            facility=user.facility,
                            invoice=invoice,
                            requisition_item=item,
                            quantity_invoiced=item.quantity_invoiced,
                            bonus_quantity=item.bonus_quantity,
                            price=item.wholesale_variation.get_final_price(),
                            owner=user
                        )

            if models.RequisitionPayments.objects.filter(requisition=requisition, facility=user.facility).count() > 0:
                requisition_payment = models.RequisitionPayments.objects.get(
                    requisition=requisition, facility=user.facility)
                requisition_payment.amount = amount
                requisition_payment.payment_method = payment_method
                requisition_payment.save()
            else:
                requisition_payment = models.RequisitionPayments.objects.create(
                    facility=user.facility,
                    owner=user, requisition=requisition,
                    payment_method=payment_method,
                    amount=amount,
                    invoice=invoice
                )

            if requisition_payment:
                requisition.retailer_confirmed = True
                requisition.status = "RETAILER_CONFIRMED"
                requisition.total_amount = amount
                requisition.is_closed = True
                requisition.save()
            else:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": "An error occurred while processing your cash payment"})
        elif payment_terms == "CREDIT":

            if retailer_account:
                if retailer_account.credit_allowed:
                    if retailer_account.credit_limit >= amount:

                        # Create or retrieve an invoice
                        if models.Invoices.objects.filter(facility=user.facility, requisition=requisition, retailer_account=retailer_account).count() > 0:
                            invoice = models.Invoices.objects.get(
                                facility=user.facility, requisition=requisition, retailer_account=retailer_account)
                        else:
                            invoice = models.Invoices.objects.create(
                                facility=user.facility, owner=user, requisition=requisition, retailer_account=retailer_account, invoice_type=payment_terms, total_amount=amount)
                        if invoice and requisition_items:
                            for item in requisition_items:
                                if models.InvoiceItems.objects.filter(invoice=invoice, requisition_item=item).count() > 0:
                                    invoice_item = models.InvoiceItems.objects.get(
                                        invoice=invoice, requisition_item=item)
                                    invoice_item.bonus_quantity = item.bonus_quantity
                                    invoice_item.quantity_invoiced = item.quantity_invoiced
                                    invoice_item.price = item.wholesale_variation.get_final_price()
                                    invoice_item.save()
                                else:
                                    invoice_item = models.InvoiceItems.objects.create(
                                        facility=user.facility,
                                        invoice=invoice,
                                        requisition_item=item,
                                        quantity_invoiced=item.quantity_invoiced,
                                        bonus_quantity=item.bonus_quantity,
                                        price=item.wholesale_variation.get_final_price(),
                                        owner=user
                                    )
                        if invoice:
                            requisition.retailer_confirmed = True
                            requisition.status = "RETAILER_CONFIRMED"
                            requisition.total_amount = amount
                            requisition.is_closed = True
                            requisition.save()

                        else:
                            raise serializers.ValidationError(
                                {"response_code": 1, "response_message": f"Available credit limit is { retailer_account.credit_limit}"})

                else:
                    raise serializers.ValidationError(
                        {"response_code": 1, "response_message": "Not eligible for this plan"})

            else:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": "Please create an account with us to enjoy this facility"})

        elif payment_terms == "PLACEMENT":
            if retailer_account:
                if retailer_account.placement_allowed:
                    if retailer_account.placement_limit >= amount:

                        # Create or retrieve an invoice
                        if models.Invoices.objects.filter(facility=user.facility, requisition=requisition, retailer_account=retailer_account).count() > 0:
                            invoice = models.Invoices.objects.get(
                                facility=user.facility, requisition=requisition, retailer_account=retailer_account)
                        else:
                            invoice = models.Invoices.objects.create(
                                facility=user.facility, owner=user, requisition=requisition, retailer_account=retailer_account, invoice_type=payment_terms, total_amount=amount)
                        if invoice and requisition_items:
                            for item in requisition_items:
                                if models.InvoiceItems.objects.filter(invoice=invoice, requisition_item=item).count() > 0:
                                    invoice_item = models.InvoiceItems.objects.get(
                                        invoice=invoice, requisition_item=item)
                                    invoice_item.bonus_quantity = item.bonus_quantity
                                    invoice_item.quantity_invoiced = item.quantity_invoiced
                                    invoice_item.price = item.wholesale_variation.get_final_price()
                                    invoice_item.save()
                                else:
                                    invoice_item = models.InvoiceItems.objects.create(
                                        facility=user.facility,
                                        invoice=invoice,
                                        requisition_item=item,
                                        quantity_invoiced=item.quantity_invoiced,
                                        bonus_quantity=item.bonus_quantity,
                                        price=item.wholesale_variation.get_final_price(),
                                        owner=user
                                    )
                        if invoice_item:
                            requisition.retailer_confirmed = True
                            requisition.status = "RETAILER_CONFIRMED"
                            requisition.total_amount = amount
                            requisition.is_closed = True
                            requisition.save()

                    else:
                        raise serializers.ValidationError(
                            {"response_code": 1, "response_message": f"Available placement limit is { retailer_account.placement_limit}"})

                else:
                    raise serializers.ValidationError(
                        {"response_code": 1, "response_message": "Not eligible for this plan"})

            else:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": "Please create an account with us to enjoy this facility"})
        return requisition


class RequisitionItemsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    product = serializers.SerializerMethodField(
        read_only=True)
    requisition = serializers.PrimaryKeyRelatedField(
        queryset=models.Requisitions.objects.all(),
        many=False)
    wholesale_variation = serializers.PrimaryKeyRelatedField(
        queryset=models.WholesaleVariations.objects.all(),
        many=False)

    class Meta:
        model = models.RequisitionItems
        fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'wholesale_variation',
            'wholesaler_confirmed',
            'retailer_confirmed',
            'quantity_required',
            'quantity_invoiced',
            'quantity_pending',
            'quantity_paid',
            'quantity_unpaid',
            'bonus_quantity',
            'get_total_quantity_issued',
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
            'quantity_invoiced',
            'quantity_pending',
            'quantity_paid',
            'quantity_unpaid',
            'bonus_quantity',
            'wholesaler_confirmed_by',
            'owner',
            'created',
            'updated'
        )

    def get_product(self, obj):
        variation = None
        if models.WholesaleVariations.objects.filter(id=obj.wholesale_variation_id).count() > 0:
            variation = models.WholesaleVariations.objects.get(
                id=obj.wholesale_variation.id)
            return WholesaleVariationsSerializer(variation, context=self.context).data
        return variation

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
        quantity_invoiced = None
        user_pk = self.context.get("user_pk")
        user = Users.objects.get(id=user_pk)

        quantity_required = int(validated_data.pop('quantity_required'))
        wholesale_variation = validated_data.pop('wholesale_variation')
        requisition = validated_data.pop('requisition')

        if requisition.owner.facility != user.facility:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "You can only add items to a requisition for your facility"})

        # Check if requisition is still open for editing
        if requisition.is_closed:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Requisition is no longer open for editing"})

        # Quantity should not be zero
        if quantity_required <= 0:
            raise serializers.ValidationError(
                "Quantity required cannot be zero")

        # Item should be in stock
        if wholesale_variation.quantity_available <= 0:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": "Item is out of stock"})
        # Item should be in stock
        if wholesale_variation.quantity_available < quantity_required and wholesale_variation.quantity_available > 0:
            quantity_invoiced = wholesale_variation.quantity_available

          # Item should be in stock
        if wholesale_variation.quantity_available >= quantity_required > 0:
            quantity_invoiced = quantity_required

            # Requisition item should be unique
        if models.RequisitionItems.objects.filter(
                facility=user.facility, requisition=requisition, wholesale_variation=wholesale_variation).count() > 0:
            new_requisition_item = models.RequisitionItems.objects.get(
                facility=user.facility, requisition=requisition, wholesale_variation=wholesale_variation)

            # Update retrieved requisition item with the new entered required quantity_available

            new_requisition_item.quantity_required = quantity_required
            # Available quantity
            new_requisition_item.quantity_invoiced = quantity_invoiced
            # Save bonus quantity
            new_requisition_item.bonus_quantity = wholesale_variation.get_bonus_quantity(
                quantity_required)
            new_requisition_item.save()
        else:
            # Create requisition item if all is well
            if quantity_required > 0:
                new_requisition_item = models.RequisitionItems.objects.create(
                    requisition=requisition,
                    wholesale_variation=wholesale_variation,
                    quantity_required=quantity_required,
                    quantity_invoiced=quantity_invoiced,
                    bonus_quantity=wholesale_variation.get_bonus_quantity(
                        quantity_invoiced),
                    ** validated_data)

        return new_requisition_item

    @ transaction.atomic
    def update(self, requisition_item, validated_data):
        """
        This method updates the prescription quote item

        """

        # Retrieve quote item ID from context as it was passed in url
        if requisition_item.retailer_confirmed:
            raise serializers.ValidationError(
                {"response_code": 1, "response_message": f"Item is closed for editing. You can only delete it"})


class RequisitionPaymentsSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
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

            # Update inventory
            if models.RequisitionPayments.objects.filter(requisition=requisition_payment.requisition).count() > 0:
                requisition_items = models.RequisitionItems.objects.filter(
                    requisition=requisition_payment.requisition)
                for item in requisition_items:
                    if item.wholesale_variation.quantity_available >= item.quantity_invoiced:
                        # Deduct sold quantity_available from inventory if quantity_available is still sufficient
                        quantity_issued = item.quantity_invoiced+item.bonus_quantity
                        item.wholesale_variation.quantity_issued += quantity_issued
                        item.wholesale_variation.quantity_available -= quantity_issued
                        item.wholesale_variation.save()

                        # Check if item has discount

                    else:
                        raise serializers.ValidationError(
                            {"response_code": 1,
                             "response_message": f"Quantity available  now is  {item.wholesale_variation.quantity_available}"})

            else:
                raise serializers.ValidationError(
                    {"response_code": 1,
                     "response_message": f"Requisition has no items added to it"})

        else:
            raise serializers.ValidationError(
                {"response_code": 1,
                 "response_message": f"Check if your payment was succesfully processed"})

        return requisition_payment


class InvoicesSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Invoices
        fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'retailer_account',
            'invoice_type',
            'total_amount',
            'paid_amount',
            'due_amount',
            'despatch_confirmed',
            'courier_confirmed',
            'receipt_confirmed',
            'owner',
            'courier',
            'wholesale_despatch_by',
            'wholesale_approved_by',
            'retail_receipt_by',
            'created',
            'updated')
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'retailer_account',
            'invoice_type',
            'total_amount',
            'paid_amount',
            'due_amount',
            'despatch_confirmed',
            'courier_confirmed',
            'receipt_confirmed',
            'owner',
            'courier',
            'wholesale_despatch_by',
            'wholesale_approved_by',
            'retail_receipt_by',
            'created',
            'updated')
