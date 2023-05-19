from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'ReservasApp'

urlpatterns = [
	path('', views.IndexView, name =  "index"),
	path('QR_gen', views.Generar_QRView, name =  "QR_gen"),
	path('ReservacionForm', views.ReservacionView, name =  "ReservacionForm"),
	path('ReservacionSuccess', views.reservacion_successView, name =  "reservacion_success"),

	path('inicioPlataforma', views.InicioPlataforma.as_view(), name='inicioPlataforma'),
	path('loginJson/', views.LoginJsonView.as_view(), name='loginjson'),
	path('agregarRegistro/', views.AgregarRegistro.as_view(), name='agregarRegistro'),
	path('logout/', auth_views.LogoutView.as_view() , name='logout'),
	path('agregarRegistro2/', views.AgregarRegistro2.as_view(), name='agregarRegistro2'),
	path('cargar_usuario/', views.CreateUsuarioView, name='cargar_usuario'),

	path('listaR', views.ListaReservacionesView, name='listaR'),
	path('actualizarR/<int:pk>/', views.ActualizarReservaciones.as_view(), name='actualizarR'),
	path('detalle/<int:reservacion_id>', views.DetalleView, name="detalle"),
	#path('actualizarU/<int:pk>/', views.ActualizarUsuarios.as_view(), name='actualizarU'),

	
	]