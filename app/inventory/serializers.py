from rest_framework import serializers
from core.serializers import FacilitySafeSerializerMixin
from . import models
from drugs.models import Product
from drugs.serializers import ProductSerializer


class VariationPhotoSerializer(FacilitySafeSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VariationPhoto
        fields = "__all__"
        read_only_fields = (
            'variation', 'owner'
        )


# Not using FacilitySafeSerializerMixin to allow global view of products
class VariationSerializer(serializers.HyperlinkedModelSerializer):
    variation_images = VariationPhotoSerializer(many=True, read_only=True)
    product_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Variation
        fields = (
            'id',  'facility', 'url',  'title', 'description', 'quantity',
            'created', 'updated', 'owner', 'product', 'slug', 'is_drug', 'is_active', 'variation_images', 'product_details',
        )
        read_only_fields = (
            'created', 'updated', 'owner', 'quantity', 'slug', 'is_active', 'is_drug', 'facility'
        )

    def get_product_details(self, obj):
        if obj.product:
            product = Product.objects.get_by_id(id=obj.product.id)
            return ProductSerializer(product, context=self.context).data


class VariationReceiptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VariationReceipt
        fields = "__all__"
        read_only_fields = (
            'created', 'updated', 'owner', 'is_active', 'unit_quantity', 'unit_buying_price', 'unit_selling_price', 'variation',
        )
