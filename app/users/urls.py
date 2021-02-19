from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path("merchant/", views.MerchantCreate.as_view(),
         name=views.MerchantCreate.name),

    path('register/', views.AnyUserRegisterAPIView.as_view(),
         name=views.AnyUserRegisterAPIView.name),
    path('user/', views.UserAPI.as_view(), name=views.UserAPI.name),
    path('users/', views.UserList.as_view(), name=views.UserList.name),
    path('users/<uuid:pk>', views.UserDetail.as_view(),
         name=views.UserDetail.name),
    path('signin/', views.UserLoginView.as_view(), name="login"),

    path('users/<uuid:pk>/image', views.UserImageAPIView.as_view(),
         name=views.UserImageAPIView.name),
    path('user-image/<uuid:pk>/', views.UserImageDetail.as_view(),
         name=views.UserImageDetail.name),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate_account, name='activate'),

    path('facilities/user', views.FacilityList.as_view(),
         name=views.FacilityList.name),

    path('facilities/user', views.FacilityListForAdmin.as_view(),
         name=views.FacilityListForAdmin.name),

    path('facilities/<uuid:pk>/verify', views.FacilityVerifyAPIView.as_view(),
         name=views.FacilityVerifyAPIView.name),
    path('facilities/default', views.DefaultFacility.as_view(),
         name=views.DefaultFacility.name),
    path('facilities/<uuid:pk>', views.FacilityDetail.as_view(),
         name=views.FacilityDetail.name),
    path('facilities/<uuid:pk>/image', views.FacilityImageAPIView.as_view(),
         name=views.FacilityImageAPIView.name),
    path('facilities/<uuid:pk>/regulator-licence', views.RegulatorLicenceAPIView.as_view(),
         name=views.RegulatorLicenceAPIView.name),
    path('facilities/<uuid:pk>/county-permit', views.CountyPermitAPIView.as_view(),
         name=views.CountyPermitAPIView.name),


    path('facility-image/<uuid:pk>/', views.FacilityImageDetail.as_view(),
         name=views.FacilityImageDetail.name),
    #     Dependants urls
    path('dependants/all', views.AllDependantListAPIView.as_view(),
         name=views.AllDependantListAPIView.name),
    path('dependants/active', views.ActiveDependantListAPIView.as_view(),
         name=views.ActiveDependantListAPIView.name),
    path('dependants/user', views.UserDependantsList.as_view(),
         name=views.UserDependantsList.name),


    path('dependants/<uuid:pk>', views.DependantDetailAPIView.as_view(),
         name=views.DependantDetailAPIView.name),
    path('dependants/<uuid:pk>/update', views.DependantUpdateAPIView.as_view(),
         name=views.DependantUpdateAPIView.name),
    path('accounts/<uuid:pk>/dependant', views.DependantCreateAPIView.as_view(),
         name=views.DependantCreateAPIView.name),



    path('accounts', views.AccountListAPIView.as_view(),
         name=views.AccountListAPIView.name),

    path('accounts/<uuid:pk>', views.AccountDetailAPIView.as_view(),
         name=views.AccountDetailAPIView.name),



    # Cadres urls
    path('cadres/create', views.CadresCreate.as_view(),
         name=views.CadresCreate.name),
    path('cadres/<uuid:pk>', views.CadresDetail.as_view(),
         name=views.CadresDetail.name),
    path('cadres', views.CadresList.as_view(),
         name=views.CadresList.name),


]
