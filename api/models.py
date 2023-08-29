from decimal import Decimal

from django.db import models
from django.db import transaction
from django.db.models import F, Case, Exists, When


class Wallet(models.Model):
    label = models.CharField(max_length=150, db_index=True)

    balance = models.DecimalField(max_digits=36, decimal_places=18, default=Decimal('0.0'))


class Transaction(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)

    txid = models.CharField(max_length=150, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # see README.md for reasoning

        if update_fields is not None and 'amount' not in update_fields:
            return super().save(force_insert, force_update, using, update_fields)

        self_query = Transaction.objects.filter(id=self.id)
        old_value_query = Case(
            When(
                Exists(self_query),
                then=self_query.values('amount')[:1],
            ),
            default=Decimal('0.0'),
        )

        with transaction.atomic():
            Wallet.objects.filter(id=self.wallet_id).update(
                balance=F('balance') - old_value_query + self.amount,
            )
            super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic():
            Wallet.objects.filter(id=self.wallet_id).update(
                balance=F('balance') - self.amount,
            )
            super().delete(using, keep_parents)
