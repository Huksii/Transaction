from rest_framework import routers
from .views import UserViewSet, ProfileViewSet, TransactionViewSet, AddBalanceViewSet

router = routers.DefaultRouter()
router.register('users/', UserViewSet, basename='users')
router.register('profiles/', ProfileViewSet, basename='profiles')
router.register('transactions/', TransactionViewSet, basename='transactions')
router.register('add-balance/', AddBalanceViewSet, basename='add-balance')

urlpatterns = router.urls