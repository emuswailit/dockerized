from django.urls import path
from . import views
from django.conf.urls import url
from users.views import DependantListAPIView


urlpatterns = [
    path('dependants/', views.DependantListAPIView.as_view(),
         name=views.DependantListAPIView.name),
    path('dependants/<uuid:pk>/', views.DependantDetailAPIView.as_view(),
         name=views.DependantDetailAPIView.name),
    path('dependants/<uuid:pk>/prescription', views.PrescriptionCreate.as_view(),
         name=views.PrescriptionCreate.name),
    path('prescriptions/', views.PrescriptionList.as_view(),
         name=views.PrescriptionList.name),
    path('prescriptions/<uuid:pk>', views.PrescriptionDetail.as_view(),
         name=views.PrescriptionDetail.name),
    path('prescriptions/<uuid:pk>/', views.PrescriptionUpdate.as_view(),
         name=views.PrescriptionUpdate.name),

    path('prescriptions/<uuid:pk>/item', views.PrescriptionItemCreate.as_view(),
         name=views.PrescriptionItemCreate.name),
    path('prescription-items/', views.PrescriptionItemList.as_view(),
         name=views.PrescriptionItemList.name),
    path('prescription-items/<uuid:pk>', views.PrescriptionItemDetail.as_view(),
         name=views.PrescriptionItemDetail.name),
    # path('prescription-items/<uuid:pk>/', views.PrescriptionItemUpdate.as_view(),
    #      name=views.PrescriptionItemUpdate.name),

]
