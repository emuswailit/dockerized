from django.urls import path
from . import views
from django.conf.urls import url
from users.views import FacilityDetail

urlpatterns = [

    path('variations/create', views.VariationCreate.as_view(),
         name=views.VariationCreate.name),
    path('variations/', views.VariationList.as_view(),
         name=views.VariationList.name),
    path('variations/<uuid:pk>', views.VariationDetail.as_view(),
         name=views.VariationDetail.name),
    path('variations/<uuid:pk>', views.VariationUpdate.as_view(),
         name=views.VariationUpdate.name),

    path('variations/<uuid:pk>/photos', views.VariationPhotoList.as_view(),
         name=views.VariationPhotoList.name),
    path('variation-photos/<uuid:pk>', views.VariationPhotoDetail.as_view(),
         name=views.VariationPhotoDetail.name),

    path('variations/<uuid:pk>/receipts', views.VariationReceiptCreate.as_view(),
         name=views.VariationReceiptCreate.name),
    path('variation-receipts/', views.VariationReceiptList.as_view(),
         name=views.VariationReceiptList.name),
    path('variation-receipts/<uuid:pk>', views.VariationReceiptDetail.as_view(),
         name=views.VariationReceiptDetail.name),
    path('variation-receipts/<uuid:pk>/', views.VariationReceiptUpdate.as_view(),
         name=views.VariationReceiptUpdate.name),
]
