
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView,\
    UpdateView, ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounting.filter_mixin import ListFilteredMixin


from .forms import AccountCreationForm, AccountUpdateForm, LedgerCreateFormSet,\
    TransactionCreateForm, DocumentCreateForm
from .models import Account, Ledger, Transaction, Document
from register.models import User
from .filters import AccountFilter, EventFilter, TransactionFilter,\
    LedgerFilter, AccountSheetFilter, IncomeFilter
from register.forms import SendEmailForm


class AccountView(ListFilteredMixin, ListView, FormView):

    model = Account
    paginate_by = 10
    template_name = "accounting/accounthome.html"
    filter_set = AccountFilter

    form_class = SendEmailForm
    success_url = reverse_lazy('accounthome')

    def form_valid(self, form):

        request = self.request
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        try:
            send_mail(
                subject,
                message,
                'donotreplymbalancer@gmail.com',
                [to_email],
                fail_silently=False,
            )
        except BadHeaderError:
            messages.error(request, "Email was not sent.")
            return super().form_invalid(form)

        messages.success(request, "Email was successfully sent.")
        return super().form_valid(form)


class AccountUpdate(UpdateView):
    model = Account
    fields = ['account_name', 'account_description',
              'account_comment', 'account_status']
    success_url = reverse_lazy('accounthome')
    template_name = "accounting/accountupdate.html"

    def form_valid(self, form):
        request = self.request
        account = Account.objects.get(id=self.kwargs['pk'])
        print(account)
        status = form.cleaned_data.get("account_status")
        if status == "Deactive":
            if int(account.account_balance) <= 0:
                messages.success(
                    request, "Account successfully deactived!")
            else:
                messages.error(
                    request, "Account amount greater than 0, can not be deactived!")
                return super().form_invalid(form)

        messages.success(
            request, "Account successfully updated!")
        return super().form_valid(form)


class AccountDeactive(View):

    def get(self, *args, **kwargs):
        account = Account.objects.get(id=self.kwargs['pk'])
        account.account_status = "Deactive"
        account.save()
        messages.success(
            self.request, "Account was deactived successfully.")
        return redirect('accounthome')


class AccountCreate(SuccessMessageMixin, CreateView):
    form_class = AccountCreationForm
    model = Account
    success_url = reverse_lazy('accounthome')
    template_name = 'accounting/accountcreate.html'
    success_message = 'Account was created successfully'
    error_message = 'Error creating account, Account name and number exist.'

    def form_valid(self, form):
        form.instance.account_user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class Journal(ListFilteredMixin, ListView):

    model = Transaction
    paginate_by = 10
    template_name = 'accounting/journalview.html'
    filter_set = TransactionFilter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionCreateForm
        context['ledger'] = Ledger.objects.all()
        return context


class JournalApprove(View):

    def get(self, *args, **kwargs):
        transaction = Transaction.objects.get(id=self.kwargs['pk'])
        transaction.transaction_status = "Approved"
        ledger = Ledger.objects.filter(transaction=self.kwargs['pk'])
        for l in ledger:
            account = Account.objects.get(id=l.account.id)
            account.account_debit = account.account_debit + l.ledger_debit
            account.account_credit = account.account_credit + l.ledger_credit
            if l.ledger_debit != 0:
                account.account_balance = account.account_balance + l.ledger_debit
            else:
                account.account_balance = account.account_balance - l.ledger_credit
            account.save()
        transaction.save()
        messages.success(
            self.request, "Journal entry was approved successfully.")
        return redirect('journal')


class JournalReject(View):

    def post(self, *args, **kwargs):
        if(self.request.method == 'POST'):
            comment = self.request.POST.get('transaction_comment')
            transaction = Transaction.objects.get(id=self.kwargs['pk'])
            transaction.transaction_comment = comment
            transaction.transaction_status = "Rejected"
            transaction.save()
            messages.success(
                self.request, "Journal entry was rejected successfully.")
            return redirect('journal')
        else:
            messages.error(
                self.request, "Journal entry was not rejected successfully.")


class JournalDetailView(DetailView):

    model = Transaction
    template_name = 'accounting/accountledgerdetail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['document'] = Document.objects.filter(
            transaction=self.kwargs['pk'])
        context['ledger'] = Ledger.objects.filter(
            transaction=self.kwargs['pk'])
        return context

# Turn into a class


