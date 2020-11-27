from django.urls import path
from core.erp.hrm.views.job.views import *
from core.erp.hrm.views.employee.views import *
from core.erp.hrm.views.contracts.views import *
import core.erp.hrm.views.assistance.admin.views as assistance_admin
import core.erp.hrm.views.assistance.employee.views as assistance_employee
import core.erp.hrm.views.salary.admin.views as salary_admin
import core.erp.hrm.views.salary.employee.views as salary_employee

urlpatterns = [
    # job
    path('job/', JobListView.as_view(), name='job_list'),
    path('job/add/', JobCreateView.as_view(), name='job_create'),
    path('job/update/<int:pk>/', JobUpdateView.as_view(), name='job_update'),
    path('job/delete/<int:pk>/', JobDeleteView.as_view(), name='job_delete'),
    # employee
    path('employee/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/update/<int:pk>/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    # contracts
    path('contracts/', ContractsListView.as_view(), name='contracts_list'),
    path('contracts/add/', ContractsCreateView.as_view(), name='contracts_create'),
    path('contracts/update/<int:pk>/', ContractsUpdateView.as_view(), name='contracts_update'),
    path('contracts/delete/<int:pk>/', ContractsDeleteView.as_view(), name='contracts_delete'),
    # assistance admin
    path('assistance/', assistance_admin.AssistanceListView.as_view(), name='assistance_list'),
    path('assistance/add/', assistance_admin.AssistanceCreateView.as_view(), name='assistance_create'),
    path('assistance/delete/<str:start_date>/<str:end_date>/', assistance_admin.AssistanceDeleteView.as_view(), name='assistance_delete'),
    # assistance
    path('assistance/employee/', assistance_employee.AssistanceListView.as_view(), name='assistance_list_employee'),
    # salary admin
    path('salary/', salary_admin.SalaryListView.as_view(), name='salary_list'),
    path('salary/add/', salary_admin.SalaryCreateView.as_view(), name='salary_create'),
    path('salary/delete/<str:datejoined>/', salary_admin.SalaryDeleteView.as_view(), name='salary_delete'),
    # salary employee
    path('salary/employee/', salary_employee.SalaryListView.as_view(), name='salary_list_employee'),
]
