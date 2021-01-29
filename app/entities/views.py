from django.db import IntegrityError
from rest_framework import permissions
from rest_framework import generics, exceptions, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from . import serializers
from . import models
from core.views import FacilitySafeViewMixin
from users.models import Facility
from core.permissions import FacilitySuperintendentPermission, ClinicSuperintendentPermission, IsOwner
from django.shortcuts import get_object_or_404
User = get_user_model()



# Professionals Views

class ProfessionalsCreate(FacilitySafeViewMixin, generics.CreateAPIView):

    # TODO : Test this view later
    """
    Logged on user
    ============================================================
    Register as professional

    """
    name = 'professionals-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ProfessionalSerializer
    queryset = models.Professionals.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(ProfessionalsCreate, self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):

        try:
            user = self.request.user
            facility = self.request.user.facility

            if user.is_staff:
                raise exceptions.NotAcceptable("Not for administrators")
            else:
                serializer.save(owner=user, user=user, facility=facility,)

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["User must be to be unique. Similar user is already added!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "You have succesfully registered as a professional", "professional": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Your registration as a professional was not succesful", "professional": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class ProfessionalProfile(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Admin User
    ============================================================
    List of all professionals 

    """
    name = 'professionals-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ProfessionalSerializer
    queryset = models.Professionals.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)


class AllProfessionalsList(generics.ListAPIView):
    """
    Admin User
    ============================================================
    List of all professionals 

    """
    name = 'professionals-list'
    permission_classes = (
        permissions.IsAdminUser,
    )
    serializer_class = serializers.ProfessionalSerializer
    queryset = models.Professionals.objects.all_professionals()

    # search_fields =('dependant__id','dependant__middle_name','dependant__last_name', 'dependant__first_name',)
    # ordering_fields =('dependant__first_name', 'id')


class AvailableProfessionalsList(generics.ListAPIView):
    """
    Clients
    ============================================================
    View list of available  professionals in different clinics

    """
    name = 'professionals-list'
    permission_classes = (
        permissions.IsAdminUser,
    )
    serializer_class = serializers.ProfessionalSerializer
    queryset = models.Professionals.objects.available_professionals()


class ProfessionalDetail(generics.RetrieveAPIView):
    """


    Authenticated users
    -------------------------------------------------------------------
    View details of a given slot id

    """
    name = 'professionals-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ProfessionalSerializer
    queryset = models.Professionals.objects.all()


class ProfessionalUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateAPIView):
    """
    Admin
    ============================================================
    Update professional: set if is verified, is active

    """
    name = 'professionals-detail'
    permission_classes = (
        permissions.IsAdminUser,
    )
    serializer_class = serializers.ProfessionalUpdateSerializer
    queryset = models.Professionals.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class SetProfessionalAvailability(FacilitySafeViewMixin, generics.RetrieveUpdateAPIView):
    """
    Professional
    ============================================================
    Update profile: set self as available for hiring or not

    """
    name = 'professionals-detail'
    permission_classes = (
        permissions.IsAuthenticated, IsOwner
    )
    serializer_class = serializers.ProfessionalAvailabilitySerializer
    queryset = models.Professionals.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


# Not using FacilitySafeView here so that Superintendents can view all pharmacists
class DepartmentCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Clinic Superintendent
    ============================================================
    1. Create a facility specialist clinic

    """
    name = 'department-create'
    permission_classes = (
        ClinicSuperintendentPermission,
    )
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

     
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(request.data['facility'])
        # print(request.data['facility'])

        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Department created successfully.", "department": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Department not created", "department": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class DepartmentsList(generics.ListAPIView):
    """
    Pharmacists
    =============================================
    Retrieve all retrieve all prescriptions forwarded to their facility
    """
    name = "departments-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DepartmentSerializer

    queryset = models.Department.objects.all()

    search_fields = ('title', 'description',)
    ordering_fields = ('title', 'id')

    def get_queryset(self):
        user = self.request.user
        # Ensure that the users belong to the company of the user that is making the request
        # dependant = Dependant.objects.get(owner=self.request.user)
        return super().get_queryset().filter(facility=user.facility)


class AllDepartmentListAPIView(generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all prescriptions for the logged in user's dependants
    """
    name = "department-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DepartmentSerializer

    queryset = models.Department.objects.all()

    search_fields = ('title', 'description',)
    ordering_fields = ('title', 'id')


class DepartmentDetailAPIView(generics.RetrieveAPIView):
    """
    Authorized user
    ---------------------------------------
    View details of a facility specialist clinic
    """
    name = "department-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class UpdateDepartment(generics.RetrieveUpdateAPIView):
    """
    Authorized user
    ---------------------------------------
    Update  a facility specialist clinic
    """
    name = "department-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class ProfessionalAnnualLicenceCreate(FacilitySafeViewMixin, generics.CreateAPIView):

    # TODO : Test this view later
    """
   Clinic Superintendent
    ============================================================
    Create a clinic Profession

    """
    name = 'professionalannuallicence-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.ProfessionalAnnualLicenceSerializer
    queryset = models.ProfessionalAnnualLicence.objects.all()

    def perform_create(self, serializer):

        user = self.request.user
        facility = self.request.user.facility
        # dependant_pk = self.kwargs.get("pk")
        serializer.save(owner=user, facility=facility,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Annual licence succesfully uploaded", "annual-licence": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Annual licence not uploaded", "annual-licence": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


# # Employee views
class EmployeesCreate(FacilitySafeViewMixin, generics.CreateAPIView):

    # TODO : Test this view later
    """
    Logged on user
    ============================================================
    Register as professional

    """
    name = 'employees-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.EmployeesSerializer
    queryset = models.Employees.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(EmployeesCreate, self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):
        try:
            user = self.request.user
            facility = self.request.user.facility
            serializer.save(owner=user, facility=facility,)

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": [f"Professional is already hired in your facility!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Employee succesfully created", "employee": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Employee not created", "employee": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class EmployeeList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Facility Administrator
    ============================================================
    View list of all facility employees
    """
    name = 'employees-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.EmployeesSerializer
    queryset = models.Employees.objects.all()


class EmployeeDetail(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Authorized user
    -----------------------------------------------------
    View details of an employee
    """
    name = 'employees-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.EmployeesSerializer
    queryset = models.Employees.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)
