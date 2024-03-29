from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser, PermissionsMixin, UserManager, BaseUserManager
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
import uuid, random
from django.contrib.auth.models import Group
import qrcode
from io import BytesIO
from django.core.files import File

from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.

class Reservacion(models.Model):
    #hora_inicio = models.DateTimeField()
    #hora_finalizacion = models.DateTimeField()
    #correo_electronico = models.EmailField(blank=True)
    #nombre = models.CharField(max_length=255, blank=True)
    nombre_cliente = models.CharField(max_length=255, blank=True)
    fecha_reservacion = models.DateField()
    nombre_rp = models.CharField(max_length=255, blank=True)
    numero_personas = models.PositiveIntegerField()
    comentarios = models.TextField(blank=True)
    qr_code = models.ImageField(upload_to='ReservasApp/static/img', blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # generar el código QR
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(str(self.fecha_reservacion)+"-"+str(self.nombre_rp)+"-"+str(self.nombre_cliente)+"-"+str(self.numero_personas))
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        # guardar el código QR como imagen en un campo de la instancia del modelo
        buffer = BytesIO()
        img.save(buffer)
        self.qr_code.save(f'{self.id}.png', File(buffer), save=False)

        super().save(*args, **kwargs)

class ReservacionHistorico(models.Model):
    hora_inicio = models.DateTimeField()
    hora_finalizacion = models.DateTimeField()
    correo_electronico = models.EmailField()
    nombre = models.CharField(max_length=255)
    nombre_cliente = models.CharField(max_length=255, blank=True)
    fecha_reservacion = models.DateField()
    nombre_rp = models.CharField(max_length=255)
    numero_personas = models.PositiveIntegerField()
    comentarios = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Reservación Histórico"
        verbose_name_plural = "Reservaciones Históricos"

    def __str__(self):
        return str(self.id)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=200, default="nm")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    @property
    def usuario_id(self):
        return unicode(self.id)