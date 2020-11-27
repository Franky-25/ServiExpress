from config.wsgi import *
from core.erp.crm.models import *
from core.erp.frm.models import *
from core.erp.hrm.models import *
from core.erp.scm.models import *
from core.security.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from core.user.models import User


def search_content_type(name):
    for i in ContentType.objects.all():
        if i.name.lower() == name.lower():
            return i
    return None


# company
comp = Company()
comp.name = 'ServiExpress'
comp.system_name = 'ServiExpress'
comp.icon = 'fas fa-laptop-code'
comp.rut = '1234567893654'
comp.mobile = '1234567890'
comp.phone = '123456789'
comp.email = 'xforce@serviexpress.page'
comp.address = 'Calle Nueva 1660, Huechuraba.'
comp.mission = 'Aquí no hay estafas. Solo hay trabajo e ingeniería de calidad para tu vehículo. Aquí en ServiExpress ponemos a tu vehículo de pie por un precio razonable. No vamos a llevar a cabo trabajos importantes sin hablar contigo primero. Es más, nuestro servicio rápido significa que tu vehículo y la carretera estarán unidos de nuevo en poco tiempo. Para saber más, o para reservar una consulta en Santiago o póngase en contacto con nosotros en el formulario'
comp.vision = 'Una cosa que queda cierta con nosotros es que si te atiende un mecánico a rostro fresco o bien un veterano, puedes estar seguro de que cada uno de nuestro equipo está altamente capacitado y comprometido a desarrollar sus habilidades al día. Tomamos nuestro trabajo muy en serio y siempre traemos la pasión y el compromiso de cada proyecto que asumimos.'
comp.about_us = 'Entre nosotros ya llevamos décadas en reparar vehículos. Desde servicios de rutina y los servicios más complejos e incluso a los proyectos de restauración por completo, puedes estar seguro de que recibirás un servicio profesional. Además, nuestros ingenieros cumplen con todas las normas y tienen años de experiencia.'
comp.layout = 1
comp.card = 'card-primary'
comp.navbar = 'navbar-dark navbar-primary'
comp.brand_logo = ''
comp.sidebar = 'sidebar-dark-primary'
comp.save()

# module type
type = ModuleType()
type.name = 'SEGURIDAD'
type.icon = 'fas fa-lock'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'USUARIOS'
type.icon = 'fas fa-users'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'ADMINISTRACIÓN'
type.icon = 'far fa-list-alt'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'SUMINISTRO'
type.icon = 'fas fa-boxes'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'COMERCIO'
type.icon = 'fas fa-calculator'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'FINANZAS'
type.icon = 'fas fa-hand-holding-usd'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'R.R.H.H.'
type.icon = 'fas fa-toolbox'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'REPORTES'
type.icon = 'fas fa-chart-pie'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'EMPLEADOS'
type.icon = 'fas fa-user-clock'
type.save()
print('insertado {}'.format(type.name))

type = ModuleType()
type.name = 'CLIENTES'
type.icon = 'fas fa-id-badge'
type.save()
print('insertado {}'.format(type.name))

