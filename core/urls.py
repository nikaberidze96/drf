from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), # ეს ხაზი რთავს Login-ს
    path('', include('snippets.urls')),
]