def JournalCreate(request):
    template_name = 'accounting/journalentry.html'
    if request.method == 'GET':
        transactionform = TransactionCreateForm(request.GET or None)
        documentform = DocumentCreateForm(request.GET or None)
        formset = LedgerCreateFormSet(request.GET or None)
    elif request.method == 'POST':
        transactionform = TransactionCreateForm(request.POST)
        documentform = DocumentCreateForm(request.FILES)
        formset = LedgerCreateFormSet(request.POST)
        if transactionform.is_valid() and formset.is_valid():
            x = 0
            # first save this transaction, as its reference will be used in `Ledger`
            transaction = transactionform.save()

            if documentform.is_valid():
                doc = documentform.save(commit=False)
                for f in request.FILES.getlist('document'):
                    print("hit")
                    doc = Document.objects.create(
                        document=f, transaction=transaction)
                    doc.save()

            for form in formset:
                account_id = request.POST.get(("form-{}-account").format(x))
                account = Account.objects.get(id=account_id)
                # so that `transaction` instance can be attached.
                ledger = form.save(commit=False)
                ledger.transaction = transaction
                ledger.user = request.user
                ledger.save()
                x = x + 1
            return redirect('journal')
    return render(request, template_name, {
        'transactionform': transactionform,
        'documentform': documentform,
        'formset': formset,
    })


class LedgerView(DetailView):

    model = Account
    template_name = 'accounting/accountledger.html'
    # filter_set = AccountSheetFilter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        ledger_list = Ledger.objects.filter(account=self.kwargs['pk']).select_related(
            'transaction').order_by('transaction__transaction_date')
        f = LedgerFilter(
            self.request.GET, queryset=ledger_list)
        print(f)
        context['filter'] = f
        return context


class EventLog(ListFilteredMixin, ListView):

    model = Account.history.model
    paginate_by = 4
    template_name = 'accounting/eventlog.html'
    filter_set = EventFilter


class TrailBalance(ListFilteredMixin, ListView, FormView):
    model = Ledger
    template_name = 'accounting/trailbalance.html'
    queryset = Ledger.objects.all().select_related(
        'account').select_related('transaction').order_by('account__account_creation_date')
    filter_set = AccountSheetFilter
    form_class = SendEmailForm
    success_url = reverse_lazy('trailbalance')

    def form_valid(self, form):

        request = self.request
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        attachment = request.FILES.getlist('attachment')

        print(attachment)

        try:
            email = EmailMessage(
                subject,
                message,
                'donotreplymbalancer@gmail.com',
                [to_email],
            )

            for a in attachment:
                email.attach(a.name, a.read(), a.content_type)

            res = email.send()
        except BadHeaderError:
            messages.error(request, "Email was not sent.")
            return super().form_invalid(form)

        messages.success(request, "Email was successfully sent.")
        return super().form_valid(form)


class IncomeSheet(ListFilteredMixin, ListView, FormView):
    model = Account
    context_object_name = 'account'
    template_name = 'accounting/incomesheet.html'
    filter_set = IncomeFilter
    form_class = SendEmailForm
    success_url = reverse_lazy('incomesheet')

    def form_valid(self, form):

        request = self.request
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        attachment = request.FILES.getlist('attachment')

        print(attachment)

        try:
            email = EmailMessage(
                subject,
                message,
                'donotreplymbalancer@gmail.com',
                [to_email],
            )

            for a in attachment:
                email.attach(a.name, a.read(), a.content_type)

            res = email.send()
        except BadHeaderError:
            messages.error(request, "Email was not sent.")
            return super().form_invalid(form)

        messages.success(request, "Email was successfully sent.")
        return super().form_valid(form)


class BalanceSheet(ListFilteredMixin, ListView, FormView):
    model = Account
    context_object_name = 'account'
    template_name = 'accounting/balancesheet.html'
    filter_set = IncomeFilter
    form_class = SendEmailForm
    success_url = reverse_lazy('balancesheet')

    def form_valid(self, form):

        request = self.request
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        attachment = request.FILES.getlist('attachment')

        print(attachment)

        try:
            email = EmailMessage(
                subject,
                message,
                'donotreplymbalancer@gmail.com',
                [to_email],
            )

            for a in attachment:
                email.attach(a.name, a.read(), a.content_type)

            res = email.send()
        except BadHeaderError:
            messages.error(request, "Email was not sent.")
            return super().form_invalid(form)

        messages.success(request, "Email was successfully sent.")
        return super().form_valid(form)


class RetainedStatement(ListFilteredMixin, ListView, FormView):
    model = Account
    context_object_name = 'account'
    template_name = 'accounting/retainedearnings.html'
    filter_set = IncomeFilter
    form_class = SendEmailForm
    success_url = reverse_lazy('retainedearnings')

    def form_valid(self, form):

        request = self.request
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        attachment = request.FILES.getlist('attachment')

        print(attachment)

        try:
            email = EmailMessage(
                subject,
                message,
                'donotreplymbalancer@gmail.com',
                [to_email],
            )

            for a in attachment:
                email.attach(a.name, a.read(), a.content_type)

            res = email.send()
        except BadHeaderError:
            messages.error(request, "Email was not sent.")
            return super().form_invalid(form)

        messages.success(request, "Email was successfully sent.")
        return super().form_valid(form)


def index(request):
    account = Account.objects.all()
    context = {
        'account': account
    }
    return render(request, 'accounting/dashboard.html', context)


def landingpage(request):
    return render(request, 'accounting/moneybalancer.html')


def faqs(request):
    return render(request, 'accounting/faqs.html')
