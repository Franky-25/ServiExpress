# Generated by Django 3.0.3 on 2020-07-25 02:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('type', models.CharField(choices=[('repuesto_herramienta', 'Repuestos y herramientas'), ('maquinaria', 'Maquinarias')], default='repuesto_herramienta', max_length=20, verbose_name='Tipo')),
                ('cost', models.IntegerField(default=0, verbose_name='Precio')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen')),
            ],
            options={
                'verbose_name': 'Repuesto/Herramienta',
                'verbose_name_plural': 'Repuestos y Herramientas',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('rut', models.CharField(max_length=13, unique=True, verbose_name='rut')),
                ('mobile', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono celular')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
                ('email', models.CharField(blank=True, max_length=500, null=True, verbose_name='Email')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='contado', max_length=50)),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_credit', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.IntegerField(default=0)),
                ('dscto', models.IntegerField(default=0)),
                ('iva', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('prov', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.Provider')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('guaranty', models.IntegerField(default=0)),
                ('cant', models.IntegerField(default=0)),
                ('saldo', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('dscto', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('state', models.BooleanField(default=True)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.Product')),
                ('purch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scm.Purchase')),
            ],
            options={
                'verbose_name': 'Inventario',
                'verbose_name_plural': 'Inventarios',
                'ordering': ['-id'],
            },
        ),
    ]
