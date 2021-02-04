from consultations.models import PrescriptionItem, Prescription
from rest_framework.exceptions import ValidationError
from payments.models import PaymentMethods
from consultations.models import Prescription
from rest_framework import exceptions
import uuid
from django.db.models import signals
from django.dispatch import receiver
from django.db import models
from users.models import Facility
from drugs.models import Products
from core.models import FacilityRelatedModel
from drugs.models import Distributor
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from .utils import unique_slug_generator
from django.utils.text import slugify
import decimal
# from drugs.models import Categories

User = get_user_model()


def variation_image_upload_to(instance, filename):
    title = instance.variation.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s.%s" % (slug, file_extension)
    return new_filename


class VariationsQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query)
                   )
    # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()


class VariationsManager(models.Manager):
    def get_queryset(self):
        return VariationsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def featured(self):  # Variations.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        # Variations.objects == self.get_queryset()
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Variations(FacilityRelatedModel):
    """
    -Model for retail product variation, unique to each facility
    -Inherits most of its parameters from Products

    """
    product = models.ForeignKey(
        Products, related_name="variations_product", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    objects = VariationsManager()

    def __str__(self):
        return f"{self.title}"

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def get_available_units(self):
        available_units = 0
        if Inventory.objects.filter(variation=self).count() > 0:
            items = Inventory.objects.filter(variation=self)

            for item in items:
                available_units += item.unit_quantity
        return available_units

    def get_available_packs(self):
        available_packs = 0
        if Inventory.objects.filter(variation=self).count() > 0:
            items = Inventory.objects.filter(variation=self)

            for item in items:
                available_packs += item.pack_quantity

        return available_packs


# TODO : When a product is deactivated all variations should be deactivated too
# A product variation with inventory greater than one cannot be activated

# TODO update variation inventory upon release to outlets


class VariationPhotos(FacilityRelatedModel):
    """Model for uploading profile product image"""
    variation = models.ForeignKey(
        Variations, related_name="variation_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=variation_image_upload_to)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.variation.title


class Inventory(FacilityRelatedModel):
    distributor = models.ForeignKey(
        Distributor, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.CharField(max_length=50, null=True,
                             blank=True, editable=True)
    variation = models.ForeignKey(Variations, on_delete=models.CASCADE)
    units_per_pack = models.IntegerField(default=0)
    pack_quantity = models.IntegerField(default=0)
    pack_buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    pack_selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    unit_quantity = models.IntegerField(default=0)
    unit_buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    unit_selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    description = models.CharField(max_length=120, blank=True, null=True)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variation.title}"


class Forwards(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    PRESCRIPTION_STATUS_CHOICES = (
        ("Forwarded", "Forwarded"),
        ("Quoted", "Quoted"),
        ("Confirmed", "Confirmed"),
        ("Partially Dispensed", "Partally Dispensed"),
        ("Fully Dispensed", "Fully Dispensed"))

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    prescription = models.ForeignKey(
        Prescription, related_name="forwarded_prescription_prescription", on_delete=models.CASCADE)
    comment = models.CharField(max_length=120, null=True)
    status = models.CharField(
        max_length=100, choices=PRESCRIPTION_STATUS_CHOICES, default="Forwarded")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['facility_id', 'prescription_id'], name='forward prescription to pharmacy once')
    #     ]

    def __str__(self):
        return f'Prescription for {self.prescription.dependant.first_name} {self.prescription.dependant.last_name} from {self.prescription.owner.first_name} {self.prescription.owner.last_name} '

# def forward_prescription_pre_save_receiver(sender, instance, *args, **kwargs):
#     if instance.facility:
#         if instance.facility.facility_type == 'Default' or instance.facility.facility_type == 'Clinic':
#             raise exceptions.NotAcceptable(
#                 {"detail": ["The selected facility is not a pharmacy", ]})


# pre_save.connect(forward_prescription_pre_save_receiver,
#                  sender=Forwards)


class PrescriptionQuote(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""

    forward = models.ForeignKey(
        Forwards, related_name="prescription_quote_forward", on_delete=models.CASCADE)
    client_confirmed = models.BooleanField(default=False)
    pharmacist_confirmed = models.BooleanField(default=False)
    pharmacist_processing = models.BooleanField(default=False)
    payment_method = models.ForeignKey(
        PaymentMethods, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    processed_by = models.ForeignKey(
        User, related_name="prescription_quote_quoted_by", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'prescription'], name='One quote per prescription')
        ]

    def __str__(self):
        return self.forward_prescription.prescription.dependant.first_name

    def get_total_quote_cost(self):
        total = 0
        if QuoteItem.objects.filter(prescription_quote=self).count() > 0:
            items = QuoteItem.objects.filter(prescription_quote=self)
            for item in items:
                total += item.get_dispensed_items_cost()

        else:
            pass
        return total


class QuoteItemQuerySet(models.QuerySet):
    def all_quote_items(self):
        return self.all()

    def partially_dispensed_quote_items(self):
        return self.filter(fully_dispensed=False)


class QuoteItemManager(models.Manager):
    def get_queryset(self):
        return QuoteItemQuerySet(self.model, using=self._db)

    def all_quote_items(self):
        return self.get_queryset().all_quote_items()

    def partially_dispensed_quote_items(self):
        return self.get_queryset().partially_dispensed_quote_items()


class QuoteItem(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    prescription_quote = models.ForeignKey(
        PrescriptionQuote, on_delete=models.CASCADE, null=True, blank=True)
    prescription_item = models.ForeignKey(
        PrescriptionItem, related_name="prescription_item", on_delete=models.CASCADE, null=True, blank=True)
    variation = models.ForeignKey(
        Variations, related_name="quote_item_inventory", on_delete=models.CASCADE, null=True, blank=True)
    quantity_required = models.IntegerField(default=0)
    quantity_dispensed = models.IntegerField(default=0)
    quantity_pending = models.IntegerField(default=0)
    pharmacist_instructions = models.TextField(blank=True, null=True)
    dose_divisible = models.BooleanField(default=True)
    item_accepted = models.BooleanField(default=True)
    fully_dispensed = models.BooleanField(default=False)
    client_comment = models.TextField(blank=True, null=True)
    client_confirmed = models.BooleanField(default=False)
    pharmacist_confirmed = models.BooleanField(default=False)
    pharmacist_processing = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    processed_by = models.ForeignKey(
        User, related_name="quote_item_processed_by", on_delete=models.CASCADE, null=True, blank=True)
    objects = QuoteItemManager()

    class Meta:
        unique_together = ('prescription_quote',
                           'prescription_item', 'variation')


class Order(FacilityRelatedModel):
    """
    -Model for an order created in a selected facility by a client
    -Several orders can be made by a client for every prescription quote to allow for partial prescription filling
    -This model ia automatically created when a client confirms a quote item, thus no view is provided for creating it

    """

    facility = models.ForeignKey(
        Facility, related_name="cart_facility", on_delete=models.CASCADE)
    prescription_quote = models.ForeignKey(
        PrescriptionQuote, related_name="cart_prescription_quote", on_delete=models.CASCADE)
    client_confirmed = models.BooleanField(default=False)
    payment_method = models.ForeignKey(
        PaymentMethods, on_delete=models.CASCADE)
    pharmacist_confirmed = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def get_total_price(self):
        total = 0

        if OrderItem.objects.filter(order_id=self.id).count() > 0:
            items = OrderItem.objects.filter(order_id=self.id)
            for order_item in items:
                total += order_item.get_total_item_price()
        return total


class OrderItem(FacilityRelatedModel):
    """
    -Model for order items
    -Items are automatically created when a client conforms a quote item
    """
    facility = models.ForeignKey(
        Facility,  on_delete=models.CASCADE)
    quote_item = models.ForeignKey(
        QuoteItem, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    client_confirmed = models.BooleanField(default=False)
    pharmacist_confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def get_total_item_price(self):
        return self.quantity * self.quote_item.inventory.unit_selling_price

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'quote_item', 'order'], name='One quote item in order')
        ]


class PharmacyPayments(FacilityRelatedModel):
    """
    -Model order payment
    -Its automatically created when a user confirms an order
    """

    PAYMENT_STATUS_CHOICES = (
        ("PENDING",  "PENDING"),
        ("SUCCESS",  "SUCCESS"),
        ("FAILED",  "FAILED"),
    )
    facility = models.ForeignKey(
        Facility, related_name="payment_facility", on_delete=models.CASCADE)
    order = models.OneToOneField(
        Order, related_name="payment_order",  on_delete=models.CASCADE)
    reference = models.CharField(
        max_length=120, null=True,  blank=True)
    status = models.CharField(
        max_length=120, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    payment_method = models.ForeignKey(
        PaymentMethods, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="pharmacy_payment_owner", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(

                fields=['facility', 'order'], name='One payment per facility per order')
        ]

    # def get_payment_method(self):
    #     return self.order.payment_method

    # def get_amount(self):
    #     return self.order.get_total_price()


class PrescriptionSale(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    PAYMENT_METHODS = (("Cash", "Cash"),
                       ("Jambopay", "Jambopay"),
                       ("Mpesa", "Mpesa"),
                       ("Visa", "Visa"),)
    prescription = models.ForeignKey(
        PrescriptionQuote, on_delete=models.CASCADE)

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)


class PrescriptionSaleItem(FacilityRelatedModel):
    """Model for prescription sale item"""
    sale = models.ForeignKey(
        PrescriptionSale, on_delete=models.CASCADE)
    item = models.ForeignKey(
        QuoteItem, related_name="sale_quote_item", on_delete=models.CASCADE)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)
    instructions = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)


