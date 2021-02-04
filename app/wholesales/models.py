from django.db import models
from core.models import FacilityRelatedModel
from drugs.models import Products
from django.contrib.auth import get_user_model
from utilities.models import Categories

User = get_user_model()


class Listings(FacilityRelatedModel):
    """Model for product variation, unique to each facility"""
    product = models.ForeignKey(
        Products, related_name="listing_product", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, related_name="listing_owner", on_delete=models.CASCADE)
