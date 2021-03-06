from django.urls import path
from . import views
from django.conf.urls import url
# from users.views import FacilityDetail

urlpatterns = [
    path('retailer-accounts/create', views.RetailerAccountsCreateAPIView.as_view(),
         name=views.RetailerAccountsCreateAPIView.name),
    path('retailer-accounts/retailer', views.RetailRetailerAccountsListAPIView.as_view(),
         name=views.RetailRetailerAccountsListAPIView.name),

    path('retailer-accounts/wholesaler', views.WholesaleRetailerAccountsListAPIView.as_view(),
         name=views.WholesaleRetailerAccountsListAPIView.name),
    path('retailer-accounts/<uuid:pk>', views.RetailerAccountsDetailAPIView.as_view(),
         name=views.RetailerAccountsDetailAPIView.name),
    path('retailer-accounts/<uuid:pk>/update', views.RetailerAccountsUpdateAPIView.as_view(),
         name=views.RetailerAccountsUpdateAPIView.name),


    #     path('wholesale-products/create', views.WholesaleProductsCreateAPIView.as_view(),
    #          name=views.WholesaleProductsCreateAPIView.name),
    #     path('wholesale-products/wholesaler', views.WholesaleProductsListForWholesaler.as_view(),
    #          name=views.WholesaleProductsListForWholesaler.name),
    #     path('wholesale-products/retailer', views.WholesaleProductsListForRetailer.as_view(),
    #          name=views.WholesaleProductsListForRetailer.name),
    #     path('wholesale-products/<uuid:pk>', views.WholesaleProductsDetailAPIView.as_view(),
    #          name=views.WholesaleProductsDetailAPIView.name),
    #     path('wholesale-products/<uuid:pk>/update', views.WholesaleProductsUpdateAPIView.as_view(),
    #          name=views.WholesaleProductsUpdateAPIView.name),



    path('wholesale-variations/create', views.WholesaleVariationsCreateAPIView.as_view(),
         name=views.WholesaleVariationsCreateAPIView.name),
    path('wholesale-variations/retailer', views.WholesaleVariationsListForRetailer.as_view(),
         name=views.WholesaleVariationsListForRetailer.name),
    path('wholesale-variations/wholesaler', views.WholesaleVariationsListForWholesaler.as_view(),
         name=views.WholesaleVariationsListForWholesaler.name),
    path('wholesale-variations/<uuid:pk>', views.WholesaleVariationsDetailAPIView.as_view(),
         name=views.WholesaleVariationsDetailAPIView.name),
    path('wholesale-variations/<uuid:pk>/update', views.WholesaleVariationsUpdateAPIView.as_view(),
         name=views.WholesaleVariationsUpdateAPIView.name),

    path('bonuses/create', views.BonusesCreateAPIView.as_view(),
         name=views.BonusesCreateAPIView.name),
    path('bonuses', views.BonusesListAPIView.as_view(),
         name=views.BonusesListAPIView.name),
    path('bonuses/<uuid:pk>', views.BonusesDetailAPIView.as_view(),
         name=views.BonusesDetailAPIView.name),
    path('bonuses/<uuid:pk>/', views.BonusesUpdateAPIView.as_view(),
         name=views.BonusesUpdateAPIView.name),

    path('discounts/create', views.DiscountsCreateAPIView.as_view(),
         name=views.DiscountsCreateAPIView.name),
    path('discounts', views.DiscountsListAPIView.as_view(),
         name=views.DiscountsListAPIView.name),
    path('discounts/<uuid:pk>', views.DiscountsDetailAPIView.as_view(),
         name=views.DiscountsDetailAPIView.name),
    path('discounts/<uuid:pk>/update', views.DiscountsUpdateAPIView.as_view(),
         name=views.DiscountsUpdateAPIView.name),


    path('requisitions/create', views.RequisitionsCreateAPIView.as_view(),
         name=views.RequisitionsCreateAPIView.name),
    path('requisitions/retailer', views.RequisitionsListForRetailer.as_view(),
         name=views.RequisitionsListForRetailer.name),
    path('requisitions/wholesaler', views.RequisitionsListForWholesaler.as_view(),
         name=views.RequisitionsListForWholesaler.name),
    path('requisitions/<uuid:pk>', views.RequisitionsDetailAPIView.as_view(),
         name=views.RequisitionsDetailAPIView.name),
    path('requisitions/<uuid:pk>/update', views.RequisitionsUpdateAPIView.as_view(),
         name=views.RequisitionsUpdateAPIView.name),
    path('requisitions/<uuid:pk>/retailer-confirm', views.RetailerConfirmRequisitionAPIView.as_view(),
         name=views.RetailerConfirmRequisitionAPIView.name),

    path('requisition-items/create', views.RequisitionItemsCreateAPIView.as_view(),
         name=views.RequisitionItemsCreateAPIView.name),
    path('requisition-items/retailer', views.RetailerRequisitionItemsListAPIView.as_view(),
         name=views.RetailerRequisitionItemsListAPIView.name),
    path('requisition-items/wholesaler', views.WholesaleRequisitionItemsListAPIView.as_view(),
         name=views.WholesaleRequisitionItemsListAPIView.name),
    path('requisition-items/<uuid:pk>', views.RequisitionItemsDetailAPIView.as_view(),
         name=views.RequisitionItemsDetailAPIView.name),
    path('requisition-items/<uuid:pk>/update', views.RequisitionItemsUpdateAPIView.as_view(),
         name=views.RequisitionItemsUpdateAPIView.name),


    path('requisition-payments', views.RequisitionPaymentsListAPIView.as_view(),
         name=views.RequisitionPaymentsListAPIView.name),
    path('requisition-payments/<uuid:pk>', views.RequisitionPaymentsDetailAPIView.as_view(),
         name=views.RequisitionPaymentsDetailAPIView.name),
    path('requisition-payments/<uuid:pk>/update', views.RequisitionPaymentsUpdateAPIView.as_view(),
         name=views.RequisitionPaymentsUpdateAPIView.name),

    path('invoices/retailer', views.InvoicesListForRetailer.as_view(),
         name=views.InvoicesListForRetailer.name),
    path('invoices/wholesaler', views.InvoicesListForWholesaler.as_view(),
         name=views.InvoicesListForWholesaler.name),
    path('invoices/<uuid:pk>', views.InvoicesDetailAPIView.as_view(),
         name=views.InvoicesDetailAPIView.name),
    path('invoices/<uuid:pk>/retailer-update', views.InvoicesUpdateForRetailer.as_view(),
         name=views.InvoicesUpdateForRetailer.name),
    path('invoices/<uuid:pk>/wholesaler-update', views.InvoicesUpdateForWholesaler.as_view(),
         name=views.InvoicesUpdateForWholesaler.name),
    path('invoices/<uuid:pk>/retailer-update', views.InvoicesUpdateForRetailer.as_view(),
         name=views.InvoicesUpdateForRetailer.name),
    path('invoices/<uuid:pk>/courier-update', views.InvoicesUpdateForCourier.as_view(),
         name=views.InvoicesUpdateForCourier.name),

]
