from django.shortcuts import render, redirect
from .forms import *
from .models import *
import pandas as pd
import qrcode
from io import BytesIO
from django.template.loader import get_template
from django.template import Context
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from django.views import View
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages 
from .decorators import authenticated_user
import numpy as np # Allow us to work with arrays
import warnings
warnings.filterwarnings('ignore') # Allow to disable Python warnings
import math # Allow us to perform mathematical tasks
import chardet
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


#-Login views
class InicioPlataforma(View):
    def get(self, request):
        #registroForm = RegistroForm()
        loginForm = LoginForm()
        return render(request, 'ReservasApp/inicioPlataforma.html', {  'loginForm': loginForm})

class LoginJsonView(View):
    def post(self, request):

        loginForm = LoginForm(request.POST)
        json_stuff = {"success": 0}
        if loginForm.is_valid():
            user = authenticate(username=loginForm.cleaned_data.get(
                'email'), password=loginForm.cleaned_data.get('password'))
        if user:
            login(request, user)
            request.session['usuario'] = None
            json_stuff["success"] = 1
        json_stuff = JsonResponse(json_stuff, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')

class AgregarRegistro(View):
    def post(self, request):
        registroForm = RegistroForm(request.POST)
        if registroForm.is_valid():
            usuario = registroForm.save()
            usuario.set_password(registroForm.cleaned_data.get('password'))
            usuario.username = usuario.email
            #grupo = Group.objects.get(name=registroForm.cleaned_data.get('grupo'))
            # usuario.groups.add(grupo)
            usuario.save()
            json_stuff = JsonResponse({"success": 1}, safe=False)
            return HttpResponse(json_stuff, content_type='application/json')
        else:
            json_stuff = JsonResponse({"success": 0}, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')

class AgregarRegistro2(View):
    def post(self, request):
        registroForm = CustomUserCreationForm(request.POST)
        if registroForm.is_valid():
            usuario = registroForm.save()
            #grupo = Group.objects.get(name=registroForm.cleaned_data.get('grupo'))
            # usuario.groups.add(grupo)
            usuario.save()
            json_stuff = JsonResponse({"success": 1}, safe=False)
            return HttpResponse(json_stuff, content_type='application/json')
        else:
            print("entre en el else de agregarregistro")
            json_stuff = JsonResponse({"success": 0}, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')

def CreateUsuarioView(request):
    
    if request.method == 'POST':
        registroForm = CustomUserCreationForm(request.POST) 
        if registroForm.is_valid():
            usuario = registroForm.save()
            usuario.save()
            registroForm.save()
            return(redirect('ReservasApp:index'))
        else:
        
            return render(request, 'ReservasApp/cargarUsuario.html', {'registroForm':registroForm})
            #return HttpResponse("""El formulario está mal, favor verifica que los datos esten correctos o que la imagen no pese mas de 10MB recarga en <a href = "javascript:history.back()"> Recargar </a>""")
    else:
        registroForm = CustomUserCreationForm()
        return render(request, 'ReservasApp/cargarUsuario.html', {'registroForm':registroForm})

def IndexView(request):
	return render (request, 'ReservasApp/index.html')

def ReservacionView(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ReservasApp:reservacion_success')
    else:
        form = ReservacionForm()
    return render(request, 'ReservasApp/reservacion.html', {'form': form})

def reservacion_successView(request):
    return render(request, 'ReservasApp/reservacion_success.html')

def Generar_QRView(request):
    # Obtener la cantidad de elementos del modelo
    cantidad_reservaciones = Reservacion.objects.count()
    catidad_reservaciones_historicas = ReservacionHistorico.objects.count()
    reservaciones_pendientes = cantidad_reservaciones - catidad_reservaciones_historicas
    # Crear un queryset para obtener todos los objetos del modelo
    if cantidad_reservaciones > 0:
        queryset = Reservacion.objects.all()
        queryset_hist = ReservacionHistorico.objects.all()

        # Convertir el queryset en un dataframe de Pandas
        df_reservaciones = pd.DataFrame(list(queryset.values()))
        df_reservaciones_hist = pd.DataFrame(list(queryset_hist.values()))

        #saber las keys de df_reservaciones
        print(df_reservaciones.columns)
        #print(df_reservaciones_hist.columns)

        """
        Asi se llaman as keys
        ['id', 'hora_inicio', 'hora_finalizacion', 'correo_electronico',
           'nombre', 'nombre_cliente', 'fecha_reservacion', 'nombre_rp',
           'numero_personas', 'comentarios'],
        """
        
        # Create Code column
        df_reservaciones['CODE'] = df_reservaciones['fecha_reservacion'].astype(str) + "-" \
            + df_reservaciones['nombre_rp'] + "-" + df_reservaciones['nombre_cliente'] + "-" \
            + df_reservaciones['numero_personas'].astype(str)

        # Get only values does not exists
        df_qrcode = pd.merge(df_reservaciones, df_reservaciones_hist, on='id', how='left', indicator='exists')
        df_qrcode = df_qrcode[df_qrcode['exists'].str.contains("left")].reset_index(drop=True)
        print(df_qrcode.columns)
        if len(df_qrcode) > 0:
            df_qrcode_hist = df_qrcode[['id', 'hora_inicio_x', 'hora_finalizacion_x', 'correo_electronico_x',
           'nombre_x', 'nombre_cliente_x', 'fecha_reservacion_x', 'nombre_rp_x',
           'numero_personas_x', 'comentarios_x']]    

        reservaciones_pendientes = len(df_qrcode)
    else:
        df_reservaciones = pd.DataFrame([])
    
    if request.method == 'POST':
        # Generar QR
        url = "https://www.ejemplo.com"  # cambiar por la URL que se desee codificar en el QR
        img = qrcode.make(url)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = 'qr.png'
        file = ContentFile(buffer.getvalue())
        # Guardar el archivo en la carpeta 'static/img'
        file_path = default_storage.save(os.path.join('ReservasApp', 'static', 'img', file_name), file)
        qr_file = InMemoryUploadedFile(buffer, None, 'qr.png', 'image/png', buffer.getbuffer().nbytes, None)

        contexto = {
            'cantidad_reservaciones': reservaciones_pendientes,
            'df_reservaciones': df_reservaciones.to_html(),
            'res_pendientes': reservaciones_pendientes,
            'qr_file': qr_file,
        }
        return render(request, 'ReservasApp/QR.html', contexto)

    # Renderizar la vista con el contexto
    contexto = {
        'cantidad_reservaciones': reservaciones_pendientes,
        'df_reservaciones': df_reservaciones.to_html(),
        'res_pendientes': reservaciones_pendientes
    }

    return render (request, 'ReservasApp/QR.html', contexto)
