from rest_framework import serializers
from . import models

class PaymentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Payment
        fields = "__all__"
        read_only_fields = (
            'owner',  'facility', 'amount', 'reference_number', 'status'
        )


class PaymentMethodSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.PaymentMethods
        fields = "__all__"
        read_only_fields = (
            'owner',
        )