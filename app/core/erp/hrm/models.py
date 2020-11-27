from datetime import datetime, timedelta
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from core.erp.choices import months
from core.user.models import User


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono Celular', null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Dirección')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')

    def __str__(self):
        return self.user.get_full_name()

    def toJSON(self):
        item = model_to_dict(self, exclude=['user'])
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['id']


class Job(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Puesto de Trabajo'
        verbose_name_plural = 'Puesto de Trabajos'
        ordering = ['id']


class Contracts(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Empleado')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Cargo')
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    rmu = models.IntegerField(default=0)
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.emp.user.get_full_name()

    def get_nro(self):
        return format(self.id, '06d')

    def worked_days(self, d):
        date_joined = datetime.strptime(d, '%Y-%m-%d')
        end_date = str((date_joined - timedelta(days=1)).date())
        start_date = str((date_joined - timedelta(days=6)).date())
        return self.assistance_set.filter(date_joined__range=[start_date, end_date])

    def get_dsctos(self, d):
        sumdscto = float(self.worked_days(d).aggregate(r=Coalesce(Sum('dscto'), 0)).get('r'))
        return sumdscto

    def get_bonus(self, d):
        date_joined = datetime.strptime(d, '%Y-%m-%d')
        end_date = str((date_joined - timedelta(days=1)).date())
        start_date = str((date_joined - timedelta(days=6)).date())
        sumbonus = float(self.detemployees_set.filter(sale__date_joined__range=[start_date, end_date]).aggregate(r=Coalesce(Sum('bonus'), 0)).get('r'))
        return sumbonus

    def toJSON(self):
        item = model_to_dict(self, exclude=['emp'])
        item['nro'] = format(self.id, '06d')
        item['emp'] = self.emp.toJSON()
        item['job'] = self.job.toJSON()
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['rmu'] = format(self.rmu, '.0f')
        return item

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['id']


class Assistance(models.Model):
    date_joined = models.DateField(default=datetime.now)
    cont = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField(choices=months, default=1)
    day = models.IntegerField()
    motive_perm = models.CharField(max_length=500, null=True, blank=True)
    dscto = models.IntegerField(default=0)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.get_month_display()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['month_name'] = self.get_month_display()
        item['cont'] = self.cont.toJSON()
        item['dscto'] = format(self.dscto, '.0f')
        return item

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['id']


class Salary(models.Model):
    date_joined = models.DateField(default=datetime.now)
    cont = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    week = models.IntegerField(default=0)
    days_work = models.IntegerField(default=0)
    dsctos = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.cont.emp.user.get_full_name()

    def toJSON(self):
        item = model_to_dict(self, exclude=['cont'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['cont'] = self.cont.toJSON()
        item['dsctos'] = format(self.dsctos, '.0f')
        item['bonus'] = format(self.bonus, '.0f')
        item['total'] = format(self.total, '.0f')
        return item

    class Meta:
        verbose_name = 'Salario'
        verbose_name_plural = 'Salarios'
        ordering = ['-id']
