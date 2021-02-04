from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, permissions, status, exceptions
from . import serializers
from . import models
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_countries.serializers import CountryFieldMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from core.app_permissions import IsSubscribedPermission, SubscribedOrStaffPermission


# Distributors


class DistributorCreateAPIView(generics.CreateAPIView):
    """
    Admin User
    ----------------------------------------------------
    Create new disributor
    """
    name = "distributor-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DistributorSerializer
    queryset = models.Distributor.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Distributor created successfully.", "distributor": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Distributor not created", "distributor": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DistributorListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "distributor-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DistributorSerializer

    queryset = models.Distributor.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class DistributorDetailAPIView(generics.RetrieveAPIView):
    """
    Distributor details
    """
    name = "distributor-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DistributorSerializer
    queryset = models.Distributor.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DistributorUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Distributor update
    """
    name = "distributor-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DistributorSerializer
    queryset = models.Distributor.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


# Posology


class PosologyCreateAPIView(generics.CreateAPIView):
    """
    Create new distributor
    """
    name = "posology-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PosologySerializer
    queryset = models.Posology.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Posology created successfully.", "posology": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Posology not created", "route": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PosologyListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "posology-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PosologySerializer

    queryset = models.Posology.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class PosologyDetailAPIView(generics.RetrieveAPIView):
    """
    Posology details
    """
    name = "posology-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PosologySerializer
    queryset = models.Posology.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PosologyUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Posology update
    """
    name = "posology-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PosologySerializer
    queryset = models.Posology.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


# Frequency


class FrequencyCreateAPIView(generics.CreateAPIView):
    """
    Create new frequency
    """
    name = "frequency-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.FrequencySerializer
    queryset = models.Frequency.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Frequency created successfully.", "frequency": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Frequency not created", "frequency": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class FrequencyListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "frequency-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.FrequencySerializer

    queryset = models.Frequency.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', 'abbreviation', 'description')
    ordering_fields = ('title', 'id')


class FrequencyDetailAPIView(generics.RetrieveAPIView):
    """
    Frequency details
    """
    name = "frequency-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.FrequencySerializer
    queryset = models.Frequency.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class FrequencyUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Frequency update
    """
    name = "frequency-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.FrequencySerializer
    queryset = models.Frequency.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


# Instruction


class InstructionCreateAPIView(generics.CreateAPIView):
    """
    Create new frequency
    """
    name = "instruction-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.InstructionSerializer
    queryset = models.Instruction.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Instruction created successfully.", "instruction": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Instruction not created", "instruction": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class InstructionListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "instruction-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.InstructionSerializer

    queryset = models.Instruction.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class InstructionDetailAPIView(generics.RetrieveAPIView):
    """
    Instruction details
    """
    name = "instruction-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.InstructionSerializer
    queryset = models.Instruction.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class InstructionUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Instruction update
    """
    name = "instruction-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.InstructionSerializer
    queryset = models.Instruction.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})

# BodySystem


class BodySystemCreateAPIView(generics.CreateAPIView):
    """
    Create new frequency
    """
    name = "bodysystem-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.BodySystemSerializer
    queryset = models.BodySystem.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Body system created successfully.", "body_system": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "BodySystem not created", "body_system": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class BodySystemListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "bodysystem-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.BodySystemSerializer

    queryset = models.BodySystem.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class BodySystemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    BodySystem details
    """
    name = "bodysystem-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.BodySystemSerializer
    queryset = models.BodySystem.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


class BodySystemUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    BodySystem update
    """
    name = "body-sytem-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.BodySystemSerializer
    queryset = models.BodySystem.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


# DrugClass


class DrugClassCreateAPIView(generics.CreateAPIView):
    """
    Create new frequency
    """
    name = "drugclass-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DrugClassSerializer
    queryset = models.DrugClass.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Drug class created successfully.", "drug_class": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "DrugClass not created", "drug_class": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DrugClassListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "drugclass-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DrugClassSerializer

    queryset = models.DrugClass.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class DrugClassDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    DrugClass details
    """
    name = "drugclass-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.DrugClassSerializer
    queryset = models.DrugClass.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


class DrugClassUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    DrugClass update
    """
    name = "drugclass-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DrugClassSerializer
    queryset = models.DrugClass.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Sub Class


