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


    # Payment methods
    path('payment-methods/create', views.PaymentMethodCreateAPIView.as_view(),
         name=views.PaymentMethodCreateAPIView.name),
    path('payment-methods/', views.PaymentMethodListAPIView.as_view(),
         name=views.PaymentMethodListAPIView.name),

    path('payment-methods/<uuid:pk>/', views.PaymentMethodDetailAPIView.as_view(),
         name=views.PaymentMethodDetailAPIView.name),
    path('payment-methods/<uuid:pk>/update', views.PaymentMethodUpdateAPIView.as_view(),
         name=views.PaymentMethodUpdateAPIView.name),

    # Payments methods
    path('payments/create', views.PaymentCreateAPIView.as_view(),
         name=views.PaymentCreateAPIView.name),
    path('payments/', views.PaymentListAPIView.as_view(),
         name=views.PaymentListAPIView.name),

    path('payments/<uuid:pk>/', views.PaymentDetailAPIView.as_view(),
         name=views.PaymentDetailAPIView.name),
    path('payments/<uuid:pk>/update', views.PaymentUpdateAPIView.as_view(),
         name=views.PaymentUpdateAPIView.name),

    # Subscriptions methods
    path('subscriptions/', views.SubscriptionListAPIView.as_view(),
         name=views.SubscriptionListAPIView.name),

    path('subscriptions/<uuid:pk>/', views.SubscriptionDetailAPIView.as_view(),
         name=views.SubscriptionDetailAPIView.name),
    path('subscriptions/<uuid:pk>/update', views.SubscriptionUpdateAPIView.as_view(),
         name=views.SubscriptionUpdateAPIView.name),

]
