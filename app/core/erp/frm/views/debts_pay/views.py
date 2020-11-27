import json

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView

from core.erp.frm.forms import DebtsPay, DetDebtsPay, DetDebtsPayForm
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class DebtsPayListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = DebtsPay
    template_name = 'debts_pay/list.html'
    permission_required = 'view_debtspay'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def check_pays(self, id):
        try:
            cta = DebtsPay.objects.get(pk=id)
            pays = DetDebtsPay.objects.filter(cta_id=cta.id).aggregate(resp=Coalesce(Sum('valor'), 0.00)).get('resp')
            cta.saldo = float(cta.total) - float(pays)
            cta.state = False if cta.saldo <= 0.00 else True
            cta.save()
        except:
            pass

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'load':
                data = []
                for i in DebtsPay.objects.filter():
                    data.append(i.toJSON())
            elif action == 'search_pays':
                data = []
                ctas = DebtsPay.objects.get(pk=request.POST['id'])
                for i in ctas.detdebtspay_set.all():
                    data.append(i.toJSON())
            elif action == 'payment':
                det = DetDebtsPay()
                det.cta_id = request.POST['id']
                det.date_joined = request.POST['date_joined']
                det.valor = float(request.POST['valor'])
                det.save()
                self.check_pays(id=det.cta_id)
            elif action == 'delete_pay':
                id = request.POST['id']
                det = DetDebtsPay.objects.get(pk=id)
                cta = det.cta
                det.delete()
                self.check_pays(id=cta.id)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cuentas por Pagar'
        context['form'] = DetDebtsPayForm()
        return context


class DebtsPayDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = DebtsPay
    template_name = 'debts_pay/delete.html'
    success_url = reverse_lazy('debts_pay_list')
    permission_required = 'delete_debtspay'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
