from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hotel, Habitacion, Reservacion


# =========================================================
# PÁGINA DE INICIO
# =========================================================
def inicio(request):
    hoteles = Hotel.objects.all()

    return render(
        request,
        'inicio.html',
        {
            'hoteles': hoteles
        }
    )


# =========================================================
# INICIAR SESIÓN
# =========================================================
def iniciar_sesion(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            login(request, usuario)

            # Guardar automáticamente el hotel del usuario
            try:
                hotel = usuario.hotel
                request.session['hotel_id'] = hotel.id
            except Hotel.DoesNotExist:
                pass

            return redirect('mi_panel')

        messages.error(
            request,
            'Usuario o contraseña incorrectos.'
        )

    return render(
        request,
        'login.html'
    )


# =========================================================
# CERRAR SESIÓN
# =========================================================
def cerrar_sesion(request):

    request.session.pop('hotel_id', None)

    logout(request)

    return redirect('inicio')


# =========================================================
# MI PANEL PRINCIPAL
# =========================================================
@login_required
def mi_panel(request):

    # =====================================================
    # SI ES SUPERUSUARIO PUEDE VER TODOS LOS HOTELES
    # =====================================================
    if request.user.is_superuser:

        hoteles = Hotel.objects.all()

        hotel_id = request.session.get('hotel_id')

        hotel = None

        if hotel_id:

            try:
                hotel = Hotel.objects.get(id=hotel_id)
            except Hotel.DoesNotExist:
                hotel = None

        if hotel is None and hoteles.exists():

            hotel = hoteles.first()

            request.session['hotel_id'] = hotel.id

    # =====================================================
    # USUARIO NORMAL SOLO VE SU HOTEL
    # =====================================================
    else:

        try:
            hotel = request.user.hotel

            hoteles = Hotel.objects.filter(
                id=hotel.id
            )

            request.session['hotel_id'] = hotel.id

        except Hotel.DoesNotExist:

            hotel = None

            hoteles = Hotel.objects.none()

    # =====================================================
    # SI NO EXISTE HOTEL
    # =====================================================
    if hotel is None:

        context = {
            'hoteles': hoteles,
            'hotel': None,
            'habitaciones': [],
            'total_habitaciones': 0,
            'habitaciones_disponibles': 0,
            'habitaciones_ocupadas': 0,
            'reservaciones': [],
        }

        return render(
            request,
            'mi_panel.html',
            context
        )

    # =====================================================
    # HABITACIONES DEL HOTEL
    # =====================================================
    habitaciones = Habitacion.objects.filter(
        hotel=hotel
    ).order_by('numero')

    habitaciones_disponibles = habitaciones.filter(
        disponible=True
    )

    habitaciones_ocupadas = habitaciones.filter(
        disponible=False
    )

    # =====================================================
    # RESERVACIONES DEL HOTEL
    # =====================================================
    reservaciones = Reservacion.objects.filter(
        habitacion__hotel=hotel
    ).select_related(
        'habitacion'
    ).order_by(
        '-fecha_entrada'
    )

    context = {
        'hoteles': hoteles,
        'hotel': hotel,

        'habitaciones': habitaciones,

        'total_habitaciones':
            habitaciones.count(),

        'habitaciones_disponibles':
            habitaciones_disponibles.count(),

        'habitaciones_ocupadas':
            habitaciones_ocupadas.count(),

        'reservaciones':
            reservaciones,
    }

    return render(
        request,
        'mi_panel.html',
        context
    )


# =========================================================
# SELECCIONAR HOTEL
# =========================================================
@login_required
def seleccionar_hotel(request, hotel_id):

    hotel = get_object_or_404(
        Hotel,
        id=hotel_id
    )

    # Un usuario normal solo puede seleccionar su propio hotel
    if not request.user.is_superuser:

        try:
            if request.user.hotel.id != hotel.id:

                messages.error(
                    request,
                    'No tienes permiso para acceder a este hotel.'
                )

                return redirect('mi_panel')

        except Hotel.DoesNotExist:

            return redirect('mi_panel')

    request.session['hotel_id'] = hotel.id

    return redirect('mi_panel')


# =========================================================
@login_required
def agregar_habitacion(request):

    hotel_id = request.session.get('hotel_id')

    if not hotel_id:

        messages.error(
            request,
            'Primero debes seleccionar un hotel.'
        )

        return redirect('mi_panel')


    hotel = get_object_or_404(
        Hotel,
        id=hotel_id
    )


    # Seguridad para usuario normal
    if not request.user.is_superuser:

        try:

            if request.user.hotel.id != hotel.id:

                messages.error(
                    request,
                    'No tienes permiso para modificar este hotel.'
                )

                return redirect('mi_panel')

        except Hotel.DoesNotExist:

            return redirect('mi_panel')


    if request.method == 'POST':

        numero = request.POST.get('numero')
        tipo = request.POST.get('tipo')
        precio = request.POST.get('precio')


        if not numero or not tipo or not precio:

            messages.error(
                request,
                'Todos los campos son obligatorios.'
            )

            return render(
                request,
                'agregar_habitacion.html',
                {
                    'hotel': hotel
                }
            )


        Habitacion.objects.create(
            hotel=hotel,
            numero=numero,
            tipo=tipo,
            precio=precio,
            disponible=True
        )


        messages.success(
            request,
            'Habitación agregada correctamente.'
        )

        return redirect('mi_panel')


    return render(
        request,
        'agregar_habitacion.html',
        {
            'hotel': hotel
        }
    )
# =========================================================
@login_required
def agregar_habitacion(request):

    hotel_id = request.session.get('hotel_id')

    if not hotel_id:

        messages.error(
            request,
            'Primero debes seleccionar un hotel.'
        )

        return redirect('mi_panel')


    hotel = get_object_or_404(
        Hotel,
        id=hotel_id
    )


    # Seguridad para usuario normal
    if not request.user.is_superuser:

        try:

            if request.user.hotel.id != hotel.id:

                messages.error(
                    request,
                    'No tienes permiso para modificar este hotel.'
                )

                return redirect('mi_panel')

        except Hotel.DoesNotExist:

            return redirect('mi_panel')


    if request.method == 'POST':

        numero = request.POST.get('numero')
        tipo = request.POST.get('tipo')
        precio = request.POST.get('precio')


        if not numero or not tipo or not precio:

            messages.error(
                request,
                'Todos los campos son obligatorios.'
            )

            return render(
                request,
                'agregar_habitacion.html',
                {
                    'hotel': hotel
                }
            )


        Habitacion.objects.create(
            hotel=hotel,
            numero=numero,
            tipo=tipo,
            precio=precio,
            disponible=True
        )


        messages.success(
            request,
            'Habitación agregada correctamente.'
        )

        return redirect('mi_panel')


    return render(
        request,
        'agregar_habitacion.html',
        {
            'hotel': hotel
        }
    )
# =========================================================
# VER DETALLE DE HABITACIÓN
# =========================================================
@login_required
def detalle_habitacion(request, habitacion_id):

    habitacion = get_object_or_404(
        Habitacion,
        id=habitacion_id
    )

    return render(
        request,
        'detalle_habitacion.html',
        {
            'habitacion': habitacion
        }
    )


# =========================================================
# RESERVAR HABITACIÓN
# =========================================================
@login_required
def reservar_habitacion(request, habitacion_id):

    habitacion = get_object_or_404(
        Habitacion,
        id=habitacion_id
    )

    if not habitacion.disponible:

        messages.error(
            request,
            'Esta habitación no está disponible.'
        )

        return redirect(
            'detalle_habitacion',
            habitacion_id=habitacion.id
        )

    if request.method == 'POST':

        nombre_huesped = request.POST.get(
            'nombre_huesped'
        )

        fecha_entrada = request.POST.get(
            'fecha_entrada'
        )

        fecha_salida = request.POST.get(
            'fecha_salida'
        )

        # Crear la reservación
        if nombre_huesped and fecha_entrada and fecha_salida:

            Reservacion.objects.create(
                habitacion=habitacion,
                nombre_huesped=nombre_huesped,
                fecha_entrada=fecha_entrada,
                fecha_salida=fecha_salida,
                estado='ocupada'
            )

        # Marcar habitación como no disponible
        habitacion.disponible = False

        habitacion.save()

        messages.success(
            request,
            'Habitación reservada correctamente.'
        )

        return redirect('mi_panel')

    return render(
        request,
        'reservar_habitacion.html',
        {
            'habitacion': habitacion
        }
    )


# =========================================================
# LIBERAR HABITACIÓN
# =========================================================
@login_required
def liberar_habitacion(request, habitacion_id):

    habitacion = get_object_or_404(
        Habitacion,
        id=habitacion_id
    )

    # Cambiar reservaciones ocupadas a finalizadas
    Reservacion.objects.filter(
        habitacion=habitacion,
        estado='ocupada'
    ).update(
        estado='finalizada'
    )

    # Liberar habitación
    habitacion.disponible = True

    habitacion.save()

    messages.success(
        request,
        'Habitación liberada correctamente.'
    )

    return redirect('mi_panel')


# =========================================================
# CALENDARIO DE RESERVACIONES
# =========================================================
@login_required
def calendario_reservaciones(request):

    import calendar
    from datetime import datetime

    hotel_id = request.session.get('hotel_id')

    hotel = None

    if hotel_id:

        try:

            hotel = Hotel.objects.get(
                id=hotel_id
            )

        except Hotel.DoesNotExist:

            hotel = None

    # Si es superusuario
    if request.user.is_superuser:

        hoteles = Hotel.objects.all()

        if hotel is None and hoteles.exists():

            hotel = hoteles.first()

            request.session['hotel_id'] = hotel.id

    # Usuario normal
    else:

        try:

            hotel = request.user.hotel

            hoteles = Hotel.objects.filter(
                id=hotel.id
            )

            request.session['hotel_id'] = hotel.id

        except Hotel.DoesNotExist:

            hoteles = Hotel.objects.none()

    hoy = datetime.now()

    try:

        mes = int(
            request.GET.get(
                'mes',
                hoy.month
            )
        )

    except ValueError:

        mes = hoy.month

    try:

        anio = int(
            request.GET.get(
                'anio',
                hoy.year
            )
        )

    except ValueError:

        anio = hoy.year

    if mes < 1 or mes > 12:

        mes = hoy.month

    calendario = calendar.monthcalendar(
        anio,
        mes
    )

    # =====================================================
    # RESERVACIONES DEL HOTEL
    # =====================================================
    reservaciones = []

    if hotel:

        reservaciones = Reservacion.objects.filter(
            habitacion__hotel=hotel
        ).select_related(
            'habitacion'
        )

    # Crear información de los días
    dias = []

    for semana in calendario:

        for dia in semana:

            reservaciones_dia = []

            if dia != 0:

                for reservacion in reservaciones:

                    if (
                        reservacion.fecha_entrada.day <= dia
                        and reservacion.fecha_salida.day >= dia
                        and reservacion.fecha_entrada.month == mes
                        and reservacion.fecha_entrada.year == anio
                    ):

                        reservaciones_dia.append(
                            reservacion
                        )

            dias.append({
                'numero': dia,
                'reservaciones': reservaciones_dia
            })

    # =====================================================
    # MES ANTERIOR
    # =====================================================
    if mes == 1:

        mes_anterior = 12
        anio_anterior = anio - 1

    else:

        mes_anterior = mes - 1
        anio_anterior = anio

    # =====================================================
    # MES SIGUIENTE
    # =====================================================
    if mes == 12:

        mes_siguiente = 1
        anio_siguiente = anio + 1

    else:

        mes_siguiente = mes + 1
        anio_siguiente = anio

    context = {

        'hotel': hotel,

        'hoteles': hoteles,

        'calendario': calendario,

        'dias': dias,

        'mes': mes,

        'anio': anio,

        'nombre_mes':
            calendar.month_name[mes],

        'mes_anterior':
            mes_anterior,

        'anio_anterior':
            anio_anterior,

        'mes_siguiente':
            mes_siguiente,

        'anio_siguiente':
            anio_siguiente,
    }

    return render(
        request,
        'calendario.html',
        context
    )