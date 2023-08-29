from django.contrib import admin

from api.models import Transaction, Wallet


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    raw_id_fields = ('wallet',)
    list_display = ('id', 'wallet_id', 'txid', 'amount',)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'balance',)
    readonly_fields = ('balance',)
