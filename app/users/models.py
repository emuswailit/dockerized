import datetime
import uuid
from datetime import date, timedelta
import jwt
from django.utils.translation import gettext as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import models, transaction
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.text import slugify
from .token_generator import account_activation_token
from django.core.mail import send_mail
from django.urls import reverse
from notifications.tasks import send_verification_email


# Create your models here.


def image_upload_to(instance, filename):
    name = instance.owner.email
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


def facility_image_upload_to(instance, filename):
    name = instance.facility.title
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename






class FacilityQuerySet(models.QuerySet):
    def all_facilities(self):
        return self.all()

    def default_facility(self):
        return self.get(facility_type="Default", title="Mobipharma")

    def pharmacies(self):
        return self.filter(facility_type="Pharmacy",)

    def clinics(self):
        return self.filter(facility_type="Clinic", )


class FacilityManager(models.Manager):
    """Manager for the Facility model. Also handles the account creation"""

    def get_queryset(self):
        return FacilityQuerySet(self.model, using=self._db)

    def all_facilities(self):
        return self.get_queryset().all_facilities()

    def pharmacies(self):
        return self.get_queryset().pharmacies()

    def clinics(self):
        return self.get_queryset().clinics()

    def default_facility(self):
        return self.get_queryset().default_facility()

    @transaction.atomic
    def create_account(self,
                       facility_title,
                       facility_type,
                       facility_county,
                       facility_town,
                       facility_road,
                       facility_building,
                       facility_longitude,
                       facility_latitude,
                       facility_description,
                       email, phone, first_name, middle_name, last_name, national_id, gender, date_of_birth, password):
        """Creates a Facility along with the User and returns them both"""

        facility = Facility(
            title=facility_title,
            facility_type=facility_type,
            county=facility_county,
            town=facility_town,
            road=facility_road,
            building=facility_building,
            longitude=facility_longitude,
            latitude=facility_latitude,
            description=facility_description,


        )
        facility.save()

        user = User.objects.create_user(
            email=email,
            phone=phone,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            national_id=national_id,
            gender=gender,
            date_of_birth=date_of_birth,
            facility=facility,
            password=password,
            is_administrator=True,
            is_superintendent=True  # Set the owner as superintendent of facility
           

        )

        return facility, user


