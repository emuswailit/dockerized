from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from . import serializers, models
from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from consultations.models import Prescription
from consultations.serializers import PrescriptionSerializer
from users.models import Dependant, Facility
from users.serializers import FacilitySerializer
from core.views import FacilitySafeViewMixin
from django.db.models import Q
from core.app_permissions import PrescriberPermission

# Create your views here.


# class PrescriptionListAPIView(generics.ListAPIView):
#     """
#     Client
#     =============================================
#     Retrieve all prescriptions for the logged in user's dependants
#     """
#     name = "prescription-list"
#     permission_classes = (PrescriberPermission,
#                           )
#     serializer_class = PrescriptionSerializer

#     queryset = Prescription.objects.all()
#     # TODO : Reuse this for filtering by q.

#     # def get_queryset(self):
#     #     # Ensure that the users belong to the company of the user that is making the request
#     #     dependant = Dependant.objects.get(owner=self.request.user)
#     #     return super().get_queryset().filter(dependant=dependant)


# class UserPrescriptionListAPIView(generics.ListAPIView):
#     """
#     Client
#     =============================================
#     Retrieve all prescriptions for the logged in user's dependants
#     """
#     name = "prescription-list"
#     permission_classes = (permissions.IsAuthenticated,
#                           )
#     serializer_class = PrescriptionSerializer

#     queryset = Prescription.objects.all()
#     # TODO : Reuse this for filtering by q.

#     def get_queryset(self):
#         # Ensure that the users belong to the company of the user that is making the request
#         dependant = Dependant.objects.get(owner=self.request.user)
#         return super().get_queryset().filter(dependant=dependant)

# class PrescriptionDetailAPIView(generics.RetrieveAPIView):
#     """
#     Prescription details
#     """
#     name = "prescription-detail"
#     permission_classes = (permissions.IsAuthenticated,
#                           )
#     serializer_class = PrescriptionSerializer
#     queryset = Prescription.objects.all()
#     lookup_fields = ('pk',)

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj


class ForwardPrescriptionCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Client
    ============================================================
    1. Forward prescription to a pharmacy

    """
    name = 'forwardprescription-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ForwardPrescriptionSerializer
    queryset = models.ForwardPrescription.objects.all()

    def perform_create(self, serializer):

        try:
            user = self.request.user

            serializer.save(owner=user)

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["Prescription item must be to be unique. Similar item is already added!", ]})

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


class ForwardPrescriptionsForFacility(generics.ListAPIView):
    """
    Pharmacists
    =============================================
    Retrieve all retrieve all prescriptions forwarded to their facility
    """
    name = "product-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ForwardPrescriptionSerializer

    queryset = models.ForwardPrescription.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_queryset(self):
        user = self.request.user
        # Ensure that the users belong to the company of the user that is making the request
        # dependant = Dependant.objects.get(owner=self.request.user)
        return super().get_queryset().filter(facility=user.facility)


class ForwardPrescriptionListAPIView(generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all prescriptions for the logged in user's dependants
    """
    name = "product-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ForwardPrescriptionSerializer

    queryset = models.ForwardPrescription.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(ForwardPrescriptionListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request
        dependant = Dependant.objects.get(owner=self.request.user)
        return super().get_queryset().filter(owner=self.request.user)


class ForwardPrescriptionDetailAPIView(generics.RetrieveAPIView):
    """
    Authorized user
    ---------------------------------------
    View details of a forwarded prescription
    """
    name = "forwardprescription-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ForwardPrescriptionSerializer
    queryset = models.ForwardPrescription.objects.all()
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
    Retrieve all pharmacies or those close to user
    """
    name = "pharmacy-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PharmacySerializer
    search_fields = ('town', 'county')
    ordering_fields = ('created',)
    queryset = models.Facility.objects.filter(facility_type="Pharmacy")
    # TODO : Reuse this for filtering by q.

    # def get_context_data(self, *args, **kwargs):
    #     context = super(PharmacyListAPIView, self).get_context_data(
    #         *args, **kwargs)
    #     # context["now"] = timezone.now()
    #     context["query"] = self.request.GET.get("q")  # None
    #     return context

    # def get_queryset(self):
    #     # Ensure that the users belong to the company of the user that is making the request

    #     return super().get_queryset().filter(facility_type='Pharmacy')
    # def get_queryset(self, *args, **kwargs):
    #     qs = super(PharmacyListAPIView, self).get_queryset(*args, **kwargs)
    #     query = self.request.GET.get("q")
    #     if query:
    #         qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
    #             Q(town__icontains=query) |
    #             Q(county__icontains=query) |
    #             Q(road__icontains=query)
    #         )
    #         try:
    #             qs2 = self.queryset.filter(
    #                 Q(price=query)
    #             )
    #             qs = (qs | qs2).distinct()
    #         except:
    #             pass
    #     return qs


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
    Retrieve all pharmacies or those close to user
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
