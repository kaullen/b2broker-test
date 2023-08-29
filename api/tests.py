from decimal import Decimal

import pytest

from api.models import Wallet, Transaction


@pytest.fixture
def wallet():
    return Wallet.objects.create(label='test_wallet')


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_amount, expected_balance', [
    (Decimal('10'), Decimal('1010')),
    (Decimal('-10'), Decimal('990')),
    (Decimal('1234.567890'), Decimal('2234.567890')),
])
def test_balance_transaction_created(wallet, transaction_amount, expected_balance):
    wallet.balance = Decimal('1000')
    wallet.save(update_fields=['balance'])

    Transaction.objects.create(wallet=wallet, txid='test', amount=transaction_amount)

    wallet.refresh_from_db()
    assert wallet.balance == expected_balance


@pytest.mark.django_db
@pytest.mark.parametrize('amount_before, amount_after, expected_balance', [
    (Decimal('10'), Decimal('-10'), Decimal('980')),
    (Decimal('-10'), Decimal('-20'), Decimal('990')),
    (Decimal('1234.567890'), Decimal('234.567890'), Decimal('0')),
])
def test_balance_transaction_updated(wallet, amount_before, amount_after, expected_balance):
    transaction = Transaction.objects.create(wallet=wallet, txid='test', amount=amount_before)

    wallet.balance = Decimal('1000')
    wallet.save(update_fields=['balance'])

    transaction.amount = amount_after
    transaction.save(update_fields=['amount'])

    wallet.refresh_from_db()
    assert wallet.balance == expected_balance


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_amount, expected_balance', [
    (Decimal('10'), Decimal('990')),
    (Decimal('-10'), Decimal('1010')),
    (Decimal('1234.567890'), Decimal('-234.567890')),
])
def test_balance_transaction_deleted(wallet, transaction_amount, expected_balance):
    transaction = Transaction.objects.create(wallet=wallet, txid='test', amount=transaction_amount)

    wallet.balance = Decimal('1000')
    wallet.save(update_fields=['balance'])

    transaction.delete()

    wallet.refresh_from_db()
    assert wallet.balance == expected_balance
