import datetime
from datetime import date, timedelta
from django.db import models
import uuid
from users.models import Facility
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# from entities import Payment

User = get_user_model()

# Create your models here.


class Plan(models.Model):
    PLAN_CHOICES = (
        ("Trial", "Trial"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256, choices=PLAN_CHOICES, unique=True)
    description = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# class PaymentMethod(models.Model):
#     id = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=256)
#     description = models.TextField(null=True)
#     owner = models.OneToOneField(
#         User, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


# class Payment(models.Model):
#     """
#     To be initiated by a facility owner
#     """
#     PAYMENT_STATUS_CHOICES = (("INITIATED", "INITIATED"),
#                               ("SUCCESS", "SUCCESS"), ("FAILED",
#                                                        "FAILED"), ("PENDING", "PENDING")
#                               )
#     id = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False)
#     facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
#     plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
#     paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
#     reference_number = models.CharField(max_length=120, null=True, blank=True)
#     status = models.CharField(
#         choices=PAYMENT_STATUS_CHOICES, default="INITIATED", max_length=30)
#     owner = models.ForeignKey(
#         User, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.facility.title} - {self.amount}"


class Subscription(models.Model):
    """
    To be created upon succesfull payment
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    initiated_on = models.DateTimeField(null=True, blank=True)
    terminated_on = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.facility.title


# @receiver(post_save, sender=Payment, dispatch_uid="create_subscription_after_payment")
# def create_subscription(sender, instance, created, **kwargs):
#     """Create subscription after succesfful payment"""
#     if created:
#         start_date = None
#         # Retrieve facility current subscription due date
#         paid_until = instance.facility.paid_until
#         print("Paid Until")
#         print(paid_until)

#         if paid_until is None:
#             # No subscription due date, set today as start date
#             start_date = date.today()
#         else:
#             # Set start date as date for expiry of current subscription
#             start_date = paid_until

#         print("Start date")
#         print(start_date)

#         # Calculate days paid for from plan subscribed for
#         days = None
#         if instance.plan.title == 'Monthly':
#             days = 30
#         elif instance.plan.title == 'Yearly':
#             days = 366
#         elif instance.plan.title == 'Trial':
#             days = 30

#         print("days")
#         print(days)
#         # Create then save subscription
#         subscription = Subscription.objects.create(
#             owner=instance.owner, facility_id=instance.facility_id, payment=instance, is_active=True, initiated_on=start_date, terminated_on=start_date + timedelta(days=days))
#         subscription.save()

#         # Update facility subscription status

#         if subscription:
#             instance.facility.set_paid_until(days)
#             instance.facility.is_subscribed = True
#             instance.facility.save()
