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
    path('notes/create', views.NotesCreateAPIView.as_view(),
         name=views.NotesCreateAPIView.name),
    path('notes', views.NotesListAPIView.as_view(),
         name=views.NotesListAPIView.name),
    path('notes/<uuid:pk>', views.NotesDetailAPIView.as_view(),
         name=views.NotesDetailAPIView.name),
    path('notes/<uuid:pk>/update', views.NotesUpdateAPIView.as_view(),
         name=views.NotesUpdateAPIView.name),

    # # Signs and symptoms urls
    path('symptoms/create', views.SymptomsCreateAPIView.as_view(),
         name=views.SymptomsCreateAPIView.name),
    path('symptoms', views.SymptomsListAPIView.as_view(),
         name=views.SymptomsListAPIView.name),
    path('symptoms/<uuid:pk>', views.SymptomsDetailAPIView.as_view(),
         name=views.SymptomsDetailAPIView.name),
    path('symptoms/<uuid:pk>/update', views.SymptomsUpdateAPIView.as_view(),
         name=views.SymptomsUpdateAPIView.name),


    # # Diagnosis urls
    path('diagnoses/create', views.DiagnosisCreateAPIView.as_view(),
         name=views.DiagnosisCreateAPIView.name),
    path('diagnoses', views.DiagnosisListAPIView.as_view(),
         name=views.DiagnosisListAPIView.name),
    path('diagnoses/<uuid:pk>', views.DiagnosisDetailAPIView.as_view(),
         name=views.DiagnosisDetailAPIView.name),
    path('diagnoses/<uuid:pk>/update', views.DiagnosisUpdateAPIView.as_view(),
         name=views.DiagnosisUpdateAPIView.name),


    # # Differential Diagnosis urls
    path('differential-diagnoses/create', views.DifferentialDiagnosisCreateAPIView.as_view(),
         name=views.DifferentialDiagnosisCreateAPIView.name),
    path('differential-diagnoses', views.DifferentialDiagnosisListAPIView.as_view(),
         name=views.DifferentialDiagnosisListAPIView.name),
    path('differential-diagnoses/<uuid:pk>', views.DifferentialDiagnosisDetailAPIView.as_view(),
         name=views.DifferentialDiagnosisDetailAPIView.name),
    path('differential-diagnoses/<uuid:pk>/update', views.DifferentialDiagnosisUpdateAPIView.as_view(),
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
