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
    path('variations/<uuid:pk>/update', views.VariationUpdate.as_view(),
         name=views.VariationUpdate.name),

    path('variations/<uuid:pk>/photos', views.VariationPhotoList.as_view(),
         name=views.VariationPhotoList.name),
    path('variation-photos/<uuid:pk>', views.VariationPhotoDetail.as_view(),
         name=views.VariationPhotoDetail.name),

    path('inventory/create', views.InventoryCreate.as_view(),
         name=views.InventoryCreate.name),
    path('inventory/', views.InventoryList.as_view(),
         name=views.InventoryList.name),
    path('inventory/<uuid:pk>', views.InventoryDetail.as_view(),
         name=views.InventoryDetail.name),
    path('inventory/<uuid:pk>/update', views.InventoryUpdate.as_view(),
         name=views.InventoryUpdate.name),


    path('categories/create', views.CategoriesCreateAPIView.as_view(),
         name=views.CategoriesCreateAPIView.name),
    path('categories/', views.CategoriesListAPIView.as_view(),
         name=views.CategoriesListAPIView.name),
    path('categories/<uuid:pk>', views.CategoriesDetailAPIView.as_view(),
         name=views.CategoriesDetailAPIView.name),
    path('categories/<uuid:pk>/', views.CategoriesUpdateAPIView.as_view(),
         name=views.CategoriesUpdateAPIView.name),
]
