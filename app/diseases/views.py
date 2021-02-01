from django.shortcuts import render
from rest_framework import generics, permissions, exceptions, status
from . import serializers, models
from rest_framework.response import Response

# Create your views here.


class DiseaseCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new payment method
    """
    name = "diseases-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseSerializer
    queryset = models.Diseases.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Disease created successfully.", "disease": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Disease not created", "disease": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DiseaseListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of payment methods
    """
    name = "diseases-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiseaseSerializer

    queryset = models.Diseases.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DiseaseListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(DiseaseListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class DiseaseDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a payment method
    """
    name = "diseases-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.DiseaseSerializer
    queryset = models.Diseases.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DiseaseUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update payment method details
    """
    name = "diseases-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseSerializer
    queryset = models.Diseases.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Diseases notes
class DiseaseNotesCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new payment method
    """
    name = "diseasenotes-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseNotesSerializer
    queryset = models.DiseaseNotes.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Disease note created successfully.", "disease-notes": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Disease note not created", "disease-notes": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DiseaseNotesListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of payment methods
    """
    name = "diseasenotes-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiseaseNotesSerializer

    queryset = models.DiseaseNotes.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DiseaseNotesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(DiseaseNotesListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class DiseaseNotesDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a payment method
    """
    name = "diseasenotes-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.DiseaseNotesSerializer
    queryset = models.DiseaseNotes.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DiseaseNotesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update payment method details
    """
    name = "diseasenotes-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseNotesSerializer
    queryset = models.DiseaseNotes.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Signs and symptoms
class SignsAndSymptomsCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new signs and symptoms entry
    """
    name = "signsandsymptoms-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SignsAndSymptomsSerializer
    queryset = models.SignsAndSymptoms.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Signs or symptom created successfully.", "signs-and-symptoms": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Signs or symptom not created", "signs-and-symptoms": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class SignsAndSymptomsListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of signs and symptoms entries
    """
    name = "signsandsymptoms-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SignsAndSymptomsSerializer

    queryset = models.SignsAndSymptoms.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(SignsAndSymptomsListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(SignsAndSymptomsListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class SignsAndSymptomsDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a signs and symptoms entry
    """
    name = "signsandsymptoms-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SignsAndSymptomsSerializer
    queryset = models.SignsAndSymptoms.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class SignsAndSymptomsUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update signs and symptoms
    """
    name = "signsandsymptoms-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SignsAndSymptomsSerializer
    queryset = models.SignsAndSymptoms.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Diagnosis views
class DiagnosisCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new diagnosis entry
    """
    name = "diagnosis-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiagnosisSerializer
    queryset = models.Diagnosis.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Diagnosis created successfully.", "diagnosis": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Diagnosis not created", "diagnosis": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DiagnosisListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of diagnosis entries
    """
    name = "diagnosis-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiagnosisSerializer

    queryset = models.Diagnosis.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DiagnosisListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(DiagnosisListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class DiagnosisDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a diagnosis entry
    """
    name = "diagnosis-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiagnosisSerializer
    queryset = models.Diagnosis.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DiagnosisUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update diagnosis
    """
    name = "diagnosis-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiagnosisSerializer
    queryset = models.Diagnosis.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Differential Diagnosis views
class DifferentialDiagnosisCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new diagnosis entry
    """
    name = "differentialdiagnosis-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DifferentialDiagnosisSerializer
    queryset = models.DifferentialDiagnosis.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Differential diagnosis created successfully.", "differential-diagnosis": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Differential diagnosis not created", "differential-diagnosis": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DifferentialDiagnosisListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of diagnosis entries
    """
    name = "differentialdiagnosis-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DifferentialDiagnosisSerializer

    queryset = models.DifferentialDiagnosis.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DifferentialDiagnosisListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(DifferentialDiagnosisListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class DifferentialDiagnosisDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a diagnosis entry
    """
    name = "differentialdiagnosis-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DifferentialDiagnosisSerializer
    queryset = models.DifferentialDiagnosis.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DifferentialDiagnosisUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update diagnosis
    """
    name = "differentialdiagnosis-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DifferentialDiagnosisSerializer
    queryset = models.DifferentialDiagnosis.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Management views
class ManagementCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new diagnosis entry
    """
    name = "management-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ManagementSerializer
    queryset = models.Management.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Disease management method created successfully.", "management": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Disease management method not created", "management": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ManagementListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of management entries
    """
    name = "management-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ManagementSerializer

    queryset = models.Management.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(ManagementListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(ManagementListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class ManagementDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a management entry
    """
    name = "management-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.ManagementSerializer
    queryset = models.Management.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ManagementUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update management
    """
    name = "management-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.ManagementSerializer
    queryset = models.Management.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Prevention views
class PreventionCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new diagnosis entry
    """
    name = "prevention-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PreventionSerializer
    queryset = models.Prevention.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Prevention method created successfully.", "prevention": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Prevention method not created", "prevention": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PreventionListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of prevention entries
    """
    name = "prevention-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PreventionSerializer

    queryset = models.Prevention.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(PreventionListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(PreventionListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class PreventionDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a prevention entry
    """
    name = "prevention-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PreventionSerializer
    queryset = models.Prevention.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class PreventionUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update prevention
    """
    name = "prevention-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.PreventionSerializer
    queryset = models.Prevention.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Disease stages views
class DiseaseStagesCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new disease stages entry
    """
    name = "diseasestages-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseStagesSerializer
    queryset = models.DiseaseStages.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Disease stage created successfully.", "disease-stage": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Disease stage not created", "disease-stage": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DiseaseStagesListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of disease stages entries
    """
    name = "diseasestages-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiseaseStagesSerializer

    queryset = models.DiseaseStages.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DiseaseStagesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(DiseaseStagesListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class DiseaseStagesDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a diseasestages entry
    """
    name = "diseasestages-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiseaseStagesSerializer
    queryset = models.DiseaseStages.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DiseaseStagesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update disease stages
    """
    name = "diseasestages-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseStagesSerializer
    queryset = models.DiseaseStages.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Disease stage categories views
class DiseaseStageCategoriesCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new disease stages entry
    """
    name = "diseasestagecategories-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseStageCategoriesSerializer
    queryset = models.DiseaseStageCategories.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Disease stage category created successfully.", "stage-category": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Disease stage category not created", "stage-category": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DiseaseStageCategoriesListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of disease stages entries
    """
    name = "diseasestagecategories-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiseaseStageCategoriesSerializer

    queryset = models.DiseaseStageCategories.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(DiseaseStageCategoriesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(DiseaseStageCategoriesListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class DiseaseStageCategoriesDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a diseasestagecategories entry
    """
    name = "diseasestagecategories-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DiseaseStageCategoriesSerializer
    queryset = models.DiseaseStageCategories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DiseaseStageCategoriesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update disease stages
    """
    name = "diseasestagecategories-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DiseaseStageCategoriesSerializer
    queryset = models.DiseaseStageCategories.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

# Sources views


class SourcesCreateAPIView(generics.CreateAPIView):
    """
    Admin
    ---------------------------------------------
    Create new diagnosis entry
    """
    name = "sources-create"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SourcesSerializer
    queryset = models.Sources.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Source created successfully.", "sources": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Source not created", "sources": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class SourcesListAPIView(generics.ListAPIView):
    """
    Authenticated user
    -------------------------------------------
    View listing of sources entries
    """
    name = "sources-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SourcesSerializer

    queryset = models.Sources.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(SourcesListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super(SourcesListAPIView,
                   self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs.filter(owner=user)


class SourcesDetailAPIView(generics.RetrieveAPIView):
    """
    Authenticated user
    ----------------------------------------
    View details of a sources entry
    """
    name = "sources-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.SourcesSerializer
    queryset = models.Sources.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class SourcesUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin
    ------------------------------
    Update sources
    """
    name = "sources-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.SourcesSerializer
    queryset = models.Sources.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
