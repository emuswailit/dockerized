from django.shortcuts import render
from rest_framework import permissions, generics, status, exceptions
from . import serializers, models
from core.views import FacilitySafeViewMixin
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from core.permissions import PrescriberPermission, IsOwner
from django.db import IntegrityError
from users.models import Dependant
from rest_framework.response import Response

# Create your views here.
# Prescription

from django.shortcuts import get_object_or_404, redirect, render


class PrescriptionCreate(FacilitySafeViewMixin, generics.CreateAPIView):
    """
   Prescriber
    ============================================================
    1. Create new prescription

    """
    name = 'prescription-create'
    permission_classes = (
        PrescriberPermission,
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
        PrescriberPermission,
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.filter(is_signed=False)

    search_fields =('dependant__id','dependant__middle_name','dependant__last_name', 'dependant__first_name',)
    ordering_fields =('dependant__first_name', 'id')

    # def get_queryset(self):
    #     facility_id = self.request.user.facility_id
    #     return super().get_queryset().filter(facility_id=facility_id)

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

    search_fields =('dependant__id','dependant__middle_name','dependant__last_name', 'dependant__first_name',)
    ordering_fields =('dependant__first_name', 'id')

    def get_queryset(self):
        user = self.request.user
        dependant_id = self.kwargs['pk']
        if Dependant.objects.filter(id=dependant_id).count()>0:
            dependant = Dependant.objects.get(id=dependant_id)
            if dependant and dependant.owner==user:
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

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Prescriber, owner
    ============================================================
    1. Update prescription

    """
    name = 'prescription-detail'
    permission_classes = (
        PrescriberPermission, IsOwner
    )
    serializer_class = serializers.PrescriptionSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

class PrescriptionSign(generics.RetrieveUpdateAPIView):
    #TODO: Reuse code: Update selected item by ID custom
    """
    Prescriber
    ---------------------------------------
    Digitally sign a prescription created by this prescriber
    """
    name = "prescription-detail"
    permission_classes = (PrescriberPermission,
                          )
    serializer_class = serializers.PrescriptionUpdateSerializer
    queryset = models.Prescription.objects.all()
  
    def get_queryset(self):
        prescription_pk = self.kwargs.get("pk")

        # facility_id = self.request.user.facility_id
        return super().get_queryset().filter(id=prescription_pk)
    def put(self, request, pk=None, **kwargs):
        prescription_pk = self.kwargs.get("pk")

        if models.Prescription.objects.filter(id=prescription_pk).count()>0:
            prescription = models.Prescription.objects.get(id=prescription_pk)
            if prescription.owner==request.user:
                if prescription.is_signed==True:
                    return Response(data={"message": "Prescription is signed"})
                else:
                    prescription_items= models.PrescriptionItem.objects.filter(prescription_id=prescription_pk)
                
                    if prescription_items.count()>0:
                        prescription.is_signed=True;
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
        PrescriberPermission,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    def perform_create(self, serializer):

        try:
            user = self.request.user
            facility = self.request.user.facility
            prescription_pk = self.kwargs.get("pk")

            if models.Prescription.objects.filter(id=prescription_pk).count()>0:
                prescription = models.Prescription.objects.get(id=prescription_pk)

                # Add items only to prescriptions which are open and not signed
                if prescription:
                    #Add items to own prescription
                    if prescription.owner==self.request.user:
                        if prescription.is_signed==False:                    
                            serializer.save(owner=user, facility=facility, prescription_id=prescription_pk)
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
                {"detail": [f"Prescription item must be to be unique. Similar item is already added! {e}", ]})

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
    

class PrescriptionItemList(FacilitySafeViewMixin, generics.ListAPIView):
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

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionItemDetail(FacilitySafeViewMixin, generics.RetrieveAPIView):
    name = 'prescriptionitem-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.Prescription.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)


class PrescriptionItemUpdate(FacilitySafeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Superintendent Pharmacist
    ============================================================
    1. Update prescription item

    """
    name = 'prescriptionitem-detail'
    permission_classes = (
        PrescriberPermission, IsOwner
    )
    serializer_class = serializers.PrescriptionItemSerializer
    queryset = models.PrescriptionItem.objects.all()

    def get_queryset(self):
        facility_id = self.request.user.facility_id
        return super().get_queryset().filter(facility_id=facility_id)

