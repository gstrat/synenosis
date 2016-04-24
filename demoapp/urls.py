from django.conf.urls import patterns, url
from .views.accounts import AddWinbankAccount, AddNBGAccount, AddPayPalAccount
from .views.monitor import ProgressMonitorView
from .views.index import Dashboard
from demoapp.views.monitor import ImportWinbankQueue, ImportNBGQueue, \
        ImportPayPalQueue


urlpatterns = patterns('',
    url(r'^$', Dashboard.as_view(), name='dashboard'),
    url(r'^accounts/add/winbank/$', AddWinbankAccount.as_view(),
        name='accounts-add-winbank'),
    url(r'^accounts/add/nbg/$', AddNBGAccount.as_view(),
        name='accounts-add-nbg'),
    url(r'^accounts/add/paypal/$', AddPayPalAccount.as_view(),
        name='accounts-add-paypal'),
    url(r'^task-progress/$', ProgressMonitorView.as_view(),
        name='monitor-progress-view'),
    url(r'^import-winbank/$', ImportWinbankQueue.as_view(),
        name = 'import-winbank-queue'),
    url(r'^import-nbg/$', ImportNBGQueue.as_view(),
        name = 'import-nbg-queue'),
    url(r'^import-paypal/$', ImportPayPalQueue.as_view(),
        name = 'import-paypal-queue')
)
