from django.db import models
from core.models import FacilityRelatedModel
from drugs.models import Products, Distributor
from django.contrib.auth import get_user_model
from utilities.models import Categories
from users.models import Facility
from entities.models import Employees
from payments.models import PaymentMethods

User = get_user_model()


class WholesaleProducts(FacilityRelatedModel):
    """Model for product variation, unique to each facility"""
    product = models.ForeignKey(
        Products, related_name="listing_products", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    trade_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="listing_owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title

    def available_packs_quantity(self):
        available_quantity = 0
        if WholesaleVariations.objects.filter(wholesale_product=self).count() > 0:
            variations = WholesaleVariations.objects.filter(
                wholesale_product=self)
            for item in variations:
                available_quantity += item.pack_quantity
        else:
            available_quantity = 0
        return available_quantity

    def total_discounts(self):
        total_discounts = 0.00
        if Discounts.objects.filter(wholesale_product=self).count() > 0:
            discounts = Discounts.objects.filter(
                wholesale_product=self)
            for item in discounts:
                total_discounts += item.percentage
        else:
            total_discounts = 0.00
        return total_discounts


class Discounts(FacilityRelatedModel):
    """
    Model for product discount expressed as a percentage

    """
    # TODO: Implement scheduled task to turn on and off a discount based on start and end date

    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="wholesale_product_discount", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True,
                             blank=True,)

    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
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
        WholesaleProducts, related_name="wholesale_product_bonus", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True,
                             blank=True,)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    for_every = models.IntegerField()
    get_free = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name="bonus_owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class WholesaleVariations(FacilityRelatedModel):
    """Model for product variation, unique to each facility"""
    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="wholesale_variation_product", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pack_quantity = models.IntegerField()
    pack_buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    pack_selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    source = models.ForeignKey(
        Distributor, related_name="listing_purchases", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        User, related_name="inventory_owner", on_delete=models.CASCADE)

    def __str__(self):
        return self.wholesale_product.title


class Requisitions(FacilityRelatedModel):
    """
    Model a retail requisition

    """
    # TODO: Implement scheduled task to turn on and off a discount based on start and end date
    PRIORITY_CHOICES = (
        ("HIGH", "HIGH PRIORITY"),
        ("NORMAL", "NORMAL PRIORITY"),
        ("LOW", "LOW PRIORITY"),
    )

    STATUS_CHOICES = (
        ("PENDING", "PENDING"),
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
    retailer_confirmed = models.BooleanField(default=True)
    wholesaler_confirmed = models.BooleanField(default=True)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    payment_terms = models.CharField(
        max_length=100, choices=PAYMENT_TERMS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="requisition_owner", on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title


class RequisitionItems(FacilityRelatedModel):
    """
    Model for requisition item

    """
    requisition = models.ForeignKey(
        Requisitions, related_name="requisition", on_delete=models.CASCADE)
    wholesale_product = models.ForeignKey(
        WholesaleProducts, related_name="requisition_wholesale", on_delete=models.CASCADE, null=True, blank=True)
    quantity_required = models.IntegerField()
    quantity_issued = models.IntegerField()
    quantity_pending = models.IntegerField()
    quantity_paid = models.IntegerField()
    quantity_unpaid = models.IntegerField()
    retailer_confirmed = models.BooleanField(default=True)
    wholesaler_confirmed = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    wholesale_authority = models.ForeignKey(
        User, related_name="wholesale_authority", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, related_name="requisition_item_owner", on_delete=models.CASCADE)

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
    status = models.CharField(max_length=100, choices=DESPATCH_STATUS_CHOICES)
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    despatch_confirmed_by = models.ForeignKey(
        User, related_name="despatch_confirmed_by", on_delete=models.CASCADE)
    receipt_confirmed_by = models.ForeignKey(
        User, related_name="receipt_confirmed_by", on_delete=models.CASCADE)
    courier_confirmed_by = models.ForeignKey(
        User, related_name="courier_confirmed_by", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    courier = models.ForeignKey(
        Employees, related_name="despatch_courier", on_delete=models.CASCADE)
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
        Requisitions, related_name="item_despatch", on_delete=models.CASCADE)
    quantity_issued = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="despatch_item_owner", on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.title


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
