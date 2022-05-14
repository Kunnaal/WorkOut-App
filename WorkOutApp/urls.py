from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('welcome.urls')),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('auth/', include('authentication.urls')),
]
