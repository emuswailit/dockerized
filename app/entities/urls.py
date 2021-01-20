from django.urls import path
from . import views
from django.conf.urls import url
from users.views import FacilityDetail

urlpatterns = [

    path('pharmacists/create', views.PharmacistCreate.as_view(),
         name=views.PharmacistCreate.name),
    path('pharmacists/', views.PharmacistList.as_view(),
         name=views.PharmacistList.name),
    path('pharmacists/available', views.AvailablePharmacistList.as_view(),
         name=views.AvailablePharmacistList.name),
    path('pharmacists/<uuid:pk>', views.PharmacistDetail.as_view(),
         name=views.PharmacistDetail.name),

     path('prescribers/create', views.PrescriberCreate.as_view(),
         name=views.PrescriberCreate.name),
    path('prescribers/', views.PrescriberList.as_view(),
         name=views.PrescriberList.name),
     path('prescribers/available', views.AvailablePrescribersList.as_view(),
         name=views.AvailablePrescribersList.name),
    path('prescribers/<uuid:pk>', views.PrescriberDetail.as_view(),
         name=views.PrescriberDetail.name),



    path('couriers/create', views.CourierCreate.as_view(),
         name=views.CourierCreate.name),
    path('couriers', views.CourierList.as_view(),
         name=views.CourierList.name),
    path('couriers/<uuid:pk>', views.CourierDetail.as_view(),
         name=views.CourierDetail.name),

    path('prescribers/create', views.PrescriberCreate.as_view(),
         name=views.PrescriberCreate.name),
    path('prescribers', views.PrescriberList.as_view(),
         name=views.PrescriberList.name),
    path('prescribers/<uuid:pk>', views.PrescriberDetail.as_view(),
         name=views.PrescriberDetail.name),


    path('pharmacists/<uuid:pk>/recruit', views.FacilityPharmacistCreate.as_view(),
         name=views.FacilityPharmacistCreate.name),
    path('facility-pharmacists/<uuid:pk>/exit', views.FacilityPharmacistExit.as_view(),
         name=views.FacilityPharmacistExit.name),
    
    path('facility-pharmacists/all', views.AllFacilityPharmacistList.as_view(),
         name=views.AllFacilityPharmacistList.name),
    path('facility-pharmacists/active', views.ActiveFacilityPharmacistList.as_view(),
         name=views.ActiveFacilityPharmacistList.name),
    path('facility-pharmacists/<uuid:pk>', views.FacilityPharmacistDetail.as_view(),
         name=views.FacilityPharmacistDetail.name),
    path('facility-pharmacists/<uuid:pk>/', views.FacilityPharmacistUpdate.as_view(),
         name=views.FacilityPharmacistUpdate.name),
    
    
    path('prescribers/<uuid:pk>/recruit', views.FacilityPrescriberCreate.as_view(),
         name=views.FacilityPrescriberCreate.name),
    path('facility-prescribers/all', views.AllFacilityPrescriberList.as_view(),
         name=views.AllFacilityPrescriberList.name),
    path('facility-prescribers/active', views.ActiveFacilityPrescriberList.as_view(),
         name=views.ActiveFacilityPrescriberList.name),
    path('facility-prescribers/<uuid:pk>', views.FacilityPrescriberDetail.as_view(),
         name=views.FacilityPrescriberDetail.name),
    path('facility-prescribers/<uuid:pk>/', views.FacilityPrescriberUpdate.as_view(),
         name=views.FacilityPrescriberUpdate.name),


    path('couriers/<uuid:pk>/recruit', views.FacilityCourierCreate.as_view(),
         name=views.FacilityCourierCreate.name),
    path('facility-couriers/', views.FacilityCourierList.as_view(),
         name=views.FacilityCourierList.name),
    path('facility-couriers/<uuid:pk>', views.FacilityCourierDetail.as_view(),
         name=views.FacilityCourierDetail.name),

    path('facility-couriers/<uuid:pk>/', views.FacilityCourierUpdate.as_view(),
         name=views.FacilityCourierUpdate.name),
]
