from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from apps.views import ProductModelViewSet, QRCodeView, OrderModelViewSet, CategoryApiView, RegisterView, \
    SendVerificationAPIView, CheckVerifyEmailView, PasswordResetView, RealTimeOrderAPIView

router = DefaultRouter()
router.register('products', ProductModelViewSet, 'products')
router.register('orders', OrderModelViewSet, 'orders')
router.register('password-reset', PasswordResetView, 'password-reset')
router.register('mongo-db', RealTimeOrderAPIView, 'mongo-db')
urlpatterns = [
    path('', include(router.urls)),

    path('qr/', QRCodeView.as_view(), name='qr'),
    # path('order/', OrderModelViewSet.as_view(), name='order'),
    path('category/', CategoryApiView.as_view(), name='category'),

    path('register', RegisterView.as_view(), name='register'),
    path('send-verification-email', SendVerificationAPIView.as_view(), name='send-verification-email'),
    path('check-verify-email', CheckVerifyEmailView.as_view(), name='check-verify-email'),

    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),
]
