from django.urls import path
from . import views
from django.conf.urls import url
from users.views import FacilityDetail

urlpatterns = [

    path('listings/create', views.ListingsCreateAPIView.as_view(),
         name=views.ListingsCreateAPIView.name),
    path('listings', views.ListingsListAPIView.as_view(),
         name=views.ListingsListAPIView.name),
    path('listings/<uuid:pk>', views.ListingsDetailAPIView.as_view(),
         name=views.ListingsDetailAPIView.name),
    path('listings/<uuid:pk>/', views.ListingsUpdateAPIView.as_view(),
         name=views.ListingsUpdateAPIView.name),
]
