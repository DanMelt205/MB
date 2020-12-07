from django import forms
from .models import Account, Ledger, Transaction, Document
from django.contrib import messages
from django.forms import modelformset_factory, formset_factory


class AccountCreationForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('account_name', 'account_number', 'account_description',
                  'account_catagory', 'account_subcatagory', 'account_inital_balance',
                  'account_statement', 'account_comment')
        widgets = {
            'account_inital_balance': forms.NumberInput(attrs={'step': 0.01}),
            'account_comment': forms.Textarea(attrs={'row': 5}),
        }

    def save(self, commit=True):
        # Call save of the super of your own class,
        # which is UserCreationForm.save() which calls user.set_password()
        account = super(AccountCreationForm, self).save(commit=False)

        # Add the things your super doesn't do for you
        account.account_balance = self.cleaned_data.get(
            "account_inital_balance")
        account.account_side = self.accountSide()

        if commit:
            account.save()

        return account

    # Left Assests | Expenses
    # Right Liability | Equity | Revenue

    def accountSide(self):
        catagory = self.cleaned_data.get("account_catagory")

        if catagory == "Assets" or catagory == "Expenses":
            return "Left"
        else:
            return "Right"


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('account_name', 'account_description',
                  'account_comment', 'account_status')
        widgets = {
            'account_description': forms.Textarea(attrs={'rows': 5}),
        }


class LedgerCreateForm(forms.ModelForm):

    account = forms.ModelChoiceField(
        queryset=Account.objects.filter(
            account_status="Active").all(),
    )

    class Meta:
        model = Ledger
        fields = ('ledger_debit', 'ledger_credit',  'account')
        widgets = {
            'ledger_debit': forms.NumberInput(attrs={'step': 0.01},),
            'ledger_credit': forms.NumberInput(attrs={'step': 0.01},),
        }


LedgerCreateFormSet = formset_factory(LedgerCreateForm, extra=2)


class TransactionCreateForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('transaction_comment',
                  'transaction_description', 'transaction_type')


class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)
        widgets = {
            'document': forms.ClearableFileInput(attrs={'multiple': True}),
        }
