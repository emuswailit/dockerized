from django.urls import path
from . import views
from django.conf.urls import url
from users.views import DependantListAPIView


urlpatterns = [
#     path('prescriptions/', views.PrescriptionListAPIView.as_view(),
#          name=views.PrescriptionListAPIView.name),
#     path('prescriptions/<uuid:pk>/', views.PrescriptionDetailAPIView.as_view(),
#          name=views.PrescriptionDetailAPIView.name),

#     path('prescriptions/<uuid:pk>/forward', views.ForwardPrescriptionCreate.as_view(),
#          name=views.ForwardPrescriptionCreate.name),
#     path('forward-prescriptions/<uuid:pk>/', views.ForwardPrescriptionDetailAPIView.as_view(),
#          name=views.ForwardPrescriptionDetailAPIView.name),
#     path('forward-prescriptions/', views.ForwardPrescriptionListAPIView.as_view(),
#          name=views.ForwardPrescriptionListAPIView.name),


    path('pharmacies/', views.PharmacyListAPIView.as_view(),
         name=views.PharmacyListAPIView.name),
    path('pharmacies/<uuid:pk>/', views.PharmacyListAPIView.as_view(),
         name=views.PharmacyListAPIView.name),

    path('clinics/', views.ClinicListAPIView.as_view(),
         name=views.ClinicListAPIView.name),
    path('clinics/<uuid:pk>/', views.ClinicDetailAPIView.as_view(),
         name=views.ClinicDetailAPIView.name),
    # path('prescription-items/<uuid:pk>', views.PrescriptionItemDetail.as_view(),
    #      name=views.PrescriptionItemDetail.name),
    # path('prescription-items/<uuid:pk>/', views.PrescriptionItemUpdate.as_view(),
    #      name=views.PrescriptionItemUpdate.name),

]
