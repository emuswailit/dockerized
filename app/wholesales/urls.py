from django.urls import path
from . import views
from django.conf.urls import url
from users.views import FacilityDetail

urlpatterns = [

    path('wholesale-products/create', views.WholesaleProductsCreateAPIView.as_view(),
         name=views.WholesaleProductsCreateAPIView.name),
    path('wholesale-products', views.WholesaleProductsListAPIView.as_view(),
         name=views.WholesaleProductsListAPIView.name),
    path('wholesale-products/<uuid:pk>', views.WholesaleProductsDetailAPIView.as_view(),
         name=views.WholesaleProductsDetailAPIView.name),
    path('wholesale-products/<uuid:pk>/', views.WholesaleProductsUpdateAPIView.as_view(),
         name=views.WholesaleProductsUpdateAPIView.name),



    path('wholesale-variations/create', views.WholesaleVariationsCreateAPIView.as_view(),
         name=views.WholesaleVariationsCreateAPIView.name),
    path('wholesale-variations', views.WholesaleVariationsListAPIView.as_view(),
         name=views.WholesaleVariationsListAPIView.name),
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
    path('requisitions/retailer', views.RetailerRequisitionsListAPIView.as_view(),
         name=views.RetailerRequisitionsListAPIView.name),
    path('requisitions/wholesaler', views.WholesalerRequisitionsListAPIView.as_view(),
         name=views.WholesalerRequisitionsListAPIView.name),
    path('requisitions/<uuid:pk>', views.RequisitionsDetailAPIView.as_view(),
         name=views.RequisitionsDetailAPIView.name),
    path('requisitions/<uuid:pk>/update', views.RequisitionsUpdateAPIView.as_view(),
         name=views.RequisitionsUpdateAPIView.name),

    path('requisition-items/create', views.RequisitionItemsCreateAPIView.as_view(),
         name=views.RequisitionItemsCreateAPIView.name),
    path('requisition-items', views.RequisitionItemsListAPIView.as_view(),
         name=views.RequisitionItemsListAPIView.name),
    path('requisition-items/<uuid:pk>', views.RequisitionItemsDetailAPIView.as_view(),
         name=views.RequisitionItemsDetailAPIView.name),
    path('requisition-items/<uuid:pk>/update', views.RequisitionItemsUpdateAPIView.as_view(),
         name=views.RequisitionItemsUpdateAPIView.name),


    path('despatches/create', views.DespatchesCreateAPIView.as_view(),
         name=views.DespatchesCreateAPIView.name),
    path('despatches', views.DespatchesListAPIView.as_view(),
         name=views.DespatchesListAPIView.name),
    path('despatches/<uuid:pk>', views.DespatchesDetailAPIView.as_view(),
         name=views.DespatchesDetailAPIView.name),
    path('despatches/<uuid:pk>/update', views.DespatchesUpdateAPIView.as_view(),
         name=views.DespatchesUpdateAPIView.name),

    path('despatch-items/create', views.DespatchItemsCreateAPIView.as_view(),
         name=views.DespatchItemsCreateAPIView.name),
    path('despatch-items', views.DespatchItemsListAPIView.as_view(),
         name=views.DespatchItemsListAPIView.name),
    path('despatch-items/<uuid:pk>', views.DespatchItemsDetailAPIView.as_view(),
         name=views.DespatchItemsDetailAPIView.name),
    path('despatch-items/<uuid:pk>/update', views.DespatchItemsUpdateAPIView.as_view(),
         name=views.DespatchItemsUpdateAPIView.name),


    path('retailer-accounts/create', views.RetailerAccountsCreateAPIView.as_view(),
         name=views.RetailerAccountsCreateAPIView.name),
    path('retailer-accounts', views.RetailerAccountsListAPIView.as_view(),
         name=views.RetailerAccountsListAPIView.name),
    path('retailer-accounts/<uuid:pk>', views.RetailerAccountsDetailAPIView.as_view(),
         name=views.RetailerAccountsDetailAPIView.name),
    path('retailer-accounts/<uuid:pk>/update', views.RetailerAccountsUpdateAPIView.as_view(),
         name=views.RetailerAccountsUpdateAPIView.name),
]
