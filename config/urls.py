from django.contrib import admin
from django.urls import path
from hotel import views


urlpatterns = [

    # ADMINISTRACIÓN
    path(
        'admin/',
        admin.site.urls
    ),


    # PÁGINA PRINCIPAL
    path(
        '',
        views.inicio,
        name='inicio'
    ),


    # INICIAR SESIÓN
    path(
        'login/',
        views.iniciar_sesion,
        name='iniciar_sesion'
    ),


    # CERRAR SESIÓN
    path(
        'logout/',
        views.cerrar_sesion,
        name='logout'
    ),


    # MI PANEL
    path(
        'mipanel/',
        views.mi_panel,
        name='mi_panel'
    ),


    # SELECCIONAR HOTEL
    path(
        'seleccionar-hotel/<int:hotel_id>/',
        views.seleccionar_hotel,
        name='seleccionar_hotel'
    ),


    # AGREGAR HABITACIÓN
    path(
        'agregar-habitacion/',
        views.agregar_habitacion,
        name='agregar_habitacion'
    ),


    # DETALLE DE HABITACIÓN
    path(
        'habitacion/<int:habitacion_id>/',
        views.detalle_habitacion,
        name='detalle_habitacion'
    ),


    # RESERVAR HABITACIÓN
    path(
        'habitacion/<int:habitacion_id>/reservar/',
        views.reservar_habitacion,
        name='reservar_habitacion'
    ),


    # LIBERAR HABITACIÓN
    path(
        'habitacion/<int:habitacion_id>/liberar/',
        views.liberar_habitacion,
        name='liberar_habitacion'
    ),


    # CALENDARIO
    path(
        'calendario/',
        views.calendario_reservaciones,
        name='calendario_reservaciones'
    ),

]