from django.db import models
from core.models import FacilityRelatedModel
from drugs.models import Products, Distributor
from django.contrib.auth import get_user_model
from utilities.models import Categories
from users.models import Facility
from entities.models import Employees
from payments.models import PaymentMethods

User = get_user_model()


class RetailerAccounts(FacilityRelatedModel):
    """
    -Model for retailer accounts
    -Will be required for retailers who will buy on credit or with placement arrangements

    """
    retailer = models.OneToOneField(
        Facility, related_name="account_retail_facility", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    credit_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    credit_allowed = models.BooleanField(default=False)
    placement_allowed = models.BooleanField(default=False)
    account_manager = models.OneToOneField(
        Employees, on_delete=models.CASCADE, null=True, blank=True)
    account_contact = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="facility_account_owner", on_delete=models.CASCADE)


class WholesaleProducts(FacilityRelatedModel):
    """Model for product variation, unique to each facility"""
    product = models.ForeignKey(
        Products, related_name="listing_products", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    total_quantity = models.IntegerField(default=0)
    trade_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="listing_owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title


class WholesaleVariations(FacilityRelatedModel):
    """
    -Model for product variation, unique to each facility
    -This represents a consignment or batch of a particular product received in the wholesale pharmacy
    -A wholesale can thus have two or more batches of a particular item in stock, difering by date received, price, discounts, expiry dates, etc,

    """
    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="wholesale_variation_product", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()
    buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    source = models.ForeignKey(
        Distributor, related_name="listing_purchases", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=140, null=True, blank=True)
    batch = models.CharField(max_length=140, null=True, blank=True)
    manufacture_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(
        User, related_name="inventory_owner", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Distributor, on_delete=models.CASCADE)

    def __str__(self):
        return self.wholesale_product.product.title


class Discounts(FacilityRelatedModel):
    """
    Model for product discount expressed as a percentage

    """
    # TODO: Implement scheduled task to turn on and off a discount based on start and end date

    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="discount_product", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True,
                             blank=True,)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    percentage = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00)
    owner = models.ForeignKey(
        User, related_name="discount_owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Bonuses(FacilityRelatedModel):
    """
    Model for product discount expressed as a percentage

    """
    # TODO: Implement scheduled task to turn on and off a bonus based on start and end date

    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="bonus_product", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True,
                             blank=True,)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    for_every = models.IntegerField()
    get_free = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name="bonus_owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Requisitions(FacilityRelatedModel):
    """
    -Model a retailer requisition
    -Order made by a retailer superintendent in a selected wholesaler

    """
    # TODO: Implement scheduled task to turn on and off a discount based on start and end date
    PRIORITY_CHOICES = (
        ("HIGH", "HIGH PRIORITY"),
        ("NORMAL", "NORMAL PRIORITY"),
        ("LOW", "LOW PRIORITY"),
    )

    STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("RETAILER_CONFIRMED", "RETAILER CONFIRMED"),
        ("PROCESSING", "PROCESSING"),
        ("PARTIALLY_DISPATCHED", "PARTIALLY DISPATCHED"),
        ("FULLY_DISPATCHED", "FULLY DISPATCHED"),
        ("CANCELLED", "CANCELLED"),
        ("CLOSED", "CLOSED"),
    )

    PAYMENT_TERMS_CHOICES = (
        ("CASH", "CASH"),
        ("CREDIT", "CREDIT"),
        ("PLACEMENT", "PLACEMENT"),
    )
    wholesale = models.ForeignKey(
        Facility, related_name="wholesale_facility", on_delete=models.CASCADE)
    retailer_account = models.ForeignKey(
        RetailerAccounts, related_name="requisitioning_account", on_delete=models.CASCADE, null=True, blank=True)
    retailer_confirmed = models.BooleanField(default=False)
    wholesaler_confirmed = models.BooleanField(default=False)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="PENDING")
    payment_terms = models.CharField(
        max_length=100, choices=PAYMENT_TERMS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="requisition_owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"Requisition : {self.wholesale.title} - {self.status}"


class RequisitionItems(FacilityRelatedModel):
    """
    Model for requisition item

    """
    requisition = models.ForeignKey(
        Requisitions, related_name="requisition", on_delete=models.CASCADE)
    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="requisition_wholesale", on_delete=models.CASCADE, null=True, blank=True)
    quantity_required = models.IntegerField()
    quantity_issued = models.IntegerField(default=0)
    quantity_pending = models.IntegerField(default=0)
    quantity_paid = models.IntegerField(default=0)
    quantity_unpaid = models.IntegerField(default=0)
    retailer_confirmed = models.BooleanField(default=True)
    wholesaler_confirmed = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    wholesaler_confirmed_by = models.ForeignKey(
        User, related_name="wholesale_authority", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        User, related_name="requisition_item_owner", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'requisition', 'wholesale_product', ], name='Unique item per requisition')
        ]

    # def __str__(self):
    #     return self.title


