from core import app_permissions
from core.views import FacilitySafeViewMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import exceptions, generics, permissions, status
from rest_framework.response import Response
from users.models import Dependant
from entities.models import Professionals, Employees
from . import models, serializers

from django.contrib.auth import get_user_model

User = get_user_model()
# Appointment slots


class SlotsCreate(FacilitySafeViewMixin, generics.CreateAPIView):

    # TODO : Test this view later
    """
   Clinic Superintendent
    ============================================================
    Create a clinic slot

    """
    name = 'slots-create'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.SlotSerializer
    queryset = models.Slots.objects.all()

    def perform_create(self, serializer):

        user = self.request.user
        facility = self.request.user.facility
        professional = Professionals.objects.get(owner=user)
        employee = Employees.objects.get(professional=professional)
        serializer.save(owner=user, facility=facility, employee=employee)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Clinic slot succesfully created", "slot": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Clinic slot not created", "slot": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class AllSlotsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Authenticated users
    ============================================================
    List of all slots for  clinic

    """
    name = 'slots-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.SlotSerializer
    queryset = models.Slots.objects.all_slots()

    # search_fields =('dependant__id','dependant__middle_name','dependant__last_name', 'dependant__first_name',)
    # ordering_fields =('dependant__first_name', 'id')


class AvailableSlotsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Clients
    ============================================================
    View list of available  slots in different clinics

    """
    name = 'slots-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.SlotSerializer
    queryset = models.Slots.objects.available_slots()


class SlotDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    """


    Authenticated users
    -------------------------------------------------------------------
    View details of a given slot id

    """
    name = 'slots-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.SlotSerializer
    queryset = models.Slots.objects.all()


class SlotUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Clinic Superintendent
    ============================================================
    Update own created clinic slot

    """
    name = 'prescription-detail'
    permission_classes = (
        app_permissions.IsOwner,
    )
    serializer_class = serializers.SlotSerializer
    queryset = models.Slots.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


# Payment for available appointment slots
class AppointmentPaymentsCreate(generics.CreateAPIView):
    """
    Authenticated user
    -----------------------------------------------------
    Pay for consultation
    """
    name = "appointmentpayments-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.AppointmentPaymentsSerializer
    queryset = models.AppointmentPayments.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(AppointmentPaymentsCreate,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):
        try:
            user = self.request.user
            serializer.save(owner=user, facility=user.facility)
        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"response_code": "1", "response_message": f"Payment for this appointment already done"})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Appointment payment created successfully.", "appointment-payment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Appointment payments not created", "appointment-payment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class AppointmentPaymentsList(generics.ListAPIView):
    """
    AppointmentPaymentss list
    """
    name = "appointmentpayments-list"
    permission_classes = (app_permissions.FacilitySuperintendentPermission,
                          )
    serializer_class = serializers.AppointmentPaymentsSerializer

    queryset = models.AppointmentPayments.objects.all()


class AppointmentPaymentsDetail(generics.RetrieveAPIView):
    """
    AppointmentPayments details
    """
    name = "appointmentpayments-detail"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.AppointmentPaymentsSerializer
    queryset = models.AppointmentPayments.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AppointmentPaymentsUpdate(generics.RetrieveUpdateAPIView):
    """
    Appointment payment update
    """
    name = "appointmentpayments-update"
    permission_classes = (app_permissions.IsOwner,
                          )
    serializer_class = serializers.AppointmentPaymentsSerializer
    queryset = models.AppointmentPayments.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AppointmentsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Prescriber
    ============================================================
    1. List of all appointments

    """
    name = 'appointments-list'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.AppointmentsSerializer
    queryset = models.Appointments.objects.all()

    search_fields = ('dependant__id', 'dependant__middle_name',
                     'dependant__last_name', 'dependant__first_name', 'owner__first_name', 'owner__last_name', 'owner__phone')
    ordering_fields = ('dependant__first_name', 'id')


class AppointmentsDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'appointments-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.AppointmentsSerializer
    queryset = models.Appointments.objects.all()


