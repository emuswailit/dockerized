from django.contrib.auth import get_user_model
from django_countries.fields import Country
from django_countries.fields import CountryField as ModelCountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from utilities.models import Categories
from utilities.serializers import CategorySerializer
from diseases.serializers import DiseaseSerializer
from diseases.models import Diseases

from . import models

User = get_user_model()


class DistributorSerializer(serializers.HyperlinkedModelSerializer):
    # owner_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Distributor
        fields = ('id', 'url', 'title', 'physical_address',
                  'postal_address', 'phone1', 'phone2', 'phone3', 'email',
                  'website', 'description', 'owner',
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
                            'updated', 'owner', 'category', 'is_active'


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
        model = models.ProductImages
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
        fields = ('id', 'url', 'title', 'description', 'drug_class', 'drug_sub_class', 'drug_class_details',
                  'drug_sub_class_details',  'owner',
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
        fields = ('id', 'url', 'title', 'country', 'owner', 'email', 'website',
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
        fields = ('id', 'url', 'website', 'distributors',
                  'title', 'country',
                  )


class ProductsSerializer(serializers.ModelSerializer):

    category_details = serializers.SerializerMethodField(read_only=True)
    preparation_details = serializers.SerializerMethodField(read_only=True)
    manufacturer_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Products
        fields = ('id', 'url', 'title', 'preparation', 'category', 'manufacturer',
                  'is_prescription_only',
                  'description', 'packaging', 'units_per_pack', 'owner', 'units_per_pack',
                  'manufacturer_details', 'active', 'created', 'updated', 'preparation_details', 'category_details')

        read_only_fields = ('id', 'url',
                            'owner',

                            'active',
                            'created',
                            'updated')

    def get_category_details(self, obj):
        category = Categories.objects.get(id=obj.category.id)
        return CategorySerializer(category, context=self.context).data

    def get_preparation_details(self, obj):
        if obj.preparation:
            preparation = models.Preparation.objects.get(id=obj.preparation.id)
            return PreparationSerializer(preparation, context=self.context).data
        else:
            return None

    def get_manufacturer_details(self, obj):
        if obj.manufacturer:
            if models.Manufacturer.objects.filter(id=obj.manufacturer.id).exists():
                manufacturer = models.Manufacturer.objects.get(
                    id=obj.manufacturer.id)
                return ManufacturerSerializer(manufacturer, context=self.context).data

        else:
            return None

    def create(self, validated_data):
        title = validated_data.pop('title')
        preparation = validated_data.pop('preparation')

        if not title:
            raise serializers.ValidationError(
                "Enter unique product title ")

        category = validated_data.pop('category')
        manufacturer = validated_data.pop('manufacturer')

        if preparation:
            title = preparation.title

            if not manufacturer:
                raise serializers.ValidationError(
                    f"Manufacturer is required  {category.title}")
            else:
                category = Categories.objects.drug_category()

        product = models.Products.objects.create(
            preparation=preparation, title=title, category=category, manufacturer=manufacturer, **validated_data)

        return product


class IndicationsSerializer(serializers.ModelSerializer):
    generic_details = serializers.SerializerMethodField(read_only=True)

    disease_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Indications
        fields = ('id', 'url', 'facility', 'disease', 'generic', 'dose', 'description', 'owner',
                  'created', 'updated', 'generic_details', 'disease_details'
                  )

        read_only_fields = ('id', 'url', 'facility',  'owner',)

    def get_generic_details(self, obj):
        generic = models.Generic.objects.get(id=obj.generic.id)
        return GenericSerializer(generic, context=self.context).data

    def get_disease_details(self, obj):
        disease = Diseases.objects.get(id=obj.disease.id)
        return DiseaseSerializer(disease, context=self.context).data


# class DosesSerializer(serializers.HyperlinkedModelSerializer):
#     # owner_details = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = models.Doses
#         fields = ('id', 'url', 'facility', 'generic', 'indication', 'route', 'dose', 'owner',  'created', 'updated'
#                   )

#         read_only_fields = ('id', 'url', 'facility',  'owner',)


class ModeOfActionsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ModeOfActions
        fields = ('id', 'url', 'facility', 'generic', 'mode_of_action',  'created', 'updated'
                  )

        read_only_fields = ('id', 'url', 'facility',  'owner',)


class ContraindicationsSerializer(serializers.HyperlinkedModelSerializer):
    generic_details = serializers.SerializerMethodField(read_only=True)
    generic = serializers.PrimaryKeyRelatedField(
        queryset=models.Generic.objects.all(),
        many=False)

    class Meta:
        model = models.Contraindications
        fields = ('id', 'url', 'facility', 'generic', 'title', 'description', 'created', 'updated',
                  'generic_details'
                  )

        read_only_fields = ('id', 'url', 'facility',  'owner',)

    def get_generic_details(self, obj):
        generic = models.Generic.objects.get(id=obj.generic.id)
        return GenericSerializer(generic, context=self.context).data


class InteractionsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Interactions
        fields = ('id', 'url', 'facility', 'generic', 'contra_indicated', 'description', 'created', 'updated'
                  )

        read_only_fields = ('id', 'url', 'facility',  'owner',)


class SideEffectsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.SideEffects
        fields = ('id', 'url', 'facility', 'generic', 'title', 'description', 'created', 'updated'
                  )

        read_only_fields = ('id', 'url', 'facility',  'owner',)


class PrecautionsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Precautions
        fields = ('id', 'url', 'facility', 'generic', 'title', 'description', 'created', 'updated'
                  )

        read_only_fields = ('id', 'url', 'facility',  'owner',)


class SpecialConsiderationsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.SpecialConsiderations
        fields = ('id', 'url', 'facility', 'generic', 'title', 'description', 'created', 'updated'
                  )

        read_only_fields = ('id', 'url', 'facility',  'owner',)


class GenericReferenceSerializer(serializers.ModelSerializer):
    preparations = serializers.SerializerMethodField(read_only=True)
    indications = serializers.SerializerMethodField(read_only=True)
    doses = serializers.SerializerMethodField(read_only=True)
    modes_of_action = serializers.SerializerMethodField(read_only=True)
    contra_indications = serializers.SerializerMethodField(read_only=True)
    interactions = serializers.SerializerMethodField(read_only=True)
    side_effects = serializers.SerializerMethodField(read_only=True)
    precautions = serializers.SerializerMethodField(read_only=True)
    special_considerations = serializers.SerializerMethodField(read_only=True)
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
        fields = (
            'id',
            'owner',
            'url',
            'title',
            'description',
            'drug_class',
            'drug_sub_class',
            'created',
            'updated',
            'drug_class_details',
            'drug_sub_class_details',
            'preparations',
            'indications',
            'doses',
            'modes_of_action',
            'side_effects',
            'contra_indications',
            'interactions',
            'precautions',
            'special_considerations'
        )

        read_only_fields = ('id', 'url', 'created',
                            'updated', 'owner', )

    def get_preparations(self, obj):
        preparations = models.Preparation.objects.filter(generic=obj)
        return PreparationSerializer(preparations, context=self.context, many=True).data

    def get_indications(self, obj):
        indications = models.Indications.objects.filter(generic=obj)
        return IndicationsSerializer(indications, context=self.context, many=True).data

    def get_doses(self, obj):
        doses = models.Indications.objects.filter(generic=obj)
        return DosesSerializer(doses, context=self.context, many=True).data

    def get_modes_of_action(self, obj):
        modes_of_action = models.ModeOfActions.objects.filter(generic=obj)
        return ModeOfActionsSerializer(modes_of_action, context=self.context, many=True).data

    def get_side_effects(self, obj):
        side_effects = models.SideEffects.objects.filter(generic=obj)
        return SideEffectsSerializer(side_effects, context=self.context, many=True).data

    def get_contra_indications(self, obj):
        contra_indications = models.Contraindications.objects.filter(
            generic=obj)
        return ContraindicationsSerializer(contra_indications, context=self.context, many=True).data

    def get_precautions(self, obj):
        precautions = models.Precautions.objects.filter(generic=obj)
        return PrecautionsSerializer(precautions, context=self.context, many=True).data

    def get_interactions(self, obj):
        interactions = models.Interactions.objects.filter(generic=obj)
        return InteractionsSerializer(interactions, context=self.context, many=True).data

    def get_special_considerations(self, obj):
        special_considerations = models.SpecialConsiderations.objects.filter(
            generic=obj)
        return SpecialConsiderationsSerializer(special_considerations, context=self.context, many=True).data

    def get_drug_class_details(self, obj):
        drug_class = models.DrugClass.objects.get(id=obj.drug_class.id)
        return DrugClassSerializer(drug_class, context=self.context).data

    def get_drug_sub_class_details(self, obj):
        if obj.drug_sub_class:
            drug_sub_class = models.DrugSubClass.objects.get(
                id=obj.drug_sub_class.id)
            return DrugSubClassSerializer(drug_sub_class, context=self.context).data
