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
    owner = models.OneToOneField(
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
    description = models.CharField(max_length=300, null=True, blank=True)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                                    'facility', 'title'], name='Unique department title in each facility')
        ]

    def __str__(self):
        return self.title


class DepartmentalCharges(FacilityRelatedModel):

    """
    Model for all clinic charges where consultation fee and other charges can be set
    """
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    consultation_fee = models.DecimalField(
        max_digits=9, default=0.00, decimal_places=2)
    other_charges = models.DecimalField(
        max_digits=9, default=0.00, decimal_places=2)

    owner = models.ForeignKey(
        User, related_name='departmental_charges_owner', on_delete=models.CASCADE)

    def get_total_departmental_charges(self):
        return self.consultation_fee + self.other_charges

# Create a departmental charges model immediately a department is created


@receiver(post_save, sender=Department)
def create_departmental_charges(sender, instance, created, **kwargs):
    if created:
        DepartmentalCharges.objects.create(facility=instance.facility,
                                           department=instance, owner=instance.owner)


class JobsQuerySet(models.QuerySet):
    def all_jobs(self):
        return self.all()

    def active_jobs(self):
        return self.filter(is_active=True)

    def vacant_jobs(self):
        return self.filter(is_vacant=True)

    def advertised_jobs(self):
        return self.filter(is_advertised=True)


class JobsManager(models.Manager):
    def get_queryset(self):
        return JobsQuerySet(self.model, using=self._db)

    def all_jobs(self):
        return self.get_queryset().all_jobs()

    def active_jobs(self):
        return self.get_queryset().active_jobs()

    def advertised_jobs(self):
        return self.get_queryset().advertised_jobs()


class Jobs(FacilityRelatedModel):
    """
    -Model for where facility defines its established job designations/vacancies
    -Ensures that employees are added based on established positions
    -Positions are created by the administrator 
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True, blank=True)
    cadre = models.ForeignKey(
        Cadres, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_advertised = models.BooleanField(default=False)
    maximum_positions = models.IntegerField(default=0)
    filled_positions = models.IntegerField(default=0)
    advertised_positions = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name='profession_owner', on_delete=models.CASCADE)

    def vacant_positions(self):
        return self.maximum_positions - self.filled_positions()

    objects = JobsManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                                    'facility', 'title'], name='Title to be unique per facility')
        ]

    def __str__(self):
        return self.title


class Employees(FacilityRelatedModel):
    """
    Model for all facility employees 

    They are created by the facility administrator or superintendent
    """

    department = models.ForeignKey(
        Department, related_name="employee_department", on_delete=models.CASCADE)
    professional = models.ForeignKey(
        Professionals, related_name="employee_professional", on_delete=models.CASCADE)
    job = models.ForeignKey(
        Jobs, related_name="employee_designation", on_delete=models.CASCADE)
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

    def __str__(self):
        return f"{self.professional.user.first_name}  {self.professional.user.last_name} - {self.professional.user.facility.title}"


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
