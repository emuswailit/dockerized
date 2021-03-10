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
    disease_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Notes
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner', 'disease_details', )
        read_only_fields = (
            'owner', 'facility',
        )

    def get_disease_details(self, obj):
        disease = models.Diseases.objects.get(id=obj.disease.id)
        return DiseaseSerializer(disease, context=self.context).data


class SymptomsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """
    disease = serializers.PrimaryKeyRelatedField(
        queryset=models.Diseases.objects.all(),
        many=False)
    disease_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Symptoms
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner', 'disease_details')
        read_only_fields = (
            'owner', 'facility',
        )

    def get_disease_details(self, obj):
        disease = models.Diseases.objects.get(id=obj.disease.id)
        return DiseaseSerializer(disease, context=self.context).data


class DiagnosisSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """
    disease = serializers.PrimaryKeyRelatedField(
        queryset=models.Diseases.objects.all(),
        many=False)
    disease_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Diagnosis
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner', 'disease_details')
        read_only_fields = (
            'owner', 'facility',
        )

    def get_disease_details(self, obj):
        disease = models.Diseases.objects.get(id=obj.disease.id)
        return DiseaseSerializer(disease, context=self.context).data


class DifferentialDiagnosisSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """
    disease = serializers.PrimaryKeyRelatedField(
        queryset=models.Diseases.objects.all(),
        many=False)
    disease_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.DifferentialDiagnosis
        fields = ('id', 'url', 'disease', 'facility', 'title',
                  'description', 'owner', 'disease_details')
        read_only_fields = (
            'owner', 'facility',
        )

    def get_disease_details(self, obj):
        disease = models.Diseases.objects.get(id=obj.disease.id)
        return DiseaseSerializer(disease, context=self.context).data


class ManagementSerializer(serializers.HyperlinkedModelSerializer):
    """
    Signs and symptoms model
    """
    disease = serializers.PrimaryKeyRelatedField(
        queryset=models.Diseases.objects.all(),
        many=False)
    disease_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Management
        fields = ('id', 'url', 'facility', 'disease', 'treatment_category', 'description', 'title',
                  'description', 'owner', 'disease_details')
        read_only_fields = (
            'owner', 'facility',
        )

    def get_disease_details(self, obj):
        disease = models.Diseases.objects.get(id=obj.disease.id)
        return DiseaseSerializer(disease, context=self.context).data


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
