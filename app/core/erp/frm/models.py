from django.db import models
from django.forms import model_to_dict

from datetime import datetime

from core.erp.scm.models import Purchase


class TypeExpense(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Gasto'
        verbose_name_plural = 'Tipos de Gastos'
        ordering = ['id']


class Expenses(models.Model):
    type = models.ForeignKey(TypeExpense, verbose_name='Tipo de Gasto', on_delete=models.CASCADE)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    valor = models.IntegerField(default=0, verbose_name='Valor')

    def __str__(self):
        return self.desc

    def toJSON(self):
        item = model_to_dict(self)
        item['type'] = self.type.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = format(self.valor, '.0f')
        return item

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['id']


class DebtsPay(models.Model):
    purch = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    total = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.purch.prov.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purch'])
        item['purch'] = self.purch.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['total'] = format(self.total, '.0f')
        item['saldo'] = format(self.saldo, '.0f')
        item['pays'] = [i.toJSON() for i in self.detdebtspay_set.all()]
        return item

    class Meta:
        verbose_name = 'Cuenta por pagar'
        verbose_name_plural = 'Cuentas por pagar'
        ordering = ['-id']


class DetDebtsPay(models.Model):
    cta = models.ForeignKey(DebtsPay, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    valor = models.IntegerField(default=0)

    def __str__(self):
        return self.cta.id

    def toJSON(self):
        item = model_to_dict(self, exclude=['cta'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = format(self.valor, '.0f')
        return item

    class Meta:
        verbose_name = 'Det. Cuenta por pagar'
        verbose_name_plural = 'Det. Cuentas por pagar'
        ordering = ['-id']
