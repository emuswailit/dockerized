from django_countries.fields import CountryField as ModelCountryField
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from . import models
from django_countries.fields import Country
from users.serializers import UserSerializer
User = get_user_model()


class DistributorSerializer(serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Distributor
        fields = ('id', 'url', 'title', 'phone', 'email', 'description', 'owner',
                  'created', 'updated', )

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner',



                            )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data


class BodySystemSerializer(serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.BodySystem
        fields = ('id', 'url', 'title', 'description', 'owner',
                  'created', 'updated', )

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner',


                            )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data


class InstructionSerializer(serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Instruction
        fields = ('id', 'url', 'title', 'description', 'owner',
                  'created', 'updated', )

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner',

                            )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data


class PosologySerializer(serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Posology
        fields = ('id', 'url', 'title', 'description', 'owner',
                  'created', 'updated', )

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner', )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = "__all__"
        read_only_fields = (
            'product', 'created_by'
        )

class FrequencySerializer(serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Frequency
        fields = ('id', 'url', 'title', 'abbreviation', 'latin', 'numerical', 'description', 'owner',
                  'created', 'updated', )

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner', )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data


class DrugClassSerializer(serializers.ModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)
    system_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.DrugClass
        fields = ('id', 'url', 'title', 'description', 'system', 'owner',
                  'created', 'updated',  'system_details')

        read_only_fields = ('id', 'url', 'created', 'system'
                            'updated', 'owner',  'system_details')

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data

    def get_system_details(self, obj):
        system = models.BodySystem.objects.get(id=obj.system.id)
        return BodySystemSerializer(system, context=self.context).data


class DrugSubClassSerializer(serializers.ModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)
    drug_class_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.DrugSubClass
        fields = ('id', 'url', 'title', 'description', 'drug_class', 'owner',
                  'created', 'updated', 'drug_class_details', )

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner', )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data

    def get_drug_class_details(self, obj):
        drug_class = models.DrugClass.objects.get(id=obj.drug_class.id)
        return DrugClassSerializer(drug_class, context=self.context).data


class GenericSerializer(serializers.ModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)
    drug_class_details = serializers.SerializerMethodField(read_only=True)
    drug_sub_class_details = serializers.SerializerMethodField(read_only=True)

    # Implement a case sensitive check for uniqueness
    title = serializers.CharField(
        max_length=240,
        validators=[
            UniqueValidator(
                queryset=models.Generic.objects.all(), lookup='iexact'

            )]
    )

    
    class Meta:
        model = models.Generic
        extra_kwargs = {'response_message': "Request successful"}
        fields = ('id', 'url', 'title', 'description', 'drug_class', 'drug_sub_class', 'drug_class_details', 'drug_sub_class_details',  'owner',
                  'created', 'updated',)

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner', )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data

    def get_drug_class_details(self, obj):
        drug_class = models.DrugClass.objects.get(id=obj.drug_class.id)
        return DrugClassSerializer(drug_class, context=self.context).data

    def get_drug_sub_class_details(self, obj):
        if obj.drug_sub_class:
            drug_sub_class = models.DrugSubClass.objects.get(
                id=obj.drug_sub_class.id)
            return DrugSubClassSerializer(drug_sub_class, context=self.context).data


class FormulationSerializer(serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    # Implement a case sensitive check for uniqueness
    title = serializers.CharField(
        max_length=240,
        validators=[
            UniqueValidator(
                queryset=models.Formulation.objects.all(), lookup='iexact'

            )]
    )

    class Meta:
        model = models.Formulation
        fields = ('id', 'url', 'title', 'description',  'owner',
                  'created', 'updated',)

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner', )

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data


class PreparationSerializer(serializers.ModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)
    generic_details = serializers.SerializerMethodField(read_only=True)
    formulation_details = serializers.SerializerMethodField(read_only=True)
    # Implement a case sensitive check for uniqueness
    title = serializers.CharField(
        max_length=240,
        validators=[
            UniqueValidator(
                queryset=models.Preparation.objects.all(), lookup='iexact'

            )]
    )

    class Meta:
        model = models.Preparation
        fields = (
            'id',
            'url',
            'generic',
            'title',
            'formulation',
            'unit',
            'description',

            'formulation_details', 'generic_details'
        )
        read_only_fields = ('owner',)

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data

    def get_generic_details(self, obj):
        generic = models.Generic.objects.get(id=obj.generic.id)
        return GenericSerializer(generic, context=self.context).data

    def get_formulation_details(self, obj):
        formulation = models.Formulation.objects.get(id=obj.formulation.id)
        return FormulationSerializer(formulation, context=self.context).data


class CountrySerializer(serializers.Serializer):
    model = Country


class CustomCountryMixin(CountryFieldMixin):
    """Custom mixin to serialize country with name instead of country code"""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in instance._meta.fields:
            if field.__class__ == ModelCountryField:
                if getattr(instance, field.name).name:
                    data[field.name] = getattr(instance, field.name).name
        return data


class ManufacturerSerializer(CustomCountryMixin, serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Manufacturer
        fields = ('id', 'url', 'title', 'country', 'owner',
                  )

        read_only_fields = ('id', 'url',  'owner',)

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data


# DISPLAY SERIALIZERS


class DistributorDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Distributor
        fields = (
            'title', 'phone', 'email',
        )


class BodySystemDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BodySystem
        fields = (
            'title', 'description',
        )


class PosologyDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Posology
        fields = (
            'title', 'description',
        )


class FrequencyDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Frequency
        fields = (
            'title', 'numerical', 'description'
        )


class GenericDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Generic
        fields = (
            'title', 'description'
        )


class FormulationDisplaySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Formulation
        fields = (
            'title', 'description'
        )


class PreparationDisplaySerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.SerializerMethodField(read_only=True)
    formulation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Preparation
        fields = (
            'item',
            'title',
            'formulation',
            'unit',
            'description',
        )

    def get_item(self, object):
        return GenericDisplaySerializer(object.item, context=self.context).data

    def get_formulation(self, object):
        return FormulationDisplaySerializer(object.formulation, context=self.context).data


class ManufacturerDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ('id', 'url',
                  'title', 'country',
                  )


class ProductSerializer(serializers.ModelSerializer):

    # owner_details = serializers.SerializerMethodField(read_only=True)
    preparation_details = serializers.SerializerMethodField(read_only=True)
    manufacturer_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Product
        fields = ('id', 'url', 'title', 'preparation', 'manufacturer',
                  'description', 'owner', 'units_per_pack', 'preparation_details', 'manufacturer_details', 'active', 'created', 'updated')

        read_only_fields = ('id', 'url',
                            'owner',

                            'active',
                            'created',
                            'updated')

    # def get_owner_details(self, obj):
    #     owner = User.objects.get(id=obj.owner.id)
    #     return UserSerializer(owner, context=self.context).data

    def get_preparation_details(self, obj):
        preparation = models.Preparation.objects.get(id=obj.preparation.id)
        return PreparationSerializer(preparation, context=self.context).data

    def get_manufacturer_details(self, obj):
        manufacturer = models.Manufacturer.objects.get(id=obj.manufacturer.id)
        return ManufacturerSerializer(manufacturer, context=self.context).data
