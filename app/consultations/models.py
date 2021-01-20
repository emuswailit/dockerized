from django.db import models
from core.models import FacilityRelatedModel
from users.models import Dependant
from drugs.models import Preparation, Product, Posology, Frequency
from django.contrib.auth import get_user_model

User = get_user_model()


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
    """Model for prescriptions raised for dependants"""

    dependant = models.ForeignKey(
        Dependant, related_name="prescription_dependant", on_delete=models.CASCADE)

    comment = models.CharField(max_length=120, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    objects = PrescriptionManager()

    def __str__(self):
        return f"Prescription for : {self.dependant.first_name} {self.dependant.last_name} c/o {self.dependant.owner.first_name} {self.dependant.owner.last_name}"

    def get_absolute_url(self):
        return self.product.get_absolute_url()


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
    duration = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('prescription', 'preparation','product')


    objects = PrescriptionManager()
    
    def __str__(self):
        return f"{self.preparation.title} - {self.product.title}"

    def get_absolute_url(self):
        return self.product.get_absolute_url()
