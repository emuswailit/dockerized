from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

    path('categories/create', views.CategoriesCreateAPIView.as_view(),
         name=views.CategoriesCreateAPIView.name),
    path('categories/', views.CategoriesListAPIView.as_view(),
         name=views.CategoriesListAPIView.name),
    path('categories/<uuid:pk>', views.CategoriesDetailAPIView.as_view(),
         name=views.CategoriesDetailAPIView.name),
    path('categories/<uuid:pk>/update', views.CategoriesUpdateAPIView.as_view(),
         name=views.CategoriesUpdateAPIView.name),
]
