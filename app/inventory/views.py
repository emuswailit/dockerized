from django.db import IntegrityError
from django.shortcuts import render
from core.views import FacilitySafeViewMixin
from core.app_permissions import FacilitySuperintendentPermission, PharmacistPermission
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
    name = 'variations-create'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.VariationsSerializer
    queryset = models.Variations.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(VariationCreate,
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
                {"detail": ["Variations must be to be unique. Similar item is already added!", ]})

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
    1. List of items in inventory
    """
    name = 'variations-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationsSerializer
    queryset = models.Variations.objects.all()
    search_fields = ('title', 'description', 'product__title',
                     'product__manufacturer__title')
    ordering_fields = ('title', 'id')

    # def get_queryset(self):
    #     facility_id = self.request.user.facility_id
    #     return super().get_queryset().filter(facility_id=facility_id)


class VariationDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'variations-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.VariationsSerializer
    queryset = models.Variations.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class VariationUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    Update inventory item
    """
    name = 'variations-update'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.VariationsUpdateSerializer
    queryset = models.Variations.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"response_code": 1, "response_message": "This item cannot be deleted!"})



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
    serializer_class = serializers.VariationPhotosSerializer
    queryset = models.VariationPhotos.objects.all()

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
    serializer_class = serializers.VariationPhotosSerializer
    queryset = models.VariationPhotos.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


# Variation receipt

class InventoryCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Create new product variation
    """
    name = 'inventory-create'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.InventorySerializer
    queryset = models.Inventory.objects.all()

    def perform_create(self, serializer):


        user = self.request.user
        facility = self.request.user.facility
        serializer.save(owner=user, facility=facility,
                        )
    
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


class InventoryList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Pharmacistst
    ============================================================
    1. List of product variations receipts
    """
    name = 'inventory-list'
    permission_classes = (
       permissions.IsAuthenticated,
    )
    serializer_class = serializers.InventorySerializer
    queryset = models.Inventory.objects.all()

    search_fields = ('distributor__title', 'description', 'variation__title',
                     'variation__product__manufacturer__title', 'variation__product__title')
    ordering_fields = ('title', 'id')

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class InventoryDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'inventory-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.InventorySerializer
    queryset = models.Inventory.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class InventoryUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Update stock item
    """
    name = 'inventory-update'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.InventorySerializer
    queryset = models.Inventory.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

# Categories


class CategoriesCreateAPIView(generics.CreateAPIView):
    """
    Create new generic
    """
    name = "categories-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.CategoriesSerializer
    queryset = models.Categories.objects.all()

    def perform_create(self, serializer):
        try:
            user = self.request.user
            serializer.save(owner=user, facility=user.facility)
        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"response_code": "1", "response_message": f"No repeating entries"})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Category created successfully.", "indication": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Category not created", "indication": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class CategoriesListAPIView(generics.ListAPIView):
    """
    List of indication drugs
    """
    name = "categories-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.CategoriesSerializer

    queryset = models.Categories.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('indication', 'description',
                     'generic__title', )
    ordering_fields = ('generic_title', 'id')


class CategoriesDetailAPIView(generics.RetrieveAPIView):
    """
    Categories details
    """
    name = "categories-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.CategoriesSerializer
    queryset = models.Categories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class CategoriesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Categories update
    """
    name = "categories-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.CategoriesSerializer
    queryset = models.Categories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
