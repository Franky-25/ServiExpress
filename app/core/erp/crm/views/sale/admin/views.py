import json
import os
from io import BytesIO

from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DeleteView, View
from xhtml2pdf import pisa

from config.settings import MEDIA_URL, MEDIA_ROOT
from core.erp.crm.forms import *
from core.erp.scm.models import Product, Inventory
from core.security.mixins import AccessModuleMixin, PermissionModuleMixin


class SaleListView(AccessModuleMixin, PermissionModuleMixin, ListView):
    model = Sale
    template_name = 'sale/admin/list.html'
    permission_required = 'view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
        try:
            if action == 'search_det_emps':
                data = []
                sale = Sale.objects.get(pk=request.POST['id'])
                for i in sale.detemployees_set.all():
                    data.append(i.toJSON())
            elif action == 'search_det_equips':
                data = []
                sale = Sale.objects.get(pk=request.POST['id'])
                for i in sale.detresources_set.filter(rec__prod__type__in=[type_prod[1][0]]):
                    data.append(i.toJSON())
            elif action == 'search_det_repuests':
                data = []
                sale = Sale.objects.get(pk=request.POST['id'])
                for i in sale.detresources_set.filter(rec__prod__type__in=[type_prod[0][0]]):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('sale_create')
        context['title'] = 'Listado de Ventas'
        return context


class SaleCreateView(AccessModuleMixin, PermissionModuleMixin, CreateView):
    model = Sale
    template_name = 'sale/admin/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_list')
    permission_required = 'add_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_client(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'run':
                if Client.objects.filter(dni__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def get_typeserv(self):
        data = [{'id': '', 'text': '-----------------'}]
        for s in Service.objects.all():
            data.append({
                'id': s.id, 'text': s.__str__(), 'data': s.toJSON()
            })
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    vent = Sale()
                    vent.veh_id = items['veh']
                    vent.type_serv_id = items['type_serv']
                    vent.km_current = items['km_current']
                    vent.km_service = vent.type_serv.duration_km
                    vent.start_date = items['start_date']
                    vent.end_date = items['end_date']
                    vent.save()

                    veh = vent.veh
                    veh.km_current = vent.km_current
                    veh.save()

                    for r in items['repuests']:
                        cant = int(r['cant'])
                        for inv in Inventory.objects.filter(prod_id=r['id'], saldo__gt=0).order_by(
                                'purch__date_joined'):
                            if inv.saldo > cant:
                                det = DetResources()
                                det.sale_id = vent.id
                                det.rec_id = inv.id
                                det.cant = cant
                                det.price = float(r['cost'])
                                det.total = det.cant * float(det.price)
                                det.save()
                                inv.saldo = inv.saldo - cant
                                inv.save()
                                cant = 0
                            else:
                                det = DetResources()
                                det.sale_id = vent.id
                                det.inv_id = inv.id
                                det.cant = inv.saldo
                                det.price = float(r['cost'])
                                det.total = det.cant * float(det.price)
                                det.save()
                                cant = cant - inv.saldo
                                inv.saldo = 0
                                inv.save()
                            if cant == 0:
                                break

                    for r in items['equips']:
                        det = DetResources()
                        det.sale_id = vent.id
                        det.rec_id = r['id']
                        det.cant = int(r['cant'])
                        det.price = float(r['depreciation'])
                        det.total = det.cant * float(det.price)
                        det.save()

                    for emp in items['emps']:
                        det = DetEmployees()
                        det.sale_id = vent.id
                        det.cont_id = emp['id']
                        det.bonus = float(emp['cost'])
                        det.save()

                    vent.calculate_invoice()
                    vent.save()

            elif action == 'search_repuests':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                search = Product.objects.filter(type=type_prod[0][0]).exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[:10]
                for p in search:
                    stock = p.get_stock()
                    item = p.toJSON()
                    item['stock'] = stock
                    item['value'] = '{} / {}'.format(p.name, stock)
                    data.append(item)
            elif action == 'search_equips':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                search = Inventory.objects.filter(prod__type=type_prod[1][0]).exclude(id__in=ids).order_by('prod__name')
                if len(term):
                    search = search.filter(prod__name__icontains=term)
                    search = search[:10]
                for p in search:
                    stock = 1
                    item = p.toJSON()
                    item['stock'] = stock
                    item['value'] = '{} / {}'.format(p.prod.name, p.serie)
                    data.append(item)
            elif action == 'search_emps':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                for p in Contracts.objects.filter(state=True).filter(
                        Q(emp__user__first_name__icontains=term) | Q(emp__user__last_name__icontains=term)).exclude(
                    id__in=ids).order_by('emp__user__first_name')[:10]:
                    item = p.toJSON()
                    item['cost'] = 0.00
                    item['value'] = '{} / {}'.format(p.emp.user.get_full_name(), p.job.name)
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Venta/Servicio'
        context['action'] = 'add'
        context['frmCli'] = ClientCreateForm()
        context['typeserv'] = self.get_typeserv()
        return context


class SaleDeleteView(AccessModuleMixin, PermissionModuleMixin, DeleteView):
    model = Sale
    template_name = 'sale/admin/delete.html'
    success_url = reverse_lazy('sale_list')
    permission_required = 'delete_sale'

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


class PrintInvoice(View):
    success_url = reverse_lazy('sale_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/admin/invoice.html')
            context = {
                'comp': Company.objects.first(),
                'sale': Sale.objects.get(pk=self.kwargs['pk'])
            }
            html = template.render(context)
            result = BytesIO()
            links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8', link_callback=links)
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.success_url)
