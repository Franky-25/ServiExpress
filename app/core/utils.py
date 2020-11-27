from config.wsgi import *
from core.erp.crm.models import *
from core.erp.frm.models import DebtsPay
from core.erp.hrm.models import *
from core.erp.scm.models import *
from core.security.models import *
from django.contrib.contenttypes.models import ContentType


def search_content_type(name):
    for i in ContentType.objects.all():
        if i.name.lower() == name.lower():
            return i
    return None


module = Module()
module.type_id = 8
module.name = 'Rep. Servicios/Tarifas'
module.url = '/reports/service/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de los servicios/tarifas'
module.save()
print('insertado {}'.format(module.name))

# v = Vehicle.objects.first()
# text = '<ul>'
# services = v.sale_set.order_by('-id').values_list('type_serv_id', flat=True).distinct()
# try:
#     for s in Service.objects.filter(id__in=services):
#         km_last = 0.00
#         sales = v.sale_set.filter(type_serv_id=s.id).order_by('-id')
#         if sales:
#             km_last = sales[0].km_current
#         km_now = v.km_current - km_last
#         if km_now > s.duration_km:
#             text += '<li>Ya debes realizar el servicio de {}, ya tienes {} KM de los {} KM</li>'.format(s.name, km_now,
#                                                                                                          s.duration_km)
#     print(text)
# except Exception as e:
#     print(e)
# c = Contracts.objects.all()[0]
# date_joined = datetime.strptime('2020-06-28', '%Y-%m-%d')
# end_date = str((date_joined - timedelta(days=1)).date())
# start_date = str((date_joined - timedelta(days=6)).date())
# print(start_date)
# print(end_date)
# index = c.assistance_set.filter(date_joined__range=[start_date, end_date]).count()
# print(index)

# for c in Contracts.objects.all():
#     for d in range(22, 28):
#         a = Assistance()
#         a.date_joined = datetime.strptime('{}-{}-{}'.format(2020, 6, d), '%Y-%m-%d')
#         a.day = d
#         a.month = 6
#         a.year = 2020
#         a.cont_id = c.id
#         a.save()
#         print('Ingresado:{}'.format(a.id))