class DrugSubClassCreateAPIView(generics.CreateAPIView):
    """
    Create new sub class
    """
    name = "drugsubclass-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DrugSubClassSerializer
    queryset = models.DrugSubClass.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Sub class created successfully.", "drug_sub_class": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "DrugSubClass not created", "drug_sub_class": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DrugSubClassListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "drugsubclass-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DrugSubClassSerializer

    queryset = models.DrugSubClass.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class DrugSubClassDetailAPIView(generics.RetrieveAPIView):
    """
    DrugSubClass details
    """
    name = "drugsubclass-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DrugSubClassSerializer
    queryset = models.DrugSubClass.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DrugSubClassUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    DrugSubClass update
    """
    name = "drugsubclass-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DrugSubClassSerializer
    queryset = models.DrugSubClass.objects.all()
    # lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Generic


class GenericCreateAPIView(generics.CreateAPIView):
    """
    Create new generic
    """
    name = "generic-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.GenericSerializer
    queryset = models.Generic.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Generic created successfully.", "generic": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Generic not created", "generic": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class GenericListAPIView(generics.ListAPIView):
    """
    List of generic drugs
    """
    name = "generic-list"
    permission_classes = (SubscribedOrStaffPermission,
                          )
    serializer_class = serializers.GenericSerializer

    queryset = models.Generic.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description',
                     'drug_class__title', 'drug_sub_class__title', )
    ordering_fields = ('title', 'id')


class GenericReferenceListAPIView(generics.ListAPIView):
    """
    List of generic drugs for reference
    """
    name = "generic-list"
    permission_classes = (SubscribedOrStaffPermission,
                          )
    serializer_class = serializers.GenericReferenceSerializer

    queryset = models.Generic.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description',
                     'drug_class__title', 'drug_sub_class__title', )
    ordering_fields = ('title', 'id')


class GenericDetailAPIView(generics.RetrieveAPIView):
    """
    Generic details
    """
    name = "generic-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.GenericSerializer
    queryset = models.Generic.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class GenericUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Generic update
    """
    name = "generic-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.GenericSerializer
    queryset = models.Generic.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Preparation

class PreparationCreateAPIView(generics.CreateAPIView):
    """
    Create new preparation
    """
    name = "preparation-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PreparationSerializer
    queryset = models.Preparation.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Preparation created successfully.", "preparation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Preparation not created", "preparation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PreparationListAPIView(generics.ListAPIView):
    """
    Products list for porfolio, searchable by title or description
    """
    name = "preparation-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PreparationSerializer

    queryset = models.Preparation.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description',
                     'generic__title', 'formulation__title', )
    ordering_fields = ('title', 'id')


class PreparationDetailAPIView(generics.RetrieveAPIView):
    """
    Preparation details
    """
    name = "preparation-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PreparationSerializer
    queryset = models.Preparation.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PreparationUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Generic update
    """
    name = "preparation-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PreparationSerializer
    queryset = models.Preparation.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


# Formulation

class FormulationCreateAPIView(generics.CreateAPIView):
    """
    Create new formulation
    """
    name = "formulation-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.FormulationSerializer
    queryset = models.Formulation.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Formulation created successfully.", "formulation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Formulation not created", "formulation": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class FormulationListAPIView(generics.ListAPIView):
    """
    drug formulations list
    """
    name = "formulation-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.FormulationSerializer

    queryset = models.Formulation.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class FormulationDetailAPIView(generics.RetrieveAPIView):
    """
    Drug formulation details
    """
    name = "formulation-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.FormulationSerializer
    queryset = models.Formulation.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class FormulationUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Generic update
    """
    name = "formulation-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.FormulationSerializer
    queryset = models.Formulation.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable(
            {"message": ["This item cannot be deleted!"]})


# Manufacturer

class ManufacturerCreateAPIView(generics.CreateAPIView):
    """
    Create new manufacturer
    """
    name = "manufacturer-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ManufacturerSerializer
    queryset = models.Manufacturer.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Manufacturer created successfully.", "manufacturer": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Manufacturer not created", "manufacturer": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ManufacturerListAPIView(generics.ListAPIView):
    """
   Manufacturers listing
    """
    name = "manufacturer-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ManufacturerSerializer

    queryset = models.Manufacturer.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description', )
    ordering_fields = ('title', 'id')


