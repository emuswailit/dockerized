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
    title =models.CharField(max_length=120, unique=True)
    description =models.TextField()
    is_active=models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Payment(FacilityRelatedModel):
    """Model for payments made to facility"""

    PAYMENT_STATUS_CHOICES =(
        ("PENDING","PENDING"),
        ("SUCCESS","SUCCESS"),
        ("FAILED","FAILED"),
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.ForeignKey(
        PaymentMethods, related_name="payment_payment_method",  on_delete=models.CASCADE)
    narrative = models.CharField(max_length=300, null=False, blank=False)
    reference= models.CharField(
        max_length=120,null=False,blank=False)
    status= models.CharField(
        max_length=120, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="payment_owner", on_delete=models.CASCADE)