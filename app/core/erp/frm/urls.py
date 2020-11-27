from django.urls import path
from core.erp.frm.views.type_expense.views import *
from core.erp.frm.views.expenses.views import *
from core.erp.frm.views.debts_pay.views import *

urlpatterns = [
    # type_expense
    path('type/expense/', TypeExpenseListView.as_view(), name='type_expense_list'),
    path('type/expense/add/', TypeExpenseCreateView.as_view(), name='type_expense_create'),
    path('type/expense/update/<int:pk>/', TypeExpenseUpdateView.as_view(), name='type_expense_update'),
    path('type/expense/delete/<int:pk>/', TypeExpenseDeleteView.as_view(), name='type_expense_delete'),
    # expenses
    path('expenses/', ExpensesListView.as_view(), name='expenses_list'),
    path('expenses/add/', ExpensesCreateView.as_view(), name='expenses_create'),
    path('expenses/update/<int:pk>/', ExpensesUpdateView.as_view(), name='expenses_update'),
    path('expenses/delete/<int:pk>/', ExpensesDeleteView.as_view(), name='expenses_delete'),
    # debts_pay
    path('debts/pay/', DebtsPayListView.as_view(), name='debts_pay_list'),
    path('debts/pay/delete/<int:pk>/', DebtsPayDeleteView.as_view(), name='debts_pay_delete'),
]
