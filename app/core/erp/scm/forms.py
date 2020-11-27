from django.forms import ModelForm
from django import forms

from .models import *


class ProviderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'rut': forms.TextInput(attrs={'placeholder': 'Ingrese un número de rut'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
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


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'cost': forms.TextInput(),
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


class PurchaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prov'].widget.attrs['autofocus'] = True

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'prov': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'payment': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#date_joined'
            }),
            'end_credit': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'end_credit',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#end_credit'
            }),
            'subtotal': forms.TextInput(),
            'iva': forms.TextInput(),
            'dscto': forms.TextInput(),
            'total': forms.TextInput()
        }


class InventoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase'].choices = self.get_dates()

    def get_dates(self):
        data = []
        data.append(('', '---------------'))
        for i in Purchase.objects.all():
            name = '{} / {}'.format(i.date_joined.strftime('%Y-%m-%d'), i.prov.name)
            data.append((int(i.id), name))
        return tuple(data)

    product = forms.ModelChoiceField(queryset=Product.objects.filter().order_by('-id'),
                                     widget=forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'
                                                                }))

    purchase = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'
                                                            }))
