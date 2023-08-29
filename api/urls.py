from rest_framework.routers import DefaultRouter

from api.views import WalletViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'wallets', WalletViewSet)

urlpatterns = router.urls
