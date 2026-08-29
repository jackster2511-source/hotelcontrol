from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# =========================================================
# HOTEL / CLIENTE
# =========================================================
class Hotel(models.Model):

    ESTADOS = [
        ('activo', 'Activo'),
        ('vencido', 'Pago vencido'),
        ('suspendido', 'Suspendido'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='hotel'
    )

    nombre = models.CharField(
        max_length=150
    )

    telefono = models.CharField(
        max_length=30,
        blank=True
    )

    correo = models.EmailField(
        blank=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    fecha_vencimiento = models.DateField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='activo'
    )

    def esta_activo(self):

        if self.estado in [
            'suspendido',
            'cancelado',
            'vencido'
        ]:
            return False

        if (
            self.fecha_vencimiento
            and self.fecha_vencimiento < timezone.now().date()
        ):
            return False

        return True

    def __str__(self):
        return self.nombre


# =========================================================
# HABITACIONES
# =========================================================
class Habitacion(models.Model):

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='habitaciones',
        null=True,
        blank=True
    )

    numero = models.IntegerField()

    tipo = models.CharField(
        max_length=50
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    disponible = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Habitación {self.numero}"


# =========================================================
# RESERVACIONES
# =========================================================
class Reservacion(models.Model):

    ESTADOS = [
        ('reservada', 'Reservada'),
        ('ocupada', 'Ocupada'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE,
        related_name='reservaciones'
    )

    nombre_huesped = models.CharField(
        max_length=100
    )

    fecha_entrada = models.DateField()

    fecha_salida = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='reservada'
    )

    def __str__(self):
        return (
            f"{self.nombre_huesped} - "
            f"Habitación {self.habitacion.numero}"
        )