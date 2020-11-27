from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction
from django.forms import ModelForm

from config import settings
from core.erp.crm.models import *


class BrandForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Brand
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


class ExemplarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Exemplar
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'brand': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
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


class ClientCreateForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus nombres'}), label='Nombres', max_length=25)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}),
                                label='Apellidos', max_length=25)
    run = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}),
                          label='Número de cedula', max_length=10)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su email'}), label='Email', max_length=30)
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
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su dirección'}), label='Dirección', max_length=500)

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

                    group = Group.objects.get(pk=settings.GROUPS.get('client'))
                    user.groups.add(group)

                    client = Client()
                    client.user = user
                    client.address = form['address']
                    client.birthdate = form['birthdate']
                    client.mobile = form['mobile']
                    client.save()
                else:
                    data['error'] = self.errors
        except Exception as e:
            data = {'error': str(e)}
        return data

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'run', 'email', 'image'
        exclude = ['password1', 'password2', 'username']


class ClientChangeForm(UserChangeForm):
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
        self.fields['first_name'].widget.attrs['autofocus'] = True
        del self.fields['password', 'username']


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

                    client = self.instance
                    client.address = form['address']
                    client.birthdate = form['birthdate']
                    client.mobile = form['mobile']
                    client.save()
                else:
                    data['error'] = self.errors
        except Exception as e :
            data = {'error': str(e)}
        return data

    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'run', 'email', 'image'
        exclude = ['password']


class VehicleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plaque'].widget.attrs['autofocus'] = True

    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'plaque': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'year': forms.TextInput({
                #'value': datetime.now().year,
                'class': 'form-control datetimepicker-input',
                'id': 'year',
                'data-toggle': 'datetimepicker',
                'data-target': '#year'
            }),
            'cli': forms.Select(attrs={'class': 'select2', 'style': 'width:100%;'}),
            'exemplar': forms.Select(attrs={'class': 'select2', 'style': 'width:100%;'}),
        }
        exclude = ['state', 'km_current']

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


class ServiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'duration_km': forms.TextInput(),
            'price': forms.TextInput(),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows':3, 'cols': 3}),
            'days': forms.TextInput(),
        }
        exclude = ['date_joined']

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


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veh'].widget.attrs['autofocus'] = True

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'veh': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'type_serv': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'km_current': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
            'dscto': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            }),
            'total': forms.TextInput(attrs={
                'class': 'form-control',
                'disabled': True
            })
        }

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))