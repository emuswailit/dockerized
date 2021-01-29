import datetime
from datetime import date, timedelta
from django.db import models
import uuid
from users.models import Facility
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from payments.models import Payment, PaymentMethods
from core.models import FacilityRelatedModel

User = get_user_model()

# Create your models here.


class Plan(FacilityRelatedModel):
    PLAN_CHOICES = (
        ("Trial", "Trial"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly")
    )
   
    title = models.CharField(max_length=256, choices=PLAN_CHOICES, unique=True)
    description = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SubscriptionPayments(FacilityRelatedModel):
    
    """
    -Model for a subscription payment

    -Create a subscription only after this payment is saved
    """
    PAYMENT_STATUS_CHOICES =(
        ("PENDING","PENDING"),
        ("SUCCESS","SUCCESS"),
        ("FAILED","FAILED"),
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    narrative = models.CharField(max_length=300, null=False, blank=False)
    reference= models.CharField(
        max_length=120,null=False,blank=False)
    status= models.CharField(
        max_length=120, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    subscription_created = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.facility.title



class Subscription(FacilityRelatedModel):
    """
    To be created upon succesfull subscription payment
    """
    subscription_payment = models.OneToOneField(SubscriptionPayments, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False) #TODO: Update this variable every hour using scheduled tasks in celery
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.facility.title

    def get_subscription_status(self):
        return self.is_active
