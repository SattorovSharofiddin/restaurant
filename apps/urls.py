from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from apps.views import ProductModelViewSet

router = DefaultRouter()
router.register('users', ProductModelViewSet, 'users')

urlpatterns = [
    path('products/', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),
]