# module
module = Module()
module.type_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.content_type = search_content_type(ModuleType._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.content_type = search_content_type(Module._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.content_type = search_content_type(Group._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 2
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.content_type = search_content_type(AccessUsers._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.content_type = search_content_type(DatabaseBackups._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 3
module.name = 'Compañia'
module.url = '/security/company/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-building'
module.description = 'Permite actualizar la información de la compañia'
module.content_type = search_content_type(Company._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 3
module.name = 'Conf. de la plantilla'
module.url = '/security/company/setting/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 2
module.name = 'Administradores'
module.url = '/user/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los administradores del sistema'
module.content_type = search_content_type(User._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Cambiar password'
module.url = '/user/change/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.name = 'Editar perfil'
module.url = '/user/change/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print('insertado {}'.format(module.name))

# FRM (6)
module = Module()
module.type_id = 6
module.name = 'Tipos de Gastos'
module.url = '/erp/frm/type/expense/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-comments-dollar'
module.description = 'Permite administrar los tipos de gastos'
module.content_type = search_content_type(TypeExpense._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 6
module.name = 'Gastos'
module.url = '/erp/frm/expenses/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-invoice-dollar'
module.description = 'Permite administrar los gastos de la compañia'
module.content_type = search_content_type(Expenses._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 6
module.name = 'Cuentas por pagar'
module.url = '/erp/frm/debts/pay/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-money-check-alt'
module.description = 'Permite administrar las cuentas por pagar de los proveedores'
module.content_type = search_content_type(DebtsPay._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

# FRM (4)
module = Module()
module.type_id = 4
module.name = 'Proveedores'
module.url = '/erp/scm/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck'
module.description = 'Permite administrar a los proveedores de las compras'
module.content_type = search_content_type(Provider._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 4
module.name = 'Productos'
module.url = '/erp/scm/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box'
module.description = 'Permite administrar los repuesto|herramienta|equipos del sistema'
module.content_type = search_content_type(Product._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 4
module.name = 'Compras'
module.url = '/erp/scm/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dolly-flatbed'
module.description = 'Permite administrar las compras de los productos'
module.content_type = search_content_type(Purchase._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 4
module.name = 'Inventarios'
module.url = '/erp/scm/inventory/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box-open'
module.description = 'Permite administrar los inventarios de las compras'
module.content_type = search_content_type(Inventory._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 5
module.name = 'Marcas'
module.url = '/erp/crm/brand/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck-loading'
module.description = 'Permite administrar las marcas de los vehículos'
module.content_type = search_content_type(Brand._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 5
module.name = 'Modelos'
module.url = '/erp/crm/exemplar/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-bell'
module.description = 'Permite administrar los modelos de los vehículos'
module.content_type = search_content_type(Exemplar._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 5
module.name = 'Clientes'
module.url = '/erp/crm/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-tag'
module.description = 'Permite administrar a los clientes del sistema'
module.content_type = search_content_type(Client._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 5
module.name = 'Vehículos'
module.url = '/erp/crm/vehicle/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-car-side'
module.description = 'Permite administrar los vehículos de los clientes'
module.content_type = search_content_type(Vehicle._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 5
module.name = 'Servicios de Veh.'
module.url = '/erp/crm/service/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-scroll'
module.description = 'Permite administrar los servicios de los vehículos'
module.content_type = search_content_type(Service._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 5
module.name = 'Ventas'
module.url = '/erp/crm/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas'
module.content_type = search_content_type(Sale._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

# HRM(7)

module = Module()
module.type_id = 7
module.name = 'Cargos'
module.url = '/erp/hrm/job/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-address-card'
module.description = 'Permite administrar los cargos de la compañia'
module.content_type = search_content_type(Job._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 7
module.name = 'Empleados'
module.url = '/erp/hrm/employee/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-friends'
module.description = 'Permite administrar los empleados de la compañia'
module.content_type = search_content_type(Employee._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 7
module.name = 'Contratos'
module.url = '/erp/hrm/contracts/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-contract'
module.description = 'Permite administrar los contratos de los empleados'
module.content_type = search_content_type(Contracts._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 7
module.name = 'Asistencias'
module.url = '/erp/hrm/assistance/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-calendar-check'
module.description = 'Permite administrar las asistencias de los empleados'
module.content_type = search_content_type(Assistance._meta.verbose_name.title())
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Salarios'
module.url = '/erp/hrm/salary/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dollar-sign'
module.description = 'Permite administrar los salarios de los empleados'
module.save()
print('insertado {}'.format(module.name))

# Reports (8)
module = Module()
module.type_id = 8
module.name = 'Rep. Gastos'
module.url = '/reports/expenses/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de gastos'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Compras'
module.url = '/reports/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de compras'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Cuentas por pagar'
module.url = '/reports/debts/pay/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de cuentas por pagar'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Clientes'
module.url = '/reports/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de clientes'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Proveedores'
module.url = '/reports/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de proveedores'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Salarios'
module.url = '/reports/salary/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de salarios'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Empleados'
module.url = '/reports/contracts/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de los contratos de los empleados'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Asistencias'
module.url = '/reports/assistance/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de las asistencias de los empleados'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 8
module.name = 'Rep. Ventas'
module.url = '/reports/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-pie'
module.description = 'Permite ver los reportes de las ventas y servicios'
module.save()
print('insertado {}'.format(module.name))

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

module = Module()
module.type_id = 9
module.name = 'Salarios'
module.url = '/erp/hrm/salary/employee/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-dollar-sign'
module.description = 'Permite ver los salarios de los empleados'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 9
module.name = 'Bonificaciones'
module.url = '/erp/crm/sale/employee/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-briefcase'
module.description = 'Permite ver los trabajos y bonificaciones'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 9
module.name = 'Asistencias'
module.url = '/erp/hrm/assistance/employee/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-calendar-check'
module.description = 'Permite ver las asistencias de los empleados'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 10
module.name = 'Ventas'
module.url = '/erp/crm/sale/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-cart-arrow-down'
module.description = 'Permite ver las ventas de los clientes'
module.save()
print('insertado {}'.format(module.name))

module = Module()
module.type_id = 10
module.name = 'Vehículos'
module.url = '/erp/crm/vehicle/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-car-side'
module.description = 'Permite ver los vehículos de los clientes'
module.save()
print('insertado {}'.format(module.name))

# group
group = Group()
group.name = 'Administrador'
group.save()
print('insertado {}'.format(group.name))

for mod in Module.objects.filter():
    gm = GroupModule()
    gm.modules = mod
    gm.groups = group
    gm.save()

    if mod.content_type is not None:
        for perm in Permission.objects.filter(content_type=mod.content_type):
            group.permissions.add(perm)

# user
u = User()
u.first_name = 'Taller Mecanico'
u.last_name = 'Servi Express'
u.username = 'Servi'
u.run = '1234567890'
u.email = 'xforce@serviexpress.page'
u.is_active = True
u.is_superuser = True
u.is_staff = True
u.password = 'express'
u.save()

u.groups.add(group)