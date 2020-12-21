from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

    # Distributors urls
    path('distributors', views.DistributorListAPIView.as_view(),
         name=views.DistributorListAPIView.name),
    path('distributors/<uuid:pk>', views.DistributorDetailAPIView.as_view(),
         name=views.DistributorDetailAPIView.name),
    path('distributors/<uuid:pk>/update', views.DistributorUpdateAPIView.as_view(),
         name=views.DistributorUpdateAPIView.name),
    path('distributors/create', views.DistributorCreateAPIView.as_view(),
         name=views.DistributorCreateAPIView.name),

    # Posology urls
    path('posologies', views.PosologyListAPIView.as_view(),
         name=views.PosologyListAPIView.name),
    path('posologies/<uuid:pk>', views.PosologyDetailAPIView.as_view(),
         name=views.PosologyDetailAPIView.name),
    path('posologies/<uuid:pk>/update', views.PosologyUpdateAPIView.as_view(),
         name=views.PosologyUpdateAPIView.name),
    path('posologies/create', views.PosologyCreateAPIView.as_view(),
         name=views.PosologyCreateAPIView.name),

    # Frequency urls
    path('frequencies', views.FrequencyListAPIView.as_view(),
         name=views.FrequencyListAPIView.name),
    path('frequencies/<uuid:pk>', views.FrequencyDetailAPIView.as_view(),
         name=views.FrequencyDetailAPIView.name),
    path('frequencies/<uuid:pk>/update', views.FrequencyUpdateAPIView.as_view(),
         name=views.FrequencyUpdateAPIView.name),
    path('frequencies/create', views.FrequencyCreateAPIView.as_view(),
         name=views.FrequencyCreateAPIView.name),

    # Instructions urls
    path('instructions', views.InstructionListAPIView.as_view(),
         name=views.InstructionListAPIView.name),
    path('instructions/<uuid:pk>', views.InstructionDetailAPIView.as_view(),
         name=views.InstructionDetailAPIView.name),
    path('instructions/<uuid:pk>/update', views.InstructionUpdateAPIView.as_view(),
         name=views.InstructionUpdateAPIView.name),
    path('instructions/create', views.InstructionCreateAPIView.as_view(),
         name=views.InstructionCreateAPIView.name),

    # BodySystems urls
    path('body-systems', views.BodySystemListAPIView.as_view(),
         name=views.BodySystemListAPIView.name),
    path('body-systems/<uuid:pk>', views.BodySystemDetailAPIView.as_view(),
         name=views.BodySystemDetailAPIView.name),
    path('body-systems/<uuid:pk>/update', views.BodySystemUpdateAPIView.as_view(),
         name=views.BodySystemUpdateAPIView.name),
    path('body-systems/create', views.BodySystemCreateAPIView.as_view(),
         name=views.BodySystemCreateAPIView.name),



    # Drug Class urls

    # Create a drug class per body system
    path('drug-classes/create', views.DrugClassCreateAPIView.as_view(),
         name=views.DrugClassCreateAPIView.name),
    path('drug-classes', views.DrugClassListAPIView.as_view(),
         name=views.DrugClassListAPIView.name),
    path('drug-classes/<uuid:pk>', views.DrugClassDetailAPIView.as_view(),
         name=views.DrugClassDetailAPIView.name),
    path('drug-classes/<uuid:pk>/update', views.DrugClassUpdateAPIView.as_view(),
         name=views.DrugClassUpdateAPIView.name),

    # Sub Class urls
    path('drug-sub-classes/create', views.DrugSubClassCreateAPIView.as_view(),
         name=views.DrugSubClassCreateAPIView.name),  # Create sub class per class
    path('drug-sub-classes', views.DrugSubClassListAPIView.as_view(),
         name=views.DrugSubClassListAPIView.name),
    path('drug-sub-classes/<uuid:pk>', views.DrugSubClassDetailAPIView.as_view(),
         name=views.DrugSubClassDetailAPIView.name),
    path('drug-sub-classes/<uuid:pk>/update', views.DrugSubClassUpdateAPIView.as_view(),
         name=views.DrugSubClassUpdateAPIView.name),

    # Preparations urls
    path('preparations', views.PreparationListAPIView.as_view(),
         name=views.PreparationListAPIView.name),
    path('preparations/<uuid:pk>', views.PreparationDetailAPIView.as_view(),
         name=views.PreparationDetailAPIView.name),
    path('preparations/<uuid:pk>/update', views.PreparationUpdateAPIView.as_view(),
         name=views.PreparationUpdateAPIView.name),
    path('preparations/create', views.PreparationCreateAPIView.as_view(),
         name=views.PreparationCreateAPIView.name),



    # Products urls
    path('products', views.ProductListAPIView.as_view(),
         name=views.ProductListAPIView.name),
    path('products/<uuid:pk>', views.ProductDetailAPIView.as_view(),
         name=views.ProductDetailAPIView.name),
    path('products/<uuid:pk>/update', views.ProductUpdateAPIView.as_view(),
         name=views.ProductUpdateAPIView.name),
    path('products/create', views.ProductCreateAPIView.as_view(),
         name=views.ProductCreateAPIView.name),

           path('products/<uuid:pk>/images', views.ProductImageList.as_view(),
         name=views.ProductImageList.name),
    path('product-images/<uuid:pk>', views.ProductImageDetail.as_view(),
         name=views.ProductImageDetail.name),

    # Formulations urls
    path('formulations', views.FormulationListAPIView.as_view(),
         name=views.FormulationListAPIView.name),
    path('formulations/<uuid:pk>', views.FormulationDetailAPIView.as_view(),
         name=views.FormulationDetailAPIView.name),
    path('formulations/<uuid:pk>/update', views.FormulationUpdateAPIView.as_view(),
         name=views.FormulationUpdateAPIView.name),
    path('formulations/create', views.FormulationCreateAPIView.as_view(),
         name=views.FormulationCreateAPIView.name),



    # Manufacturers urls
    path('manufacturers', views.ManufacturerListAPIView.as_view(),
         name=views.ManufacturerListAPIView.name),
    path('manufacturers/<uuid:pk>', views.ManufacturerDetailAPIView.as_view(),
         name=views.ManufacturerDetailAPIView.name),
    path('manufacturers/<uuid:pk>/update', views.ManufacturerUpdateAPIView.as_view(),
         name=views.ManufacturerUpdateAPIView.name),
    path('manufacturers/create', views.ManufacturerCreateAPIView.as_view(),
         name=views.ManufacturerCreateAPIView.name),

    # Generics urls
    path('generics', views.GenericListAPIView.as_view(),
         name=views.GenericListAPIView.name),
    path('generics/<uuid:pk>', views.GenericDetailAPIView.as_view(),
         name=views.GenericDetailAPIView.name),
    path('generics/<uuid:pk>/update', views.GenericUpdateAPIView.as_view(),
         name=views.GenericUpdateAPIView.name),
    path('generics/create', views.GenericCreateAPIView.as_view(),
         name=views.GenericCreateAPIView.name),


]
