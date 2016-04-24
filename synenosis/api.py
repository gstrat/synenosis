from rest_framework import routers
from .views import InstitutionViewSet, BankAccountViewSet, \
        WalletViewSet, AccountListing, TransactionViewSet

router = routers.SimpleRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'bankaccounts', BankAccountViewSet)
router.register(r'walletaccounts', WalletViewSet)
router.register(r'accounts', AccountListing)
router.register(r'transactions', TransactionViewSet)
