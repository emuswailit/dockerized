from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

    # 1.  Facility superintendent creates slots for self diary
    path('slots/create', views.SlotsCreate.as_view(),
         name=views.SlotsCreate.name),
    path('slots/all', views.AllSlotsList.as_view(),
         name=views.AllSlotsList.name),
    path('slots/available', views.AvailableSlotsList.as_view(),
         name=views.AvailableSlotsList.name),
    path('slots/<uuid:pk>', views.SlotDetail.as_view(),
         name=views.SlotDetail.name),
    path('slots/<uuid:pk>/update', views.SlotUpdate.as_view(),
         name=views.SlotUpdate.name),

    # 2. Appointment payments to be created and managed by clients
    path('appointment-payments/create', views.AppointmentPaymentsCreate.as_view(),
         name=views.AppointmentPaymentsCreate.name),
    path('appointment-payments/', views.AppointmentPaymentsList.as_view(),
         name=views.AppointmentPaymentsList.name),
    path('appointment-payments/<uuid:pk>/', views.AppointmentPaymentsDetail.as_view(),
         name=views.AppointmentPaymentsDetail.name),
    path('appointment-payments/<uuid:pk>/update', views.AppointmentPaymentsUpdate.as_view(),
         name=views.AppointmentPaymentsUpdate.name),

    # 3. Appointments are automagically created upon payment by client, client can also manage them
    path('appointments/all', views.AppointmentsList.as_view(),
         name=views.AllPrescriptionList.name),
    path('appointments/<uuid:pk>', views.AppointmentsDetail.as_view(),
         name=views.AppointmentsDetail.name),

    # 4. Appointment consultations are created by a doctor, an appointment is required
    path('appointment-consultations/create', views.AppointmentConsultationsCreate.as_view(),
         name=views.AppointmentConsultationsCreate.name),
    path('appointment-consultations/', views.AppointmentConsultationsList.as_view(),
         name=views.AppointmentConsultationsList.name),
    path('appointment-consultations/<uuid:pk>/', views.AppointmentConsultationsDetail.as_view(),
         name=views.AppointmentConsultationsDetail.name),
    path('appointment-consultations/<uuid:pk>/update', views.AppointmentConsultationsUpdate.as_view(),
         name=views.AppointmentConsultationsUpdate.name),


    # 5. Prescriptions is automatically created when creating an appointment consultation. It can be edited and managed such as adding items
    path('prescriptions/all', views.AllPrescriptionList.as_view(),
         name=views.AllPrescriptionList.name),
    path('prescriptions/dependants/<uuid:pk>', views.DependantPrescriptionsList.as_view(),
         name=views.DependantPrescriptionsList.name),
    path('prescriptions/create', views.PrescriptionCreate.as_view(),
         name=views.PrescriptionCreate.name),
    path('prescriptions/<uuid:pk>', views.PrescriptionDetail.as_view(),
         name=views.PrescriptionDetail.name),
    path('prescriptions/<uuid:pk>/sign', views.PrescriptionSign.as_view(),
         name=views.PrescriptionSign.name),
    path('prescriptions/<uuid:pk>/update', views.PrescriptionUpdate.as_view(),
         name=views.PrescriptionUpdate.name),
    path('prescriptions/<uuid:pk>/item', views.PrescriptionItemCreate.as_view(),
         name=views.PrescriptionItemCreate.name),
    path('prescription-items/', views.PrescriptionItemList.as_view(),
         name=views.PrescriptionItemList.name),
    path('prescription-items/<uuid:pk>', views.PrescriptionItemDetail.as_view(),
         name=views.PrescriptionItemDetail.name),


    #   6.   Allergy for dependant can be updated during consultation, if its not listed, a doctor can create a new allergy and then report it for the patient
    path('allergies', views.AllergyListAPIView.as_view(),
         name=views.AllergyListAPIView.name),
    path('allergies/<uuid:pk>', views.AllergyDetailAPIView.as_view(),
         name=views.AllergyDetailAPIView.name),
    path('allergies/<uuid:pk>/update', views.AllergyUpdateAPIView.as_view(),
         name=views.AllergyUpdateAPIView.name),
    path('allergies/create', views.AllergyCreateAPIView.as_view(),
         name=views.AllergyCreateAPIView.name),

]
