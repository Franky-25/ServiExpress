from django.urls import include, path

urlpatterns = [
    path('frm/', include('core.erp.frm.urls')),
    path('scm/', include('core.erp.scm.urls')),
    path('crm/', include('core.erp.crm.urls')),
    path('hrm/', include('core.erp.hrm.urls')),
]
