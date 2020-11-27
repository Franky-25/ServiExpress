import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.frm.forms import ExpensesForm, Expenses
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class ExpensesListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Expenses
    template_name = 'expenses/list.html'
    permission_required = 'view_expenses'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('expenses_create')
        context['title'] = 'Listado de Gastos'
        return context


class ExpensesCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Expenses
    template_name = 'expenses/create.html'
    form_class = ExpensesForm
    success_url = reverse_lazy('expenses_list')
    permission_required = 'add_expenses'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Gasto'
        context['action'] = 'add'
        return context


class ExpensesUpdateView(AccessModuleMixin, PermissionModuleMixin, UpdateView):
    model = Expenses
    template_name = 'expenses/create.html'
    form_class = ExpensesForm
    success_url = reverse_lazy('expenses_list')
    permission_required = 'change_expenses'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Gasto'
        context['action'] = 'edit'
        return context


class ExpensesDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Expenses
    template_name = 'expenses/delete.html'
    success_url = reverse_lazy('expenses_list')
    permission_required = 'delete_expenses'

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
