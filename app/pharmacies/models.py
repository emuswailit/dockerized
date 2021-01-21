from django.db import models
from core.models import FacilityRelatedModel
from clients.models import ForwardPrescription
from django.contrib.auth import get_user_model
from consultations.models import PrescriptionItem, Prescription
from inventory.models import VariationReceipt
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
User = get_user_model()
# Create your models here.


class PrescriptionQuote(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""

    prescription = models.ForeignKey(
        Prescription, related_name="prescription_quote_prescription", on_delete=models.CASCADE)
    prescription_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    client_confirmed = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.prescription.dependant.first_name


class QuoteItem(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    prescription_quote = models.ForeignKey(
        PrescriptionQuote, on_delete=models.CASCADE)
    prescription_item = models.ForeignKey(
        PrescriptionItem, related_name="prescription_item", on_delete=models.CASCADE)
    quoted_item = models.ForeignKey(
        VariationReceipt, related_name="variation_receipt", on_delete=models.CASCADE)
    item_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity_required = models.IntegerField(default=0)
    quantity_dispensed = models.IntegerField(default=0)
    quantity_pending = models.IntegerField(default=0)
    instructions = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prescription_quote', 'prescription_item','quoted_item')


    # def __str__(self):
    #     return self.prescription.dependant.first_name

#  Check if prescribed drug is the one being quoted


def quote_item_pre_save_receiver(sender, instance, *args, **kwargs):

    instance.item_cost = instance.quoted_item.unit_selling_price * \
        instance.quantity_required
    instance.quantity_pending = instance.quantity_required - instance.quantity_dispensed
    if instance.quoted_item.variation.is_drug:
        if instance.prescription_item.preparation == instance.quoted_item.variation.product.preparation:
            raise exceptions.NotAcceptable(
                {"detail": ["Correct item quoted!", ]})
        else:
            raise exceptions.NotAcceptable(
                {"detail": ["Please quote the prescribed item", ]})
    else:
        print("Will proceed to save!")


pre_save.connect(quote_item_pre_save_receiver,
                 sender=QuoteItem)


@receiver(post_save, sender=QuoteItem, dispatch_uid="update_prescription_total")
def create_offer(sender, instance, created, **kwargs):
    """Calculate unit quantities and prices"""
    if created:
        try:
            instance.prescription.prescription_cost = instance.prescription.prescription_cost + \
                instance.item_cost

            instance.prescription.save()
        except:

            pass


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
        VariationReceipt, related_name="sale_item", on_delete=models.CASCADE)
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
