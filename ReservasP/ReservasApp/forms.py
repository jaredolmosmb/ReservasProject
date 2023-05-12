from django import forms

from django.contrib.auth.models import Group
from django.db.models import Q
import datetime
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['hora_inicio', 'hora_finalizacion', 'correo_electronico', 'nombre', 'nombre_cliente', 'fecha_reservacion', 'nombre_rp', 'numero_personas', 'comentarios']
        widgets = {
            'hora_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'hora_finalizacion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_reservacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombre_rp': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_personas': forms.TextInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuario', 'id':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'id':'password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['password'].label = ''

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'name')