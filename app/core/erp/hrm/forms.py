from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction
from django.forms import ModelForm
from django import forms
from config import settings

from core.erp.hrm.models import *


class JobForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EmployeeCreateForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres'}), label='Nombres',
                                 max_length=25)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}),
                                label='Apellidos', max_length=25)
    run = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}),
                          label='Número de cedula', max_length=10)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su email'}), label='Email',
                            max_length=30)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su teléfono celular'}),
                             label='Teléfono celular', max_length=10)
    birthdate = forms.DateField(input_formats=['%Y-%m-%d'],
                                widget=forms.TextInput(attrs={
                                    'value': datetime.now().strftime('%Y-%m-%d'),
                                    'class': 'form-control datetimepicker-input',
                                    'id': 'birthdate',
                                    'data-toggle': 'datetimepicker',
                                    'data-target': '#birthdate'
                                }),
                                label='Fecha de nacimiento')
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su dirección'}), label='Dirección',
                              max_length=500)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
        del self.fields['password1']
        del self.fields['password2']

    def save(self, commit=True):
        data = {}
        try:
            with transaction.atomic():
                if self.is_valid():
                    form = self.cleaned_data
                    user = User()
                    user.email = form['email']
                    user.first_name = form['first_name']
                    user.last_name = form['last_name']
                    user.run = form['run']
                    user.username = user.run
                    user.set_password(user.run)
                    image = form['image']
                    if image is not None:
                        user.image = image
                    user.save()

                    group = Group.objects.get(pk=settings.GROUPS.get('employee'))
                    user.groups.add(group)

                    emp = Employee()
                    emp.user = user
                    emp.address = form['address']
                    emp.birthdate = form['birthdate']
                    emp.mobile = form['mobile']
                    emp.save()
                else:
                    data['error'] = self.errors
        except Exception as e:
            data = {'error': str(e)}
        return data

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'run', 'email', 'image'
        exclude = ['password1', 'password2', 'username']


class EmployeeChangeForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres'}), label='Nombres',
                                 max_length=25)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}),
                                label='Apellidos', max_length=25)
    run = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}),
                          label='Número de cedula', max_length=10)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su email'}), label='Email',
                            max_length=30)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su teléfono celular'}),
                             label='Teléfono celular', max_length=10)
    birthdate = forms.DateField(input_formats=['%Y-%m-%d'],
                                widget=forms.TextInput(attrs={
                                    'value': datetime.now().strftime('%Y-%m-%d'),
                                    'class': 'form-control datetimepicker-input',
                                    'id': 'birthdate',
                                    'data-toggle': 'datetimepicker',
                                    'data-target': '#birthdate'
                                }),
                                label='Fecha de nacimiento')
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su dirección'}), label='Dirección',
                              max_length=500)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        del self.fields['password']

    def save(self, commit=True):
        data = {}
        try:
            with transaction.atomic():
                if self.is_valid():
                    user = self.instance.user
                    form = self.cleaned_data
                    user.email = form['email']
                    user.first_name = form['first_name']
                    user.last_name = form['last_name']
                    user.run = form['run']
                    user.username = user.run
                    image = form['image']
                    if image is not None:
                        if type(image) is bool:
                            user.image.delete(save=True)
                            user.image = None
                        else:
                            user.image = image
                    user.save()

                    emp = self.instance
                    emp.address = form['address']
                    emp.birthdate = form['birthdate']
                    emp.mobile = form['mobile']
                    emp.save()
                else:
                    data['error'] = self.errors
        except Exception as e:
            data = {'error': str(e)}
        return data

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'run', 'email', 'image'
        exclude = ['password', 'username']


class ContractsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit', False)
        super().__init__(*args, **kwargs)
        if edit:
            self.fields['emp'].widget.attrs['disabled'] = True

    class Meta:
        model = Contracts
        fields = '__all__'
        widgets = {
            'emp': forms.Select(attrs={'class': 'form-control select2'}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'start_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#start_date'
            }),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_date',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_date'
            }),
            'job': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'rmu': forms.TextInput(),
        }
        exclude = ['state']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class AssistanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit', False)
        super().__init__(*args, **kwargs)
        if edit:
            self.fields['date_joined'].widget.attrs['disabled'] = True

    class Meta:
        model = Assistance
        fields = '__all__'
        widgets = {
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'year': forms.TextInput(attrs={
                'id': 'year',
                'class': 'form-control datetimepicker-input',
                'data-toggle': 'datetimepicker',
                'data-target': '#year',
            }),
            'month': forms.Select(
                attrs={
                    'id': 'month',
                    'class': 'form-control select2',
                    'style': 'width: 100%'
                })
        }
        exclude = ['state']

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))


class SalaryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {
            'year': forms.TextInput(attrs={
                'id': 'year',
                'class': 'form-control datetimepicker-input',
                'data-toggle': 'datetimepicker',
                'data-target': '#year',
            }),
            'month': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;'
            }),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'autocomplete': 'off',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
        }