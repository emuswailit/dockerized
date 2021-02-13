from decimal import *
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
    wholesale = models.OneToOneField(
        Facility, related_name="retail_account_wholesale", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    credit_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    placement_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    credit_allowed = models.BooleanField(default=False)
    placement_allowed = models.BooleanField(default=False)
    retailer_verified = models.BooleanField(default=False)
    wholesaler_contact = models.OneToOneField(
        Employees, on_delete=models.CASCADE, null=True, blank=True)
    retailer_contact = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="facility_account_owner", on_delete=models.CASCADE)
    retailer_verified_by = models.ForeignKey(
        User, related_name="retailer_verifier", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        # Enforce account uniqueness
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'wholesale', ], name='Unique account per retailer')
        ]


# class WholesaleProducts(FacilityRelatedModel):
#     """Model for product variation, unique to each facility"""
#     product = models.ForeignKey(
#         Products, related_name="listing_products", on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     owner = models.ForeignKey(
#         User, related_name="listing_owner", on_delete=models.CASCADE)

#     def __str__(self):
#         return self.product.title

class WholesaleVariationsQuerySet(models.QuerySet):
    def all_wholesale_variations(self):
        return self.all()

    def available_wholesale_variations(self):
        return self.filter(quantity_available__gte=1)


class WholesaleVariationsManager(models.Manager):
    def get_queryset(self):
        return WholesaleVariationsQuerySet(self.model, using=self._db)

    def all_wholesale_variations(self):
        return self.get_queryset().all_wholesale_variations()

    def available_wholesale_variations(self):
        return self.get_queryset().available_wholesale_variations()


class WholesaleVariations(FacilityRelatedModel):
    """
    -Model for product variation, unique to each facility
    -This represents a consignment or batch of a particular product received in the wholesale pharmacy
    -A wholesale can thus have two or more batches of a particular item in stock, difering by date received, price, discounts, expiry dates, etc,

    """
    product = models.ForeignKey(
        Products, related_name="wholesale_variation_product", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    quantity_received = models.IntegerField()
    quantity_issued = models.IntegerField(default=0)
    quantity_available = models.IntegerField(default=0)
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

    objects = WholesaleVariationsManager()

    def __str__(self):
        if self.product.preparation:
            return f"{self.product.preparation.title} ({self.product.title}) - Available: {self.quantity_available} -Expiry:  {self.expiry_date}"
        return f"{self.product.title} - Available qty: {self.quantity_available} -Expiry: {self.expiry_date}"

    def get_final_price(self):
        final_price = self.selling_price
        if Discounts.objects.filter(wholesale_variation=self).count() > 0:
            discount = Discounts.objects.get(wholesale_variation=self)
            final_price = (self.selling_price) - \
                (self.selling_price * discount.percentage/100)

        return final_price

    def get_bonus_quantity(self, quantity_required):
        """
        -Calculate bonus based on quantity required and return to calling object
        """
        bonus_earned = 0
        if Bonuses.objects.filter(wholesale_variation=self).count() > 0:
            bonuses = Bonuses.objects.filter(wholesale_variation=self)
            for bonus in bonuses:
                if quantity_required >= bonus.lowest_limit and quantity_required <= bonus.highest_limit:
                    bonus_earned = bonus.bonus_quantity
                else:
                    pass
        else:
            pass

        return bonus_earned


class Discounts(FacilityRelatedModel):
    """
    Model for product discount expressed as a percentage

    """
    # TODO: Implement scheduled task to turn on and off a discount based on start and end date

    wholesale_variation = models.ForeignKey(
        WholesaleVariations, related_name="wholesale_variation_discount", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True,
                             blank=True,)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    percentage = models.DecimalField(
        max_digits=4, decimal_places=2)
    owner = models.ForeignKey(
        User, related_name="discount_owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Bonuses(FacilityRelatedModel):
    """
    Model for product discount expressed as a percentage

    """
    # TODO: Implement scheduled task to turn on and off a bonus based on start and end date

    wholesale_variation = models.ForeignKey(
        WholesaleVariations, related_name="wholesale_variation_bonus", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True,
                             blank=True,)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lowest_limit = models.IntegerField()
    highest_limit = models.IntegerField()
    bonus_quantity = models.IntegerField()
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
    is_closed = models.BooleanField(default=False)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="PENDING")
    payment_terms = models.CharField(
        max_length=100, choices=PAYMENT_TERMS_CHOICES, default="CASH")
    payment_method = models.ForeignKey(
        PaymentMethods, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="requisition_owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"Requisition : {self.wholesale.title} - {self.status}"


class RequisitionItemsQuerySet(models.QuerySet):
    def all_requisition_items(self):
        return self.all()

    def retailer_confirmed_items(self):
        return self.filter(retailer_confirmed=True)

    def draft_requisition_items(self):
        return self.filter(retailer_confirmed=False)


class RequisitionItemsManager(models.Manager):
    def get_queryset(self):
        return RequisitionItemsQuerySet(self.model, using=self._db)

    def all_requisition_items(self):
        return self.get_queryset().all_requisition_items()

    def retailer_confirmed_items(self):
        return self.get_queryset().retailer_confirmed_items()

    def draft_requisition_items(self):
        return self.get_queryset().draft_requisition_items()


class RequisitionItems(FacilityRelatedModel):
    """
    Model for requisition item

    """
    requisition = models.ForeignKey(
        Requisitions, related_name="requisition", on_delete=models.CASCADE)
    wholesale_variation = models.ForeignKey(
        WholesaleVariations, related_name="requisition_item", on_delete=models.CASCADE)
    quantity_required = models.IntegerField()
    quantity_invoiced = models.IntegerField(default=0)
    quantity_pending = models.IntegerField(default=0)
    quantity_paid = models.IntegerField(default=0)
    quantity_unpaid = models.IntegerField(default=0)
    bonus_quantity = models.IntegerField(default=0)
    retailer_confirmed = models.BooleanField(default=False)
    wholesaler_confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    wholesaler_confirmed_by = models.ForeignKey(
        User, related_name="wholesale_authority", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        User, related_name="requisition_item_owner", on_delete=models.CASCADE)

    objects = RequisitionItemsManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'requisition', 'wholesale_variation', ], name='Unique item per requisition')
        ]

    # def __str__(self):
    #     return self.title
    def get_total_quantity_issued(self):
        return f"{self.quantity_invoiced+ self.bonus_quantity}"


class RequisitionPayments(FacilityRelatedModel):
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
    requisition = models.OneToOneField(
        Requisitions, related_name="payment_requisition", on_delete=models.CASCADE)
    payment_method = models.ForeignKey(
        PaymentMethods, related_name="requisition_payment_method", on_delete=models.CASCADE)
    payment_terms = models.CharField(
        max_length=100, choices=PAYMENT_TERMS_CHOICES)
    status = models.CharField(
        max_length=100, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="despatch_payment_owner", on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title
