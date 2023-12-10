from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main.views import UserViewSet, ProfileViewSet, TransactionViewSet, AddBalanceViewSet
from rest_framework import routers, permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Portfolio API Documentation",
    default_version='v1',
    description="Backend Portfolio API Documentation",
    contact=openapi.Contact(name="yeraly", email="turarbekoveraly17@gmail.com"),
    license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'addbalance', AddBalanceViewSet)                # r - read

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc/', include('django.contrib.admindocs.urls')),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)