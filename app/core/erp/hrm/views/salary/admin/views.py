import json
from datetime import datetime, timedelta

from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView

from core.erp.crm.models import DetEmployees
from core.erp.hrm.forms import Salary, SalaryForm, Contracts
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class SalaryListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Salary
    template_name = 'salary/admin/list.html'
    permission_required = 'view_salary'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['create_url'] = reverse_lazy('salary_create')
        context['title'] = 'Listado de Salarios'
        context['form'] = SalaryForm()
        return context


class SalaryCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Salary
    template_name = 'salary/admin/create.html'
    form_class = SalaryForm
    success_url = reverse_lazy('salary_list')
    permission_required = 'add_salary'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            date_joined = self.request.POST['date_joined']
            if Salary.objects.filter(date_joined=date_joined).exists():
                data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    date_now = datetime.strptime(request.POST['date_joined'], '%Y-%m-%d')
                    date_joined = request.POST['date_joined']
                    for cont in Contracts.objects.filter(state=True):
                        dsctos = cont.get_dsctos(date_joined)
                        bonus = cont.get_bonus(date_joined)
                        total = float(cont.rmu) - float(dsctos) + float(bonus)

                        rolpay = Salary()
                        rolpay.cont_id = cont.id
                        rolpay.date_joined = date_joined
                        rolpay.days_work = cont.worked_days(date_joined).count()
                        rolpay.week = date_now.isocalendar()[1]
                        rolpay.dsctos = dsctos
                        rolpay.bonus = bonus
                        rolpay.total = total
                        rolpay.save()
            elif action == 'generate_salary':
                data = []
                date_now = datetime.strptime(request.POST['date_joined'], '%Y-%m-%d')
                date_joined = request.POST['date_joined']
                for cont in Contracts.objects.filter(state=True):
                    item = cont.toJSON()
                    dsctos = cont.get_dsctos(date_joined)
                    bonus = cont.get_bonus(date_joined)
                    total = float(cont.rmu) - float(dsctos) + float(bonus)
                    item['days_work'] = cont.worked_days(date_joined).count()
                    item['dsctos'] = format(dsctos, '.0f')
                    item['bonus'] = format(bonus, '.0f')
                    item['total'] = format(total, '.0f')
                    item['week'] = date_now.isocalendar()[1]
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
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Salario'
        context['action'] = 'add'
        return context


class SalaryDeleteView(DeleteView):
    model = Salary
    template_name = 'salary/admin/delete.html'
    success_url = reverse_lazy('salary_list')
    permission_required = 'delete_salary'

    def get_object(self, queryset=None):
        return None

    def get(self, request, *args, **kwargs):
        if 'datejoined' in self.kwargs:
            if Salary.objects.filter(date_joined=self.kwargs['datejoined']):
                return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            Salary.objects.filter(date_joined=self.kwargs['datejoined']).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        date_joined = self.kwargs['datejoined']
        date_now = datetime.strptime(date_joined, '%Y-%m-%d')
        context['datejoined'] = date_joined
        context['week'] = date_now.isocalendar()[1]
        return context
