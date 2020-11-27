import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.erp.crm.forms import *
from core.security.mixins import AccessModuleMixin


class SaleListView(AccessModuleMixin, ListView):
    model = Sale
    template_name = 'sale/client/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Sale.objects.filter(veh__cli__user_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_det_emps':
                data = []
                sale = Sale.objects.get(pk=request.POST['id'])
                for i in sale.detemployees_set.all():
                    data.append(i.toJSON())
            elif action == 'search_det_equips':
                data = []
                sale = Sale.objects.get(pk=request.POST['id'])
                for i in sale.detresources_set.filter(rec__prod__type__in=[type_prod[1][0]]):
                    data.append(i.toJSON())
            elif action == 'search_det_repuests':
                data = []
                sale = Sale.objects.get(pk=request.POST['id'])
                for i in sale.detresources_set.filter(rec__prod__type__in=[type_prod[0][0]]):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        return context