from django.shortcuts import render


def index(request):
    return render(request, 'accounting/base.html')


def eventlog(request):
    return render(request, 'accounting/eventlog.html')
