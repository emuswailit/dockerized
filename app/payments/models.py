from django.db import models
from core.models import FacilityRelatedModel
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class PaymentMethods(FacilityRelatedModel):
    #TODO : Create views and urls for this model
    """
    Model for all payment methods
    """
    title =models.CharField(max_length=120)
    description =models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

class Payment(FacilityRelatedModel):
    """Model for prescriptions raised for dependants"""

    PAYMENT_STATUS_CHOICES =(
        ("PENDING","PENDING"),
        ("SUCCESS","SUCCESS"),
        ("FAILED","FAILED"),
    )
    
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.ForeignKey(
        PaymentMethods, related_name="payment_payment_method",  on_delete=models.CASCADE)
    narrative = models.CharField(max_length=300)
    reference= models.CharField(
        max_length=120, null=True,blank=True)
    status= models.CharField(
        max_length=120, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="payment_owner", on_delete=models.CASCADE)