from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, permissions, status, exceptions
from . import serializers
from . import models
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_countries.serializers import CountryFieldMixin


# Distributors


class DistributorCreateAPIView(generics.CreateAPIView):
    """
    Create new disributor
    """
    name = "distributor-create"
    permission_classes = (permissions.IsAuthenticated,
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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.DistributorSerializer

    queryset = models.Distributor.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DistributorListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DistributorListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class DistributorDetailAPIView(generics.RetrieveAPIView):
    """
    Distributor details
    """
    name = "distributor-detail"
    permission_classes = (permissions.AllowAny,
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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PosologySerializer

    queryset = models.Posology.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PosologyListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(PosologyListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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

    def get_context_data(self, *args, **kwargs):
        context = super(FrequencyListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FrequencyListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.InstructionSerializer

    queryset = models.Instruction.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(InstructionListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(InstructionListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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
    permission_classes = (permissions.IsAuthenticated,
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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.BodySystemSerializer

    queryset = models.BodySystem.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(BodySystemListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(BodySystemListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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
    permission_classes = (permissions.IsAuthenticated,
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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.DrugClassSerializer

    queryset = models.DrugClass.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DrugClassListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DrugClassListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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
    permission_classes = (permissions.IsAuthenticated,
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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.DrugSubClassSerializer

    queryset = models.DrugSubClass.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DrugSubClassListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(DrugSubClassListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class DrugSubClassDetailAPIView(generics.RetrieveAPIView):
    """
    DrugSubClass details
    """
    name = "drugsubclass-detail"
    permission_classes = (permissions.AllowAny,
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
    permission_classes = (permissions.IsAuthenticated,
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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.GenericSerializer

    queryset = models.Generic.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(GenericListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(GenericListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class GenericDetailAPIView(generics.RetrieveAPIView):
    """
    Generic details
    """
    name = "generic-detail"
    permission_classes = (permissions.AllowAny,
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
    permission_classes = (permissions.IsAuthenticated,
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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.PreparationSerializer

    queryset = models.Preparation.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PreparationListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(PreparationListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.FormulationSerializer

    queryset = models.Formulation.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(FormulationListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(FormulationListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.ManufacturerSerializer

    queryset = models.Manufacturer.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(ManufacturerListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ManufacturerListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


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


# Product

class ProductCreateAPIView(generics.CreateAPIView):
    """
    Create new product
    """
    name = "product-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

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
    name = "product-list"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.ProductSerializer

    queryset = models.Product.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Product details
    """
    name = "product-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
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
    name = "product-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
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
    queryset = models.ProductImage.objects.all()

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
    queryset = models.ProductImage.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(created_by=user)
