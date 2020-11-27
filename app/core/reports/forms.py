from django.forms import *
from core.erp.choices import months
from datetime import datetime


class ReportForm(forms.Form):
    year = CharField(widget=TextInput(attrs={
        'id': 'year',
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#year',
    }))

    month = ChoiceField(choices=months, widget=Select(
        attrs={
            'id': 'month',
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    date_joined = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'date_joined',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#date_joined'
        }))

    date_range = CharField(widget=TextInput(attrs={
        'id': 'date_range',
        'class': 'form-control',
    }))

    start_date = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'start_date',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#start_date'
        }))

    end_date = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'end_date',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#end_date'
        }))
