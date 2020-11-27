from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.erp.crm.models import DetEmployees
from core.security.mixins import AccessModuleMixin


class SaleListView(AccessModuleMixin, ListView):
    model = DetEmployees
    template_name = 'sale/employee/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return DetEmployees.objects.filter(cont__emp__user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Trabajos/Bonificaciones'
        return context