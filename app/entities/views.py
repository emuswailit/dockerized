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

# Professions Views


# class ProfessionsCreate(generics.CreateAPIView):

#     # TODO : Test this view later
#     """
#    Clinic Superintendent
#     ============================================================
#     Create a clinic Profession

#     """
#     name = 'professions-create'
#     permission_classes = (
#         permissions.IsAdminUser,
#     )
#     serializer_class = serializers.ProfessionSerializer
#     queryset = models.Professions.objects.all()

#     def perform_create(self, serializer):

#         user = self.request.user
#         facility = self.request.user.facility
#         # dependant_pk = self.kwargs.get("pk")
#         serializer.save(owner=user, facility=facility,)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_create(serializer)
#             return Response(data={"message": "Profession succesfully created", "profession": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"message": "Profession not created", "profession": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


# class ProfessionsList(generics.ListAPIView):
#     """
#     Clinic Superintendent
#     ============================================================
#     List of all Professions for own clinic

#     """
#     name = 'professions-list'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.ProfessionSerializer
#     queryset = models.Professions.objects.all()

#     # search_fields =('dependant__id','dependant__middle_name','dependant__last_name', 'dependant__first_name',)
#     # ordering_fields =('dependant__first_name', 'id')


# class ProfessionDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
#     """


#     Authenticated users
#     -------------------------------------------------------------------
#     View details of a given Profession id

#     """
#     name = 'professions-detail'
#     permission_classes = (
#         ClinicSuperintendentPermission,
#     )
#     serializer_class = serializers.ProfessionSerializer
#     queryset = models.Professions.objects.all()


# class ProfessionUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
#     """
#     Admin User
#     ============================================================
#     Update profession created by self

#     """
#     name = 'professions-detail'
#     permission_classes = (
#         permissions.IsAuthenticated, IsOwner
#     )
#     serializer_class = serializers.ProfessionSerializer
#     queryset = models.Professions.objects.all()

#     def get_queryset(self):
#         facility_id = self.request.user.facility_id
#         return super().get_queryset().filter(facility_id=facility_id, owner=self.request.user)


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


class AllProfessionalsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Admin User
    ============================================================
    List of all professionals 

    """
    name = 'professionals-list'
    permission_classes = (
        ClinicSuperintendentPermission,
    )
    serializer_class = serializers.ProfessionalSerializer
    queryset = models.Professionals.objects.all_professionals()

    # search_fields =('dependant__id','dependant__middle_name','dependant__last_name', 'dependant__first_name',)
    # ordering_fields =('dependant__first_name', 'id')


class AvailableProfessionalsList(FacilitySafeViewMixin, generics.ListAPIView):
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


class ProfessionalDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
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

        try:
            user = self.request.user

            serializer.save(owner=user, facility=user.facility)

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": ["Facility clinic item must be to be unique. Similar item is already added!", ]})

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


class PharmacistCreate(generics.CreateAPIView):
    """
    Logged in user
    ==============================================
    1. Register as a pharmacist
    2. User shouldnt have already registered as prescriber or courier
    """
    name = 'pharmacist-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PharmacistSerializer
    queryset = models.Pharmacist.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        facility_id = self.request.user.facility_id
        # # Check if  user is already registered as a pharmacist
        if models.Pharmacist.objects.filter(owner=user).count() > 0:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered in the system as a pharmacist!", ]})
        else:
            pass
        if user.is_prescriber:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered in the system as a prescriber!", ]})
        elif user.is_courier:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered as a courier!", ]})
        else:
            user.is_pharmacist = True
            user.save()
            serializer.save(facility_id=facility_id, owner=user)


class PharmacistList(generics.ListAPIView):
    """
    Admin
    =======================================
    1. View list of all pharmacists
    """
    name = 'pharmacist-list'

    # TODO : Determine who needs this permission
    permission_classes = (
        permissions.IsAdminUser,
    )
    serializer_class = serializers.PharmacistSerializer
    queryset = models.Pharmacist.objects.all_pharmacists()

    # def get_queryset(self):
    #     user = self.request.user
    #     return super().get_queryset().filter(is_active=False)


class AvailablePharmacistList(generics.ListAPIView):
    """
    Facility Superintendent
    =======================================
    1. View list of pharmacists who are available for recruitment
    """
    name = 'pharmacist-list'

    # TODO : Determine who needs this permission
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.PharmacistSerializer
    queryset = models.Pharmacist.objects.available_pharmacists()


class PharmacistDetail(generics.RetrieveAPIView):
    name = 'pharmacist-detail'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.PharmacistSerializer
    queryset = models.Pharmacist.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().all()

# Courier Views


class CourierCreate(generics.CreateAPIView):
    """
    Logged in user
    ==============================================
    1. Register as a courier
    2. User shouldnt have already registered as prescriber or courier
    """
    name = 'courier-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CourierSerializer
    queryset = models.Courier.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        facility_id = self.request.user.facility_id
        # # Check if  user is already registered as a courier
        if models.Courier.objects.filter(owner=user).count() > 0:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered in the system as a courier!", ]})
        else:
            pass
        if user.is_prescriber:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered in the system as a prescriber!", ]})
        elif user.is_pharmacist:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered as a pharmacist!", ]})
        else:
            user.is_courier = True
            user.save()
            serializer.save(facility_id=facility_id, owner=user)


class CourierList(generics.ListAPIView):
    name = 'courier-list'

    # TODO : Determine who needs this permission
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.CourierSerializer
    queryset = models.Courier.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().all()


# Not using view mixin in order to view all
class CourierDetail(generics.RetrieveAPIView):
    name = 'courier-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CourierSerializer
    queryset = models.Courier.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().all()

# Prescriber views


class PrescriberCreate(generics.CreateAPIView):
    """
    Logged in user
    ==============================================
    1. Register as a prescriber
    2. User shouldnt have already registered as prescriber or courier
    """
    name = 'prescriber-create'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriberSerializer
    queryset = models.Prescriber.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        facility_id = self.request.user.facility_id
        # # Check if  user is already registered as a prescriber
        if models.Prescriber.objects.filter(owner=user).count() > 0:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered in the system as a prescriber!", ]})
        else:
            pass
        if user.is_pharmacist:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered in the system as a pharmacist!", ]})
        elif user.is_courier:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered as a courier!", ]})
        else:
            user.is_prescriber = True
            user.save()
            serializer.save(facility_id=facility_id, owner=user)


class PrescriberList(generics.ListAPIView):
    name = 'prescriber-list'

    # TODO : Determine who needs this permission
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.PrescriberSerializer
    queryset = models.Prescriber.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().all()


class AvailablePrescribersList(generics.ListAPIView):
    """
    Facility Superintendent
    =======================================
    1. View list of pharmacists who are available for recruitment
    """
    name = 'prescribers-list'

    # TODO : Determine who needs this permission
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.PrescriberSerializer
    queryset = models.Prescriber.objects.available_prescribers()


class PrescriberDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'prescriber-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriberSerializer
    queryset = models.Prescriber.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().all()

# Pharmacist photo views


# Facility Pharmacist views


class FacilityPharmacistCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Recruit a pharmacist to own facility
    2. Only pharmacists are available
    3. Pharmacist will be set to unavailable immediately after recruitment. Until he s/she sets otherwise
    """
    name = 'facilitypharmacist-create'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityPharmacistSerializer
    queryset = models.FacilityPharmacist.objects.all()

    def perform_create(self, serializer):

        facility_id = self.request.user.facility_id
        pharmacist_pk = self.kwargs.get("pk")

        pharmacist = models.Pharmacist.objects.get(id=pharmacist_pk)

        if pharmacist:
            # facility_pharmacist = models.FacilityPharmacist.objects.get(pharmacist=pharmacist, facility_id=facility_id)

            if models.FacilityPharmacist.objects.filter(pharmacist=pharmacist, facility_id=facility_id).exists():
                facility_pharmacist = models.FacilityPharmacist.objects.get(
                    pharmacist=pharmacist, facility_id=facility_id)
                """
                1. Pharmacist already registered for to this facility
                2. If pharmacist is available, activate him
                """

                if pharmacist.is_available == True:
                    facility_pharmacist.is_active = True
                    facility_pharmacist.save()
                    pharmacist.is_available = False
                    pharmacist.facility = self.request.user.facility
                    pharmacist.save()

                    user = User.objects.get(id=pharmacist.owner_id)
                    user.facility = user.facility
                    user.save()

                    # return  Response(data={"message": "Existing facility pharmacist activated successfully."})
                else:
                    raise exceptions.NotAcceptable(
                        {"detail": ["Pharmacist is not available!", ]})
                    #  return Response(data={"message": "Pharmacist is already engaged elsewhere", "errors": errors_messages}, status=status.HTTP_201_CREATED)

                # raise exceptions.NotAcceptable(
                #     {"detail": ["The pharmacist has already been added to facility!", ]})
            else:
                print(pharmacist_pk)
                print(facility_id)
                # Retrieve the pharmacist object

                if pharmacist.is_available:

                    serializer.save(facility_id=facility_id,
                                    owner=self.request.user, pharmacist=pharmacist)
                    user = User.objects.get(id=pharmacist.owner_id)
                    user.facility_id = facility_id
                    user.save()
                    pharmacist.is_available = False
                    pharmacist.facility_id = facility_id
                    pharmacist.save()
                else:
                    raise exceptions.NotAcceptable(
                        {"detail": ["The pharmacist has not confirmed availability!", ]})
        else:
            raise exceptions.NotAcceptable(
                {"detail": ["The pharmacist has not confirmed availability!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)

            return Response(data={"message": "Facility pharmacist created successfully.", "facility-pharmacist": serializer.validated_data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Facility pharmacist not created", "facility-pharmacist": serializer.validated_data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class AllFacilityPharmacistList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Facility Superintendent
    ============================================================
    1. View list of all pharmacists attached to facility
    """
    name = 'facilitypharmacist-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityPharmacistSerializer
    queryset = models.FacilityPharmacist.objects.all_facility_pharmacists()


class ActiveFacilityPharmacistList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Facility Superintendent
    ============================================================
    1. View list of active pharmacists attached to facility
    """
    name = 'facilitypharmacist-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityPharmacistSerializer
    queryset = models.FacilityPharmacist.objects.active_facility_pharmacists()


class FacilityPharmacistDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'facilitypharmacist-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilityPharmacistSerializer
    queryset = models.FacilityPharmacist.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class FacilityPharmacistUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Set pharmacist as superintendent or not
    2. Activate or deactivate pharmacist
    """
    name = 'facilitypharmacist-detail'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityPharmacistSerializer
    queryset = models.FacilityPharmacist.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def put(self, request, pk=None, **kwargs):
        facility_id = self.request.user.facility_id
        facility_pharmacist_pk = self.kwargs.get("pk")
        facility_pharmacist = models.FacilityPharmacist.objects.get(
            id=facility_pharmacist_pk)
        default_facility = Facility.objects.get(title="Mobipharma")

        if facility_pharmacist and default_facility:
            pharmacist = models.Pharmacist.objects.get(
                id=facility_pharmacist.pharmacist_id)
            if pharmacist:

                user = User.objects.get(id=pharmacist.owner.id)
                if facility_pharmacist.owner.id == request.user.id and pharmacist.owner.id == request.user.id:
                    facility_pharmacist.is_active = True
                    facility_pharmacist.is_superintendent = True
                    facility_pharmacist.save()
                    return Response(data={"message": f"You cannot do this!"})
                else:
                    if facility_pharmacist.is_active == False:
                        facility_pharmacist.is_active = True
                        facility_pharmacist.save()
                        # Set Pharmacist not available for recruitment elsewhere
                        pharmacist.is_available = False
                        pharmacist.facility = request.user.facility
                        pharmacist.save()

                        user.facility = request.user.facility
                        user.save()

                        return Response(data={"message": f"{facility_pharmacist.pharmacist.owner.first_name } {facility_pharmacist.pharmacist.owner.last_name } succesfully activated in your facility"})

                    else:

                        facility_pharmacist.is_active = False
                        facility_pharmacist.is_superintendent = False
                        # facility_pharmacist.pharmacist.is_available=True
                        # facility_pharmacist.facility=default_facility
                        facility_pharmacist.save()

                        pharmacist.is_available = True
                        pharmacist.facility = default_facility
                        pharmacist.save()

                        user.facility = default_facility
                        user.save()

                        # Set the pharmacist as available for recruitment elsewhere

                        return Response(data={"message": f"{facility_pharmacist.pharmacist.owner.first_name } {facility_pharmacist.pharmacist.owner.last_name } succesfully deactivated from facility to {default_facility.title}"})

        else:
            return Response(data={"message": f"Default facility not retrieved"})


class FacilityPharmacistExit(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Set pharmacist as superintendent or not
    2. Activate or deactivate pharmacist
    """
    name = 'facilitypharmacist-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilityPharmacistSerializer
    queryset = models.FacilityPharmacist.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def put(self, request, pk=None, **kwargs):
        facility_id = self.request.user.facility_id
        facility_pharmacist_pk = self.kwargs.get("pk")
        facility_pharmacist = models.FacilityPharmacist.objects.get(
            id=facility_pharmacist_pk)
        user = self.request.user

        if facility_pharmacist:
            pharmacist = models.Pharmacist.objects.get(
                id=facility_pharmacist.pharmacist_id)
            default_facility = Facility.objects.get(title="Mobipharma")
            if pharmacist and pharmacist.id == request.user.id:
                if facility_pharmacist.is_active == True:
                    facility_pharmacist.is_active = False
                    facility_pharmacist.save()
                    # Set Pharmacist not available for recruitment elsewhere
                    pharmacist.is_available = True
                    pharmacist.facility = default_facility
                    pharmacist.save()
                    user.facility = default_facility
                    user.save()
                    return Response(data={"message": f"{facility_pharmacist.pharmacist.owner.first_name } {facility_pharmacist.pharmacist.owner.last_name } succesfully deactivated from your facility"})
            else:
                return Response(data={"message": f"Only the self can quit"})


# class FacilityPrescriberCreate(FacilitySafeViewMixin, generics.CreateAPIView):
#     """
#     Superintendent Pharmacist
#     ============================================================
#     1. Recruit a pharmacist to own facility
#     2. Only pharmacists are available
#     3. Pharmacist will be set to unavailable immediately after recruitment. Until he s/she sets otherwise
#     """
#     name = 'facilityprescriber-create'
#     permission_classes = (
#         FacilitySuperintendentPermission,
#     )
#     serializer_class = serializers.FacilityPrescriberSerializer
#     queryset = models.FacilityPrescriber.objects.all()

#     def perform_create(self, serializer):

#         facility_id = self.request.user.facility_id
#         prescriber_pk = self.kwargs.get("pk")

#         prescriber = models.Prescriber.objects.get(id=prescriber_pk)

#         if prescriber:
#             # facility_pharmacist = models.FacilityPrescriber.objects.get(pharmacist=pharmacist, facility_id=facility_id)

#             if models.FacilityPrescriber.objects.filter(prescriber=prescriber, facility_id=facility_id).exists():
#                 facility_prescriber = models.FacilityPrescriber.objects.get(
#                     prescriber=prescriber, facility_id=facility_id)
#                 """
#                 1. Pharmacist already registered for to this facility
#                 2. If pharmacist is available, activate him
#                 """

#                 if prescriber.is_available == True:
#                     facility_prescriber.is_active = True
#                     facility_prescriber.save()
#                     prescriber.is_available = False
#                     prescriber.facility = self.request.user.facility
#                     prescriber.save()

#                     user = User.objects.get(id=prescriber.owner_id)
#                     user.facility = user.facility
#                     user.save()

#                     # return  Response(data={"message": "Existing facility pharmacist activated successfully."})
#                 else:
#                     raise exceptions.NotAcceptable(
#                         {"detail": ["Prescriber is not available!", ]})
#                     #  return Response(data={"message": "Pharmacist is already engaged elsewhere", "errors": errors_messages}, status=status.HTTP_201_CREATED)

#                 # raise exceptions.NotAcceptable(
#                 #     {"detail": ["The pharmacist has already been added to facility!", ]})
#             else:

#                 # Retrieve the pharmacist object

#                 if prescriber.is_available:

#                     serializer.save(facility_id=facility_id,
#                                     owner=self.request.user, prescriber=prescriber)
#                     user = User.objects.get(id=prescriber.owner_id)
#                     user.facility_id = facility_id
#                     user.save()
#                     prescriber.is_available = False
#                     prescriber.facility_id = facility_id
#                     prescriber.save()
#                 else:
#                     raise exceptions.NotAcceptable(
#                         {"detail": ["The prescriber has not confirmed availability!", ]})
#         else:
#             raise exceptions.NotAcceptable(
#                 {"detail": ["The prescriber has not confirmed availability!", ]})

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             errors_messages = []
#             self.perform_create(serializer)

#             return Response(data={"message": "Facility prescriber created successfully.", "facility-prescriber": serializer.validated_data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
#         else:
#             default_errors = serializer.errors  # default errors dict
#             errors_messages = []
#             for field_name, field_errors in default_errors.items():
#                 for field_error in field_errors:
#                     error_message = '%s: %s' % (field_name, field_error)
#                     errors_messages.append(error_message)

#             return Response(data={"message": "Facility prescriber not created", "facility-prescriber": serializer.validated_data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


# class AllFacilityPrescriberList(FacilitySafeViewMixin, generics.ListAPIView):
#     """
#     Facility Superintendent
#     ============================================================
#     1. View list of all pharmacists attached to facility
#     """
#     name = 'facilitypharmacist-list'
#     permission_classes = (
#         FacilitySuperintendentPermission,
#     )
#     serializer_class = serializers.FacilityPrescriberSerializer
#     queryset = models.FacilityPrescriber.objects.all_facility_prescribers()


# class ActiveFacilityPrescriberList(FacilitySafeViewMixin, generics.ListAPIView):
#     """
#     Facility Superintendent
#     ============================================================
#     1. View list of active pharmacists attached to facility
#     """
#     name = 'facilityprescriber-list'
#     permission_classes = (
#         FacilitySuperintendentPermission,
#     )
#     serializer_class = serializers.FacilityPrescriberSerializer
#     queryset = models.FacilityPrescriber.objects.active_facility_prescribers()


# class FacilityPrescriberDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
#     name = 'facilityprescriber-detail'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.FacilityPrescriberSerializer
#     queryset = models.FacilityPrescriber.objects.all()

#     def get_queryset(self):
#         facility_id = self.request.user.facility_id
#         return super().get_queryset().filter(facility_id=facility_id)


# class FacilityPrescriberDeactivate(FacilitySafeViewMixin, generics.RetrieveUpdateAPIView):
#     """
#     Superintendent Prescriber
#     ============================================================
#     1. Set prescriber as superintendent or not
#     2. Activate or deactivate prescriber
#     """
#     name = 'facilityprescriber-detail'
#     permission_classes = (
#         FacilitySuperintendentPermission,
#     )
#     serializer_class = serializers.FacilityPrescriberSerializer
#     queryset = models.FacilityPrescriber.objects.all()

#     def get_queryset(self):
#         facility_id = self.request.user.facility_id
#         return super().get_queryset().filter(facility_id=facility_id)

#     def put(self, request, pk=None, **kwargs):
#         facility_id = self.request.user.facility_id
#         facility_prescriber_pk = self.kwargs.get("pk")

#         facility_prescriber = models.FacilityPrescriber.objects.get(
#             id=facility_prescriber_pk)

#         default_facility = Facility.objects.get(title="Mobipharma")

#         if facility_prescriber and default_facility:
#             prescriber = models.Prescriber.objects.get(
#                 id=facility_prescriber.prescriber_id)
#             if prescriber:

#                 user = User.objects.get(id=prescriber.owner.id)
#                 if facility_prescriber.owner.id == request.user.id and prescriber.owner.id == request.user.id:
#                     facility_prescriber.is_active = True
#                     facility_prescriber.is_superintendent = True
#                     facility_prescriber.save()
#                     return Response(data={"message": f"You cannot do this!"})
#                 else:
#                     if facility_prescriber.is_active == False:
#                         facility_prescriber.is_active = True
#                         facility_prescriber.save()
#                         # Set Pharmacist not available for recruitment elsewhere
#                         prescriber.is_available = False
#                         prescriber.facility = request.user.facility
#                         prescriber.save()

#                         user.facility = request.user.facility
#                         user.save()

#                         return Response(data={"message": f"{facility_prescriber.prescriber.owner.first_name } {facility_prescriber.prescriber.owner.last_name } succesfully activated in your facility"})

#                     else:

#                         facility_prescriber.is_active = False
#                         facility_prescriber.is_superintendent = False
#                         # facility_prescriber.prescriber.is_available=True
#                         # facility_prescriber.facility=default_facility
#                         facility_prescriber.save()

#                         prescriber.is_available = True
#                         prescriber.facility = default_facility
#                         prescriber.save()

#                         user.facility = default_facility
#                         user.save()

#                         # Set the prescriber as available for recruitment elsewhere

#                         return Response(data={"message": f"{facility_prescriber.prescriber.owner.first_name } {facility_prescriber.prescriber.owner.last_name } succesfully deactivated from facility to {default_facility.title}"})

#         else:
#             return Response(data={"message": f"Default facility not retrieved"})


# class FacilityPrescriberExit(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
#     """
#     Superintendent Prescriber
#     ============================================================
#     1. Set pharmacist as superintendent or not
#     2. Activate or deactivate pharmacist
#     """
#     name = 'facilityprescriber-detail'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.FacilityPrescriberSerializer
#     queryset = models.FacilityPrescriber.objects.all()

#     def get_queryset(self):
#         facility_id = self.request.user.facility_id
#         return super().get_queryset().filter(facility_id=facility_id)

#     def put(self, request, pk=None, **kwargs):
#         facility_id = self.request.user.facility_id
#         facility_prescriber_pk = self.kwargs.get("pk")
#         facility_prescriber = models.FacilityPrescriber.objects.get(
#             id=facility_prescriber_pk)
#         user = self.request.user

#         if facility_prescriber:
#             prescriber = models.Pharmacist.objects.get(
#                 id=facility_prescriber.prescriber_id)
#             default_facility = Facility.objects.get(title="Mobipharma")
#             if prescriber and prescriber.id == request.user.id:
#                 if facility_prescriber.is_active == True:
#                     facility_prescriber.is_active = False
#                     facility_prescriber.save()
#                     # Set Pharmacist not available for recruitment elsewhere
#                     prescriber.is_available = True
#                     prescriber.facility = default_facility
#                     prescriber.save()
#                     user.facility = default_facility
#                     user.save()
#                     return Response(data={"message": f"{facility_prescriber.prescriber.owner.first_name } {facility_prescriber.prescriber.owner.last_name } succesfully deactivated from your facility"})
#             else:
#                 return Response(data={"message": f"Only the self can quit"})

# Facility Courier views


class FacilityCourierCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Facility Superintendent 
    ============================================================
    1. Recruit a courier to own facility
    2. Only courier who have confirmed availability can be recruited
    3. Prescriber will be set to unavailable immediately after recruitment. Until he s/she sets otherwise
    """
    name = 'facilitycourier-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityCourierSerializer
    queryset = models.FacilityCourier.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        facility_id = self.request.user.facility_id
        courier_pk = self.kwargs.get("pk")

        courier = models.Courier.objects.get(id=courier_pk)

        if courier:

            if models.FacilityCourier.objects.filter(courier=courier, facility_id=facility_id).exists():
                raise exceptions.NotAcceptable(
                    {"detail": ["The courier has already been added to facility!", ]})
            else:
                print(courier_pk)
                print(facility_id)
                # Retrieve the courier object

                if courier.is_available:

                    serializer.save(facility_id=facility_id,
                                    owner=user, courier=courier)
                    user = User.objects.get(id=courier.owner_id)
                    user.facility_id = facility_id
                    user.save()
                    courier.is_available = False
                    courier.save()
                else:
                    raise exceptions.NotAcceptable(
                        {"detail": ["The courier has not confirmed availability!", ]})
        else:
            raise exceptions.NotAcceptable(
                {"detail": ["The courier has not confirmed availability!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Facility courier created successfully.", "facility-courier": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Facility courier not created", "facility-courier": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class FacilityCourierList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Facility Superintendent 
    ============================================================
    1. List of all couriers attached to facility

    """
    name = 'facilitycourier-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityCourierSerializer
    queryset = models.FacilityCourier.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class FacilityCourierDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'facilitycourier-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilityCourierSerializer
    queryset = models.FacilityCourier.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class FacilityCourierUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Facility Superintendent 
    ============================================================
    1. Set courier as superintendent or not
    2. Activate or deactivate courier
    """
    name = 'facilitycourier-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilityCourierSerializer
    queryset = models.FacilityCourier.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def delete(self, request, pk=None, **kwargs):

        facility_id = self.request.user.facility_id
        facility_courier_pk = self.kwargs.get("pk")
        print(facility_courier_pk)
        # Retrieve the courier object
        facility_courier = models.FacilityCourier.objects.get(
            id=facility_courier_pk)
        if facility_courier:
            courier = models.Courier.objects.get(
                id=facility_courier.courier_id)
            if courier:
                if courier.owner == self.request.user:

                    raise exceptions.NotAcceptable(
                        {"detail": ["This is your place. You cannot quit!", ]})
                else:

                    print(courier.owner.first_name)
                    user = User.objects.get(id=courier.owner_id)
                    print(user.first_name)

                    default_facility = Facility.objects.get(title="Mobipharma")
                    if default_facility:

                        user.facility = default_facility
                        user.save()
                        courier.facility = default_facility
                        courier.is_available = True
                        courier.save()
                        facility_courier.facility = default_facility
                        facility_courier.is_active = False
                        facility_courier.save()

                        return Response(data={"message": "Courier succesfully removed from your facility"})

                    else:
                        raise exceptions.NotAcceptable(
                            {"detail": ["The courier has not confirmed availability!", ]})
            else:
                raise exceptions.NotAcceptable(
                    {"detail": ["Prescriber details could not be retrieved!", ]})


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
