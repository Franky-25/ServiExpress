import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.erp.crm.forms import Vehicle
from core.security.mixins import AccessModuleMixin


class VehicleListView(AccessModuleMixin, ListView):
    model = Vehicle
    template_name = 'vehicle/client/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_vehs':
                data = []
                for v in Vehicle.objects.filter(cli__user_id=request.user.id):
                    data.append(v.toJSON())
            elif action == 'set_km_current':
                veh = Vehicle.objects.get(pk=request.POST['id'])
                veh.km_current = request.POST['km_current']
                veh.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Vehículos'
        return context