# Consultation
class AppointmentConsultationsCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
   Doctor
    ============================================================
    Create a consultation

    """
    name = 'appointmentconsultations-create'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.AppointmentConsultationsSerializer
    queryset = models.AppointmentConsultations.objects.all()

    def get_serializer_context(self):
        user_pk = self.request.user.id
        context = super(AppointmentConsultationsCreate,
                        self).get_serializer_context()

        context.update({
            "user_pk": user_pk

        })
        return context

    def perform_create(self, serializer):

        user = self.request.user
        facility = self.request.user.facility
        # dependant_pk = self.kwargs.get("pk")
        serializer.save(owner=user, facility=facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Appointment succesfully created", "appointment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Appointment not created", "appointment": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class AppointmentConsultationsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Prescriber
    ============================================================
    1. List of all appointments

    """
    name = 'appointmentconsultations-list'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.AppointmentConsultationsSerializer
    queryset = models.AppointmentConsultations.objects.all()

    # search_fields = ('dependant__id', 'dependant__middle_name',
    #                  'dependant__last_name', 'dependant__first_name',)
    # ordering_fields = ('dependant__first_name', 'id')


class AppointmentConsultationsDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'appointmentconsultations-detail'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.AppointmentConsultationsSerializer
    queryset = models.AppointmentConsultations.objects.all()


