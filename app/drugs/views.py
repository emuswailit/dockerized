from core.app_permissions import (
    SubscribedOrStaffPermission)
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, generics, permissions, status
from rest_framework.response import Response

from . import models, serializers

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
            return Response(data={"response_code": 0, "response_message": "Distributor created successfully.",
                                  "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Distributor not created", "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Distributor details updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "0", "response_message": "Distributor details not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code": 0, "response_message": "Posology created successfully.",
                                  "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Posology not created", "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0, "response_message": "Posology entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Posology entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code": 0, "response_message": "Frequency created successfully.",
                                  "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Frequency not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0, "response_message": "Frequency entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Frequency entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code": 0, "response_message": "Instruction entry created successfully.",
                                  "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Instruction entry not created",
                                  "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0, "response_message": "Instruction entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Instruction entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code":0,"response_message": "Body system created successfully.", "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "BodySystem not created",
                                  "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_400_BAD_REQUEST)


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

    # def delete(self, request, *args, **kwargs):
    #     raise exceptions.NotAcceptable(
    #         {"message": ["This item cannot be deleted!"]})


class BodySystemUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Body system update
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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0, "response_message": "Body system entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Body system entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code":0,"response_message": "Drug class created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "DrugClass not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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


class DrugClassDetailAPIView(generics.RetrieveAPIView):
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


class DrugClassUpdateAPIView(generics.UpdateAPIView):
    """
    DrugClass update
    """
    name = "drugclassupdate"
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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Drug class updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Drug class not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code":0,"response_message": "Sub class created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "Drug sub class not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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


class DrugSubClassUpdateAPIView(generics.UpdateAPIView):
    """
    DrugSubClass update
    """
    name = "drugsubclassupdate"
    permission_classes = (permissions.IsAdminUser,
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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Drug sub class updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Drug sub class not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code": 0, "response_message": "Generic created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Generic not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0, "response_message": "Generic updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Generic  was not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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
            return Response(data={"response_code":0,"response_message": "Preparation created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1, "response_message": "Preparation not created",
                                  "preparation": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0, "response_message": "Preparation updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Preparation  was not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)
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
            return Response(data={"response_code": 0, "response_message": "Formulation created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Formulation not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Formulation entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Formulation entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)
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
            return Response(data={"response_code":0,"response_message": "Manufacturer created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":0,"response_message": "Manufacturer not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Manufacturer details updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Manufacturer details not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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
        except IntegrityError:
            raise exceptions.NotAcceptable(
                {"response_code": "1", "response_message": "No repeating entries",
                 "errors": ['%s: %s' % ("duplicate", "Similar entry exists")], })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code":0,"response_message": "Product created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":0,"response_message": "Product not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Product details updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Product details not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code":0,"response_message": "Product photo created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "Product image not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
    errors = []

    def perform_create(self, serializer):
        try:
            user = self.request.user
            serializer.save(owner=user, facility=user.facility)
        except IntegrityError:

            raise exceptions.NotAcceptable(
                {"response_code": "1", "response_message": "No repeating entries",
                 "errors": ['%s: %s' % ("duplicate", "Similar entry exists")], })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code": 0, "response_message": "Indication entry created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Indication entry not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Indication entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Indication entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)
# Doses


# class DosesCreateAPIView(generics.CreateAPIView):
#     """
#     Create new generic
#     """
#     name = "doses-create"
#     permission_classes = (permissions.IsAdminUser,
#                           )
#     serializer_class = serializers.DosesSerializer
#     queryset = models.Doses.objects.all()

#     def perform_create(self, serializer):
#         try:
#             user = self.request.user
#             serializer.save(owner=user, facility=user.facility)
#         except IntegrityError:
#             raise exceptions.NotAcceptable(
#                 {"response_code": "1", "response_message": "No repeating entries"})

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_create(serializer)
#             return Response(data={"message": "Dose created successfully.",
#                                   "dose": serializer.data,  "errors": errors_messages},
#                             status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"message": "Doses not created", "dose": serializer.data,
#                                   "errors": errors_messages}, status=status.HTTP_201_CREATED)


# class DosesListAPIView(generics.ListAPIView):
#     """
#     List of indication drugs
#     """
#     name = "doses-list"
#     permission_classes = (SubscribedOrStaffPermission,
#                           )
#     serializer_class = serializers.DosesSerializer

#     queryset = models.Doses.objects.all()
#     # TODO : Reuse this for filtering by q.

#     search_fields = ('dose', 'route__title',
#                      'generic__title', 'indication__title', )
#     ordering_fields = ('generic__title',)


# class DosesDetailAPIView(generics.RetrieveAPIView):
#     """
#     Doses details
#     """
#     name = "doses-detail"
#     permission_classes = (permissions.IsAuthenticated,
#                           )
#     serializer_class = serializers.DosesSerializer
#     queryset = models.Doses.objects.all()
#     lookup_fields = ('pk',)

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj


# class DosesUpdateAPIView(generics.RetrieveUpdateAPIView):
#     """
#     Indications update
#     """
#     name = "doses-update"
#     permission_classes = (permissions.IsAdminUser,
#                           )
#     serializer_class = serializers.DosesSerializer
#     queryset = models.Doses.objects.all()
#     lookup_fields = ('pk',)

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return obj

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
        except IntegrityError:
            raise exceptions.NotAcceptable(
                {"response_code": "1", "response_message": "No repeating entries",
                 "errors": ['%s: %s' % ("duplicate", "Similar entry exists")], })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code": 0, "response_message": "Mode of action created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 0, "response_message": "Mode of action not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0", "response_message": "Mode of action entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "1", "response_message": "Mode of action entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)
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

        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code": 0, "response_message": "Contraindication entry created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Contraindication entry not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.H)


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
    Distributor update
    """
    name = "contraindication-update"
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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": "0",
                                  "response_message": "Contraindication entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": "0",
                                  "response_message": "Contraindication entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

# class ContraindicationsUpdateAPIView(generics.RetrieveUpdateAPIView):
#     """
#     Admin user
#     ------------------------------------------------------------
#     Update contraindication
#     """
#     name = "contraindicationsupdate"
#     permission_classes = (permissions.IsAdminUser,
#                           )
#     serializer_class = serializers.ContraindicationsSerializer
#     queryset = models.Contraindications.objects.all()
#     lookup_fields = ('pk',)

#     def get_object(self):
#         queryset = self.get_queryset()
#         filter = {}
#         for field in self.lookup_fields:
#             filter[field] = self.kwargs[field]

#         obj = get_object_or_404(queryset, **filter)
#         self.check_object_permissions(self.request, obj)
#         return

#     def update(self, request, *args, **kwargs):
#         """
#         Custom update and return custom message

#         """
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_update(serializer)
#             return Response(data={"response_code": 0, "response_message": "Drug contraindication updated successfully.",
#                                   "bodysystem": serializer.data,  "errors": errors_messages},
#                             status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"response_code": 1, "response_message": "Drug contraindication not updated",
#                                   "generic": serializer.data,  "errors": errors_messages},
#                             status=status.HTTP_400_BAD_REQUEST)

# Drug Interations views


class InteractionsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new drug interaction
    """
    name = "interactions-create"
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = serializers.InteractionsSerializer
    queryset = models.Interactions.objects.all()

    def perform_create(self, serializer):
        
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)
   

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code": 0, "response_message": "Drug interaction created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Drug interaction not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)


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
    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0,
                                  "response_message": "Drug interactions entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1,
                                  "response_message": "Drug interactions entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data={"response_code":0, "response_message": "Drug side effect created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":0, "response_message": "Drug side effect not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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
    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0,
                                  "response_message": "Side effect entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1,
                                  "response_message": "Side effect entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)
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
            return Response(data={"response_code":0,"response_message": "Drug precaution created successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "Drug precaution not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0,
                                  "response_message": "Precaution entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1,
                                  "response_message": "Precaution entry not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)
# Special drug considerations views


class ConsiderationsCreateAPIView(generics.CreateAPIView):
    """
    Admin user
    ----------------------------------------------------
    Create new drug special consideration
    """
    name = "specialconsiderations-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ConsiderationsSerializer
    queryset = models.Considerations.objects.all()

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_code":0,"response_message": "Drug special considerations created successfully.",
                                  "obj": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code":1,"response_message": "Drug special considerations not created",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


class ConsiderationsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    ------------------------------------------------
    List of drug special considerations
    """
    name = "considerations-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ConsiderationsSerializer

    queryset = models.Considerations.objects.all()
    # TODO : Reuse this for filtering by q.

    search_fields = ('description',
                     'title', 'generic__title', )
    ordering_fields = ('generic__title')


class ConsiderationsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ------------------------------------------------------
    Special considerations details
    """
    name = "considerations-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ConsiderationsSerializer
    queryset = models.Considerations.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ConsiderationsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin user
    ------------------------------------------------------------
    Update special consideration
    """
    name = "specialconsiderations-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ConsiderationsSerializer
    queryset = models.Considerations.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
    def update(self, request, *args, **kwargs):
        """
        Custom update and return custom message

        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_code": 0, "response_message": "Special instruction entry updated successfully.",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_code": 1, "response_message": "Special instruction entry  was not updated",
                                  "obj": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_400_BAD_REQUEST)


