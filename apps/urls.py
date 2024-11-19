from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from apps.views import ProductModelViewSet, QRCodeView, OrderModelViewSet, CategoryApiView

router = DefaultRouter()
router.register('products', ProductModelViewSet, 'products')
router.register('orders', OrderModelViewSet, 'orders')
urlpatterns = [
    path('', include(router.urls)),

    path('qr/', QRCodeView.as_view(), name='qr'),

    path('category/', CategoryApiView.as_view(), name='category'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),
]
