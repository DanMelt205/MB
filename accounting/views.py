
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView, UpdateView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounting.filter_mixin import ListFilteredMixin

from .forms import AccountCreationForm, AccountUpdateForm
from .models import Account
from register.models import User
from .filters import AccountFilter, EventFilter


class AccountView(ListFilteredMixin, ListView):

    model = Account
    paginate_by = 25
    template_name = "accounting/accounthome.html"
    filter_set = AccountFilter


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

        return super().form_valid(form)


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


class AccountLedger(DetailView):

    model = Account
    template_name = 'accounting/accountledger.html'


class EventLog(ListFilteredMixin, ListView):

    model = Account.history.model
    paginate_by = 4
    template_name = 'accounting/eventlog.html'
    filter_set = EventFilter


def index(request):
    return render(request, 'accounting/base.html')


def faqs(request):
    return render(request, 'accounting/faqs.html')


def eventlog(request):
    return render(request, 'accounting/eventlog.html')
