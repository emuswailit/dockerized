from django.shortcuts import render
from rest_framework import permissions, generics, status, exceptions
from . import serializers, models
from core.views import FacilitySafeViewMixin
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from core.permissions import PrescriberPermission, IsOwner
from django.db import IntegrityError

# Create your views here.
# Prescription

from django.shortcuts import get_object_or_404, redirect, render


class PrescriptionCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
   Prescriber
    ============================================================
    1. Create new prescription

    """
    name = 'prescription-create'
    permission_classes = (
        PrescriberPermission,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()

    def perform_create(self, serializer):

        user = self.request.user
        facility = self.request.user.facility
        dependant_pk = self.kwargs.get("pk")
        serializer.save(owner=user, facility=facility,
                        dependant_id=dependant_pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Prescription created successfully.", "prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Prescription not created", "prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PrescriptionList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Logged in authorized user
    ============================================================
    1. List of product variations receipts

    """
    name = 'prescription-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'prescription-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Prescriber, owner
    ============================================================
    1. Update prescription

    """
    name = 'prescription-detail'
    permission_classes = (
        PrescriberPermission, IsOwner
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


# Prescription item


class PrescriptionItemCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Create new product variation

    """
    name = 'prescriptionitem-create'
    permission_classes = (
        PrescriberPermission,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    def perform_create(self, serializer):

        try:
            user = self.request.user
            facility = self.request.user.facility
            prescription_pk = self.kwargs.get("pk")

            if prescription_pk:
                print(prescription_pk)
             
                serializer.save(owner=user, facility=facility,
                                prescription_id=prescription_pk)
            else:
                raise exceptions.NotAcceptable(
                    {"detail": ["Prescription not retrieved", ]})

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["Prescription item must be to be unique. Similar item is already added!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Prescription item added successfully.", "prescription-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Precsription item not added", "prescription-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PrescriptionItemList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. List of prescription items

    """
    name = 'prescriptionitem-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionItemDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'prescriptionitem-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionItemUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Update prescription item

    """
    name = 'prescriptionitem-detail'
    permission_classes = (
        PrescriberPermission, IsOwner
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class DependantListAPIView(generics.ListAPIView):
    """
    Prescriber
    =============================================
    Retrieve all dependants
    """
    name = "dependant-list"
    permission_classes = (PrescriberPermission,
                          )
    serializer_class = serializers.DependantSerializer

    queryset = models.Dependant.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DependantListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(DependantListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class DependantDetailAPIView(generics.RetrieveAPIView):
    """
    Dependant details
    """
    name = "dependant-detail"
    permission_classes = (PrescriberPermission,
                          )
    serializer_class = serializers.DependantSerializer
    queryset = models.Dependant.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

