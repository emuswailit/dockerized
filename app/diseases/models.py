from django.db import models
from core.models import FacilityRelatedModel
from django.contrib.auth import get_user_model


User = get_user_model()


class Diseases(FacilityRelatedModel):

    """
    Model for all diseases

    """
    title = models.TextField(max_length=100, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Notes(FacilityRelatedModel):

    """
    Model for all disease notes

    """
    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=100, unique=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SignsAndSymptoms(FacilityRelatedModel):

    """
    Disease signs and symptoms

    """
    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=120)
    description = models.TextField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Diagnosis(FacilityRelatedModel):

    """
    Model for all disease diagnosis

    """
    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=120)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class DifferentialDiagnosis(FacilityRelatedModel):

    """
    Model for all diseases

    """
    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=120)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Management(FacilityRelatedModel):

    """
    Model for all diseases

    """
    TREATMENT_CATEGORY = (
        ("Drug Management", "Drug Management"),
        ("Non-Drug Management", "Non-Drug Management"),
    )
    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)
    treatment_category = models.CharField(
        max_length=100, choices=TREATMENT_CATEGORY)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Prevention(FacilityRelatedModel):

    """
    Model for all diseases

    """
    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class DiseaseStages(FacilityRelatedModel):

    """
    Model for all diseases

    """

    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)

    title = models.TextField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class DiseaseStageCategories(FacilityRelatedModel):

    """
    Model for all diseases

    """

    disease_stage = models.ForeignKey(
        DiseaseStages, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Sources(FacilityRelatedModel):

    """
    Model for all disease reference sources

    """

    disease = models.ForeignKey(
        Diseases, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
