from django_filters import FilterSet, DateRangeFilter, DateFilter, CharFilter
from .models import Account, Transaction, Ledger


class AccountFilter(FilterSet):

    class Meta:
        model = Account
        fields = ['account_name', 'account_number', 'account_catagory',
                  'account_subcatagory', 'account_balance']


class IncomeFilter(FilterSet):
    date_range = DateRangeFilter(field_name='account_creation_date')
    start_date = DateFilter(
        field_name='account_creation_date', lookup_expr='lt')
    end_date = DateFilter(
        field_name='account_creation_date', lookup_expr='gt')

    class Meta:
        model = Account
        fields = ['date_range', 'start_date', 'end_date']


class AccountSheetFilter(FilterSet):
    date_range = DateRangeFilter(field_name='transaction__transaction_date')
    start_date = DateFilter(
        field_name='transaction__transaction_date', lookup_expr='lt')
    end_date = DateFilter(
        field_name='transaction__transaction_date', lookup_expr='gt')

    class Meta:
        model = Ledger
        fields = ['date_range', 'start_date', 'end_date']


class EventFilter(FilterSet):

    history_date = DateRangeFilter(
        field_name='history_date', lookup_expr='lt')

    class Meta:
        model = Account.history.model
        fields = ['account_name', 'account_number', 'account_status',
                  'history_user', 'history_date', 'history_id']


class TransactionFilter(FilterSet):

    date_range = DateRangeFilter(field_name='transaction_date')
    start_date = DateFilter(
        field_name='transaction_date', lookup_expr='lt')
    end_date = DateFilter(
        field_name='transaction_date', lookup_expr='gt')

    class Meta:
        model = Transaction
        fields = ['transaction_status', 'date_range', 'start_date', 'end_date']


class LedgerFilter(FilterSet):

    date_range = DateRangeFilter(field_name='transaction__transaction_date')
    start_date = DateFilter(
        field_name='transaction__transaction_date', lookup_expr='lt')
    end_date = DateFilter(
        field_name='transaction__transaction_date', lookup_expr='gt')

    class Meta:
        model = Ledger
        fields = ['date_range', 'start_date', 'end_date']
