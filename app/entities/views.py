from django.db import IntegrityError
from rest_framework import permissions
from rest_framework import generics, exceptions, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from . import serializers
from . import models
from core.views import FacilitySafeViewMixin
from users.models import Facility
from core.permissions import FacilitySuperintendentPermission
User = get_user_model()

# Not using FacilitySafeView here so that Superintendents can view all pharmacists


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
    queryset = models.Pharmacist.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(is_available=True)


class PharmacistDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'pharmacist-detail'
    permission_classes = (
        permissions.IsAuthenticated,
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


class PharmacistPhotoList(FacilitySafeViewMixin, generics.ListCreateAPIView):
    """
    Logged In User
    =================================================================
    1. Add pharmacist photo
    2. View own courier instance
    """
    name = 'pharmacistphoto-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PharmacistPhotoSerializer
    queryset = models.PharmacistPhoto.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        pharmacist_pk = self.kwargs.get("pk")
        facility_id = self.request.user.facility_id
        serializer.save(facility_id=facility_id, owner=user,
                        pharmacist_id=pharmacist_pk)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class PharmacistPhotoDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    """
    Logged in pharmacist
    ================================================================
    1. View details of photo instance

    """
    name = 'pharmacistphoto-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PharmacistPhotoSerializer
    queryset = models.PharmacistPhoto.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)

# Courier photo views


class CourierPhotoList(FacilitySafeViewMixin, generics.ListCreateAPIView):
    """
    Logged In User
    =================================================================
    1. Add courier photo
    2. View own courier instance
    """
    name = 'courierphoto-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CourierPhotoSerializer
    queryset = models.CourierPhoto.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        courier_pk = self.kwargs.get("pk")
        facility_id = self.request.user.facility_id
        serializer.save(facility_id=facility_id, owner=user,
                        courier_id=courier_pk)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class CourierPhotoDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    """
    Logged in courier
    ================================================================
    1. View details of photo instance

    """
    name = 'courierphoto-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CourierPhotoSerializer
    queryset = models.CourierPhoto.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


# Prescriber photos
class PrescriberPhotoList(FacilitySafeViewMixin, generics.ListCreateAPIView):
    """
    Logged In User
    =================================================================
    1. Add prescriber photo
    2. View own prescriber instance
    """
    name = 'prescriberphoto-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriberPhotoSerializer
    queryset = models.PrescriberPhoto.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        prescriber_pk = self.kwargs.get("pk")
        facility_id = self.request.user.facility_id
        serializer.save(facility_id=facility_id, owner=user,
                        prescriber_id=prescriber_pk)

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class PrescriberPhotoDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    """
    Logged in prescriber
    ================================================================
    1. View details of photo instance

    """
    name = 'prescriberphoto-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriberPhotoSerializer
    queryset = models.PrescriberPhoto.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)

# Facility Pharmacist views


class FacilityPharmacistCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Recruit a pharmacist to own facility
    2. Only pharmacists who have confirmed availability can be recruited
    3. Pharmacist will be set to unavailable immediately after recruitment. Until he s/she sets otherwise
    """
    name = 'facilitypharmacist-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityPharmacistSerializer
    queryset = models.FacilityPharmacist.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        facility_id = self.request.user.facility_id
        pharmacist_pk = self.kwargs.get("pk")

        pharmacist = models.Pharmacist.objects.get(id=pharmacist_pk)

        if pharmacist:

            if models.FacilityPharmacist.objects.filter(pharmacist=pharmacist, facility_id=facility_id).exists():
                raise exceptions.NotAcceptable(
                    {"detail": ["The pharmacist has already been added to facility!", ]})
            else:
                print(pharmacist_pk)
                print(facility_id)
                # Retrieve the pharmacist object

                if pharmacist.is_available:

                    serializer.save(facility_id=facility_id,
                                    owner=user, pharmacist=pharmacist)
                    user = User.objects.get(id=pharmacist.owner_id)
                    user.facility_id = facility_id
                    user.save()
                    pharmacist.is_available = False
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
            return Response(data={"message": "Facility pharmacist created successfully.", "facility-pharmacist": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Facility pharmacist not created", "facility-pharmacist": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class FacilityPharmacistList(FacilitySafeViewMixin, generics.ListAPIView):
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
    queryset = models.FacilityPharmacist.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


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


class FacilityPharmacistUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
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

    def delete(self, request, pk=None, **kwargs):

        facility_id = self.request.user.facility_id
        facility_pharmacist_pk = self.kwargs.get("pk")
        print(facility_pharmacist_pk)
        # Retrieve the pharmacist object
        facility_pharmacist = models.FacilityPharmacist.objects.get(
            id=facility_pharmacist_pk)
        if facility_pharmacist:
            pharmacist = models.Pharmacist.objects.get(
                id=facility_pharmacist.pharmacist_id)
            if pharmacist:
                if pharmacist.owner == self.request.user:

                    raise exceptions.NotAcceptable(
                        {"detail": ["This is your place. You cannot quit!", ]})
                else:

                    print(pharmacist.owner.first_name)
                    user = User.objects.get(id=pharmacist.owner_id)
                    print(user.first_name)

                    default_facility = Facility.objects.get(title="Mobipharma")
                    if default_facility:

                        user.facility = default_facility
                        user.save()
                        pharmacist.facility = default_facility
                        pharmacist.is_available = True
                        pharmacist.save()
                        facility_pharmacist.facility = default_facility
                        facility_pharmacist.is_active = False
                        facility_pharmacist.is_superintendent = False
                        facility_pharmacist.save()

                        return Response(data={"message": "Pharmacist succesfully removed from pharmacy"})

                    else:
                        raise exceptions.NotAcceptable(
                            {"detail": ["The pharmacist has not confirmed availability!", ]})
            else:
                raise exceptions.NotAcceptable(
                    {"detail": ["Pharmacist details could not be retrieved!", ]})


# Facility Prescriber views
class FacilityPrescriberCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Superintendent Prescriber
    ============================================================
    1. Recruit a prescriber to own facility
    2. Only prescriber who have confirmed availability can be recruited
    3. Prescriber will be set to unavailable immediately after recruitment. Until he s/she sets otherwise
    """
    name = 'facilityprescriber-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityPrescriberSerializer
    queryset = models.FacilityPrescriber.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        facility_id = self.request.user.facility_id
        prescriber_pk = self.kwargs.get("pk")

        prescriber = models.Prescriber.objects.get(id=prescriber_pk)

        if prescriber:

            if models.FacilityPrescriber.objects.filter(prescriber=prescriber, facility_id=facility_id).exists():
                raise exceptions.NotAcceptable(
                    {"detail": ["The prescriber has already been added to facility!", ]})
            else:
                print(prescriber_pk)
                print(facility_id)
                # Retrieve the prescriber object

                if prescriber.is_available:

                    serializer.save(facility_id=facility_id,
                                    owner=user, prescriber=prescriber)
                    user = User.objects.get(id=prescriber.owner_id)
                    user.facility_id = facility_id
                    user.save()
                    prescriber.is_available = False
                    prescriber.save()
                else:
                    raise exceptions.NotAcceptable(
                        {"detail": ["The prescriber has not confirmed availability!", ]})
        else:
            raise exceptions.NotAcceptable(
                {"detail": ["The prescriber has not confirmed availability!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Facility prescriber created successfully.", "facility-prescriber": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Facility prescriber not created", "facility-prescriber": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class FacilityPrescriberList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Superintendent Prescriber
    ============================================================
    1. List of all prescribers attached to facility

    """
    name = 'facilityprescriber-list'
    permission_classes = (
        FacilitySuperintendentPermission,
    )
    serializer_class = serializers.FacilityPrescriberSerializer
    queryset = models.FacilityPrescriber.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class FacilityPrescriberDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'facilityprescriber-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilityPrescriberSerializer
    queryset = models.FacilityPrescriber.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class FacilityPrescriberUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Prescriber
    ============================================================
    1. Set prescriber as superintendent or not
    2. Activate or deactivate prescriber
    """
    name = 'facilityprescriber-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilityPrescriberSerializer
    queryset = models.FacilityPrescriber.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def delete(self, request, pk=None, **kwargs):

        facility_id = self.request.user.facility_id
        facility_prescriber_pk = self.kwargs.get("pk")
        print(facility_prescriber_pk)
        # Retrieve the prescriber object
        facility_prescriber = models.FacilityPrescriber.objects.get(
            id=facility_prescriber_pk)
        if facility_prescriber:
            prescriber = models.Prescriber.objects.get(
                id=facility_prescriber.prescriber_id)
            if prescriber:
                if prescriber.owner == self.request.user:

                    raise exceptions.NotAcceptable(
                        {"detail": ["This is your place. You cannot quit!", ]})
                else:

                    print(prescriber.owner.first_name)
                    user = User.objects.get(id=prescriber.owner_id)
                    print(user.first_name)

                    default_facility = Facility.objects.get(title="Mobipharma")
                    if default_facility:

                        user.facility = default_facility
                        user.save()
                        prescriber.facility = default_facility
                        prescriber.is_available = True
                        prescriber.save()
                        facility_prescriber.facility = default_facility
                        facility_prescriber.is_active = False
                        facility_prescriber.is_superintendent = False
                        facility_prescriber.save()

                        return Response(data={"message": "Prescriber succesfully removed from your facility"})

                    else:
                        raise exceptions.NotAcceptable(
                            {"detail": ["The prescriber has not confirmed availability!", ]})
            else:
                raise exceptions.NotAcceptable(
                    {"detail": ["Prescriber details could not be retrieved!", ]})


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
