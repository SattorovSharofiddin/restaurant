from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProductModelViewSet

router = DefaultRouter()
router.register('users', ProductModelViewSet, 'users')

urlpatterns = [
    path('products/', include(router.urls)),
]
