import json

from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, TemplateView

from core.erp.hrm.forms import *
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class AssistanceListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Assistance
    template_name = 'assistance/admin/list.html'
    permission_required = 'view_assistance'

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
                    for a in Assistance.objects.filter(date_joined__range=[start_date, end_date]):
                        data.append(a.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('assistance_create')
        context['title'] = 'Listado de Asistencias'
        context['form'] = AssistanceForm()
        return context


class AssistanceCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Assistance
    template_name = 'assistance/admin/create.html'
    form_class = AssistanceForm
    success_url = reverse_lazy('assistance_list')
    permission_required = 'add_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def generate_assistance(self):
        data = []
        try:
            for i in Contracts.objects.filter(state=True):
                item = i.toJSON()
                item['dscto'] = 0.00
                item['state'] = 0
                item['motive_perm'] = ''
                data.append(item)
        except Exception as e:
            print(e)
            pass
        return data

    def validate_data(self):
        data = {'valid': True}
        try:
            obj = self.request.POST['obj'].strip()
            data['valid'] = True
            if Assistance.objects.filter(date_joined=obj):
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
                    items = json.loads(request.POST['items'])
                    date_joined = datetime.strptime(items['date_joined'], '%Y-%m-%d')
                    for i in items['assistances']:
                        a = Assistance()
                        a.cont_id = int(i['id'])
                        a.date_joined = date_joined
                        a.year = date_joined.year
                        a.month = date_joined.month
                        a.day = date_joined.day
                        a.motive_perm = i['motive_perm']
                        a.dscto = float(i['dscto'])
                        a.state = i['state']
                        a.save()
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'generate_assistance':
                data = self.generate_assistance()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Asistencia'
        context['action'] = 'add'
        return context


class AssistanceDeleteView(AccessModuleMixin, PermissionModuleMixin, TemplateView):
    model = Assistance
    template_name = 'assistance/admin/delete.html'
    success_url = reverse_lazy('assistance_list')
    permission_required = 'delete_assistance'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = self.kwargs['start_date']
            end_date = self.kwargs['end_date']
            Assistance.objects.filter(date_joined__range=[start_date, end_date]).delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        context['dates'] = self.kwargs
        return context
