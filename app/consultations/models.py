from django.db import models
from core.models import FacilityRelatedModel
from users.models import Dependant
from drugs.models import Preparation, Product, Posology, Frequency
from django.contrib.auth import get_user_model
from drugs.models import Generic
from entities.models import Employees, Department
from payments.models import Payment
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from payments.models import PaymentMethods

User = get_user_model()


class Allergy(FacilityRelatedModel):

    ALLERGY_CATEGORY = (
        ("Drug Allergy", "Drug Allergy"),
        ("Food Allergy", "Food Allergy"),
        ("Environmental Allergy", "Environmental Allargy"),

    )
    """ Model for any dependant allergies.
    This is important for reporting any allergies that a dependant
    has ever exhibited on drugs, environment e.t.c"""

    title = models.TextField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    allergy_category = models.CharField(
        max_length=100, choices=ALLERGY_CATEGORY)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SlotsQuerySet(models.QuerySet):
    def all_slots(self):
        return self.all()

    def available_slots(self):
        return self.filter(is_available=True)


class SlotsManager(models.Manager):
    def get_queryset(self):
        return SlotsQuerySet(self.model, using=self._db)

    def all_slots(self):
        return self.get_queryset().all_slots()

    def available_slots(self):
        return self.get_queryset().available_slots()


class Slots(FacilityRelatedModel):
    """
    Model for appointment slots
    -Slots must be created prior by a doctor(employee)
    -Users will only see available slots and pay to reserve them
    """

    employee = models.ForeignKey(
        Employees, related_name="slot_employee", on_delete=models.CASCADE)
    start = models.DateTimeField(default=None)
    end = models.DateTimeField(default=None)
    is_available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.start} to {self.end}"

    objects = SlotsManager()


class AppointmentPayments(FacilityRelatedModel):

    """
    -Model for a appointment payment

    -Create an appointment only after this payment is saved
    """
    PAYMENT_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    )
    dependant = models.ForeignKey(
        Dependant, related_name="appointment_dependant", on_delete=models.CASCADE)
    slot = models.ForeignKey(Slots, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(
        PaymentMethods, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    narrative = models.CharField(max_length=300, null=False, blank=False)
    reference = models.CharField(
        max_length=120, null=False, blank=False)
    status = models.CharField(
        max_length=120, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    appointment_created = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.facility.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                                    'facility', 'dependant', 'slot', 'reference'], name='One payment per appointment')
        ]


class Appointments(FacilityRelatedModel):
    APPOINTMENT_STATUS_CHOICES = (
        ("SCHEDULED", "SCHEDULED"),
        ("ATTENDED", "ATTENDED"),
        ("ABSCONDED", "ABSCONDED"),
        ("RESCHEDULED", "RESCHEDULED"),
        ("CANCELLED", "CANCELLED"),
    )

    appointment_payment = models.OneToOneField(
        AppointmentPayments, related_name="appointment_slot", on_delete=models.CASCADE)
    dependant = models.ForeignKey(Dependant, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100, choices=APPOINTMENT_STATUS_CHOICES, default="PENDING")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Appointment: {self.dependant.first_name} {self.dependant.last_name} c/o {self.owner.first_name} {self.owner.last_name}"


class AppointmentConsultations(FacilityRelatedModel):

    COMPLAINT_DURATION_UNIT = (
        ("Days", "Days"),
        ("Weeks", "Weeks"),
        ("Months", "Months"),
        ("Years", "Years"),
    )
    appointment = models.OneToOneField(
        Appointments, related_name="patient_consultation_appointment", on_delete=models.CASCADE)
    current_complaint = models.TextField()
    complaint_duration_length = models.IntegerField(default=0)
    complaint_duration_unit = models.CharField(
        max_length=100, choices=COMPLAINT_DURATION_UNIT)
    location = models.CharField(max_length=100)
    onset = models.CharField(max_length=300)
    course = models.CharField(max_length=300)
    aggravating_factors = models.CharField(max_length=300)
    previous_treatment = models.CharField(max_length=300)
    current_medication = models.ManyToManyField(Generic, null=True, blank=True)

    uses_alcohol = models.BooleanField(default=False)
    uses_tobbaco = models.BooleanField(default=False)
    is_married = models.BooleanField(default=False)
    current_occupation = models.TextField()
    allergies = models.ManyToManyField(Allergy, null=True, blank=True)

    current_diagnosis = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)


class PrescriptionQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query)
                   )
    # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()


class PrescriptionManager(models.Manager):
    def get_queryset(self):
        return PrescriptionQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def featured(self):  # Prescription.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        # Prescription.objects == self.get_queryset()
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Prescription(FacilityRelatedModel):
    """
    -Model for prescriptions raised for dependants
    -Prescription can be created on creation of an appointment or deliberately
    """
    patient_consultation = models.ForeignKey(
        AppointmentConsultations, on_delete=models.CASCADE, null=True, blank=True)
    dependant = models.ForeignKey(
        Dependant, related_name="prescription_dependant", on_delete=models.CASCADE)

    comment = models.CharField(max_length=120, null=True)
    is_signed = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    objects = PrescriptionManager()

    def __str__(self):
        return f"Prescription for : {self.dependant.first_name} {self.dependant.last_name} c/o {self.dependant.owner.first_name} {self.dependant.owner.last_name}"

    def get_absolute_url(self):
        return self.product.get_absolute_url()


@receiver(post_save, sender=AppointmentConsultations)
def create_prescription_for_appointment(sender, instance, created, **kwargs):
    """
    Create a prescription for an appointment
    """
    if created:
        Prescription.objects.create(
            patient_consultation=instance,
            dependant=instance.appointment.appointment_payment.dependant,
            facility=instance.facility,
            owner=instance.owner
        )


class PrescriptionItemQuerySet(models.QuerySet):
    def all_prescription_items(self):
        return self.all()


class PrescriptionItemManager(models.Manager):
    def get_queryset(self):
        return PrescriptionItemQuerySet(self.model, using=self._db)

    def all_prescription_items(self):
        return self.get_queryset().all_prescription_items()


class PrescriptionItem(FacilityRelatedModel):
    """Model for products with different variants"""

    prescription = models.ForeignKey(
        Prescription, related_name="prescription_item_prescription", on_delete=models.CASCADE)
    preparation = models.ForeignKey(
        Preparation, related_name="prescription_item_preparation", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="prescription_item_product", on_delete=models.CASCADE)
    frequency = models.ForeignKey(
        Frequency, related_name="prescription_item_frequency", on_delete=models.CASCADE)
    posology = models.ForeignKey(
        Posology, related_name="prescription_item_posology", on_delete=models.CASCADE)
    instruction = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prescription', 'preparation', 'product')

    objects = PrescriptionItemManager()

    def __str__(self):
        return f"{self.preparation.title} - {self.product.title}"

    def get_absolute_url(self):
        return self.product.get_absolute_url()
