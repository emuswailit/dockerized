import base64

from core import app_permissions
from core.views import FacilitySafeViewMixin
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import exceptions, generics, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from . import models, serializers
from .token_generator import account_activation_token
from .utils import jwt_response_payload_handler

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()


# Create facility
class FacilityCreate(generics.CreateAPIView):
    """
    Authenticated user
    -----------------------------------------------------
    Create facility
    """
    name = "facility-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.FacilitySerializer
    queryset = models.Facility.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(FacilityCreate,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(owner=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Facility created successfully.",
                                  "facility": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Facility not created", "facility": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class FacilityListForAdmin(generics.ListAPIView):
    """List of all porfolios"""
    name = 'portfolio-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilitySerializer
    queryset = models.Facility.objects.all()

    def get_queryset(self):
        # Ensure that the users belong to the portfolio of the user that is making the request
        # user = self.request.user
        return super().get_queryset().all()


class FacilityList(generics.ListAPIView):
    """List of all porfolios"""
    name = 'portfolio-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilitySerializer
    queryset = models.Facility.objects.all()

    def get_queryset(self):
        # Ensure that the users belong to the portfolio of the user that is making the request
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class FacilityDetail(generics.RetrieveAPIView):
    """
    Prescription details
    """
    name = "facility-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.FacilitySerializer
    queryset = models.Facility.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DefaultFacility(generics.ListAPIView):
    """
    Prescriber
    ============================================================
    1. List of all prescriptions for this

    """
    name = 'facility-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilitySerializer
    queryset = models.Facility.objects.all()


class FacilityVerifyAPIView(generics.RetrieveUpdateAPIView):
    """
    Account update
    """
    name = "account-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.FacilityVerifySerializer
    queryset = models.Account.objects.all()
    lookup_fields = ('pk',)

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(FacilityVerifyAPIView,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class UsersCreate(generics.CreateAPIView):

    """
   Anyone
    ============================================================
    Register as user

    """
    name = 'users-create'
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"response_message": "Registration was succesful", "user": serializer.data,
                                  "errors": errors_messages, "response_code": 0}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name.replace("_", " ").upper(), field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_message": "Registration was not successfull", "user": serializer.data,
                                  "errors": errors_messages, "response_code": 1})


# class AnyUserRegisterAPIView(generics.CreateAPIView):
#     """Allow any user to register in the system"""
#     name = 'user-register'
#     permission_classes = ()
#     authentication_classes = ()

#     serializer_class = serializers.UserSerializer
#     queryset = User.objects.all()

#     def perform_create(self, serializer):
#         serializer.save()

#     def create(self, request, *args, **kwargs):
#         errors_messages = []
#         if(User.objects.filter(email=request.data['email']).exists()):

#             raise exceptions.ValidationError(
#                 {"message": ["The email provided is already in use", ]})

#         if(User.objects.filter(national_id=request.data['national_id']).exists()):

#             raise exceptions.ValidationError({"message": [
#                 "The national ID number provided is already in use", ]})

#         if(User.objects.filter(phone=request.data['phone']).exists()):
#             raise exceptions.ValidationError({"message": [
#                 "The phone number provided is already in use", ]})

#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():

#             self.perform_create(serializer)
#             return Response(data={"message": "User created successfully.Please login to
# your email to verify activate your account.",
#                                   "user": serializer.data, "status": status.HTTP_201_CREATED,
#                                   "errors": errors_messages}, status=status.HTTP_201_CREATED)
#         else:

#             raise exceptions.ValidationError(
#                 {"data": ["The seems to be an error with your provide data!", ]})
#         default_errors = serializer.errors  # default errors dict
#         errors_messages = []
#         for field_name, field_errors in default_errors.items():
#             for field_error in field_errors:
#                 error_message = '%s: %s' % (field_name, field_error)
#                 errors_messages.append(error_message)

#         return Response(data={"message": "User not created", "user": serializer.data,
#  "status": status.HTTP_400_BAD_REQUEST, "errors": errors_messages}, status=status.HTTP_201_CREATED)


