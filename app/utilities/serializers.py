
from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields = ('id', 'url', 'facility', 'title', 'description',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',
                            'owner', 'created', 'updated')


class SubCategorySerializer(serializers.ModelSerializer):
    category_details = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.SubCategories
        fields = ('id', 'url', 'facility','category', 'title', 'description','is_active',
                  'owner', 'created', 'updated','category_details')
        read_only_fields = ('id', 'url', 'facility',
                            'owner', 'created', 'updated')
    def get_category_details(self, obj):
        category = models.Categories.objects.get(id=obj.category.id)
        return CategorySerializer(category, context=self.context).data
