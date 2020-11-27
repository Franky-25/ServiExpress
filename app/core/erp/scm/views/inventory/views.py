import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.scm.forms import Inventory, InventoryForm
from core.security.mixins import AccessModuleMixin


class InventoryListView(AccessModuleMixin, TemplateView):
    template_name = 'inventory/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search':
                data = []
                product = request.POST['product']
                purchase = request.POST['purchase']
                search = Inventory.objects.all()
                if len(purchase):
                    search = search.filter(purch_id=purchase)
                if len(product):
                    search = search.filter(prod_id=product)
                for i in search:
                    item = i.toJSON()
                    item['purch'] = i.purch.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inventario de Compras'
        context['form'] = InventoryForm()
        return context
