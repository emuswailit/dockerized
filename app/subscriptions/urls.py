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
    path('subscriptions/create', views.SubscriptionCreateAPIView.as_view(),
         name=views.SubscriptionCreateAPIView.name),
    path('subscriptions/', views.SubscriptionListAPIView.as_view(),
         name=views.SubscriptionListAPIView.name),

    path('subscriptions/<uuid:pk>/', views.SubscriptionDetailAPIView.as_view(),
         name=views.SubscriptionDetailAPIView.name),
    path('subscriptions/<uuid:pk>/update', views.SubscriptionUpdateAPIView.as_view(),
         name=views.SubscriptionUpdateAPIView.name),

          # Subscription payments
    path('subscription-payments/create', views.SubscriptionPaymentsCreate.as_view(),
         name=views.SubscriptionPaymentsCreate.name),
    path('subscription-payments/', views.SubscriptionPaymentsList.as_view(),
         name=views.SubscriptionPaymentsList.name),

    path('subscription-payments/<uuid:pk>/', views.SubscriptionPaymentsDetail.as_view(),
         name=views.SubscriptionPaymentsDetail.name),
    path('subscription-payments/<uuid:pk>/update', views.SubscriptionPaymentsUpdate.as_view(),
         name=views.SubscriptionPaymentsUpdate.name),


]
