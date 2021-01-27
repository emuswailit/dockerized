
from rest_framework import serializers
from . import models


class PlanSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Plan
        fields = ('id', 'url', 'title', 'description',
                  'price', 'owner', 'created', 'updated')
        read_only_fields = (
            'owner', 'id',
        )





class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Subscription
        fields = "__all__"
        read_only_fields = (
            'owner',
        )