def counter_sale_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.item.quoted_item.unit_quantity < instance.quantity:
        raise exceptions.NotAcceptable(
            {"detail": ["Insufficient stock!", ]})


pre_save.connect(counter_sale_pre_save_receiver,
                 sender=PrescriptionSaleItem)

# Deduct inventory


@receiver(post_save, sender=PrescriptionSaleItem, dispatch_uid="update_prescription_total")
def create_offer(sender, instance, created, **kwargs):
    """Deduct from inventoty"""
    if created:
        try:
            instance.item.quoted_item.unit_quantity = instance.quoted_item.item.unit_quantity - instance.quantity
            instance.item.quoted_item.save()
            instance.item.quoted_item.variation.quantity = instance.item.quoted_item.variation.quantity - \
                instance.quantity
            instance.item.variation.save()
        except:
            pass


class CounterSale(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    PAYMENT_METHODS = (("Cash", "Cash"),
                       ("Jambopay", "Jambopay"),
                       ("Mpesa", "Mpesa"),
                       ("Visa", "Visa"),)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)


class CounterSaleItem(FacilityRelatedModel):
    """Model for counter, non prescription sale item"""
    client_phone = models.CharField(max_length=30, null=True, blank=True)
    item = models.ForeignKey(
        Inventory, related_name="sale_item", on_delete=models.CASCADE)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)
    instructions = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)


