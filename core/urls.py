from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.api.v1.urls', namespace='users')),
    path('files/', include('files.api.v1.urls', namespace='files')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
