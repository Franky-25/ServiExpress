import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.frm.models import DebtsPay
from core.reports.forms import ReportForm
from core.security.mixins import AccessModuleMixin


class DebtsPayReportView(AccessModuleMixin, TemplateView):
    template_name = 'debts_pay_report/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def search_report(self):
        data = []
        try:
            start_date = self.request.POST.get('start_date', '')
            end_date = self.request.POST.get('end_date', '')
            search = DebtsPay.objects.filter()
            if len(start_date) and len(end_date):
                search = search.filter(date_joined__range=[start_date, end_date])
            for i in search:
                data.append(i.toJSON())
        except:
            pass
        return data

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = self.search_report()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReportForm()
        context['title'] = 'Informe de Cuentas por Pagar'
        return context
