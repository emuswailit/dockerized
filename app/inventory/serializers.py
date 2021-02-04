from rest_framework import serializers
from core.serializers import FacilitySafeSerializerMixin
from . import models
from drugs.models import Product
from drugs.serializers import ProductSerializer
from django.db import transaction
from django.contrib.auth import get_user_model
from users.models import Facility

User = get_user_model()


class VariationPhotosSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VariationPhotos
        fields = "__all__"
        read_only_fields = (
            'variation', 'owner'
        )


class InventoryDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Inventory
        fields = (
            ('id', 'url')
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'is_active', 'unit_quantity', 'unit_buying_price', 'unit_selling_price', 'variations', 'facility'
        )

# Not using FacilitySafeSerializerMixin to allow global view of products


class VariationsSerializer(serializers.HyperlinkedModelSerializer):
    variation_images = VariationPhotosSerializer(many=True, read_only=True)
    product_details = serializers.SerializerMethodField(read_only=True)
    inventory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Variations
        fields = (
            'id',  'facility', 'url', 'category',  'title', 'description', 'get_available_units', 'get_available_packs',
            'created', 'updated', 'owner', 'product', 'slug', 'is_drug', 'is_active', 'variation_images', 'product_details', 'inventory'
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'quantity', 'slug', 'is_active', 'is_drug', 'facility'
        )

    def get_product_details(self, obj):
        if obj.product:
            product = Product.objects.get_by_id(id=obj.product.id)
            return ProductSerializer(product, context=self.context).data

    def get_inventory(self, obj):

        items = models.Inventory.objects.filter(variation=obj)
        return InventoryDisplaySerializer(items, context=self.context, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        user_pk = self.context.get("user_pk")
        user = User.objects.get(id=user_pk)
        title = validated_data.pop('title')
        product = validated_data.pop('product')
        category = validated_data.pop('category')

        if user.facility == Facility.objects.default_facility():
            raise serializers.ValidationError(
                f"You are not allowed to create inventory in this facility")
        final_title = None
        if product:
            if models.Variations.objects.filter(product=product, facility=user.facility).count() > 0:
                raise serializers.ValidationError(
                    {"response_code": 1, "response_message": f" A variation for {product.title} already exists for your facility"})

            else:
                final_title = f"{product.preparation.title } -{product.title}"
        else:
            final_title = title
        created = models.Variations.objects.create(
            product=product, title=final_title, category=category, **validated_data)

        return created


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Inventory
        fields = (
            "__all__"
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'is_active', 'unit_quantity', 'unit_buying_price', 'unit_selling_price', 'facility'
        )


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Categories
        fields = (
            "__all__"
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'is_active', 'facility',
        )


class VariationsUpdateSerializer(serializers.HyperlinkedModelSerializer):
    variation_images = VariationPhotosSerializer(many=True, read_only=True)
    product_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Variations
        fields = (
            'id',  'facility', 'url', 'category',  'title', 'description', 'get_available_units', 'get_available_packs',
            'created', 'updated', 'owner', 'product', 'slug', 'is_drug', 'is_active', 'variation_images', 'product_details',
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'quantity', 'slug', 'is_active', 'is_drug', 'facility', 'product', 'category'
        )

    def get_product_details(self, obj):
        if obj.product:
            product = Product.objects.get_by_id(id=obj.product.id)
            return ProductSerializer(product, context=self.context).data

    def delete(self):
        raise serializers.ValidationError(
            {"response_code": 1, "response_message": "Item cannot be deleted"})
