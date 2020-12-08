from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.index, name="home"),
    path('', views.landingpage, name="notlogged"),
    path('faqs', views.faqs, name="faqs"),

    path('account', views.AccountView.as_view(), name="accounthome"),

    path('account/create', views.AccountCreate.as_view(),
         name="accountcreate"),

    path('account/<int:pk>/update', views.AccountUpdate.as_view(),
         name="accountupdate"),

    path('account/<int:pk>/deactive', views.AccountDeactive.as_view(),
         name="accountdeactive"),

    path('journal',
         views.Journal.as_view(), name="journal"),

    path('journal/<int:pk>/reject',
         views.JournalReject.as_view(), name="journalreject"),

    path('journal/<int:pk>/approve',
         views.JournalApprove.as_view(), name="journalapprove"),

    path('journal/journalentry', views.JournalCreate, name="journalentry"),

    path('journal/<int:pk>/details',
         views.JournalDetailView.as_view(), name="journaldetail"),

    path('account/<int:pk>/ledger',
         views.LedgerView.as_view(), name="accountledger"),

    path('eventlog',
         views.EventLog.as_view(), name="eventlog"),

    path('trailbalance',
         views.TrailBalance.as_view(), name="trailbalance"),

    path('balancesheet',
         views.BalanceSheet.as_view(), name="balancesheet"),

    path('incomesheet',
         views.IncomeSheet.as_view(), name="incomesheet"),

    path('retainedearnings',
         views.RetainedStatement.as_view(), name="retainedearnings"),

    #     path('',
    #          views.DashBoardView.as_view(), name="home"),

    # path('account/<int:id>/deactive', views.deactive, name="accountdeactive")
]
