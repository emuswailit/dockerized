
from rest_framework import serializers
from . import models


class WholesaleProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.WholesaleProducts
        fields = ('id', 'url', 'facility',  'product', 'available_packs_quantity', 'total_discounts',   'is_active',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')


class WholesaleVariationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.WholesaleVariations
        fields = (
            'id',
            'url',
            'facility',
            'wholesale_product',
            'is_active',
            'pack_quantity',
            'pack_buying_price',
            'pack_selling_price',
            'source',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')


class BonusesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Bonuses
        fields = ('id', 'url', 'facility',  'wholesale_product', 'title', 'description', 'start_time', 'end_', 'for_every', 'get_free',  'is_active',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')


class DiscountsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Discounts
        fields = ('id', 'url', 'facility',  'wholesale_product', 'title', 'description', 'start_time', 'end_time', 'percentage',   'is_active',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active',
                            'owner', 'created', 'updated')


class RequisitionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Requisitions
        fields = ('id', 'url', 'facility',  'wholesale', 'retailer_confirmed', 'wholesaler_confirmed', 'payment_terms', 'priority',
                  'owner', 'created', 'updated')
        read_only_fields = ('id', 'url', 'facility',  'is_active', 'retailer_confirmed', 'wholesaler_confirmed',
                            'owner', 'created', 'updated')


class RequisitionItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RequisitionItems
        fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'wholesale_product',
            'wholesaler_confirmed',
            'retailer_confirmed',
            'quantity_required',
            'quantity_issued',
            'quantity_pending',
            'quantity_paid',
            'quantity_unpaid',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'is_active',
            'retailer_confirmed',
            'wholesaler_confirmed',
            'quantity_issued',
            'quantity_pending',
            'quantity_paid',
            'quantity_unpaid',
            'owner',
            'created',
            'updated'
        )


class DespatchesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Despatches
        fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'despatch_confirmed',
            'receipt_confirmed',
            'courier_confirmed',
            'despatch_confirmed_by',
            'receipt_confirmed_by',
            'courier_confirmed_by',
            'courier',
            'priority',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition',
            'despatch_confirmed',
            'receipt_confirmed',
            'courier_confirmed',
            'despatch_confirmed_by',
            'receipt_confirmed_by',
            'courier_confirmed_by',
            'courier',
            'priority',
            'owner',
            'created',
            'updated'
        )


class DespatchItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DespatchItems
        fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )


class DespatchPaymentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DespatchPayments
        fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )
        read_only_fields = (
            'id',
            'url',
            'facility',
            'requisition_item',
            'despatch',
            'owner',
            'created',
            'updated'
        )
