from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet

router = DefaultRouter()
router.register('files', FileViewSet, basename='files')

app_name = 'files'
urlpatterns = [
    path('api/v1/', include(router.urls))
]