class Facility(models.Model):
    COUNTY_CHOICES = (
        ('Busia', 'Busia'),
        ('Bungoma', 'Bungoma'),
        ('Mombasa', 'Mombasa'),
        ('Nairobi', 'Nairobi'),

    )
    FACILITY_TYPES = (
        ('Default', 'Default'),
        ('Pharmacy', 'Pharmacy'),
        ('Clinic', 'Clinic'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    county = models.CharField(max_length=50, choices=COUNTY_CHOICES)
    town = models.CharField(max_length=256)
    road = models.CharField(max_length=256)
    building = models.CharField(max_length=256, null=True, blank=True)
    latitude = models.DecimalField(
        decimal_places=20, max_digits=20, null=True, blank=True)
    longitude = models.DecimalField(
        decimal_places=20, max_digits=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    paid_until = models.DateField(
        null=True,
        blank=True
    )
    is_subscribed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    trial_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = FacilityManager()

    class Meta:
        db_table = 'facilities'

    def __str__(self):
        return self.title

    def set_paid_until(self, days):
        if self.paid_until and self.paid_until > date.today():
            # Current subscription has not elapsed
            self.paid_until = self.paid_until + timedelta(days=days)
        else:
            # Current subscription has elapsed
            self.paid_until = date.today() + timedelta(days=days)

    def has_paid(
        self,
        current_date=datetime.date.today()
    ):
        if self.paid_until is None:
            self.is_subscribed=False
            return False

        return current_date < self.paid_until

    def get_is_subscribed(self):
        return self.is_subscribed


class FacilityImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """Model for uploading profile user image"""
    facility = models.ForeignKey(
        Facility, related_name="facility_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=facility_image_upload_to)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        'User', on_delete=models.CASCADE)

    def __str__(self):
        return self.facility.title

class Cadres(models.Model):
    CADRE_CLUSTERS = (
        ("ADMIN","ADMIN"),
        ("CLERICAL","CLERICAL"),
        ("CONSULTATION","CONSULTATION"),
        ("NURSING","NURSING"),
        ("OTHERS","OTHERS"),
        ("PHARMACY","PHARMACY"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20)
    cluster = models.CharField(max_length=20, choices=CADRE_CLUSTERS, default="OTHERS")
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        'User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Send email
        # if Site._meta.installed:
        #     current_site = Site.objects.get_current()
        # current_site = get_current_site(request)
        # email_subject = 'Activate Your Account'
        # message = render_to_string('activate_account.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
        #     'token': account_activation_token.make_token(user),
        # })
        # to_email = email
        # email = EmailMessage(email_subject, message, to=[to_email])
        # email.send()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    GENDER_CHOICES = (
        ('Female', 'Female'),
        ('Male', 'Male'),

    )
    ROLE_CATEGORY_CHOICES = (
        ("ADMINISTRATIVE-ASSISTANT", "ADMINISTRATIVE ASSISTANT"),
        ("HEALTH-RECORDS-OFFICER", "ADMINISTRATIVE ASSISTANT"),
        ("CLERK", "CLERK"),
        ("CLINICAL-OFFICER", "CLINICAL OFFICER"),
        ("MEDICAL-OFFICER", "MEDICAL OFFICER"),
        ("MEDICAL-CONSULTANT", "MEDICAL CONSULTANT"),
        ("NURSING-OFFICER", "NURSING OFFICER"),
        ("PHARMACEUTICAL-TECHNOLOGIST", "PHARMACEUTICAL TECHNOLOGIST"),
        ("PHARMACIST", "PHARMACIST"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(
        Facility, related_name='%(class)s', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    email = models.EmailField('email', unique=True)
    phone = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(
        max_length=120, blank=True, null=True, default="")
    last_name = models.CharField(max_length=120)
    national_id = models.CharField(max_length=30, unique=True)
    is_client = models.BooleanField(default=True)
    is_professional = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)
    is_prescriber = models.BooleanField(default=False)
    is_courier = models.BooleanField(default=False)
    is_superintendent = models.BooleanField(default=False)
    is_facility_admin = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    cadre = models.ForeignKey(Cadres, on_delete=models.CASCADE, null=True,blank=True)
    gender = models.CharField(
        max_length=120, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    verification_uuid = models.UUIDField(
        'Unique Verification UUID', default=uuid.uuid4)

    class Meta:
        db_table = 'users'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name',
                       'last_name',  'national_id', 'gender', 'date_of_birth']
    objects = CustomUserManager()

    def __str__(self):
        return f' {self.first_name } {self.last_name} - {self.phone}'

    @ property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.email

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.email

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
            Sends an email to this User.
            """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_role(self):
        """
        Retrieve user role
        """
        return self.role


class UserImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """Model for uploading profile user image"""
    owner = models.ForeignKey(
        User, related_name="user_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Account(models.Model):
    """This is an account for each client user. Dependants can then be added into the account"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    limit = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    current_balance = models.DecimalField(
        decimal_places=2, max_digits=20, default=0.00)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email



class Dependant(models.Model):
    """Dependants under a user account. This include family members and other persons under the account holder's care"""

    GENDER_CHOICES = (
        ('Female', 'Female'),
        ('Male', 'Male'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    gender = models.CharField(
        max_length=120, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    # allergy = models.ManyToManyField(Allergy)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.first_name} c/o {self.owner.first_name} {self.owner.last_name}"


# Create account for each registered user who is not staff and also add user as dependant of the account


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)
        # Send verification email

        # Send verification email
        # Send email
        # if Site._meta.installed:
        #     current_site = Site.objects.get_current()
        # current_site = get_current_site(request)
        # email_subject = 'Activate Your Account'
        # message = render_to_string('activate_account.html', {
        #     'user': instance,
        #     'domain':'http://212.22.173.231',
        #     'uid': force_text(urlsafe_base64_encode(force_bytes(instance.pk))),
        #     'token': account_activation_token.make_token(instance),
        # })
        # to_email = instance.email
        # email = EmailMessage(email_subject, message, to=[to_email])
        # email.send()


signals.post_save.connect(user_post_save, sender=User)


@receiver(post_save, sender=User, dispatch_uid="add_default_facility")
def create_offer(sender, instance, created, **kwargs):
    """Every user must be attached to a facility. Either created by sel as merchant or by default Mobipharma is created"""
    if created:
        # send_verification_email(instance.id)

        if instance.facility is None:

            if Facility.objects.filter(title="Mobipharma").count() >= 1:
                print("Default facility retrieved")
                default_facility = Facility.objects.get(title="Mobipharma")
                instance.facility = default_facility
                instance.save()
            else:
                print("Default facility not found. Will attempt creating it!")
                default_facility = Facility(
                    title="Mobipharma",
                    facility_type="Default",
                    county="Nairobi",
                    town="Nairobi",
                    road="Utalii Lane",
                    building="facility_building",
                )
                default_facility.save()
                instance.facility = default_facility
                instance.save()
                print("Default facility created")
                print(default_facility)

        # Create a user account
        account = Account.objects.create(owner=instance)
        account.save()
        dependant = Dependant.objects.create(owner=instance, first_name=instance.first_name, middle_name=instance.middle_name,
                                             last_name=instance.last_name, gender=instance.gender, date_of_birth=instance.date_of_birth, account=account)
        dependant.save()
