
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wos.views import CategoryProductViewSet

router = DefaultRouter()
router.register(r'category-product', CategoryProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # path('', include('wos.urls')),
]
