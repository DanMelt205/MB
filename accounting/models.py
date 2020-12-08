from django.db import models
from simple_history.models import HistoricalRecords
from register.models import User


class Account(models.Model):

    account_sides = (
        ("Left", "Left"),
        ("Right", "Right"),
    )

    # Left Assests | Expenses
    # Right Liability | Equity | Revenue

    account_catagories = (
        ("Assets", "Assets"),
        ("Liabilities", "Liabilities"),
        ("Equity", "Equity"),
        ("Revenues", "Revenues"),
        ("Expenses", "Expenses"),
    )

    account_subcatagories = (
        # Assets
        ("Cash", "Cash"),
        ("Receivables", "Receivables"),
        ("Inventories", "Inventories"),
        ("Prepaid Items", "Prepaid Items"),
        ("Long-Term Investments", "Long-Term Investments"),
        ("Land", "Land"),
        ("Building", "Building"),
        ("Equipment", "Equipment"),
        ("Intangibles", "Intangibles"),
        # Liabilites
        ("Short-Term Payables", "Short-Term Payables"),
        ("Employee Payroll", "Employee Payroll"),
        ("Sales Tax", "Sales Tax"),
        ("Deferred Revenues and Long-Term Debt",
         "Deferred Revenues and Long-Term Debt"),
        ("Long-Term Liabilities", "Long-Term Liabilities"),
        # No Subcatagory Equity
        ("Retained Earnings", "Retained Earnings"),
        # Revenue
        ("Operating Revenues", "Operating Revenues"),
        ("Other Revenues", "Other Revenues"),
        # Expenses
        ("Cost of Goods Sold", "Cost of Goods Sold"),
        ("Selling Expenses", "Selling Expenses"),
        ("General and Administrative Expenses",
         "General and Administrative Expenses"),
        ("Other Expenses", "Other Expenses"),
    )

    acccount_statements = (
        ("Income", "Income"),
        ("Balance", "Balance"),
        ("Retained", "Retained"),
    )

    acccount_statuses = (
        ("Active", "Active"),
        ("Deactive", "Deactive"),
        ("Pending", "Pending"),
    )

    account_name = models.CharField(unique=True, max_length=50, null=True)
    account_number = models.PositiveIntegerField(
        unique=True,
        null=True,
    )
    account_description = models.TextField(blank=True)
    account_side = models.CharField(
        choices=account_sides, max_length=10)
    account_catagory = models.CharField(
        choices=account_catagories, max_length=255, null=True)
    account_subcatagory = models.CharField(
        choices=account_subcatagories, max_length=255, null=True)
    account_inital_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    account_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    account_debit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    account_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    account_statement = models.CharField(
        choices=acccount_statements, max_length=50, null=True)
    account_status = models.CharField(
        choices=acccount_statuses, max_length=10, default="Active"
    )
    account_comment = models.TextField(blank=True)

    account_user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    history = HistoricalRecords(
        table_name='accounting_eventlog',

    )

    def __str__(self):
        return str(self.account_name)

    class Meta:
        ordering = ('account_creation_date',)


class Transaction(models.Model):

    transaction_statuses = (
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Pending", "Pending"),
    )

    transaction_types = (
        ("Adjusting", "Adjusting"),
        ("Regular", "Regular"),
        ("Reversing", "Reversing"),
        ("Closing", "Closing"),
    )

    transaction_status = models.CharField(
        choices=transaction_statuses, max_length=10, default="Pending"
    )
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_description = models.TextField(blank=True)
    transaction_comment = models.TextField(blank=True)
    transaction_type = models.CharField(
        choices=transaction_types, max_length=10, default="Regular"
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-transaction_date',)


class Document(models.Model):
    document = models.FileField(
        upload_to='transaction_documents/', blank=True, null=True)

    transaction = models.ForeignKey(
        Transaction,
        models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)


class Ledger(models.Model):

    ledger_debit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    ledger_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    transaction = models.ForeignKey(
        Transaction,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    account = models.ForeignKey(
        Account,
        models.CASCADE,
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('id',)