class UserList(FacilitySafeViewMixin, generics.ListCreateAPIView):
    name = 'user-list'
    permission_classes = (
        permissions.IsAdminUser,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data['email'])
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            qs = User.objects.filter(
                Q(email__iexact=request.data['email'])
            ).distinct()
            if qs.count() == 1:
                user_obj = qs.first()
                print("user_obj")
                print(user_obj)
                if user_obj.check_password(request.data['password']):
                    user = user_obj
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    response = jwt_response_payload_handler(
                        token, user, request=request)
                    return Response(response)
            return Response(data={"message": "User created successfully.", "user": response,
                                  "status": status.HTTP_201_CREATED,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "User not created", "user": serializer.data,
                                  "status": status.HTTP_400_BAD_REQUEST, "errors": errors_messages},
                            status=status.HTTP_201_CREATED)

    def get_queryset(self, *args, **kwargs):
        facility_id = self.request.user.facility_id
        qs = super(UserList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.queryset.filter(
                Q(email__icontains=query) |
                Q(username__icontains=query) |
                Q(national_id__icontains=query)
            )

        return qs.filter(facility_id=facility_id)


class UserDetail(generics.RetrieveAPIView):
    name = 'user-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    # def get_queryset(self):
    #     # Ensure that the user belongs to the company of the user that is making the request
    #     # Note that this method is identical to the one in `UserList`
    #     facility_id = self.request.user.facility_id
    #     return super().get_queryset().filter(facility_id=facility_id)


def activate_account(request, uidb64, token):
    """Confirm email account, if succesful user is redirected to login"""
    try:
        uid = base64.b64decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if not user.is_verified and not user.is_active:
            user.is_active = True
            user.is_verified = True
            user.save()
            return redirect("/")
        else:
            return redirect("/")
    else:
        return HttpResponse('Activation link is invalid!')


class UserLoginView(generics.views.APIView):
    """Log in a user using JWT"""

    permission_classes = [permissions.AllowAny, ]
    serializer_class = serializers.UserLoginSerializer

    def get_queryset(self):
        user = self.request.user
        return user.customer.all()
    # queryset = User.objects.all()

    def post(self, request):
        data = request.data
        username = data.get('email')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        # print(user)
        qs = User.objects.filter(
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            print("user_obj")
            print(user_obj)
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(
                    token, user, request=request)
                return Response(response)
            else:
                raise exceptions.AuthenticationFailed('Wrong password')
        else:
            raise exceptions.AuthenticationFailed('User not found')
        return Response({'status': 401, 'detail': 'Invalid credentials'})


class FacilityImageAPIView(generics.CreateAPIView):
    name = 'facilityimage'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.FacilityImageSerializer
    queryset = models.FacilityImage.objects.all()
    lookup_fields = ('pk',)

    def perform_create(self, serializer):

        user = self.request.user

        serializer.save(created_by=user, facility=user.facility
                        )

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class FacilityImageDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'facilityimage-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.FacilityImageSerializer
    queryset = models.FacilityImage.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def delete(self, request, pk=None, **kwargs):

        print("No deletes")


# ADd new regulator licence
class RegulatorLicenceCreate(generics.CreateAPIView):
    """
    Authenticated user
    -----------------------------------------------------
    Add new regulator licence
    """
    name = "regulatorlicence-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.RegulatorLicenceSerializer
    queryset = models.RegulatorLicence.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(RegulatorLicenceCreate,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Licence uploaded successfully.",
                                  "regulator-licence": serializer.data,  "errors": errors_messages},
                            status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Licence not uploaded", "regulator-licence": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class RegulatorLicenceDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'regulatorlicence-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.RegulatorLicenceSerializer
    queryset = models.RegulatorLicence.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def delete(self, request, pk=None, **kwargs):

        print("No deletes")


# County permits

# ADd new regulator licence
class CountyPermitCreate(generics.CreateAPIView):
    """
    Authenticated user
    -----------------------------------------------------
    Add new regulator licence
    """
    name = "countypermit-create"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.CountyPermitSerializer
    queryset = models.CountyPermit.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(CountyPermitCreate,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Permit uploaded successfully.", "county-permit": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Permit not uploaded", "county-permit": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class CountyPermitDetail(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    name = 'countypermit-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CountyPermitSerializer
    queryset = models.CountyPermit.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

    def delete(self, request, pk=None, **kwargs):

        print("No deletes")


class UserImageAPIView(generics.CreateAPIView):
    name = 'userimage'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserImageSerializer
    queryset = models.UserImage.objects.all()
    lookup_fields = ('pk',)

    def perform_create(self, serializer):

        user = self.request.user

        serializer.save(created_by=user, owner=user
                        )

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class UserImageDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'userimage-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserImageSerializer
    queryset = models.UserImage.objects.all()

    def get_queryset(self):
        portfolio_id = self.request.user.portfolio_id
        return super().get_queryset().filter(portfolio_id=portfolio_id)

    def delete(self, request, pk=None, **kwargs):

        print("No deletes")
# Get User API


class UserAPI(generics.RetrieveAPIView):
    """
    Get user
    """
    name = 'user-retrieve'
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = serializers.UserSerializer

    def get_object(self):
        try:
            return self.request.user
        except Exception as ex:
            raise exceptions.PermissionDenied(
                {"error": f"{ex}"})

# Account


class AccountCreateAPIView(generics.CreateAPIView):
    """
    Create new account
    """
    name = "account-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if models.Account.objects.filter(owner=user).count() > 0:
            raise exceptions.NotAcceptable(
                {"detail": ["You are already registered an account!", ]})
        else:
            pass

        if user.is_client:
            user.is_prescriber = True
            user.save()
            serializer.save(owner=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Account created successfully.", "prescriber": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Account not created", "prescriber": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class AccountListAPIView(generics.ListAPIView):
    """
    Listing of all or permitted client accounts
    """
    name = "account-list"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.AccountSerializer

    queryset = models.Account.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(AccountListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AccountListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class AccountDetailAPIView(generics.RetrieveAPIView):
    name = 'account-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects.all()

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class AccountUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Account update
    """
    name = "account-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# # Dependants
class DependantCreateAPIView(generics.CreateAPIView):
    """
    Create new dependant
    """
    name = "dependant-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DependantSerializer
    queryset = models.Dependant.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        account_pk = self.kwargs.get("pk")
        account = models.Account.objects.get(id=account_pk)
        if account:
            serializer.save(owner=user, account=account)
        else:
            raise exceptions.ValidationError(
                {"detail": ["No such account in the system", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Dependant created successfully.", "dependant": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Dependant not created", "dependant": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class AllDependantListAPIView(generics.ListAPIView):
    """
    Admin user
    ----------------------------------
    All dependants, active and inactive
    """
    name = "dependant-list"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.DependantSerializer

    queryset = models.Dependant.objects.all()

    search_fields = ('first_name', 'middle_name', 'last_name', 'owner__phone')
    ordering_fields = ('first_name', 'id')


class ActiveDependantListAPIView(generics.ListAPIView):
    """
    Prescribers
    ------------------------------------------------
    Active users
    """
    name = "dependant-list"
    permission_classes = (app_permissions.PrescriberPermission,
                          )
    serializer_class = serializers.DependantSerializer

    queryset = models.Dependant.objects.filter(is_active=True)

    search_fields = ('first_name', 'middle_name', 'last_name', 'owner__phone')
    ordering_fields = ('first_name', 'id')


class UserDependantsList(generics.ListAPIView):
    """
    General user
    -------------------------------------------
    View own active dependants

    """
    name = "dependant-list"
    permission_classes = (permissions.IsAuthenticated,
                          )

    serializer_class = serializers.DependantSerializer

    queryset = models.Dependant.objects.filter(is_active=True)

    search_fields = ('first_name', 'middle_name', 'last_name', 'owner__phone')
    ordering_fields = ('first_name', 'id')

    def get_queryset(self):
        # Retrieve dependants for specific user
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class DependantDetailAPIView(generics.RetrieveAPIView):
    """
    Dependant details
    """
    name = "dependant-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.DependantSerializer
    queryset = models.Dependant.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class DependantUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Dependant update
    """
    name = "dependant-update"
    permission_classes = (app_permissions.IsOwner,
                          )
    serializer_class = serializers.DependantSerializer
    queryset = models.Dependant.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


# Role views
class CadresCreate(FacilitySafeViewMixin, generics.CreateAPIView):

    # TODO : Test this view later
    """
    Logged on user
    ============================================================
    Register as professional

    """
    name = 'cadres-create'
    permission_classes = (
        permissions.IsAdminUser,
    )
    serializer_class = serializers.CadresSerializer
    queryset = models.Cadres.objects.all()

    def perform_create(self, serializer):
        try:
            user = self.request.user
            facility = self.request.user.facility
            serializer.save(owner=user, facility=facility,)

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"error": f"{e}", })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Role succesfully created", "role": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Role not created", "role": serializer.data,
                                  "errors": errors_messages}, status=status.HTTP_400_BAD_REQUEST)


class CadresList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Authenticated User
    ============================================================
    View list of all facility cadres
    """
    name = 'cadres-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CadresSerializer
    queryset = models.Cadres.objects.all()


class CadresDetail(generics.RetrieveAPIView):
    """
    Authenticated user
    -----------------------------------------------------
    View details of a cadre
    """
    name = 'cadres-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.CadresSerializer
    queryset = models.Cadres.objects.all()


class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Users update
    """
    name = "users-update"
    permission_classes = (permissions.IsAdminUser,
                          )
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.User.objects.all()
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

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            errors_messages = []
            self.perform_update(serializer)
            return Response(data={"response_message": "User update was successfull",
                                  "user": serializers.UserSerializer(instance, context={'request': request}).data,
                                  "errors": errors_messages, "response_code": 0})
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name.replace("_", " ").upper(), field_error)
                    errors_messages.append(error_message)

            return Response(data={"response_message": "User update was not successfull", "user": serializer.data,
                                  "errors": errors_messages, "response_code": 1})
