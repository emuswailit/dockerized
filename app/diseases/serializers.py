from rest_framework import serializers
from . import models


class DiseaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Diseases
        fields = ('id', 'url', 'facility', 'title',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class NotesSerializer(serializers.ModelSerializer):
    disease = serializers.PrimaryKeyRelatedField(
        queryset=models.Diseases.objects.all(),
        many=False)

    class Meta:
        model = models.Notes
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class SignsAndSymptomsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """

    class Meta:
        model = models.SignsAndSymptoms
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class DiagnosisSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """

    class Meta:
        model = models.Diagnosis
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class DifferentialDiagnosisSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """

    class Meta:
        model = models.DifferentialDiagnosis
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class ManagementSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """

    class Meta:
        model = models.Management
        fields = ('id', 'url', 'facility', 'disease', 'treatment_category', 'drug', 'description', 'title',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class PreventionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Prevention model serializer
    """

    class Meta:
        model = models.Prevention
        fields = ('id', 'url', 'facility', 'disease', 'title', 'description',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class DiseaseStagesSerializer(serializers.HyperlinkedModelSerializer):
    """
    DiseaseStages model serializer
    """

    class Meta:
        model = models.DiseaseStages
        fields = ('id', 'url', 'facility', 'disease', 'title', 'description',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class DiseaseStageCategoriesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Disease Stage Categories model serializer
    """

    class Meta:
        model = models.DiseaseStageCategories
        fields = ('id', 'url', 'facility', 'disease_stage', 'title', 'description',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )


class SourcesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Sources model serializer
    """

    class Meta:
        model = models.Sources
        fields = ('id', 'url', 'facility', 'disease', 'title', 'description',
                  'description', 'owner')
        read_only_fields = (
            'owner', 'facility',
        )