class ManufacturerDetailAPIView(generics.RetrieveAPIView):
    """
    Manufacturer details
    """
    name = "manufacturer-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.ManufacturerSerializer
    queryset = models.Manufacturer.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ManufacturerUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Manufacturer update
    """
    name = "manufacturer-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ManufacturerSerializer
    queryset = models.Manufacturer.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Products

class ProductCreateAPIView(generics.CreateAPIView):
    """
    Create new product
    """
    name = "products-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ProductsSerializer
    queryset = models.Products.objects.all()

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
            return Response(data={"message": "Product created successfully.", "product": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Product not created", "product": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ProductListAPIView(generics.ListAPIView):
    """
   Products listing
    """
    name = "products-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ProductsSerializer

    queryset = models.Products.objects.all()

    # Searching and filtering
    search_fields = ('title', 'description',
                     'preparation__title', 'manufacturer__title')
    ordering_fields = ('title', 'description', 'id')


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Product details
    """
    name = "products-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ProductsSerializer
    queryset = models.Products.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ProductUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Product update
    """
    name = "products-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ProductsSerializer
    queryset = models.Products.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ProductImageList(generics.ListCreateAPIView):
    """
    Logged In User
    =================================================================
    1. Add pharmacist photo
    2. View own courier instance
    """
    name = 'productphoto-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImages.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        product_pk = self.kwargs.get("pk")

        serializer.save(facility_id=user.facility_id, created_by=user,
                        product_id=product_pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Product photo created successfully.", "product-image": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Product image not created", "product-image": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(created_by=user)


class ProductImageDetail(generics.RetrieveAPIView):
    """
    Logged in Facility Superintendent
    ================================================================
    1. View details of product photo instance
    """
    name = 'productimage-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImages.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(created_by=user)


# Indications
class IndicationsCreateAPIView(generics.CreateAPIView):
    """
    Create new generic
    """
    name = "indications-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.IndicationsSerializer
    queryset = models.Indications.objects.all()

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
            return Response(data={"message": "Indications created successfully.", "indication": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Indications not created", "indication": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class IndicationsListAPIView(generics.ListAPIView):
    """
    List of indication drugs
    """
    name = "indications-list"
    permission_classes = (SubscribedOrStaffPermission,
                          )
    serializer_class = serializers.IndicationsSerializer

    queryset = models.Indications.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('indication', 'description',
                     'generic__title', )
    ordering_fields = ('generic_title', 'id')


class IndicationsDetailAPIView(generics.RetrieveAPIView):
    """
    Indications details
    """
    name = "indications-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.IndicationsSerializer
    queryset = models.Indications.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class IndicationsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Indications update
    """
    name = "indications-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.IndicationsSerializer
    queryset = models.Indications.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

# Doses


