from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from clients.models import ForwardPrescription
from clients.serializers import ForwardPrescriptionSerializer
from rest_framework import generics, exceptions, permissions, status
from core.views import FacilitySafeViewMixin
from . import serializers, models
from rest_framework.response import Response
from core.permissions import PharmacistPermission,FacilitySuperintendentPermission
from consultations.models import Prescription
from inventory.models import VariationReceipt
from django.urls import resolve

# Create your views here.


# class ForwardPrescriptionListAPIView(generics.ListAPIView):
#     """
#     Client
#     =============================================
#     Retrieve all forwarded prescriptions from clients
#     """
#     name = "forwardprescription-list"
#     permission_classes = (PharmacistPermission,
#                           )
#     serializer_class = ForwardPrescriptionSerializer

#     queryset = ForwardPrescription.objects.all()
#     # TODO : Reuse this for filtering by q.

#     def get_context_data(self, *args, **kwargs):
#         context = super(ForwardPrescriptionListAPIView, self).get_context_data(
#             *args, **kwargs)
#         # context["now"] = timezone.now()
#         context["query"] = self.request.GET.get("q")  # None
#         return context

#     def get_queryset(self):
#         # Ensure that the users belong to the company of the user that is making the request
#         facility = self.request.user.facility
#         return super().get_queryset().filter(facility=facility)


# class ForwardPrescriptionDetailAPIView(generics.RetrieveAPIView):
#     """
#     ForwardPrescription details
#     """
#     name = "forwardprescription-detail"
#     permission_classes = (PharmacistPermission,
#                           )
#     serializer_class = ForwardPrescriptionSerializer
#     queryset = ForwardPrescription.objects.all()
#     lookup_fields = ('pk',)

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj


class PrescriptionQuoteCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Pharmacist
    ============================================================
    1. Create quote for forwarded prescription

    """
    name = 'prescriptionquote-create'
    permission_classes = (
        PharmacistPermission,
    )
    serializer_class = serializers.PrescriptionQuoteSerializer
    queryset = models.PrescriptionQuote.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        try:
            if user:
                serializer.save(owner=user, facility=user.facility)   
            else:
                return Response(data={"message":"User not retrieved"})
        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["Similar item is already added!", ]})

        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Prescription quoted successfully.", "prescription-quote": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Precsription not quoted", "prescription-quote": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)

class AllPrescriptionQuotesListAPIView(generics.ListAPIView):
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
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PrescriptionQuoteListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request
        return super().get_queryset().filter(facility=self.request.user.facility)


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


# class QuoteItemCreate(FacilitySafeViewMixin, generics.CreateAPIView):
#     """
#     Pharmacist
#     ============================================================
#     1. Create quote item for forwarded prescription

#     """
#     name = 'quiteitem-create'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.QuoteItemSerializer
#     queryset = models.QuoteItem.objects.all()

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(owner=user, facility=self.request.user.facility,)
        
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_create(serializer)
#             return Response(data={"message": "Prescription forwarded successfully.", "forwarded-prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"message": "Precsription not forwarded", "forwarded-prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class QuoteItemListAPIView(FacilitySafeViewMixin,generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all prescription quotes for the logged in user's pharmacy
    """
    name = "quoteitem-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.QuoteItemSerializer

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


class QuoteItemDetailAPIView(generics.RetrieveAPIView):
    """
    Prescription details
    """
    name = "quoteitem-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.QuoteItemSerializer
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

class UpdateQuoteItem(generics.RetrieveUpdateAPIView):
    """
    Prescription details
    """
    name = "quoteitem-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.QuoteItemSerializer
    queryset = models.QuoteItem.objects.all()
    lookup_fields = ('pk',)
    def get_serializer_context(self):
        prescription_quote_item_pk = self.kwargs.get("pk")
        context = super(UpdateQuoteItem, self).get_serializer_context()
        
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
    # def put(self, request, pk=None, **kwargs):
    #     prescription_quote_item_pk = self.kwargs.get("pk")

    #     if models.QuoteItem.objects.filter(id=prescription_quote_item_pk).count()>0:
    #         prescription_quote_item = models.QuoteItem.objects.get(id=prescription_quote_item_pk)
    #         if prescription_quote_item.owner==request.user:
    #             return Response(data={"message": f"You are authorized to edit this quotation {request.POST.get('variation_item')} "})
    #         else:
    #             return Response(data={"message": "You can only edit quotations you created"})
               
    #     else:
    #         return Response(data={"message": "No prescription for this ID"})
        
