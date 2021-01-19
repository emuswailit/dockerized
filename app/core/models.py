import uuid
from django.db import models


class FacilityRelatedModel(models.Model):
    """Abstract class used by models that belong to a Company"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(
        'users.Facility', related_name='%(class)s', on_delete=models.CASCADE, editable=True)

    class Meta:
        abstract = True