class DosesCreateAPIView(generics.CreateAPIView):
    """
    Create new generic
    """
    name = "doses-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DosesSerializer
    queryset = models.Doses.objects.all()

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
            return Response(data={"message": "Dose created successfully.", "dose": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Doses not created", "dose": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DosesListAPIView(generics.ListAPIView):
    """
    List of indication drugs
    """
    name = "doses-list"
    permission_classes = (SubscribedOrStaffPermission,
                          )
    serializer_class = serializers.DosesSerializer

    queryset = models.Doses.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('dose', 'route__title',
                     'generic__title', 'indication__title', )
    ordering_fields = ('generic__title',)


class DosesDetailAPIView(generics.RetrieveAPIView):
    """
    Doses details
    """
    name = "doses-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DosesSerializer
    queryset = models.Doses.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DosesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Indications update
    """
    name = "doses-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DosesSerializer
    queryset = models.Doses.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

# Mode of action views


class ModeOfActionsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new mode of action
    """
    name = "modeofactions-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ModeOfActionsSerializer
    queryset = models.ModeOfActions.objects.all()

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
            return Response(data={"message": "Mode of action created successfully.", "mode-of-action": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Mode of action not created", "mode-of-action": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ModeOfActionsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ------------------------------------------------
    List of mode of actions
    """
    name = "modeofactions-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ModeOfActionsSerializer

    queryset = models.ModeOfActions.objects.all()

    search_fields = ('mode_of_action',
                     'generic__title', )
    ordering_fields = ('generic_title', 'id')


class ModeOfActionsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ------------------------------------------------------
    Mode of actions details
    """
    name = "modeofactions-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ModeOfActionsSerializer
    queryset = models.ModeOfActions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ModeOfActionsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin user
    ------------------------------------------------------------
    Update mode of action
    """
    name = "modeofactions-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ModeOfActionsSerializer
    queryset = models.ModeOfActions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Contraindications views


class ContraindicationsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new contraindication
    """
    name = "contraindications-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ContraindicationsSerializer
    queryset = models.Contraindications.objects.all()

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
            return Response(data={"message": "Contraindication created successfully.", "contraindication": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Contraindication not created", "contraindication": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ContraindicationsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ------------------------------------------------
    List of contraindications
    """
    name = "contraindications-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ContraindicationsSerializer

    queryset = models.Contraindications.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('title', 'description',
                     'generic__title',)
    ordering_fields = ('generic__title',)


class ContraindicationsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ------------------------------------------------------
    Contraindication details
    """
    name = "contraindications-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ContraindicationsSerializer
    queryset = models.Contraindications.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ContraindicationsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin user
    ------------------------------------------------------------
    Update contraindication
    """
    name = "contraindications-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ContraindicationsSerializer
    queryset = models.Contraindications.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

# Drug Interations views


class InteractionsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new drug interaction
    """
    name = "interactions-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.InteractionsSerializer
    queryset = models.Interactions.objects.all()

    def perform_create(self, serializer):
        try:
            user = self.request.user
            serializer.save(owner=user, facility=user.facility)
        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"response_code": "1", "response_message": f"The two contraindicating drugs must be different"})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Drug interaction created successfully.", "interaction": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Drug interaction not created", "interaction": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class InteractionsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ------------------------------------------------
    List of interactions
    """
    name = "interactions-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.InteractionsSerializer

    queryset = models.Interactions.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('description',
                     'contra_indicated__title', 'generic__title', )
    ordering_fields = ('generic__title')


class InteractionsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ------------------------------------------------------
    Contraindication details
    """
    name = "interactions-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.InteractionsSerializer
    queryset = models.Interactions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class InteractionsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin user
    ------------------------------------------------------------
    Update contraindication
    """
    name = "interactions-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.InteractionsSerializer
    queryset = models.Interactions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

# Drug side effects views


class SideEffectsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new drug side effects
    """
    name = "sideeffects-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SideEffectsSerializer
    queryset = models.SideEffects.objects.all()

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Drug side effect created successfully.", "side-effect": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Drug side effect not created", "side-effect": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class SideEffectsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ------------------------------------------------
    List of side effects
    """
    name = "sideeffects-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SideEffectsSerializer

    queryset = models.SideEffects.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('description',
                     'title', 'generic__title', )
    ordering_fields = ('generic__title')


class SideEffectsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ------------------------------------------------------
    Side effect details
    """
    name = "sideeffects-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SideEffectsSerializer
    queryset = models.SideEffects.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class SideEffectsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin user
    ------------------------------------------------------------
    Update side effect
    """
    name = "sideeffects-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SideEffectsSerializer
    queryset = models.SideEffects.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

# Drug precautions views


class PrecautionsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new drug precaution
    """
    name = "precautions-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PrecautionsSerializer
    queryset = models.Precautions.objects.all()

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Drug precaution created successfully.", "precaution": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Drug precaution not created", "precaution": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PrecautionsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ------------------------------------------------
    List of drug precautions
    """
    name = "precautions-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PrecautionsSerializer

    queryset = models.Precautions.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('description',
                     'title', 'generic__title', )
    ordering_fields = ('generic__title')


class PrecautionsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ------------------------------------------------------
    Precaution details
    """
    name = "precautions-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PrecautionsSerializer
    queryset = models.Precautions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PrecautionsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin user
    ------------------------------------------------------------
    Update precaution
    """
    name = "precautions-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PrecautionsSerializer
    queryset = models.Precautions.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

# Special drug considerations views


class SpecialConsiderationsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new drug special consideration
    """
    name = "specialconsiderations-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SpecialConsiderationsSerializer
    queryset = models.SpecialConsiderations.objects.all()

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Drug special considerations created successfully.", "special-consideration": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Drug special considerations not created", "special-consideration": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class SpecialConsiderationsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ------------------------------------------------
    List of drug special considerations
    """
    name = "specialconsiderations-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SpecialConsiderationsSerializer

    queryset = models.SpecialConsiderations.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('description',
                     'title', 'generic__title', )
    ordering_fields = ('generic__title')


class SpecialConsiderationsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ------------------------------------------------------
    Special considerations details
    """
    name = "specialconsiderations-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SpecialConsiderationsSerializer
    queryset = models.SpecialConsiderations.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class SpecialConsiderationsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin user
    ------------------------------------------------------------
    Update special consideration
    """
    name = "specialconsiderations-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SpecialConsiderationsSerializer
    queryset = models.SpecialConsiderations.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
