import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.erp.crm.models import DetEmployees
from core.erp.hrm.forms import Salary, SalaryForm, Contracts
from core.security.mixins import AccessModuleMixin


class SalaryListView(AccessModuleMixin, ListView):
    model = Salary
    template_name = 'salary/employee/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Salary.objects.filter(cont__emp__user_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_salary':
                data = []
                date_joined = request.POST['date_joined']
                for i in Salary.objects.filter(date_joined=date_joined):
                    item = i.toJSON()
                    data.append(item)
            elif action == 'search_det_assistance':
                data = []
                date_joined = request.POST['date_joined']
                assistances = Contracts.objects.get(pk=request.POST['id']).worked_days(date_joined)
                for a in assistances:
                    data.append(a.toJSON())
            elif action == 'search_det_bonus':
                data = []
                date_joined = datetime.strptime(request.POST['date_joined'], '%Y-%m-%d')
                end_date = str((date_joined - timedelta(days=1)).date())
                start_date = str((date_joined - timedelta(days=6)).date())
                cont = Contracts.objects.get(pk=request.POST['id'])
                for det in DetEmployees.objects.filter(sale__date_joined__range=[start_date, end_date], cont_id=cont.id):
                    item = det.toJSON()
                    item['sale'] = det.sale.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Salarios'
        context['form'] = SalaryForm()
        return context