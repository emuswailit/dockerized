from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

    # Disease urls
    path('diseases/create', views.DiseaseCreateAPIView.as_view(),
         name=views.DiseaseCreateAPIView.name),
    path('diseases', views.DiseaseListAPIView.as_view(),
         name=views.DiseaseListAPIView.name),
    path('diseases/<uuid:pk>', views.DiseaseDetailAPIView.as_view(),
         name=views.DiseaseDetailAPIView.name),
    path('diseases/<uuid:pk>/update', views.DiseaseUpdateAPIView.as_view(),
         name=views.DiseaseUpdateAPIView.name),

    # # Disease notes
    path('disease-notes/create', views.DiseaseNotesCreateAPIView.as_view(),
         name=views.DiseaseNotesCreateAPIView.name),
    path('disease-notes', views.DiseaseNotesListAPIView.as_view(),
         name=views.DiseaseNotesListAPIView.name),
    path('disease-notes/<uuid:pk>', views.DiseaseNotesDetailAPIView.as_view(),
         name=views.DiseaseNotesDetailAPIView.name),
    path('disease-notes/<uuid:pk>/update', views.DiseaseNotesUpdateAPIView.as_view(),
         name=views.DiseaseNotesUpdateAPIView.name),

    # # Signs and symptoms urls
    path('diagnosis/create', views.SignsAndSymptomsCreateAPIView.as_view(),
         name=views.SignsAndSymptomsCreateAPIView.name),
    path('signs-and-symptoms', views.SignsAndSymptomsListAPIView.as_view(),
         name=views.SignsAndSymptomsListAPIView.name),
    path('signs-and-symptoms/<uuid:pk>', views.SignsAndSymptomsDetailAPIView.as_view(),
         name=views.SignsAndSymptomsDetailAPIView.name),
    path('signs-and-symptoms/<uuid:pk>/update', views.SignsAndSymptomsUpdateAPIView.as_view(),
         name=views.SignsAndSymptomsUpdateAPIView.name),


    # # Diagnosis urls
    path('diagnosis/create', views.DiagnosisCreateAPIView.as_view(),
         name=views.DiagnosisCreateAPIView.name),
    path('diagnosis', views.DiagnosisListAPIView.as_view(),
         name=views.DiagnosisListAPIView.name),
    path('diagnosis/<uuid:pk>', views.DiagnosisDetailAPIView.as_view(),
         name=views.DiagnosisDetailAPIView.name),
    path('diagnosis/<uuid:pk>/update', views.DiagnosisUpdateAPIView.as_view(),
         name=views.DiagnosisUpdateAPIView.name),


    # # Differential Diagnosis urls
    path('differential-diagnosis/create', views.DifferentialDiagnosisCreateAPIView.as_view(),
         name=views.DifferentialDiagnosisCreateAPIView.name),
    path('differential-diagnosis', views.DifferentialDiagnosisListAPIView.as_view(),
         name=views.DifferentialDiagnosisListAPIView.name),
    path('differential-diagnosis/<uuid:pk>', views.DifferentialDiagnosisDetailAPIView.as_view(),
         name=views.DifferentialDiagnosisDetailAPIView.name),
    path('differential-diagnosis/<uuid:pk>/update', views.DifferentialDiagnosisUpdateAPIView.as_view(),
         name=views.DifferentialDiagnosisUpdateAPIView.name),


    # # Management urls
    path('management/create', views.ManagementCreateAPIView.as_view(),
         name=views.ManagementCreateAPIView.name),
    path('management', views.ManagementListAPIView.as_view(),
         name=views.ManagementListAPIView.name),
    path('management/<uuid:pk>', views.ManagementDetailAPIView.as_view(),
         name=views.ManagementDetailAPIView.name),
    path('management/<uuid:pk>/update', views.ManagementUpdateAPIView.as_view(),
         name=views.ManagementUpdateAPIView.name),

    # # Prevention urls
    path('prevention/create', views.PreventionCreateAPIView.as_view(),
         name=views.PreventionCreateAPIView.name),
    path('prevention', views.PreventionListAPIView.as_view(),
         name=views.PreventionListAPIView.name),
    path('prevention/<uuid:pk>', views.PreventionDetailAPIView.as_view(),
         name=views.PreventionDetailAPIView.name),
    path('prevention/<uuid:pk>/update', views.PreventionUpdateAPIView.as_view(),
         name=views.PreventionUpdateAPIView.name),


    # # Disease stages urls
    path('disease-stages/create', views.DiseaseStagesCreateAPIView.as_view(),
         name=views.DiseaseStagesCreateAPIView.name),
    path('disease-stages', views.DiseaseStagesListAPIView.as_view(),
         name=views.DiseaseStagesListAPIView.name),
    path('disease-stages/<uuid:pk>', views.DiseaseStagesDetailAPIView.as_view(),
         name=views.DiseaseStagesDetailAPIView.name),
    path('disease-stages/<uuid:pk>/update', views.DiseaseStagesUpdateAPIView.as_view(),
         name=views.DiseaseStagesUpdateAPIView.name),

    # # Disease stage Categories urls
    path('disease-stage-categories/create', views.DiseaseStageCategoriesCreateAPIView.as_view(),
         name=views.DiseaseStageCategoriesCreateAPIView.name),
    path('disease-stage-categories', views.DiseaseStageCategoriesListAPIView.as_view(),
         name=views.DiseaseStageCategoriesListAPIView.name),
    path('disease-stage-categories/<uuid:pk>', views.DiseaseStageCategoriesDetailAPIView.as_view(),
         name=views.DiseaseStageCategoriesDetailAPIView.name),
    path('disease-stage-categories/<uuid:pk>/update', views.DiseaseStageCategoriesUpdateAPIView.as_view(),
         name=views.DiseaseStageCategoriesUpdateAPIView.name),

    # # Sources urls
    path('sources/create', views.SourcesCreateAPIView.as_view(),
         name=views.SourcesCreateAPIView.name),
    path('sources', views.SourcesListAPIView.as_view(),
         name=views.SourcesListAPIView.name),
    path('sources/<uuid:pk>', views.SourcesDetailAPIView.as_view(),
         name=views.SourcesDetailAPIView.name),
    path('sources/<uuid:pk>/update', views.SourcesUpdateAPIView.as_view(),
         name=views.SourcesUpdateAPIView.name),

]
