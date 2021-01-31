from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated, NotAcceptable
from django.shortcuts import get_object_or_404
from users.models import Facility


class FacilityAdministratorPermission(permissions.BasePermission):
    """Facility administrator permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            return request.user.is_administrator
        else:
            raise NotAcceptable("Administrators only")


class FacilitySuperintendentPermission(permissions.BasePermission):
    """Facility superintendent permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print(request.user.role)
            return request.user.is_pharmacist and request.user.is_superintendent
        else:
            raise NotAcceptable("Superintendents only")


class ClinicSuperintendentPermission(permissions.BasePermission):
    """Medical superintendent permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print(request.user.role)
            return request.user.is_prescriber and request.user.is_superintendent
        else:
            raise NotAcceptable("Med Sups only")


class SubscribedOrStaffPermission(permissions.BasePermission):
    """Subscribed or Staff permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print(request.user.facility.is_subscribed)

            if request.user.facility.is_subscribed or request.user.is_staff:
                return True
            else:
                raise NotAcceptable(
                    {"response_code": 1, "response_message": "You are not authorized to view this content: admins or subscribed users only"})


class ConsultationPermission(permissions.BasePermission):
    """Permissions for users who can create consultations: doctors and clinical officers"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            if not user.cadre:
                raise NotAcceptable(
                    {"response_code": 1, "response_message": "You are not registered as a professional"})

            if user.cadre.cluster == "CONSULTATION":
                return True
            else:
                raise NotAcceptable(
                    {"response_code": 1, "response_message": "You are not authorized to view this content"})


class NonProfessionalsPermission(permissions.BasePermission):
    """Only users not registered as professionals can access"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            if request.user.is_professional == False:
                return True
            else:
                raise NotAcceptable(
                    {"response_code": 1, "response_message": "You have already created your professional profile in the system"})


class ProfessionalsOnlyPermission(permissions.BasePermission):
    """Only users registered as professionals can access"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            if request.user.is_professional == True:
                return True
            else:
                raise NotAcceptable(
                    {"response_code": 1, "response_message": "You have not created your professional profile in the system"})


class IsSubscribedPermission(permissions.BasePermission):
    """Subscribed Only permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            print(request.user.facility.is_subscribed)

            if request.user.facility.is_subscribed:
                return True
            else:
                raise NotAcceptable(
                    {"detail": ["You have no running subscription. Subscribe to continue using the service", ]})


class PharmacistPermission(permissions.BasePermission):
    """Pharmacist permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.get_role() == "PHARMACIST" or request.user.get_role() == "PHARMACEUTICAL-TECHNOLOGIST":
                return True
            else:
                raise NotAcceptable(
                    "Pharmacists or Pharmaceutical Technologists only")
        else:
            raise NotAcceptable("Pharmacists only")


class PrescriberPermission(permissions.BasePermission):
    """Prescriber permissions: doctors and clinical officers"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.cadre:
                if request.user.cadre.cluster == "CONSULTATION":
                    return True
                else:
                    raise NotAcceptable("Prescribers only")
            else:
                raise NotAcceptable(
                    {"response_code": 1, "response_message": "You do not have permissions to access this content"})


class IsMyFacilityObjectPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        my_pharmacy = Facility.objects.get(owner=request.user)
        if obj.pharmacy == my_pharmacy:
            return True
        else:
            raise NotAcceptable("Not your pharmacy")
            return False


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,

        return obj.owner == request.user


class ClientPermission(permissions.BasePermission):
    """Prescriber permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            return request.user.is_client
        else:
            raise NotAcceptable("Clients only")


class CourierPermission(permissions.BasePermission):
    """Courier permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            return request.user.is_courier
        else:
            raise NotAcceptable("Couriers only")


class FacilitySuperintendentPermission(permissions.BasePermission):
    """Facility Superintendent permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superintendent:
                return True

            else:
                raise NotAcceptable(
                    "Facility superintendent only!")
        else:
            raise NotAcceptable("Please log in")


class ClinicSuperintendentPermission(permissions.BasePermission):
    """Facility Superintendent permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            if request.user.is_superintendent and request.user.facility.facility_type == "Clinic":
                return True

            else:
                raise NotAcceptable(
                    "Clinic superintendents only!")
        else:
            raise NotAcceptable("Please log in")


class PharmacySuperintendentPermission(permissions.BasePermission):
    """Facility Superintendent permissions"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            if request.user.is_superintendent and request.user.facility.facility_type == "Pharmacy":
                return True
            else:
                raise NotAcceptable(
                    "Clinic superintendents only!")
        else:
            raise NotAcceptable("Please log in")
