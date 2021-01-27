from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('plans/create', views.PlanCreateAPIView.as_view(),
         name=views.PlanCreateAPIView.name),
    path('plans/', views.PlanListAPIView.as_view(),
         name=views.PlanListAPIView.name),

    path('plans/<uuid:pk>/', views.PlanDetailAPIView.as_view(),
         name=views.PlanDetailAPIView.name),
    path('plans/<uuid:pk>/update', views.PlanUpdateAPIView.as_view(),
         name=views.PlanUpdateAPIView.name),


    # Subscriptions methods
    path('subscriptions/', views.SubscriptionListAPIView.as_view(),
         name=views.SubscriptionListAPIView.name),

    path('subscriptions/<uuid:pk>/', views.SubscriptionDetailAPIView.as_view(),
         name=views.SubscriptionDetailAPIView.name),
    path('subscriptions/<uuid:pk>/update', views.SubscriptionUpdateAPIView.as_view(),
         name=views.SubscriptionUpdateAPIView.name),

]
