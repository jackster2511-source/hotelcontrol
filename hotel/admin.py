from django.contrib import admin
from .models import Hotel, Habitacion, Reservacion


# =========================================================
# HOTELES / CLIENTES
# =========================================================
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'usuario',
        'telefono',
        'fecha_vencimiento',
        'estado'
    )

    list_filter = (
        'estado',
    )

    search_fields = (
        'nombre',
        'usuario__username',
        'telefono',
        'correo'
    )


# =========================================================
# HABITACIONES
# =========================================================
@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):

    list_display = (
        'numero',
        'hotel',
        'tipo',
        'precio',
        'disponible'
    )

    list_filter = (
        'hotel',
        'disponible'
    )

    search_fields = (
        'numero',
        'hotel__nombre'
    )


# =========================================================
# RESERVACIONES
# =========================================================
@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):

    list_display = (
        'habitacion',
        'nombre_huesped',
        'fecha_entrada',
        'fecha_salida',
        'estado'
    )

    list_filter = (
        'estado',
        'fecha_entrada',
        'fecha_salida'
    )

    search_fields = (
        'nombre_huesped',
        'habitacion__numero'
    )