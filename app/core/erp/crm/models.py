from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from core.erp.choices import type_prod
from core.erp.hrm.models import Contracts
from core.erp.scm.models import Inventory
from core.security.models import Company
from core.user.models import User


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    mobile = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.user.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self, exclude=['user'])
        item['user'] = self.user.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marca'
        ordering = ['id']


class Exemplar(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marca')

    def __str__(self):
        return 'Modelo: {} / Marca: {}'.format(self.name, self.brand.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['brand'] = self.brand.toJSON()
        return item

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        ordering = ['id']


class Vehicle(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE, verbose_name='Modelo/Marca')
    year = models.IntegerField(default=0, verbose_name='Año')
    plaque = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    state = models.BooleanField(default=True, verbose_name='Estado')
    km_current = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Km Actual')

    def __str__(self):
        return '{} / {} / {} / {}'.format(self.cli.user.get_full_name(), self.plaque, self.exemplar.name,
                                          self.exemplar.brand.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['exemplar'] = self.exemplar.toJSON()
        item['cli'] = self.cli.toJSON()
        item['km_current'] = format(self.km_current, '.2f')
        return item

    def get_alerts(self):
        text = ''
        services = self.sale_set.order_by('-id').values_list('type_serv_id', flat=True).distinct()
        try:
            for s in Service.objects.filter(id__in=services):
                km_last = 0.00
                sales = self.sale_set.filter(type_serv_id=s.id).order_by('-id')
                if sales:
                    km_last = sales[0].km_current
                km_now = self.km_current - km_last
                if km_now >= s.duration_km:
                    text = '<ul>'
                    text += '<li>Ya debes realizar el servicio de {} en tu vehículo, el valor del kilometraje es el indicado para activar el servicio de los {} KM (Tu último servicio fue realizado en el kilometraje {} KM)</li>'.format(s.name,
                                                                                                                s.duration_km, km_last)
                    text += '</ul>'
        except:
            pass
        return text

    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'
        ordering = ['id']


class Service(models.Model):
    date_joined = models.DateField(default=datetime.now)
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name='Descripción')
    price = models.IntegerField(default=0, verbose_name='Tarifa')
    duration_km = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Duración KM')
    days = models.IntegerField(default=0, verbose_name='Días')

    def __str__(self):
        return '{} / ${} / {} KM'.format(self.name, self.price, self.duration_km)

    def toJSON(self):
        item = model_to_dict(self)
        item['price'] = format(self.price, '.0f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['duration_km'] = format(self.duration_km, '.2f')
        return item

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['id']


class Sale(models.Model):
    veh = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    type_serv = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    km_current = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    km_service = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    date_joined = models.DateField(default=datetime.now)
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    subtotal = models.IntegerField(default=0)
    dscto = models.IntegerField(default=0)
    iva = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.veh.plaque

    def get_repuests(self):
        return self.detresources_set.filter(rec__prod__type__in=[type_prod[0][0]])

    def get_equips(self):
        return self.detresources_set.filter(rec__prod__type__in=[type_prod[1][0]])

    def nro(self):
        return format(self.id, '06d')

    def toJSON(self):
        item = model_to_dict(self, exclude=['type_serv'])
        if self.type_serv:
            item['type_serv'] = self.type_serv.toJSON()
        if self.veh:
            item['veh'] = self.veh.toJSON()
        item['nro'] = format(self.id, '06d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['km_current'] = format(self.km_current, '.2f')
        item['km_service'] = format(self.km_service, '.2f')
        item['subtotal'] = format(self.subtotal, '.0f')
        item['dscto'] = format(self.dscto, '.0f')
        item['iva'] = format(self.iva, '.0f')
        item['total'] = format(self.total, '.0f')
        return item

    def get_iva(self):
        try:
            return float(Company.objects.first().iva)
        except:
            pass
        return 0.00

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.detresources_set.filter(rec__prod__type__in=[type_prod[0][0]]):
            subtotal += float(d.price) * int(d.cant)
        # for d in self.detemployees_set.all():
        #     subtotal += float(d.bonus)
        self.subtotal = float(subtotal) + float(self.type_serv.price)
        self.iva = self.get_iva() * float(self.subtotal)
        self.total = float(self.subtotal) - float(self.dscto) + float(self.iva)
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.detresources_set.filter(rec__prod__type__in=[type_prod[0][0]]):
                i.rec.saldo += i.cant
                i.inv.save()
                i.delete()
        except:
            pass
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Ventas'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class DetResources(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    rec = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.rec.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['rec'] = self.rec.toJSON()
        item['price'] = format(self.price, '.0f')
        item['dscto'] = format(self.dscto, '.0f')
        item['total'] = format(self.total, '.0f')
        return item

    class Meta:
        verbose_name = 'Det. Venta'
        verbose_name_plural = 'Det. Ventas'
        ordering = ['-id']


class DetEmployees(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    cont = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    bonus = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.cont.emp.user.get_full_name()

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['cont'] = self.cont.toJSON()
        item['bonus'] = format(self.bonus, '.0f')
        return item

    class Meta:
        verbose_name = 'Det. Empleado'
        verbose_name_plural = 'Det. Empleados'
        ordering = ['-id']
