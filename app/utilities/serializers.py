
from rest_framework import serializers
from . import models


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Categories
        fields = ('id', 'url', 'facility', 'title', 'description',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',
                            'owner', 'created', 'updated')
