from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

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
    # path('payments/<uuid:pk>/update', views.PaymentUpdateAPIView.as_view(),
    #      name=views.PaymentUpdateAPIView.name),

  

]
