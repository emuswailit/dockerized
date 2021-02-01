from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from clients.models import ForwardPrescription
from clients.serializers import ForwardPrescriptionSerializer
from rest_framework import generics, exceptions, permissions, status
from core.views import FacilitySafeViewMixin
from . import serializers, models
from rest_framework.response import Response
from core.app_permissions import PharmacistPermission, FacilitySuperintendentPermission, IsOwner
from consultations.models import Prescription
from inventory.models import VariationReceipt
from django.urls import resolve

# Create your views here.


class AllPrescriptionQuotesListAPIView(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Pharmacy Superintendent
    =============================================
    Retrieve all prescription quotes for all pharmacists in the facility
    """
    name = "prescriptionquote-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PrescriptionQuoteSerializer

    queryset = models.PrescriptionQuote.objects.all()
    search_fields = ('forward_prescription__owner__id', 'owner__id')
    ordering_fields = ('id',)


class PharmacistPrescriptionQuotesListAPIView(generics.ListAPIView):
    """
    Pharmacist
    =============================================
    Retrieve all prescription quotes logged in pharmacist only
    """
    name = "prescriptionquote-list"
    permission_classes = (PharmacistPermission,
                          )
    serializer_class = serializers.PrescriptionQuoteSerializer

    queryset = models.PrescriptionQuote.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PrescriptionQuoteListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request

        return super().get_queryset().filter(facility=self.request.user.facility, owner=self.request.user)


class PrescriptionQuoteDetailAPIView(generics.RetrieveAPIView):
    """
    Logged on user
    -----------------------------------------------------------
    View details of prescription quote
    Prescription details
    """
    name = "prescriptionquote-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PrescriptionQuoteSerializer
    queryset = models.PrescriptionQuote.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PharmacistConfirmPrescriptionQuote(generics.RetrieveUpdateAPIView):
    """
    Pharmacist
    -----------------------------------------------------------
    Confirm that prescription quote has been quoted fully, client can now access to view
    """
    name = "prescriptionquote-update"
    permission_classes = (FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.PharmacistConfirmPrescriptionQuoteSerializer
    queryset = models.PrescriptionQuote.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        prescription_quote_item_pk = self.kwargs.get("pk")
        context = super(PharmacistConfirmPrescriptionQuote,




                        self).get_serializer_context()

        context.update({
            "user_pk":     self.request.user.id
        })
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ClientConfirmQuote(generics.RetrieveUpdateAPIView):
    """
    Client
    -----------------------------------------------------------
    Confirm that  quote has been accepted, pharmacist can now dispense
    """
    name = "prescriptionquote-update"
    permission_classes = (IsOwner,
                          )
    serializer_class = serializers.ClientConfirmQuoteSerializer
    queryset = models.PrescriptionQuote.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class QuoteItemListAPIView(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all prescription quotes for the logged in user's pharmacy
    """
    name = "quoteitem-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacistUpdateQuoteItemSerializer

    queryset = models.QuoteItem.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(QuoteItemListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request

        return super().get_queryset().filter(facility=self.request.user.facility)


class PrescriptionQuoteItemsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Pharmacist
    ============================================================
    Retrieve quote items for given prescription ID

    """
    name = 'quoteitem-list'
    permission_classes = (
        PharmacistPermission,
    )
    serializer_class = serializers.PharmacistUpdateQuoteItemSerializer
    queryset = models.QuoteItem.objects.all()

    # search_fields =('dependant__id','dependant__middle_name','dependant__last_name', 'dependant__first_name',)
    # ordering_fields =('dependant__first_name', 'id')

    def get_queryset(self):
        user = self.request.user
        prescription_quote_id = self.kwargs['pk']
        if models.PrescriptionQuote.objects.filter(id=prescription_quote_id).count() > 0:
            prescription_quote = models.PrescriptionQuote.objects.get(
                id=prescription_quote_id)
            if prescription_quote and prescription_quote.owner == user:
                return models.QuoteItem.objects.filter(prescription_quote=prescription_quote)
            else:
                raise exceptions.NotAcceptable(
                    {"detail": ["No quote for given ID  found in your records", ]})
        else:
            raise exceptions.NotAcceptable(
                {"detail": ["Quote for given ID not retrieved", ]})


class QuoteItemDetailAPIView(generics.RetrieveAPIView):
    """
    Prescription details
    """
    name = "quoteitem-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacistUpdateQuoteItemSerializer
    queryset = models.QuoteItem.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PharmacistUpdateQuoteItem(FacilitySafeViewMixin, generics.RetrieveUpdateAPIView):

    """
    Pharmacist
    ----------------------------------------------------
    Update prescription quote item
    """
    name = "quoteitem-update"
    permission_classes = (FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.PharmacistUpdateQuoteItemSerializer
    queryset = models.QuoteItem.objects.all()
    lookup_fields = ('pk',)
    # TODO : Refer -> Pass data from view to serializer using context

    def get_serializer_context(self):
        prescription_quote_item_pk = self.kwargs.get("pk")
        context = super(PharmacistUpdateQuoteItem,




                        self).get_serializer_context()

        context.update({
            "prescription_quote_item_pk": prescription_quote_item_pk, "user_pk":     self.request.user.id
            # extra data
        })
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AcceptQuoteItem(generics.RetrieveUpdateAPIView):

    """
    Pharmacist
    ----------------------------------------------------
    Update prescription quote item
    """
    name = "quoteitem-accept"
    permission_classes = (
        IsOwner,
    )
    serializer_class = serializers.ClientQuoteItemSerializer
    queryset = models.QuoteItem.objects.all()
    lookup_fields = ('pk',)
    # TODO : Refer -> Pass data from view to serializer using context

    def get_serializer_context(self):
        prescription_quote_item_pk = self.kwargs.get("pk")

        context = super(AcceptQuoteItem, self).get_serializer_context()

        context.update({
            "prescription_quote_item_pk": prescription_quote_item_pk
            # extra data
        })
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class FacilityOrdersList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Facility employees
    ============================================================
    1. List of product variations
    """
    name = 'order-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    # search_fields =('title','description', 'product__title','product__manufacturer__title')
    # ordering_fields =('title', 'id')

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class ClientOrdersList(generics.ListAPIView):
    """
    Client
    ============================================================
    List of all own orders
    """
    name = 'order-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    # search_fields =('title','description', 'product__title','product__manufacturer__title')
    # ordering_fields =('title', 'id')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OrderDetailAPIView(generics.RetrieveAPIView):
    """
    Pharmacist
    -----------------------------------------------
    View list of all confirmed orders
    """
    name = "order-detail"
    permission_classes = (PharmacistPermission,
                          )
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.filter(client_confirmed=True)
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AllOrderItemsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. List of product variations
    """
    name = 'orderitem-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.OrderItemSerializer
    queryset = models.OrderItem.objects.all()
    # search_fields =('title','description', 'product__title','product__manufacturer__title')
    # ordering_fields =('title', 'id')

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class OrderItemDetailAPIView(generics.RetrieveAPIView):
    """
    Prescription details
    """
    name = "orderitem-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.OrderItemSerializer
    queryset = models.OrderItem.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AllPrescriptionQuotesListAPIView(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Pharmacy Superintendent
    =============================================
    Retrieve all prescription quotes for all pharmacists in the facility
    """
    name = "prescriptionquote-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PrescriptionQuoteSerializer

    queryset = models.PrescriptionQuote.objects.all()
    search_fields = ('forward_prescription__owner__id', 'owner__id')
    ordering_fields = ('id',)


class ClientPharmacyPaymentsListAPIView(generics.ListAPIView):
    """
    Clients
    =============================================
    Retrieve all pharmacy payments for a client
    """
    name = "pharmacypayments-list"
    permission_classes = (permissions.IsAuthenticated, IsOwner
                          )
    serializer_class = serializers.PharmacyPaymentsSerializer

    queryset = models.PharmacyPayments.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PrescrClientPharmacyPaymentsListAPIViewiptionQuoteListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(owner=self.request.user)


class PharmacyPaymentsDetailAPIView(generics.RetrieveAPIView):
    """
    Pharmacy payments detail
    """
    name = "pharmacypayments-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacyPaymentsSerializer
    queryset = models.PharmacyPayments.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
