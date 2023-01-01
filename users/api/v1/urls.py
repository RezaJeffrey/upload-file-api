from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, 'users')

app_name = 'users'
urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router.urls)),
]
