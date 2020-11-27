import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.erp.hrm.forms import *
from core.security.mixins import AccessModuleMixin


class AssistanceListView(AccessModuleMixin, ListView):
    model = Assistance
    template_name = 'assistance/employee/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'load':
                data = []
                start_date = request.POST.get('start_date', datetime.now().date().strftime('%Y-%m-%d'))
                end_date = request.POST.get('end_date', datetime.now().date().strftime('%Y-%m-%d'))
                if len(start_date) and len(end_date):
                    for a in Assistance.objects.filter(date_joined__range=[start_date, end_date], cont__emp__user_id=self.request.user.id):
                        data.append(a.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Asistencias'
        context['form'] = AssistanceForm()
        return context