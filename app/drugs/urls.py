from django.urls import path
from . import views


urlpatterns = [



    # BodySystems urls
    path('body-systems', views.BodySystemListAPIView.as_view(),
         name=views.BodySystemListAPIView.name),
    path('body-systems/<uuid:pk>', views.BodySystemDetailAPIView.as_view(),
         name=views.BodySystemDetailAPIView.name),
    path('body-systems/<uuid:pk>/update', views.BodySystemUpdateAPIView.as_view(),
         name=views.BodySystemUpdateAPIView.name),
    path('body-systems/create', views.BodySystemCreateAPIView.as_view(),
         name=views.BodySystemCreateAPIView.name),


    # Contraindications urls
    path('formulations', views.FormulationListAPIView.as_view(),
         name=views.FormulationListAPIView.name),
    path('formulations/<uuid:pk>', views.FormulationDetailAPIView.as_view(),
         name=views.FormulationDetailAPIView.name),
    path('formulations/<uuid:pk>/update', views.FormulationUpdateAPIView.as_view(),
         name=views.FormulationUpdateAPIView.name),
    path('formulations/create', views.FormulationCreateAPIView.as_view(),
         name=views.FormulationCreateAPIView.name),

    # Contraindications urls
    path('contraindications', views.ContraindicationsListAPIView.as_view(),
         name=views.ContraindicationsListAPIView.name),
    path('contraindications/<uuid:pk>', views.ContraindicationsDetailAPIView.as_view(),
         name=views.ContraindicationsDetailAPIView.name),
    path('contraindications/<uuid:pk>/update', views.ContraindicationsUpdateAPIView.as_view(),
         name=views.ContraindicationsUpdateAPIView.name),
    path('contraindications/create', views.ContraindicationsCreateAPIView.as_view(),
         name=views.ContraindicationsCreateAPIView.name),

    # Distributors urls
    path('distributors', views.DistributorListAPIView.as_view(),
         name=views.DistributorListAPIView.name),
    path('distributors/<uuid:pk>', views.DistributorDetailAPIView.as_view(),
         name=views.DistributorDetailAPIView.name),
    path('distributors/<uuid:pk>/update', views.DistributorUpdateAPIView.as_view(),
         name=views.DistributorUpdateAPIView.name),
    path('distributors/create', views.DistributorCreateAPIView.as_view(),
         name=views.DistributorCreateAPIView.name),


    # Doses urls
    #     path('doses', views.DosesListAPIView.as_view(),
    #          name=views.DosesListAPIView.name),
    #     path('doses/<uuid:pk>', views.DosesDetailAPIView.as_view(),
    #          name=views.DosesDetailAPIView.name),
    #     path('doses/<uuid:pk>/update', views.DosesUpdateAPIView.as_view(),
    #          name=views.DosesUpdateAPIView.name),
    #     path('doses/create', views.DosesCreateAPIView.as_view(),
    #          name=views.DosesCreateAPIView.name),

    # Drug Class urls
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



    # Frequency urls
    path('frequencies', views.FrequencyListAPIView.as_view(),
         name=views.FrequencyListAPIView.name),
    path('frequencies/<uuid:pk>', views.FrequencyDetailAPIView.as_view(),
         name=views.FrequencyDetailAPIView.name),
    path('frequencies/<uuid:pk>/update', views.FrequencyUpdateAPIView.as_view(),
         name=views.FrequencyUpdateAPIView.name),
    path('frequencies/create', views.FrequencyCreateAPIView.as_view(),
         name=views.FrequencyCreateAPIView.name),


    # Generics urls
    path('generics', views.GenericListAPIView.as_view(),
         name=views.GenericListAPIView.name),
    path('generics/reference', views.GenericReferenceListAPIView.as_view(),
         name=views.GenericReferenceListAPIView.name),
    path('generics/<uuid:pk>', views.GenericDetailAPIView.as_view(),
         name=views.GenericDetailAPIView.name),
    path('generics/<uuid:pk>/update', views.GenericUpdateAPIView.as_view(),
         name=views.GenericUpdateAPIView.name),
    path('generics/create', views.GenericCreateAPIView.as_view(),
         name=views.GenericCreateAPIView.name),


    # Indications urls
    path('indications', views.IndicationsListAPIView.as_view(),
         name=views.IndicationsListAPIView.name),
    path('indications/<uuid:pk>', views.IndicationsDetailAPIView.as_view(),
         name=views.IndicationsDetailAPIView.name),
    path('indications/<uuid:pk>/update', views.IndicationsUpdateAPIView.as_view(),
         name=views.IndicationsUpdateAPIView.name),
    path('indications/create', views.IndicationsCreateAPIView.as_view(),
         name=views.IndicationsCreateAPIView.name),


    # Instructions urls
    path('instructions', views.InstructionListAPIView.as_view(),
         name=views.InstructionListAPIView.name),
    path('instructions/<uuid:pk>', views.InstructionDetailAPIView.as_view(),
         name=views.InstructionDetailAPIView.name),
    path('instructions/<uuid:pk>/update', views.InstructionUpdateAPIView.as_view(),
         name=views.InstructionUpdateAPIView.name),
    path('instructions/create', views.InstructionCreateAPIView.as_view(),
         name=views.InstructionCreateAPIView.name),


    # Drug interactions urls
    path('interactions', views.InteractionsListAPIView.as_view(),
         name=views.InteractionsListAPIView.name),
    path('interactions/<uuid:pk>', views.InteractionsDetailAPIView.as_view(),
         name=views.InteractionsDetailAPIView.name),
    path('interactions/<uuid:pk>/update', views.InteractionsUpdateAPIView.as_view(),
         name=views.InteractionsUpdateAPIView.name),
    path('interactions/create', views.InteractionsCreateAPIView.as_view(),
         name=views.InteractionsCreateAPIView.name),
    # Manufacturers urls
    path('manufacturers', views.ManufacturerListAPIView.as_view(),
         name=views.ManufacturerListAPIView.name),
    path('manufacturers/<uuid:pk>', views.ManufacturerDetailAPIView.as_view(),
         name=views.ManufacturerDetailAPIView.name),
    path('manufacturers/<uuid:pk>/update', views.ManufacturerUpdateAPIView.as_view(),
         name=views.ManufacturerUpdateAPIView.name),
    path('manufacturers/create', views.ManufacturerCreateAPIView.as_view(),
         name=views.ManufacturerCreateAPIView.name),

    # Posology urls
    path('posologies', views.PosologyListAPIView.as_view(),
         name=views.PosologyListAPIView.name),
    path('posologies/<uuid:pk>', views.PosologyDetailAPIView.as_view(),
         name=views.PosologyDetailAPIView.name),
    path('posologies/<uuid:pk>/update', views.PosologyUpdateAPIView.as_view(),
         name=views.PosologyUpdateAPIView.name),
    path('posologies/create', views.PosologyCreateAPIView.as_view(),
         name=views.PosologyCreateAPIView.name),


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





    # Mode of actions urls
    path('mode-of-actions', views.ModeOfActionsListAPIView.as_view(),
         name=views.ModeOfActionsListAPIView.name),
    path('mode-of-actions/<uuid:pk>', views.ModeOfActionsDetailAPIView.as_view(),
         name=views.ModeOfActionsDetailAPIView.name),
    path('mode-of-actions/<uuid:pk>/update', views.ModeOfActionsUpdateAPIView.as_view(),
         name=views.ModeOfActionsUpdateAPIView.name),
    path('mode-of-actions/create', views.ModeOfActionsCreateAPIView.as_view(),
         name=views.ModeOfActionsCreateAPIView.name),





    # Drug interactions urls
    path('side-effects', views.SideEffectsListAPIView.as_view(),
         name=views.SideEffectsListAPIView.name),
    path('side-effects/<uuid:pk>', views.SideEffectsDetailAPIView.as_view(),
         name=views.SideEffectsDetailAPIView.name),
    path('side-effects/<uuid:pk>/update', views.SideEffectsUpdateAPIView.as_view(),
         name=views.SideEffectsUpdateAPIView.name),
    path('side-effects/create', views.SideEffectsCreateAPIView.as_view(),
         name=views.SideEffectsCreateAPIView.name),

    # Drug precautions urls
    path('precautions', views.PrecautionsListAPIView.as_view(),
         name=views.PrecautionsListAPIView.name),
    path('precautions/<uuid:pk>', views.PrecautionsDetailAPIView.as_view(),
         name=views.PrecautionsDetailAPIView.name),
    path('precautions/<uuid:pk>/update', views.PrecautionsUpdateAPIView.as_view(),
         name=views.PrecautionsUpdateAPIView.name),
    path('precautions/create', views.PrecautionsCreateAPIView.as_view(),
         name=views.PrecautionsCreateAPIView.name),

    # Drug special considerations urls
    path('considerations', views.ConsiderationsListAPIView.as_view(),
         name=views.ConsiderationsListAPIView.name),
    path('considerations/<uuid:pk>', views.ConsiderationsDetailAPIView.as_view(),
         name=views.ConsiderationsDetailAPIView.name),
    path('considerations/<uuid:pk>/update', views.ConsiderationsUpdateAPIView.as_view(),
         name=views.ConsiderationsUpdateAPIView.name),
    path('considerations/create', views.ConsiderationsCreateAPIView.as_view(),
         name=views.ConsiderationsCreateAPIView.name),


]
