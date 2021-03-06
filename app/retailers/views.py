from django.db import IntegrityError
from django.shortcuts import render
from core.views import FacilitySafeViewMixin
from core.app_permissions import FacilitySuperintendentPermission, PharmacistPermission
from rest_framework import generics, permissions, response, status, exceptions
from . import serializers
from rest_framework.response import Response
from . import models
# RetailProducts Views

from retailers.serializers import PrescriptionQuoteSerializer
from retailers.models import PrescriptionQuote, QuoteItem
from django.db import transaction
from retailers.models import PrescriptionQuote
from users.models import Facility, Dependant
from rest_framework.validators import UniqueTogetherValidator
from consultations.serializers import PrescriptionItemSerializer, PrescriptionSerializer
from rest_framework import serializers
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, exceptions, permissions, status
from core.views import FacilitySafeViewMixin
from . import serializers, models
from rest_framework.response import Response
from core.app_permissions import PharmacistPermission, FacilitySuperintendentPermission, IsOwner
from consultations.models import Prescription
from django.urls import resolve


class ForwardsCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Client
    ============================================================
    1. Forward prescription to a pharmacy

    """
    name = 'forwards-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ForwardsSerializer
    queryset = models.Forwards.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(ForwardsCreate,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):

        try:
            user = self.request.user

            serializer.save(owner=user)

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": [f"{e}", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data['facility'])
        # print(request.data['facility'])

        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Prescription forwarded successfully.", "forwarded-prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Precsription not forwarded", "forwarded-prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ForwardssForFacility(generics.ListAPIView):
    """
    Pharmacists
    =============================================
    Retrieve all retrieve all prescriptions forwarded to their facility
    """
    name = "product-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ForwardsSerializer

    queryset = models.Forwards.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_queryset(self):
        user = self.request.user
        # Ensure that the users belong to the company of the user that is making the request
        # dependant = Dependant.objects.get(owner=self.request.user)
        return super().get_queryset().filter(facility=user.facility)


class ForwardsListAPIView(generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all prescriptions for the logged in user's dependants
    """
    name = "product-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ForwardsSerializer

    queryset = models.Forwards.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(ForwardsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request
        dependant = Dependant.objects.get(owner=self.request.user)
        return super().get_queryset().filter(owner=self.request.user)


class ForwardsDetailAPIView(generics.RetrieveAPIView):
    """
    Authorized user
    ---------------------------------------
    View details of a forwarded prescription
    """
    name = "forwards-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ForwardsSerializer
    queryset = models.Forwards.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PharmacyListAPIView(generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all pharmacies
    """
    name = "pharmacy-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacySerializer
    search_fields = ('town', 'county')
    ordering_fields = ('created',)
    queryset = models.Facility.objects.filter(facility_type="Pharmacy")


class PharmacyDetailAPIView(generics.RetrieveAPIView):
    """
    Pharmacy details
    """
    name = "pharmacy-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacySerializer
    queryset = models.Facility.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ClinicListAPIView(generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all retailers or those close to user
    """
    name = "clinic-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacySerializer

    queryset = models.Facility.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(ClinicListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request

        return super().get_queryset().filter(facility_type='Clinic')


class ClinicDetailAPIView(generics.RetrieveAPIView):
    """
    Clinic details
    """
    name = "clinic-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacySerializer
    queryset = models.Facility.objects.all()
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
    permission_classes = (FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.PrescriptionQuoteSerializer

    queryset = models.PrescriptionQuote.objects.all()
    search_fields = ('forward__owner__id', 'owner__id')
    ordering_fields = ('id',)


class PharmacistPrescriptionQuotesListAPIView(generics.ListAPIView):
    """
    Pharmacist
    =============================================
    Retrieve all quote which a pharmacist is currently processing
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
        # Pharmacist only views prescriptions he is processing

        return super().get_queryset().filter(processed_by=self.request.user)


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
    Confirm that  quote has been quoted fully, client can now access to view
    """
    name = "prescriptionquote-update"
    permission_classes = (PharmacistPermission,
                          )
    serializer_class = serializers.PharmacistConfirmPrescriptionQuoteSerializer
    queryset = models.PrescriptionQuote.objects.all()
    lookup_fields = ('pk',)

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request

        return super().get_queryset().filter(processed_by=self.request.user)

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


#

class QuoteItemCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Pharmacist
    ============================================================
    1. Create quote item for forwarded prescription

    """
    name = 'quiteitem-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.QuoteItemSerializer
    queryset = models.QuoteItem.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=self.request.user.facility,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Prescription forwarded successfully.", "forwarded-prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Precsription not forwarded", "forwarded-prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


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
    queryset = models.QuoteItem.objects.all_quote_items()

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
    Quote item details
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
    permission_classes = (PharmacistPermission,
                          )
    serializer_class = serializers.PharmacistUpdateQuoteItemSerializer
    queryset = models.QuoteItem.objects.all_quote_items()
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
    Client
    ----------------------------------------------------
    Update prescription quote item to accept it
    """
    name = "quoteitem-accept"
    permission_classes = (
        IsOwner,
    )
    serializer_class = serializers.ClientAcceptQuoteItemSerializer
    queryset = models.QuoteItem.objects.partially_dispensed_quote_items()
    lookup_fields = ('pk',)
    # TODO : Refer -> Pass data from view to serializer using context

    def get_serializer_context(self):
        prescription_quote_item_pk = self.kwargs.get("pk")

        context = super(AcceptQuoteItem, self).get_serializer_context()

        context.update({
            "user_id": self.request.user.id
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
    1. List of orders
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
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ClientConfirmOrderAPIView(generics.RetrieveUpdateAPIView):
    """
    Client
    -----------------------------------------------
    Confirm an order and proceed to payment
    """
    name = "order-update"
    permission_classes = (IsOwner,
                          )
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()


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
    search_fields = ('forward__owner__id', 'owner__id')
    ordering_fields = ('id',)


class ClientPharmacyPaymentsListAPIView(generics.ListAPIView):
    """
    Clients
    =============================================
    Retrpython manage.py runserverieve all pharmacy payments for a client
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


# class RetailProductsCreate(FacilitySafeViewMixin, generics.CreateAPIView):
#     """
#     Superintendent Pharmacist
#     ============================================================
#     1. Create new product variation
#     """
#     name = 'retailproducts-create'
#     permission_classes = (
#         FacilitySuperintendentPermission,
#     )
#     serializer_class = serializers.RetailProductsSerializer
#     queryset = models.RetailProducts.objects.all()

#     def get_serializer_context(self):
#         user_pk = self.request.user.id
#         context = super(RetailProductsCreate,
#                         self).get_serializer_context()

#         context.update({
#             "user_pk": user_pk

#         })
#         return context

#     def perform_create(self, serializer):

#         try:
#             user = self.request.user
#             facility = self.request.user.facility
#             serializer.save(owner=user, facility=facility)
#         except IntegrityError as e:
#             raise exceptions.NotAcceptable(
#                 {"detail": ["RetailProducts must be to be unique. Similar item is already added!", ]})

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_create(serializer)
#             return Response(data={"message": "Facility pharmacist created successfully.", "variation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"message": "Facility pharmacist not created", "variation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


# class RetailProductsList(FacilitySafeViewMixin, generics.ListAPIView):
#     """
#     Superintendent Pharmacist
#     ============================================================
#     1. List of items in inventory
#     """
#     name = 'retailproducts-list'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.RetailProductsSerializer
#     queryset = models.RetailProducts.objects.all()
#     search_fields = ('title', 'description', 'product__title',
#                      'product__manufacturer__title')
#     ordering_fields = ('title', 'id')

#     # def get_queryset(self):
#     #     facility_id = self.request.user.facility_id
#     #     return super().get_queryset().filter(facility_id=facility_id)


# class RetailProductsDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
#     name = 'retailproducts-detail'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.RetailProductsSerializer
#     queryset = models.RetailProducts.objects.all()

#     def get_queryset(self):
#         facility_id = self.request.user.facility_id
#         return super().get_queryset().filter(facility_id=facility_id)


# class RetailProductsUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateAPIView):
#     """
#     Superintendent Pharmacist
#     ============================================================
#     Update inventory item
#     """
#     name = 'retailproducts-update'
#     permission_classes = (
#         FacilitySuperintendentPermission,
#     )
#     serializer_class = serializers.RetailProductsUpdateSerializer
#     queryset = models.RetailProducts.objects.all()

#     def get_queryset(self):
#         facility_id = self.request.user.facility_id
#         return super().get_queryset().filter(facility_id=facility_id)

#     def delete(self, request, *args, **kwargs):
#         raise exceptions.NotAcceptable(
#             {"response_code": 1, "response_message": "This item cannot be deleted!"})


# class RetailProductsPhotoList(FacilitySafeViewMixin, generics.ListCreateAPIView):
#     """
#     Logged In User
#     =================================================================
#     1. Add pharmacist photo
#     2. View own courier instance
#     """
#     name = 'variationphoto-list'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.RetailProductPhotosSerializer
#     queryset = models.RetailProductPhotos.objects.all()

#     def perform_create(self, serializer):
#         user = self.request.user
#         variation_pk = self.kwargs.get("pk")
#         facility_id = self.request.user.facility_id
#         serializer.save(facility_id=facility_id, owner=user,
#                         variation_id=variation_pk)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_create(serializer)
#             return Response(data={"message": "RetailProducts photo created successfully.", "variation-photo": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"message": "RetailProducts photo not created", "variation-photo": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)

#     def get_queryset(self):
#         user = self.request.user
#         return super().get_queryset().filter(owner=user)


# class RetailProductsPhotoDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
#     """
#     Logged in Facility Superintendent
#     ================================================================
#     1. View details of variation photo instance
#     """
#     name = 'variationphoto-detail'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.RetailProductPhotosSerializer
#     queryset = models.RetailProductPhotos.objects.all()

#     def get_queryset(self):
#         user = self.request.user
#         return super().get_queryset().filter(owner=user)


class RetailVariationsCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Create new product variation
    """
    name = 'retailvariations-create'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.RetailVariationsSerializer
    queryset = models.RetailVariations.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(RetailVariationsCreate,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):

        try:
            user = self.request.user
            facility = self.request.user.facility
            serializer.save(owner=user, facility=facility)
        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["RetailVariations must be to be unique. Similar item is already added!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Facility pharmacist created successfully.", "variation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Facility pharmacist not created", "variation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class RetailVariationsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. List of items in inventory
    """
    name = 'retailvariations-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.RetailVariationsSerializer
    queryset = models.RetailVariations.objects.all()
    search_fields = ('title', 'description', 'product__title',
                     'product__manufacturer__title')
    ordering_fields = ('title', 'id')

    # def get_queryset(self):
    #     facility_id = self.request.user.facility_id
    #     return super().get_queryset().filter(facility_id=facility_id)


class RetailVariationsDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'retailvariations-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.RetailVariationsSerializer
    queryset = models.RetailVariations.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class RetailVariationsUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    Update inventory item
    """
    name = 'retailvariations-update'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.RetailVariationsSerializer
    queryset = models.RetailVariations.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"response_code": 1, "response_message": "This item cannot be deleted!"})
