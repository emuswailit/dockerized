from django.contrib.auth import get_user_model
from django.db import models
import uuid
from core.models import FacilityRelatedModel
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

User = get_user_model()


def courier_photo_upload_to(instance, filename):
    name = instance.courier.owner.email
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


def pharmacist_photo_upload_to(instance, filename):
    name = instance.owner.email
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


def courier_photo_upload_to(instance, filename):
    name = instance.courier.owner.email
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


def courier_licence_upload_to(instance, filename):
    name = instance.owner.email
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


def prescriber_photo_upload_to(instance, filename):
    name = instance.prescriber.owner.email
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


def certificate_upload_to(instance, filename):
    email = instance.owner.email
    slug = slugify(email)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


class PharmacistQuerySet(models.QuerySet):
    def all_pharmacists(self):
        return self.all()
    def available_pharmacists(self):
        return self.filter(is_available=True) 

class PharmacistManager(models.Manager):
    def get_queryset(self):
        return PharmacistQuerySet(self.model, using=self._db)
    def all_pharmacists(self):
        return self.get_queryset().all_pharmacists()
    def available_pharmacists(self):
        return self.get_queryset().available_pharmacists()

class Pharmacist(FacilityRelatedModel):

    PHARMACY_CADRES = (
        ('PharmTech', 'Pharmaceutical Technologist'),
        ('Pharmacist', 'Pharmacist'),

    )
    cadre = models.CharField(
        max_length=30, choices=PHARMACY_CADRES, blank=False, null=False)
    board_number = models.CharField(max_length=30,)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    certificate = models.FileField(upload_to=certificate_upload_to)
    owner = models.OneToOneField(
        User, related_name="pharmacist_owner", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    objects= PharmacistManager()
    def __str__(self):
        return f"{self.owner.first_name} {self.owner.middle_name}  {self.owner.last_name}"


class PharmacistPhoto(FacilityRelatedModel):
    """Model for uploading pharmacist photo"""
    pharmacist = models.ForeignKey(
        Pharmacist, related_name="courier_certificate", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=pharmacist_photo_upload_to)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email


class Prescriber(FacilityRelatedModel):

    PRESCRIBER_CADRES = (
        ('ClinicalOfficer', 'Clinical Officer'),
        ('Doctor', 'Doctor'),
    )
    SALUTATIONS = (
        ('Dr', 'Doctor'),
        ('Mr', 'Mr'),
        ('Prof.', 'Professor'),
    )
    salutation = models.CharField(
        max_length=30, choices=SALUTATIONS, null=True, blank=True)
    cadre = models.CharField(max_length=30, choices=PRESCRIBER_CADRES)
    board_number = models.CharField(max_length=30,)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    certificate = models.FileField(upload_to=certificate_upload_to)
    owner = models.OneToOneField(
        User, related_name="prescriber_owner", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.owner.email


class PrescriberPhoto(FacilityRelatedModel):
    """Model for uploading pharmacist photo"""

    prescriber = models.ForeignKey(
        Prescriber, related_name="courier_certificate", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=prescriber_photo_upload_to)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email


class Courier(FacilityRelatedModel):
    VEHICLE_TYPE = (
        ('MotorCycle', 'Motor Cycle'),
        ('SaloonCar', 'Saloon Car'),

    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle = models.CharField(max_length=30, choices=VEHICLE_TYPE)
    vehicle_number = models.CharField(max_length=30,)
    licence = models.FileField(upload_to=courier_licence_upload_to)
    permit_number = models.CharField(max_length=30,)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.owner.email


class CourierPhoto(FacilityRelatedModel):
    """Model for uploading courier certificate"""
    courier = models.ForeignKey(
        Courier, related_name="courier_certificate", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=courier_photo_upload_to)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email

class FacilityPharmacistQuerySet(models.QuerySet):
    def all_facility_pharmacists(self):
        return self.all()
    def active_facility_pharmacists(self):
        return self.filter(is_active=True) 

class FacilityPharmacistManager(models.Manager):
    def get_queryset(self):
        return FacilityPharmacistQuerySet(self.model, using=self._db)
    def active_facility_pharmacists(self):
        return self.get_queryset().active_facility_pharmacists()
    def all_facility_pharmacists(self):
        return self.get_queryset().all_facility_pharmacists()


class FacilityPharmacist(FacilityRelatedModel):
    is_active = models.BooleanField(default=True)
    is_superintendent = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    pharmacist = models.ForeignKey(
        Pharmacist, related_name='facility_pharmacist', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, related_name='facility_pharmacist_owner', on_delete=models.CASCADE)

    objects=FacilityPharmacistManager()

    class Meta:
        db_table = 'pharmacists_for_facility'
        ordering = ['created']

    def __str__(self):
        return self.pharmacist.owner.email

    def activate_facility_pharmacist(self):
        "Activates a facility pharmacist"
        if (self.is_active==False):
            self.is_active=True
            self.save();
            return self

    def deactivate_facility_pharmacist(self):
        "Deactivates a facility pharmacist"
        if (self.is_active):
            self.is_active=False
            self.save();
            return self


class FacilityPrescriber(FacilityRelatedModel):
    is_active = models.BooleanField(default=True)
    is_superintendent = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    prescriber = models.ForeignKey(
        Prescriber, related_name='facility_prescriber', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, related_name='facility_prescriber_owner', on_delete=models.CASCADE)

    class Meta:
        db_table = 'prescribers_for_facility'
        ordering = ['created']

    def __str__(self):
        return self.prescriber.owner.email


class FacilityCourier(FacilityRelatedModel):
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    courier = models.ForeignKey(
        Courier, related_name='facility_courier', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, related_name='facility_courier_owner', on_delete=models.CASCADE)

    class Meta:
        db_table = 'couriers_for_facility'
        ordering = ['created']

    def __str__(self):
        return self.courier.owner.email

