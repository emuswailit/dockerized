from django.contrib.auth import get_user_model
from django.db import models
import uuid
from core.models import FacilityRelatedModel
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from users.models import Facility, Cadres

from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()

# class Professions(FacilityRelatedModel):

#     """
#     Model for all facility sjob roles
#     They are created by the facility administrator
#     """
#     title = models.CharField(max_length=100)
#     description = models.CharField(max_length=300)
#     regulator = models.CharField(max_length=100)
#     professional_role = models.ForeignKey(Cadres, on_delete=models.CASCADE,null=True,blank=True)
#     is_active = models.BooleanField(default=True)
#     created = models.DateField(auto_now_add=True)
#     updated = models.DateField(auto_now=True)
#     owner = models.ForeignKey(
#         User, related_name='profession_owner', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title


def professional_certificate_upload_to(instance, filename):
    email = instance.owner.email
    slug = slugify(email)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


def professional_licence_upload_to(instance, filename):
    email = instance.owner.email
    slug = slugify(email)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


class ProfessionalsQuerySet(models.QuerySet):
    def all_professionals(self):
        return self.all()

    def active_professionals(self):
        return self.filter(is_active=True)

    def available_professionals(self):
        return self.filter(is_available=True)


class ProfessionalsManager(models.Manager):
    def get_queryset(self):
        return ProfessionalsQuerySet(self.model, using=self._db)

    def all_professionals(self):
        return self.get_queryset().all_professionals()

    def active_professionals(self):
        return self.get_queryset().active_professionals()

    def available_professionals(self):
        return self.get_queryset().available_professionals()


class Professionals(FacilityRelatedModel):
    cadre = models.ForeignKey(
        Cadres, related_name="professionals_professions", on_delete=models.CASCADE)
    user = models.OneToOneField(
        User, related_name='professional_user', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    certificate = models.FileField(
        upload_to=professional_certificate_upload_to)
    national_id = models.FileField(upload_to=professional_licence_upload_to)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name='professional_owner', on_delete=models.CASCADE)

    objects = ProfessionalsManager()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.cadre.title}"


def professional_annual_licence_upload_to(instance, filename):
    email = instance.owner.email
    slug = slugify(email)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


class ProfessionalAnnualLicence(FacilityRelatedModel):

    """Model for uploading profile user image"""
    professional = models.ForeignKey(
        Professionals, related_name="professional_annual_licence_professional", on_delete=models.CASCADE)
    annual_licence = models.ImageField(
        upload_to=professional_annual_licence_upload_to)
    expires_on = models.DateField()
    is_current = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.user.email})"



def courier_licence_upload_to(instance, filename):
    name = instance.owner.email
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


class DepartmentQuerySet(models.QuerySet):
    def all_departments(self):
        return self.all()

    def active_departments(self):
        return self.filter(is_active=True)

    def active_departments(self):
        return self.filter(is_active=True)

    def open_monday(self):
        return self.filter(open_monday=True, is_active=True)

    def open_tuesday(self):
        return self.filter(open_tuesday=True, is_active=True)

    def open_wednesday(self):
        return self.filter(open_wednesday=True, is_active=True)

    def open_thursday(self):
        return self.filter(open_thursday=True, is_active=True)

    def open_friday(self):
        return self.filter(open_friday=True, is_active=True)

    def open_saturday(self):
        return self.filter(open_saturdays=True, is_active=True)

    def open_sunday(self):
        return self.filter(open_sunday=True, is_active=True)


class DepartmentManager(models.Manager):
    def get_queryset(self):
        return DepartmentQuerySet(self.model, using=self._db)

    def all_departments(self):
        return self.get_queryset().all_departments()

    def active_departments(self):
        return self.get_queryset().active_departments()

    def open_monday(self):
        return self.get_queryset().open_monday()

    def open_tuesday(self):
        return self.get_queryset().open_tuesday()

    def open_wednesday(self):
        return self.get_queryset().open_wednesday()

    def open_thursday(self):
        return self.get_queryset().open_thursday()

    def open_friday(self):
        return self.get_queryset().open_friday()

    def open_saturday(self):
        return self.get_queryset().open_saturday()

    def open_sunday(self):
        return self.get_queryset().open_sunday()


