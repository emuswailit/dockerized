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
from rest_framework.exceptions import ValidationError
from users.models import Facility
# Create your models here.


class PrescriptionQuote(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""

    forward_prescription = models.ForeignKey(
        ForwardPrescription, related_name="prescription_quote_prescription", on_delete=models.CASCADE)
    prescription_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    client_confirmed = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['facility', 'prescription'], name='One quote per prescription')
        ]

    def __str__(self):
        return self.forward_prescription.prescription.dependant.first_name




class QuoteItem(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    prescription_quote = models.ForeignKey(
        PrescriptionQuote, on_delete=models.CASCADE,null=True,blank=True)
    prescription_item = models.ForeignKey(
        PrescriptionItem, related_name="prescription_item", on_delete=models.CASCADE,null=True, blank=True)
    variation_item= models.ForeignKey(
        VariationReceipt, related_name="variation_receipt", on_delete=models.CASCADE, null=True,blank=True)
    item_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    quantity_required = models.IntegerField(default=0)
    quantity_dispensed = models.IntegerField(default=0)
    quantity_pending = models.IntegerField(default=0)
    instructions = models.TextField(blank=True, null=True)
    dose_divisible= models.BooleanField(default=True)
    item_accepted= models.BooleanField(default=True)
    fully_dispensed= models.BooleanField(default=False)
    client_comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prescription_quote', 'prescription_item','variation_item')



class Order(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    PAYMENT_METHOD_CHOICES =(
        ("CASH","CASH"),
        ("MPESA","MPESA"),
        ("AIRTEL MONEY","AIRTEL MONEY"),
        ("EQUITEL","EQUITEL"),
        ("JAMBOPAY WALLET","JAMBOPAY WALLET"),
        ("VISA","VISA"),
    )
    facility = models.ForeignKey(
        Facility, related_name="cart_facility", on_delete=models.CASCADE)
    prescription_quote = models.ForeignKey(
        PrescriptionQuote, related_name="cart_prescription_quote", on_delete=models.CASCADE)
    # items = models.ManyToManyField(OrderItem)
    is_confirmed = models.BooleanField(default=False)
    payment_method= models.CharField(
        max_length=120, choices=PAYMENT_METHOD_CHOICES)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def get_total_price(self):
        total=0

        if OrderItem.objects.filter(order_id=self.id).count()>0:
            items =OrderItem.objects.filter(order_id=self.id)
            for order_item in items:
                total += order_item.get_total_item_price()
        return total
        
class OrderItem(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""
    facility = models.ForeignKey(
        Facility,  on_delete=models.CASCADE)
    quote_item = models.ForeignKey(
        QuoteItem, on_delete=models.CASCADE,null=True, blank=True)
    order =models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def get_total_item_price(self):
        return self.quantity * self.quote_item.variation_item.unit_selling_price
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['facility', 'quote_item'], name='One quote item in order')
        ]
  

class Payment(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""

    PAYMENT_STATUS_CHOICES =(
        ("PENDING","PENDING"),
        ("SUCCESS","SUCCESS"),
        ("FAILED","FAILED"),
    )
    facility = models.ForeignKey(
        Facility, related_name="payment_facility", on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, related_name="payment_order",  on_delete=models.CASCADE)
    reference= models.CharField(
        max_length=120, null=True,blank=True)
    status= models.CharField(
        max_length=120, choices=PAYMENT_STATUS_CHOICES)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="payment_owner", on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['facility', 'order'], name='One payment per facility per order')
        ]

    def get_payment_method(self):
        return self.order.payment_method

    def get_amount(self):
        return self.order.get_total_price()





#  Check if prescribed drug is the one being quoted


# def quote_item_pre_save_receiver(sender, instance, *args, **kwargs):

#     instance.item_cost = instance.quoted_item.unit_selling_price * \
#         instance.quantity_required
#     instance.quantity_pending = instance.quantity_required - instance.quantity_dispensed
#     if instance.quoted_item.variation.is_drug:
#         if instance.prescription_item.preparation == instance.quoted_item.variation.product.preparation:
#             raise exceptions.NotAcceptable(
#                 {"detail": ["Correct item quoted!", ]})
#         else:
#             raise exceptions.NotAcceptable(
#                 {"detail": ["Please quote the prescribed item", ]})
#     else:
#         print("Will proceed to save!")


# pre_save.connect(quote_item_pre_save_receiver,
#                  sender=QuoteItem)


# @receiver(post_save, sender=QuoteItem, dispatch_uid="update_prescription_total")
# def create_offer(sender, instance, created, **kwargs):
#     """Calculate unit quantities and prices"""
#     if not created:
#         raise ValidationError("Updated")
     


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


    
@receiver(post_save, sender=PrescriptionQuote, dispatch_uid="create_prescription_items")
def create_offer(sender, instance, created, **kwargs):
    """Deduct from inventoty"""
    if created:
        prescription_id = instance.forward_prescription.prescription.id

        if PrescriptionItem.objects.filter(prescription_id=prescription_id).count()>0:
            prescription_items = PrescriptionItem.objects.filter(prescription_id=prescription_id)

            for item in prescription_items:
                QuoteItem.objects.create(facility=instance.facility,owner=instance.owner,prescription_quote=instance,prescription_item=item)

                raise ValidationError(f"Ziko {prescription_items.count()}") 
            
        else:
            raise ValidationError(f"Hakuna kitu ya {prescription_id}") 
     
