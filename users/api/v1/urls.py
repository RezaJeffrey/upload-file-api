from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    ('api/v1/token/', TokenObtainPairView.as_view(), 'token_obtain'),
    ('api/v1/token/refresh/', TokenRefreshView.as_view(), 'token_refresh'),
]
