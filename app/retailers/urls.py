from django.urls import path
from . import views
from django.conf.urls import url
from users.views import FacilityDetail

urlpatterns = [

    path('forwards/create', views.ForwardsCreate.as_view(),
         name=views.ForwardsCreate.name),
    path('forwards/<uuid:pk>', views.ForwardsDetailAPIView.as_view(),
         name=views.ForwardsDetailAPIView.name),
    path('forwards/client', views.ForwardsListAPIView.as_view(),
         name=views.ForwardsListAPIView.name),
    path('forwards/facility', views.ForwardssForFacility.as_view(),
         name=views.ForwardssForFacility.name),


    path('pharmacies/', views.PharmacyListAPIView.as_view(),
         name=views.PharmacyListAPIView.name),
    path('pharmacies/<uuid:pk>', views.PharmacyListAPIView.as_view(),
         name=views.PharmacyListAPIView.name),
    path('clinics', views.ClinicListAPIView.as_view(),
         name=views.ClinicListAPIView.name),
    path('clinics/<uuid:pk>', views.ClinicDetailAPIView.as_view(),
         name=views.ClinicDetailAPIView.name),
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

    # Pharmacist confirms prescription quote
    path('prescription-quotes/<uuid:pk>/pharmacist-confirm', views.PharmacistConfirmPrescriptionQuote.as_view(),
         name=views.PharmacistConfirmPrescriptionQuote.name),

    #     # Client confirms prescripption quote
    #     path('prescription-quotes/<uuid:pk>/client-confirm', views.ClientConfirmQuote.as_view(),
    #          name=views.ClientConfirmQuote.name),



    path('prescription-quotes/<uuid:pk>/item', views.QuoteItemCreate.as_view(),
         name=views.QuoteItemCreate.name),
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

    path('prescription-quote-items', views.QuoteItemListAPIView.as_view(),
         name=views.QuoteItemListAPIView.name),
    path('prescription-quotes/<uuid:pk>/items', views.PrescriptionQuoteItemsList.as_view(),
         name=views.PrescriptionQuoteItemsList.name),

    path('orders/facility', views.FacilityOrdersList.as_view(),
         name=views.FacilityOrdersList.name),
    path('orders/client', views.ClientOrdersList.as_view(),
         name=views.ClientOrdersList.name),
    path('orders/<uuid:pk>', views.OrderDetailAPIView.as_view(),
         name=views.OrderDetailAPIView.name),

    path('orders/<uuid:pk>/client-confirm', views.ClientConfirmOrderAPIView.as_view(),
         name=views.ClientConfirmOrderAPIView.name),
    path('order-items/all', views.AllOrderItemsList.as_view(),
         name=views.AllOrderItemsList.name),
    path('order-items/<uuid:pk>', views.OrderItemDetailAPIView.as_view(),
         name=views.OrderItemDetailAPIView.name),

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

]
