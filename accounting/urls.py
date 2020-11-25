from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    # path('', views.eventlog, name="eventlog"),
    path('faqs', views.faqs, name="faqs"),
    path('account', views.AccountView.as_view(), name="accounthome"),
    path('account/create', views.AccountCreate.as_view(),
         name="accountcreate"),
    path('account/<int:pk>/update', views.AccountUpdate.as_view(),
         name="accountupdate"),
    path('account/<int:pk>/ledger',
         views.AccountLedger.as_view(), name="accountledger"),
    path('eventlog',
         views.EventLog.as_view(), name="eventlog")
    # path('account/<int:id>/deactive', views.deactive, name="accountdeactive")
]
