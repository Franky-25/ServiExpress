import json
import random

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView

from core.erp.frm.models import DebtsPay
from core.erp.scm.forms import *
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class PurchaseListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Purchase
    template_name = 'purchase/list.html'
    permission_required = 'view_purchase'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_repuests':
                data = []
                for inv in Inventory.objects.filter(purch_id=request.POST['id'], prod__type=type_prod[0][0]):
                    data.append(inv.toJSON())
            elif action == 'search_equips':
                data = []
                for inv in Inventory.objects.filter(purch_id=request.POST['id'], prod__type=type_prod[1][0]):
                    data.append(inv.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('purchase_create')
        context['title'] = 'Listado de Compras'
        return context


class PurchaseCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Purchase
    template_name = 'purchase/create.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase_list')
    permission_required = 'add_purchase'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_prov(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Provider.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'rut':
                if Provider.objects.filter(ruc__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def generate_serie(self):
        letters_numbers = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                   's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7']
        return ''.join(random.choices(letters_numbers, k=10)).upper()

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    comp = Purchase()
                    comp.prov_id = items['prov']
                    comp.payment = items['payment']
                    comp.date_joined = items['date_joined']
                    comp.save()

                    for p in items['repuests']:
                        prod = Product.objects.get(pk=p['id'])
                        inv = Inventory()
                        inv.purch_id = comp.id
                        inv.prod_id = prod.id
                        inv.cant = int(p['cant'])
                        inv.saldo = inv.cant
                        inv.price = float(p['cost'])
                        inv.total = inv.cant * float(inv.price)
                        inv.save()

                    for p in items['equips']:
                        prod = Product.objects.get(pk=p['id'])
                        for s in p['series']:
                            inv = Inventory()
                            inv.purch_id = comp.id
                            inv.prod_id = prod.id
                            inv.cant = 1
                            inv.serie = s
                            inv.saldo = inv.cant
                            inv.price = float(p['cost'])
                            inv.guaranty = int(p['guaranty'])
                            inv.total = inv.cant * float(inv.price)
                            inv.save()

                    comp.calculate_invoice()

                    if comp.payment == type_payment[1][0]:
                        cta = DebtsPay()
                        cta.purch_id = comp.id
                        cta.date_joined = items['date_joined']
                        cta.end_date = items['end_date']
                        cta.total = comp.total
                        cta.saldo = comp.total
                        cta.save()
            elif action == 'search_repuests':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                search = Product.objects.filter(type__in=[type_prod[0][0]]).exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    stock = p.get_stock()
                    item['stock'] = stock
                    item['value'] = '{} / {}'.format(p.name, stock)
                    data.append(item)
            elif action == 'search_prov':
                data = []
                for p in Provider.objects.filter(name__icontains=request.POST['term']).order_by('name')[0:10]:
                    item = p.toJSON()
                    item['value'] = p.name
                    data.append(item)
            elif action == 'search_equips':
                data = []
                # ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                search = Product.objects.filter(type__in=[type_prod[1][0]]).exclude().order_by('name')  # id__in=ids
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    stock = p.get_stock()
                    item['stock'] = stock
                    item['value'] = '{} / {}'.format(p.name, stock)
                    data.append(item)
            elif action == 'validate_serie':
                data = {'valid': True}
                code = request.POST['pk']
                series = json.loads(request.POST['series'])
                if code in series:
                    data = {'valid': False}
                else:
                    data['valid'] = not Inventory.objects.filter(serie=code).exclude(serie__in=series).exists()
                return JsonResponse(data)
            elif action == 'validate_prov':
                return self.validate_prov()
            elif action == 'create_prov':
                c = Provider()
                c.name = request.POST['name']
                c.mobile = request.POST['mobile']
                c.address = request.POST['address']
                c.email = request.POST['email']
                c.rut = request.POST['rut']
                c.save()
            elif action == 'generate_serie':
                serie = self.generate_serie()
                while Inventory.objects.filter(serie=serie, state=True).exists():
                    serie = self.generate_serie()
                data['serie'] = serie
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['frmProv'] = ProviderForm()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Compra'
        context['action'] = 'add'
        return context


class PurchaseDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Purchase
    template_name = 'purchase/delete.html'
    success_url = reverse_lazy('purchase_list')
    permission_required = 'delete_purchase'

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
