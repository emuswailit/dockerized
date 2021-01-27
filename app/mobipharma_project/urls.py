"""backend URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from users.views import verify

urlpatterns = [
    path('', include('frontend.urls')),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/subscriptions/', include('subscriptions.urls')),
    path('api/v1/drugs/', include('drugs.urls')),
    path('api/v1/entities/', include('entities.urls')),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/consultations/', include('consultations.urls')),
    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/pharmacies/', include('pharmacies.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('admin/', admin.site.urls),
    url(r'^verify/(?P<uuid>[a-z0-9\-]+)/', verify, name='verify'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
