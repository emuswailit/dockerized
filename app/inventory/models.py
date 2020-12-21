from django.db.models import signals
from django.dispatch import receiver
from django.db import models
from users.models import Facility
from drugs.models import Product
from core.models import FacilityRelatedModel
from drugs.models import Distributor
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from .utils import unique_slug_generator
from django.utils.text import slugify
import decimal

User = get_user_model()

# Create your models here.


def variation_image_upload_to(instance, filename):
    title = instance.variation.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s.%s" % (slug,file_extension)
    return new_filename


class VariationQuerySet(models.query.QuerySet):
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


class VariationManager(models.Manager):
    def get_queryset(self):
        return VariationQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def featured(self):  # Variation.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        # Variation.objects == self.get_queryset()
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Variation(FacilityRelatedModel):
    """Model for products with different variants"""

    product = models.ForeignKey(
        Product, related_name="product_variation", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=120, null=True)
    is_active = models.BooleanField(default=True)
    is_drug = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    objects = VariationManager()

    class Meta:

        unique_together = (
            ('product', 'title'),
        )

    def __str__(self):
        return f"{self.title} {self.product.title}"

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


# TODO : When a product is deactivated all variations should be deactivated too
# A product variation with inventory greater than one cannot be activated

# TODO update variation inventory upon release to outlets


class VariationPhoto(FacilityRelatedModel):
    """Model for uploading profile product image"""
    variation = models.ForeignKey(
        Variation, related_name="variation_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=variation_image_upload_to)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.variation.title


class VariationReceipt(FacilityRelatedModel):
    distributor = models.ForeignKey(
        Distributor, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.CharField(max_length=50, null=True,
                             blank=True, editable=True)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    units_per_pack = models.IntegerField(default=0)
    pack_quantity = models.IntegerField(default=0)
    pack_buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    pack_selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    unit_quantity = models.IntegerField(default=0)
    unit_buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    unit_selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    description = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.variation.title}"


def variation_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if instance.product:
        instance.is_drug = True
        instance.title = f"{instance.product.preparation.title} - {instance.product.title}"


pre_save.connect(variation_pre_save_receiver, sender=Variation)


@receiver(post_save, sender=Variation, dispatch_uid="set_product_title")
def create_offer(sender, instance, created, **kwargs):
    """Set the final title for product either to custom entered title or to produc preparation title"""
    if created:
        instance.unit_quantity = instance.units_per_pack * instance.pack_quantity
        instance.unit_buying_price = instance.pack_buying_price / instance.units_per_pack
        instance.unit_selling_price = instance.pack_selling_price / instance.units_per_pack
        instance.variation.quantity = instance.variation.quantity + instance.unit_quantity
        instance.save()


@receiver(post_save, sender=VariationReceipt, dispatch_uid="variation_receipt_calculations")
def create_offer(sender, instance, created, **kwargs):
    """Calculate unit quantities and prices"""
    if created:
        try:
            instance.unit_quantity = instance.units_per_pack * instance.pack_quantity
            instance.unit_buying_price = instance.pack_buying_price / \
                decimal.Decimal(instance.units_per_pack)
            instance.unit_selling_price = instance.pack_selling_price / \
                decimal.Decimal(instance.units_per_pack)
            instance.variation.quantity = instance.variation.quantity + instance.unit_quantity
            instance.save()
            instance.variation.save()
        except decimal.DecimalException as e:

            print(e)
