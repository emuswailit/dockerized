from django.db import IntegrityError
from django.shortcuts import render
from core.views import FacilitySafeViewMixin
from core.permissions import FacilitySuperintendentPermission
from rest_framework import generics, permissions, response, status, exceptions
from . import serializers
from rest_framework.response import Response
from . import models
# Variation Views


class VariationCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Create new product variation
    """
    name = 'variation-create'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.VariationSerializer
    queryset = models.Variation.objects.all()

    def perform_create(self, serializer):

        try:
            user = self.request.user
            facility = self.request.user.facility
            serializer.save(owner=user, facility=facility)
        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["Variation must be to be unique. Similar item is already added!", ]})

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


class VariationList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. List of product variations
    """
    name = 'variation-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.VariationSerializer
    queryset = models.Variation.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class VariationDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'variation-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationSerializer
    queryset = models.Variation.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class VariationUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Set pharmacist as superintendent or not
    2. Activate or deactivate pharmacist
    """
    name = 'variation-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationSerializer
    queryset = models.Variation.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class VariationPhotoList(FacilitySafeViewMixin, generics.ListCreateAPIView):
    """
    Logged In User
    =================================================================
    1. Add pharmacist photo
    2. View own courier instance
    """
    name = 'variationphoto-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationPhotoSerializer
    queryset = models.VariationPhoto.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        variation_pk = self.kwargs.get("pk")
        facility_id = self.request.user.facility_id
        serializer.save(facility_id=facility_id, owner=user,
                        variation_id=variation_pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Variation photo created successfully.", "variation-photo": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Variation photo not created", "variation-photo": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class VariationPhotoDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    """
    Logged in Facility Superintendent
    ================================================================
    1. View details of variation photo instance
    """
    name = 'variationphoto-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationPhotoSerializer
    queryset = models.VariationPhoto.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


# Variation receipt

class VariationReceiptCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Create new product variation
    """
    name = 'variationreceipt-create'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.VariationReceiptSerializer
    queryset = models.VariationReceipt.objects.all()

    def perform_create(self, serializer):

        try:
            user = self.request.user
            facility = self.request.user.facility
            variation_pk = self.kwargs.get("pk")
            serializer.save(owner=user, facility=facility,
                            variation_id=variation_pk)
        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["Variation receipt must be to be unique. Similar item is already added!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Variation stock successfully.", "variation-receipt": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Variation stock not created", "variation-receipt": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class VariationReceiptList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. List of product variations receipts
    """
    name = 'variationreceipt-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationReceiptSerializer
    queryset = models.VariationReceipt.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class VariationReceiptDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'variationreceipt-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationReceiptSerializer
    queryset = models.VariationReceipt.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class VariationReceiptUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Update stock item
    """
    name = 'variationreceipt-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationReceiptSerializer
    queryset = models.VariationReceipt.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)
