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

         # Prescription quotes for a pharmacist
     path('prescription-quotes/pharmacist', views.PharmacistPrescriptionQuotesListAPIView.as_view(),
         name=views.PharmacistPrescriptionQuotesListAPIView.name),
    path('prescription-quotes/<uuid:pk>/pharmacist-confirm', views.PharmacistConfirmQuote.as_view(),
         name=views.PharmacistConfirmQuote.name),
     
#     path('prescription-quotes/item', views.QuoteItemCreate.as_view(),
#          name=views.QuoteItemCreate.name),
    path('prescription-quote-item/<uuid:pk>', views.QuoteItemDetailAPIView.as_view(),
         name=views.QuoteItemDetailAPIView.name),

     path('prescription-quote-item/<uuid:pk>/update', views.UpdateQuoteItem.as_view(),
         name=views.UpdateQuoteItem.name),

      path('prescription-quote-item/<uuid:pk>/accept', views.AcceptQuoteItem.as_view(),
         name=views.AcceptQuoteItem.name),


    path('prescription-quote-items/', views.QuoteItemListAPIView.as_view(),
         name=views.QuoteItemListAPIView.name),
     path('prescription-quotes/<uuid:pk>/items', views.PrescriptionQuoteItemsList.as_view(),
         name=views.PrescriptionQuoteItemsList.name),

     path('orders/all', views.AllOrdersList.as_view(),
         name=views.AllOrdersList.name),
    path('orders/<uuid:pk>/', views.OrderDetailAPIView.as_view(),
         name=views.OrderDetailAPIView.name),
    path('orders/<uuid:pk>/confirm', views.ConfirmOrderAPIView.as_view(),
         name=views.ConfirmOrderAPIView.name),
     path('order-items/all', views.AllOrderItemsList.as_view(),
         name=views.AllOrderItemsList.name),
    path('order-items/<uuid:pk>/', views.OrderItemDetailAPIView.as_view(),
         name=views.OrderItemDetailAPIView.name),

]
