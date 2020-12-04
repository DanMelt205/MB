from django.contrib import admin
from .models import Account, Ledger, Transaction, Document

admin.site.register(Account)
admin.site.register(Ledger)
admin.site.register(Transaction)
admin.site.register(Document)
