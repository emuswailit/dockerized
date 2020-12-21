from django.db import models
from consultations.models import Prescription
from users.models import Facility
from core.models import FacilityRelatedModel
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework import exceptions
import uuid
User = get_user_model()

# Create your models here.


class ForwardPrescription(FacilityRelatedModel):
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
    updated = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['facility', 'prescription'], name='forward prescription to pharmacy once')
        ]


def forward_prescription_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.facility:
        if instance.facility.facility_type == 'Default' or instance.facility.facility_type == 'Clinic':
            raise exceptions.NotAcceptable(
                {"detail": ["The selected facility is not a pharmacy", ]})


pre_save.connect(forward_prescription_pre_save_receiver,
                 sender=ForwardPrescription)