def counter_sale_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.item.unit_quantity < instance.quantity:
        raise exceptions.NotAcceptable(
            {"detail": ["Insufficient stock!", ]})


pre_save.connect(counter_sale_pre_save_receiver,
                 sender=CounterSaleItem)

# Deduct inventory


@receiver(post_save, sender=CounterSaleItem, dispatch_uid="update_prescription_total")
def create_offer(sender, instance, created, **kwargs):
    """Deduct from inventoty"""
    if created:
        try:
            instance.item.unit_quantity = instance.item.unit_quantity - instance.quantity
            instance.item.save()
            instance.item.variation.quantity = instance.item.variation.quantity - instance.quantity
            instance.item.variation.save()
        except:
            pass


# @receiver(post_save, sender=PrescriptionQuote, dispatch_uid="create_prescription_items")
# def create_offer(sender, instance, created, **kwargs):
#     """Deduct from inventoty"""
#     if created:
#         prescription_id = instance.forward_prescription.prescription.id

#         if PrescriptionItem.objects.filter(prescription_id=prescription_id).count()>0:
#             prescription_items = PrescriptionItem.objects.filter(prescription_id=prescription_id)

#             for item in prescription_items:
#                 QuoteItem.objects.create(facility=instance.facility,owner=instance.owner,prescription_quote=instance,prescription_item=item)

#                 raise ValidationError(f"Ziko {prescription_items.count()}")

#         else:
#             raise ValidationError(f"Hakuna kitu ya {prescription_id}")
