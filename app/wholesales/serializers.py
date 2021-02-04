
from rest_framework import serializers
from . import models


class ListingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Listings
        fields = ('id', 'url', 'facility', 'category', 'product', 'title', 'description', 'is_active', 'slug', 'is_drug',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility', 'slug', 'is_active', 'is_drug',
                            'owner', 'created', 'updated')
