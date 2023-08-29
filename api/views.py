from rest_framework import viewsets

from api.models import Transaction, Wallet
from api.serializers import TransactionSerializer, WalletSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    filterset_fields = {
        'id': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
        'wallet_id': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
        'txid': ('icontains', 'iexact', 'contains'),
        'amount': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
    }


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    filterset_fields = {
        'id': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
        'label': ('icontains', 'iexact', 'contains'),
        'balance': ('exact', 'lt', 'gt', 'gte', 'lte', 'in'),
    }
