from django.db import models
import uuid
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from core.models import FacilityRelatedModel
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
User = get_user_model()


class Distributor(FacilityRelatedModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'drug_distributors'


class Posology(FacilityRelatedModel):

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'drug_routes'


class Frequency(FacilityRelatedModel):
    title = models.CharField(max_length=100)
    latin = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100)
    numerical = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'intake_frequencies'
        verbose_name_plural = "Intake Frequencies"


class Instruction(FacilityRelatedModel):

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

        class Meta:
            db_table = 'special_instructions'


class BodySystem(FacilityRelatedModel):

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'body_systems'

    def __str__(self):
        return self.title


class DrugClass(FacilityRelatedModel):

    system = models.ForeignKey(BodySystem, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drug_classes'
        verbose_name_plural = "Drug Classes"

    def __str__(self):
        return self.title


class DrugSubClass(FacilityRelatedModel):

    drug_class = models.ForeignKey(DrugClass, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drug_sub_classes'
        verbose_name_plural = "Drug Sub Classes"

    def __str__(self):
        return self.title


class Generic(FacilityRelatedModel):

    drug_class = models.ForeignKey(DrugClass, on_delete=models.CASCADE)
    drug_sub_class = models.ForeignKey(
        DrugSubClass, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=240, unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

        class Meta:
            db_table = 'drug_generics'
        # override save

    # def save(self,  *args, **kwargs):

    #     if self.drug_sub_class is None:
    #         default_drug_sub_class = DrugSubClass.objects.get(
    #             title="Default")  # set to default
    #         self.drug_sub_class = default_drug_sub_class

    #     super(Generic, self).save(
    #         self, *args, **kwargs)  # the 'real' save


class Formulation(FacilityRelatedModel):

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        self.title = self.title.upper()

    def __str__(self):
        return self.title

        class Meta:
            db_table = 'drug_formulations'


class Preparation(FacilityRelatedModel):

    title = models.CharField(max_length=240, unique=True)
    generic = models.ForeignKey(
        Generic, on_delete=models.CASCADE, null=True)
    formulation = models.ForeignKey(
        Formulation, on_delete=models.CASCADE)
    unit = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.formulation}"

        class Meta:
            db_table = 'drug_preparations'
            verbose_name_plural = "drug_preparations"


class Manufacturer(FacilityRelatedModel):

    title = models.CharField(max_length=100, unique=True)
    country = CountryField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'drug_manufacturers'


class ProductQuerySet(models.query.QuerySet):
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


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().filter(active=True)

    def featured(self):  # Product.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        # Product.objects == self.get_queryset()
        qs = self.get_queryset().filter(id=id, active=True)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_category(self, category_id):
        # Product.objects == self.get_queryset()
        qs = self.get_queryset().filter(category_id=category_id)
        if qs.count() > 0:
            return qs
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(FacilityRelatedModel):

    title = models.CharField(max_length=100, null=True,
                             blank=True, default="Non-proprietary Name")
    preparation = models.ForeignKey(
        Preparation, related_name="preparation", on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE)
    packaging = models.CharField(max_length=100)
    units_per_pack = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.preparation.title} - {self.title}"

        class Meta:
            db_table = 'drug_products'

    objects = ProductManager()


def product_image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return new_filename


class ProductImage(FacilityRelatedModel):
    """Model for uploading profile product image"""
    product = models.OneToOneField(
        Product, related_name="product_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_to)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title
