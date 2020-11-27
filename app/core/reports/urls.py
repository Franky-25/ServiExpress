from django.urls import path

from .views.assistance_report.views import AssistanceReportView
from .views.client_report.views import ClientReportView
from .views.contracts_report.views import ContractsReportView
from .views.debts_pay_report.views import DebtsPayReportView
from .views.expenses_report.views import ExpensesReportView
from .views.provider_report.views import ProviderReportView
from .views.purchase_report.views import PurchaseReportView
from .views.salary_report.views import SalaryReportView
from .views.sale_report.views import SaleReportView
from .views.service_report.views import ServiceReportView

urlpatterns = [
    path('client/', ClientReportView.as_view(), name='client_report'),
    path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    path('provider/', ProviderReportView.as_view(), name='provider_report'),
    path('salary/', SalaryReportView.as_view(), name='salary_report'),
    path('expenses/', ExpensesReportView.as_view(), name='expenses_report'),
    path('debts/pay/', DebtsPayReportView.as_view(), name='debts_pay_report'),
    path('contracts/', ContractsReportView.as_view(), name='contracts_report'),
    path('assistance/', AssistanceReportView.as_view(), name='assistance_report'),
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('service/', ServiceReportView.as_view(), name='service_report'),
]
