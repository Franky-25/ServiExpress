import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.crm.forms import ClientCreateForm, Client, ClientChangeForm, User
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class ClientListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Client
    template_name = 'client/list.html'
    permission_required = 'view_client'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('client_create')
        context['title'] = 'Listado de Clientes'
        return context


class ClientCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Client
    template_name = 'client/create.html'
    form_class = ClientCreateForm
    success_url = reverse_lazy('client_list')
    permission_required = 'add_client'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'run':
                if User.objects.filter(run=obj):
                    data['valid'] = False
            elif type == 'username':
                if User.objects.filter(username=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                form = ClientCreateForm(request.POST, request.FILES)
                data = form.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Cliente'
        context['action'] = 'add'
        return context


class ClientUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Client
    template_name = 'client/create.html'
    form_class = ClientChangeForm
    success_url = reverse_lazy('client_list')
    permission_required = 'change_client'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = ClientChangeForm(instance=self.object.user, initial={
            'mobile': self.object.mobile,
            'birthdate': self.object.birthdate,
            'address': self.object.address,
        })
        return form

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().user.id
            if type == 'run':
                if User.objects.filter(run=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'username':
                if User.objects.filter(username=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                form = ClientChangeForm(request.POST, request.FILES, instance=self.get_object())
                data = form.save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Cliente'
        context['action'] = 'edit'
        return context


class ClientDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'delete_client'

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
