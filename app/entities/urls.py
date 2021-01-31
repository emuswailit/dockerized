from django.urls import path
from . import views
from django.conf.urls import url
from users.views import FacilityDetail

urlpatterns = [
    # 1. Facility administrator creates his facility departments
    path('departments/create', views.DepartmentCreate.as_view(),
         name=views.DepartmentCreate.name),
    path('departments/all', views.AllDepartmentListAPIView.as_view(),
         name=views.AllDepartmentListAPIView.name),
    path('departments/facility', views.DepartmentsList.as_view(),
         name=views.DepartmentsList.name),
    path('departments/<uuid:pk>/', views.DepartmentDetailAPIView.as_view(),
         name=views.DepartmentDetailAPIView.name),
    path('departments/<uuid:pk>/update', views.UpdateDepartment.as_view(),
         name=views.UpdateDepartment.name),

    # 2. User with a profession creates and manages professional profile
    path('professionals', views.ProfessionalProfile.as_view(),
         name=views.ProfessionalProfile.name),
    path('professionals/create', views.ProfessionalsCreate.as_view(),
         name=views.ProfessionalsCreate.name),
    path('professionals/all', views.AllProfessionalsList.as_view(),
         name=views.AllProfessionalsList.name),
    path('professionals/available', views.AvailableProfessionalsList.as_view(),
         name=views.AvailableProfessionalsList.name),
    path('professionals/<uuid:pk>', views.ProfessionalDetail.as_view(),
         name=views.ProfessionalDetail.name),
    path('professionals/<uuid:pk>/update', views.ProfessionalUpdate.as_view(),
         name=views.ProfessionalUpdate.name),
    path('professionals/<uuid:pk>/availability', views.SetProfessionalAvailability.as_view(),
         name=views.SetProfessionalAvailability.name),

    # 3. Facility administrator creates and manages job descriptions
    path('jobs/create', views.JobsCreate.as_view(),
         name=views.JobsCreate.name),
    path('jobs/facility', views.FacilityJobsList.as_view(),
         name=views.FacilityJobsList.name),
    path('jobs/advertised', views.AdvertisedJobsList.as_view(),
         name=views.AdvertisedJobsList.name),
    path('jobs/<uuid:pk>', views.JobsDetail.as_view(),
         name=views.JobsDetail.name),
    path('jobs/<uuid:pk>/update', views.JobsUpdate.as_view(),
         name=views.JobsUpdate.name),

    # 4. Facility administrator creates employees
    path('employees/create', views.EmployeesCreate.as_view(),
         name=views.EmployeesCreate.name),
    path('employees/<uuid:pk>', views.EmployeeDetail.as_view(),
         name=views.EmployeeDetail.name),
    path('employees', views.EmployeeList.as_view(),
         name=views.EmployeeList.name),
    path('employees/<uuid:pk>/update', views.EmployeeUpdate.as_view(),
         name=views.EmployeeUpdate.name),


    # Flow moves to consultations app

]
