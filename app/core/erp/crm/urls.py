from django.urls import path
from .views.brand.views import *
from .views.client.views import *
from .views.exemplar.views import *
import core.erp.crm.views.vehicle.admin.views as vehicle_admin
import core.erp.crm.views.vehicle.client.views as vehicle_client
from .views.service.views import *
import core.erp.crm.views.sale.admin.views as sale_admin
import core.erp.crm.views.sale.employee.views as sale_employee
import core.erp.crm.views.sale.client.views as sale_client

urlpatterns = [
    # brand
    path('brand/', BrandListView.as_view(), name='brand_list'),
    path('brand/add/', BrandCreateView.as_view(), name='brand_create'),
    path('brand/update/<int:pk>/', BrandUpdateView.as_view(), name='brand_update'),
    path('brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete'),
    # exemplar
    path('exemplar/', ExemplarListView.as_view(), name='exemplar_list'),
    path('exemplar/add/', ExemplarCreateView.as_view(), name='exemplar_create'),
    path('exemplar/update/<int:pk>/', ExemplarUpdateView.as_view(), name='exemplar_update'),
    path('exemplar/delete/<int:pk>/', ExemplarDeleteView.as_view(), name='exemplar_delete'),
    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # vehicle admin
    path('vehicle/', vehicle_admin.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicle/add/', vehicle_admin.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicle/update/<int:pk>/', vehicle_admin.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicle/delete/<int:pk>/', vehicle_admin.VehicleDeleteView.as_view(), name='vehicle_delete'),
    # vehicle client
    path('vehicle/client/', vehicle_client.VehicleListView.as_view(), name='vehicle_list_client'),
    # service
    path('service/', ServiceListView.as_view(), name='service_list'),
    path('service/add/', ServiceCreateView.as_view(), name='service_create'),
    path('service/update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'),
    # sale employee
    path('sale/', sale_admin.SaleListView.as_view(), name='sale_list'),
    path('sale/add/', sale_admin.SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', sale_admin.SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/print/invoice/<int:pk>/', sale_admin.PrintInvoice.as_view(), name='sale_print'),
    # sale employee
    path('sale/employee/', sale_employee.SaleListView.as_view(), name='sale_list_employee'),
    # sale client
    path('sale/client/', sale_client.SaleListView.as_view(), name='sale_list_client'),
]
