from django.urls import path
from . import views
from django.conf.urls import url
from users.views import AllDependantListAPIView


urlpatterns = [
#     path('prescriptions/', views.ForwardPrescriptionListAPIView.as_view(),
#          name=views.ForwardPrescriptionListAPIView.name),
#     path('prescriptions/<uuid:pk>/', views.ForwardPrescriptionDetailAPIView.as_view(),
#          name=views.ForwardPrescriptionDetailAPIView.name),


    #     path('prescription-quotes/create', views.PrescriptionQuoteCreate.as_view(),
    #          name=views.PrescriptionQuoteCreate.name),
    path('prescription-quotes/<uuid:pk>/', views.PrescriptionQuoteDetailAPIView.as_view(),
         name=views.PrescriptionQuoteDetailAPIView.name),
    path('prescription-quotes/all', views.AllPrescriptionQuotesListAPIView.as_view(),
         name=views.AllPrescriptionQuotesListAPIView.name),

    # Prescription quotes
     path('prescription-quotes/pharmacist', views.PharmacistPrescriptionQuotesListAPIView.as_view(),
          name=views.PharmacistPrescriptionQuotesListAPIView.name),

    #Pharmacist confirms prescription quote
    path('prescription-quotes/<uuid:pk>/pharmacist-confirm', views.PharmacistConfirmPrescriptionQuote.as_view(),
         name=views.PharmacistConfirmPrescriptionQuote.name),

    #Client confirms prescripption quote
    path('prescription-quotes/<uuid:pk>/client-confirm', views.ClientConfirmQuote.as_view(),
         name=views.ClientConfirmQuote.name),


    path('prescription-quote-item/<uuid:pk>', views.QuoteItemDetailAPIView.as_view(),
         name=views.QuoteItemDetailAPIView.name),

    path('prescription-quote-item/<uuid:pk>/pharmacist-quote', views.PharmacistUpdateQuoteItem.as_view(),
         name=views.PharmacistUpdateQuoteItem.name),

      path('prescription-quote-item/<uuid:pk>/accept', views.AcceptQuoteItem.as_view(),
         name=views.AcceptQuoteItem.name),

    # Pharmacy payments
    path('pharmacy-payments/client', views.ClientPharmacyPaymentsListAPIView.as_view(),
          name=views.ClientPharmacyPaymentsListAPIView.name),

    path('pharmacy-payments/<uuid:pk>', views.PharmacyPaymentsDetailAPIView.as_view(),
         name=views.PharmacyPaymentsDetailAPIView.name),

    path('prescription-quote-items/', views.QuoteItemListAPIView.as_view(),
         name=views.QuoteItemListAPIView.name),
     path('prescription-quotes/<uuid:pk>/items', views.PrescriptionQuoteItemsList.as_view(),
         name=views.PrescriptionQuoteItemsList.name),

    path('orders/facility', views.FacilityOrdersList.as_view(),
          name=views.FacilityOrdersList.name),
    path('orders/client', views.ClientOrdersList.as_view(),
         name=views.ClientOrdersList.name),
    path('orders/<uuid:pk>/', views.OrderDetailAPIView.as_view(),
         name=views.OrderDetailAPIView.name),
     path('order-items/all', views.AllOrderItemsList.as_view(),
         name=views.AllOrderItemsList.name),
    path('order-items/<uuid:pk>/', views.OrderItemDetailAPIView.as_view(),
         name=views.OrderItemDetailAPIView.name),

]