class Department(FacilityRelatedModel):
    """
    Model for facility departments

    """
    title = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=300, null=True)
    is_active = models.BooleanField(default=False)
    open_monday = models.BooleanField(default=False)
    open_tuesday = models.BooleanField(default=False)
    open_wednesday = models.BooleanField(default=False)
    open_thursday = models.BooleanField(default=False)
    open_friday = models.BooleanField(default=False)
    open_saturday = models.BooleanField(default=False)
    open_sunday = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, related_name="department_owner", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    objects = DepartmentManager()

    def __str__(self):
        return self.title


class Employees(FacilityRelatedModel):
    """
    Model for all facility employee such as clerks and secretaries to doctors. 
    They manage administrative services in the facility such as appointments, records, etc.

    They are created by the facility administrator
    """
    professional = models.OneToOneField(
        Professionals, related_name="employee_professional", on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, related_name="employee_department", on_delete=models.CASCADE, null=True,blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superintendent = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name='facility_admin_owner', on_delete=models.CASCADE)
#  Employee can only be employed once in a facility

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                                    'facility', 'professional'], name='Professional can only be employed once in a facility')
        ]


class Salary(FacilityRelatedModel):
    """
    Model for employee salary
    """
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(
        max_digits=9, default=0.00, decimal_places=2)
    house_allowance = models.DecimalField(
        max_digits=9, default=0.00, decimal_places=2)
    risk_allowance = models.DecimalField(
        max_digits=9, default=0.00, decimal_places=2)
    uniform_allowance = models.DecimalField(
        max_digits=9, default=0.00, decimal_places=2)
    owner = models.ForeignKey(
        User, related_name='salary_owner', on_delete=models.CASCADE)

    def get_total_earnings(self):
        return self.basic_salary + self.house_allowance + self.risk_allowance+self.uniform_allowance

# Create a salary immediately an employee is created


@receiver(post_save, sender=Employees)
def create_employee_salary(sender, instance, created, **kwargs):
    if created:
        Salary.objects.create(facility=instance.facility,
                              employee=instance, owner=instance.owner)


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

    objects = PharmacistManager()

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.middle_name}  {self.owner.last_name}"


class PrescriberQuerySet(models.QuerySet):
    def all_prescribers(self):
        return self.all()

    def available_prescribers(self):
        return self.filter(is_available=True)


class PrescriberManager(models.Manager):
    def get_queryset(self):
        return PrescriberQuerySet(self.model, using=self._db)

    def all_prescribers(self):
        return self.get_queryset().all_prescribers()

    def available_prescribers(self):
        return self.get_queryset().available_prescribers()


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

    objects = PrescriberManager()

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

    objects = FacilityPharmacistManager()

    class Meta:
        db_table = 'pharmacists_for_facility'
        ordering = ['created']
        unique_together = ('facility', 'pharmacist')

    def __str__(self):
        return self.pharmacist.owner.email

    def activate_facility_pharmacist(self):
        "Activates a facility pharmacist"
        if (self.is_active == False):
            self.is_active = True
            self.save()
            return self

    def deactivate_facility_pharmacist(self):
        "Deactivates a facility pharmacist"
        if (self.is_active):
            self.is_active = False
            self.save()
            return self


class FacilityPrescriberQuerySet(models.QuerySet):
    def all_facility_prescribers(self):
        return self.all()

    def active_facility_prescribers(self):
        return self.filter(is_active=True)


class FacilityPrescriberManager(models.Manager):
    def get_queryset(self):
        return FacilityPrescriberQuerySet(self.model, using=self._db)

    def active_facility_prescribers(self):
        return self.get_queryset().active_facility_prescribers()

    def all_facility_prescribers(self):
        return self.get_queryset().all_facility_prescribers()


# class FacilityPrescriber(FacilityRelatedModel):
#     is_active = models.BooleanField(default=True)
#     is_superintendent = models.BooleanField(default=False)
#     created = models.DateField(auto_now_add=True)
#     updated = models.DateField(auto_now=True)
#     prescriber = models.ForeignKey(
#         Prescriber, related_name='facility_prescriber', on_delete=models.CASCADE)
#     # department = models.ForeignKey(
#     #     Department, related_name='facility_prescriber_clinic', on_delete=models.CASCADE, null=True, blank=True)
#     owner = models.ForeignKey(
#         User, related_name='facility_prescriber_owner', on_delete=models.CASCADE)

#     objects = FacilityPrescriberManager()

#     def __str__(self):
#         return self.prescriber.owner.email


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