class AppointmentConsultationsUpdate(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'appointments-update'
    permission_classes = (
        app_permissions.IsOwner,
    )
    serializer_class = serializers.AppointmentConsultationsSerializer
    queryset = models.AppointmentConsultations.objects.all()


# Prescription Views
class PrescriptionCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
   Prescriber
    ============================================================
    1. Create new prescription

    """
    name = 'prescription-create'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()

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
            return Response(data={"message": "Prescription created successfully.", "prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Prescription not created", "prescription": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PrescriptionsForDependant(generics.ListAPIView):
    """
    Client
    =============================================
    Retrieve all prescriptions for the logged in user's dependants
    """
    name = "prescription-list"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.PrescriptionSerializer

    queryset = models.Prescription.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_queryset(self):
        # Ensure that the users belong to the company of the user that is making the request
        dependant = Dependant.objects.get(owner=self.request.user)
        return super().get_queryset().filter(dependant=dependant)


class AllPrescriptionList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Prescriber
    ============================================================
    1. List of all prescriptions for this

    """
    name = 'prescription-list'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.filter(is_signed=False)

    search_fields = ('dependant__id', 'dependant__middle_name',
                     'dependant__last_name', 'dependant__first_name',)
    ordering_fields = ('dependant__first_name', 'id')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class DependantPrescriptionsList(FacilitySafeViewMixin, generics.ListAPIView):
    """
    Logged in user
    ============================================================
    Retrieve prescriptions for provided dependant ID. Dependant must belong to the logged on user

    """
    name = 'prescription-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.filter(is_signed=True)

    search_fields = ('dependant__id', 'dependant__middle_name',
                     'dependant__last_name', 'dependant__first_name',)
    ordering_fields = ('dependant__first_name', 'id')

    def get_queryset(self):
        user = self.request.user
        dependant_id = self.kwargs['pk']
        if Dependant.objects.filter(id=dependant_id).count() > 0:
            dependant = Dependant.objects.get(id=dependant_id)
            if dependant and dependant.owner == user:
                return models.Prescription.objects.filter(dependant_id=dependant_id, is_signed=True)
            else:
                raise exceptions.NotAcceptable(
                    {"detail": ["Dependant for given ID not found in your records", ]})
        else:
            raise exceptions.NotAcceptable(
                {"detail": ["Dependant for given ID not retrieved", ]})


class PrescriptionDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'prescription-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()


class PrescriptionUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Prescriber, owner
    ============================================================
    1. Update prescription

    """
    name = 'prescription-update'
    permission_classes = (
        app_permissions.PrescriberPermission, app_permissions.IsOwner
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionSign(generics.RetrieveUpdateAPIView):
    # TODO: Reuse code: Update selected item by ID custom
    """
    Prescriber
    ---------------------------------------
    Digitally sign a prescription created by this prescriber
    """
    name = "prescription-sign"
    permission_classes = (app_permissions.PrescriberPermission,
                          )
    serializer_class = serializers.PrescriptionUpdateSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        prescription_pk = self.kwargs.get("pk")

        # facility_id = self.request.user.facility_id
        return super().get_queryset().filter(id=prescription_pk)

    def put(self, request, pk=None, **kwargs):
        prescription_pk = self.kwargs.get("pk")

        if models.Prescription.objects.filter(id=prescription_pk).count() > 0:
            prescription = models.Prescription.objects.get(id=prescription_pk)
            if prescription.owner == request.user:
                if prescription.is_signed == True:
                    return Response(data={"message": "Prescription is signed"})
                else:
                    prescription_items = models.PrescriptionItem.objects.filter(
                        prescription_id=prescription_pk)

                    if prescription_items.count() > 0:
                        prescription.is_signed = True
                        prescription.save()
                        return Response(data={"message": f"Prescription with {prescription_items.count()} items signed"})
                    else:
                        return Response(data={"message": f"Prescription has no items thus will not be signed"})

            else:
                return Response(data={"message": "You can only sign a prescription you created"})

        else:
            return Response(data={"message": "No prescription for this ID"})


# Prescription item


class PrescriptionItemCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
    Prescriber
    ============================================================
    Add item to a prescription which is not signed

    """
    name = 'prescriptionitem-create'
    permission_classes = (
        app_permissions.PrescriberPermission,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    def perform_create(self, serializer):

        try:
            user = self.request.user
            facility = self.request.user.facility
            prescription_pk = self.kwargs.get("pk")

            if models.Prescription.objects.filter(id=prescription_pk).count() > 0:
                prescription = models.Prescription.objects.get(
                    id=prescription_pk)

                # Add items only to prescriptions which are open and not signed
                if prescription:
                    # Add items to own prescription
                    if prescription.owner == self.request.user:
                        if prescription.is_signed == False:
                            serializer.save(
                                owner=user, facility=facility, prescription_id=prescription_pk)
                            # raise exceptions.NotAcceptable(
                            # {"detail": ["Prescription is signed", ]})
                        else:
                            raise exceptions.NotAcceptable(
                                {"detail": ["Prescription is already signed and closed", ]})

                    else:
                        raise exceptions.NotAcceptable(
                            {"detail": ["You can only add items to your own prescription", ]})

                else:
                    raise exceptions.NotAcceptable(
                        {"detail": ["Prescription not retrieved", ]})

        except IntegrityError as e:
            raise exceptions.NotAcceptable(
                {"detail": [f"Prescription item must be to be unique. Similar item is already added!", ]})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Prescription item added successfully.", "prescription-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Precsription item not added", "prescription-item": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class PrescriptionItemList(generics.ListAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. List of prescription items

    """
    name = 'prescriptionitem-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    # def get_queryset(self):
    #     facility_id = self.request.user.facility_id
    #     return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionItemDetail(generics.RetrieveAPIView):
    name = 'prescriptionitem-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    # def get_queryset(self):
    #     facility_id = self.request.user.facility_id
    #     return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionItemUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Update prescription item

    """
    name = 'prescriptionitem-detail'
    permission_classes = (
        app_permissions.PrescriberPermission, app_permissions.IsOwner
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    # def get_queryset(self):
    #     facility_id = self.request.user.facility_id
    #     return super().get_queryset().filter(facility_id=facility_id)


# # Allergy


class AllergyCreateAPIView(generics.CreateAPIView):
    """
    Post new allergy for dependant
    """
    name = "allergy-create"
    permission_classes = (permissions.IsAuthenticated,
                          )
    serializer_class = serializers.AllergySerializer
    queryset = models.Allergy.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user, facility=user.facility)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            errors_messages = []
            self.perform_create(serializer)
            return Response(data={"message": "Allergy created successfully.", "allergy": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)
        else:
            default_errors = serializer.errors  # default errors dict
            errors_messages = []
            for field_name, field_errors in default_errors.items():
                for field_error in field_errors:
                    error_message = '%s: %s' % (field_name, field_error)
                    errors_messages.append(error_message)

            return Response(data={"message": "Allergy not created", "allergy": serializer.data,  "errors": errors_messages}, status=status.HTTP_201_CREATED)


class AllergyListAPIView(generics.ListAPIView):
    """
    Allergies list
    """
    name = "allergy-list"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.AllergySerializer

    queryset = models.Allergy.objects.all()
    # TODO : Reuse this for filtering by q.

    def get_context_data(self, *args, **kwargs):
        context = super(AllergyListAPIView, self).get_context_data(
            *args, **kwargs)
        # context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(AllergyListAPIView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset().filter(  # Change this to ensure it searches only already filtered queryset
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return qs


class AllergyDetailAPIView(generics.RetrieveAPIView):
    """
    Allergy details
    """
    name = "allergy-detail"
    permission_classes = (permissions.AllowAny,
                          )
    serializer_class = serializers.AllergySerializer
    queryset = models.Allergy.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class AllergyUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Allergy update
    """
    name = "allergy-update"
    permission_classes = (app_permissions.IsOwner,
                          )
    serializer_class = serializers.AllergySerializer
    queryset = models.Allergy.objects.all()
    lookup_fields = ('pk',)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_verified=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()

    return redirect('home')
