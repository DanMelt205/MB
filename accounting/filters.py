from django_filters import FilterSet
from .models import Account, Transaction, Ledger


class AccountFilter(FilterSet):

    class Meta:
        model = Account
        fields = ['account_name', 'account_number', 'account_catagory',
                  'account_subcatagory', 'account_balance']


class EventFilter(FilterSet):

    class Meta:
        model = Account.history.model
        fields = ['account_name', 'account_number', 'account_status',
                  'history_user', 'history_date', 'history_id']


class TransactionFilter(FilterSet):

    class Meta:
        model = Transaction
        fields = {
            'transaction_status': ['exact'],
            'transaction_date': ['exact', 'range'],
        }


class LedgerFilter(FilterSet):

    class Meta:
        model = Transaction
        fields = {
            'transaction_date': ['exact', 'range'],
        }
