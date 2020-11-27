from datetime import datetime

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config.settings import STATIC_URL, MEDIA_URL
from core.erp.choices import type_payment, type_prod


class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    rut = models.CharField(max_length=13, unique=True, verbose_name='rut')
    mobile = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=500, null=True, blank=True, verbose_name='Email')
    date_joined = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    type = models.CharField(choices=type_prod, default='repuesto_herramienta', max_length=20, verbose_name='Tipo')
    cost = models.IntegerField(default=0, verbose_name='Precio')
    image = models.ImageField(upload_to='product/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_stock(self):
        return int(self.inventory_set.filter(saldo__gt=0, state=True).aggregate(r=Coalesce(Sum('saldo'), 0)).get('r'))

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['cost'] = format(self.cost, '.0f')
        item['image'] = self.get_image()
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/default/empty.png')

    class Meta:
        verbose_name = 'Repuesto/Herramienta'
        verbose_name_plural = 'Repuestos y Herramientas'
        ordering = ['-name']


class Purchase(models.Model):
    prov = models.ForeignKey(Provider, on_delete=models.CASCADE)
    payment = models.CharField(choices=type_payment, max_length=50, default='contado')
    date_joined = models.DateField(default=datetime.now)
    end_credit = models.DateField(default=datetime.now)
    subtotal = models.IntegerField(default=0)
    dscto = models.IntegerField(default=0)
    iva = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.prov.name

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.inventory_set.all():
            subtotal += float(d.price) * int(d.cant)
        self.subtotal = subtotal
        self.iva = 0.00
        self.total = float(self.subtotal) - float(self.dscto)
        self.save()

    def toJSON(self):
        item = model_to_dict(self, exclude=['prov'])
        item['nro'] = format(self.id, '06d')
        item['type_payment'] = {'id': self.payment, 'name': self.get_payment_display()}
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['prov'] = self.prov.toJSON()
        item['subtotal'] = format(self.subtotal, '.0f')
        item['dscto'] = format(self.dscto, '.0f')
        item['iva'] = format(self.iva, '.0f')
        item['total'] = format(self.total, '.0f')
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-id']


class Inventory(models.Model):
    purch = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    serie = models.CharField(max_length=10, unique=True, null=True, blank=True)
    guaranty = models.IntegerField(default=0)
    cant = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    dscto = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.prod.name

    def guaranty_format(self):
        if self.guaranty > 1:
            return '{} Años'.format(self.guaranty)
        if self.guaranty == 1:
            return '{} Año'.format(self.guaranty)
        return 'Sin años'

    def get_depreciation(self):
        dep = 0.00
        if self.guaranty > 0:
            dep = (float(self.price) / int(self.guaranty)) / 365
        return dep

    def toJSON(self):
        item = model_to_dict(self, exclude=['purch'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.0f')
        item['dscto'] = format(self.dscto, '.0f')
        item['total'] = format(self.total, '.0f')
        item['depreciation'] = format(self.get_depreciation(), '.0f')
        return item

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['-id']
