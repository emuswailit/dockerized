from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

    # Slots urls
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

    # Prescriptions urls
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
    # path('prescription-items/<uuid:pk>/', views.PrescriptionItemUpdate.as_view(),
    #      name=views.PrescriptionItemUpdate.name),


    # Appointments urls
    path('appointments/all', views.AppointmentsList.as_view(),
         name=views.AllPrescriptionList.name),
#     path('appointments/dependants/<uuid:pk>', views.DependantPrescriptionsList.as_view(),
#          name=views.DependantPrescriptionsList.name),
    path('appointments/create', views.AppointmentsCreate.as_view(),
         name=views.AppointmentsCreate.name),

    path('appointments/<uuid:pk>', views.AppointmentsDetail.as_view(),
         name=views.AppointmentsDetail.name),

]