class Despatches(FacilityRelatedModel):
    """
    -Model for a requisition despatch, created by a wholesale superintendent
    -Created when  first requisition item is confirmed by the wholesale superintendent
    -A requisition can have several despatches to support part filling of requisitions incase of stock outs, etc
    -A despatch will form a basis for a retailer variation receipt

    """

    DESPATCH_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("DESPATCHED", "DESPATCHED"),
        ("RECEIVED", "RECEIVED"),
        ("CANCELLED", "CANCELLED"),
    )
    PRIORITY_CHOICES = (
        ("HIGH", "HIGH PRIORITY"),
        ("NORMAL", "NORMAL PRIORITY"),
        ("LOW", "LOW PRIORITY"),
    )

    requisition = models.ForeignKey(
        Requisitions, related_name="requisition_despatch", on_delete=models.CASCADE)

    despatch_confirmed = models.BooleanField(default=True)
    receipt_confirmed = models.BooleanField(default=True)
    courier_confirmed = models.BooleanField(default=True)
    status = models.CharField(
        max_length=100, choices=DESPATCH_STATUS_CHOICES, default="PENDING")
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    despatch_confirmed_by = models.ForeignKey(
        User, related_name="despatch_confirmed_by", on_delete=models.CASCADE, null=True, blank=True)
    receipt_confirmed_by = models.ForeignKey(
        User, related_name="receipt_confirmed_by", on_delete=models.CASCADE, null=True, blank=True)
    courier_confirmed_by = models.ForeignKey(
        User, related_name="courier_confirmed_by", on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    courier = models.ForeignKey(
        Employees, related_name="despatch_courier", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        User, related_name="despatch_owner", on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title


class DespatchItems(FacilityRelatedModel):
    """
    Model for requisition item

    """
    despatch = models.ForeignKey(
        Despatches, related_name="item_despatch", on_delete=models.CASCADE)
    requisition_item = models.ForeignKey(
        RequisitionItems, related_name="despatch_item_requisition", on_delete=models.CASCADE)
    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="despatch_item_product", on_delete=models.CASCADE)
    quantity_issued = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="despatch_item_owner", on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'despatch', 'requisition_item', 'wholesale_variation'], name='One variation item in despatch')
        ]


class DespatchPayments(FacilityRelatedModel):
    """
    -Model for despatch payment
    -Created alongside a despatch in a 1:1 relationship

    """
    PAYMENT_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
        ("CANCELLED", "CANCELLED"),
    )

    PAYMENT_TERMS_CHOICES = (
        ("CASH", "CASH"),
        ("CREDIT", "CREDIT"),
        ("PLACEMENT", "PLACEMENT"),
    )
    despatch = models.ForeignKey(
        Despatches, related_name="payment_for_despatch", on_delete=models.CASCADE)
    payment_method = models.ForeignKey(
        PaymentMethods, related_name="requisition_payment_method", on_delete=models.CASCADE)
    payment_terms = models.CharField(
        max_length=100, choices=PAYMENT_TERMS_CHOICES)
    status = models.CharField(
        max_length=100, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="despatch_payment_owner", on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title
