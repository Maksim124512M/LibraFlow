from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),
    path('api/v3/', include('api.v3.urls')),
    path('api/v4/', include('api.v4.urls')),
]
