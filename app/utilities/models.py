from django.db import models
from core.models import FacilityRelatedModel
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class CategoriesQuerySet(models.QuerySet):
    def all_categories(self):
        return self.all()

    def drug_category(self):
        return self.get(title="Drugs")


class CategoriesManager(models.Manager):
    def get_queryset(self):
        return CategoriesQuerySet(self.model, using=self._db)

    def all_categories(self):
        return self.get_queryset().all_categories()

    def drug_category(self):
        return self.get_queryset().drug_category()


class Categories(FacilityRelatedModel):
    """Model for product variation, unique to each facility"""

    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    objects = CategoriesManager()

    def __str__(self):
        return self.title


class SubCategories(FacilityRelatedModel):
    """Model for product sub categoriesy"""
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Pricing(FacilityRelatedModel):
    """Model for product variation, unique to each facility"""
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=120, null=True)
    markup = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.00)
    other_charges = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
