"""
EJERCICIO 1: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
SERVICIOS Y RESERVAS
Curso: Programación (213023)
Fase: 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Autor: Christian Melo Amaya y Eduardo Luis Molina
Descripción: Este archivo tiene como funcion principal realizar las pruebas del proyecto software FJ, en este archivo
se utiliza  las clases cliente, ReservaSaka, AlquilerEquipo, AseoriaEspecializada y Reserva. Todo esto nos permite verificar la funcionalidad del sistema.
Se ejecutan  10 pruebas, 5 validas y cinco invalidas, las validas verifican cliente, servicios y las reservas. Las invalidas
comprueban que el sistema puede detectar situacion como  correos incorrectos, precios negativos, servicios no disponibles
y cancelaciones  repetidas. Adicional  se utiliza try y except para controlar excepciones y evitar que un error detenga  la simulacion.

"""


#Tomamos la clase cliente, esta clase se encuentra en el archivo cliente.py
from cliente import Cliente


#Tomamos los tres tipos de servicios, estas clases se encuentran en el archivo servicio.py
from servicio import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)


# Tomamos la clase Reserva, esta clase se encuentra en el archivo reserva.py
from reserva import Reserva


# Tomamos la clase excepciones, esta clase se encuentra en el archivo excepciones.py
from excepciones import (
    SoftwareFJError,
    ServicioInvalidoError
)
# Tomamos la clase logger_config, esta clase se encuentra en el archivo logger_config.py
from logger_config import registrar_evento

# Se crea la función principal en una sola, para poder ejecutar.
def ejecutar_simulacion():

    # Se crea una lista para almacenar los clientes.
    clientes = []
    # Se crea una lista para almacenar los servicios.
    servicios = []
    # Se crea una lista para almacenar las reservas.
    reservas = []

    #TITULO DE LA SIMULACION.
    print("\n****************************************")
    print(" Simulacion Del Sistema Software FJ")
    print("******************************************")

    # ..........................................
    # PRUEBA 1: CREAR UN CLIENTE.
    # ..........................................
    try:
        # Se crea un cliente con información correcta.
        cliente = Cliente(
            "Carlos Perez",
            "12345678",
            "carlos@gmail.com"
        )
        # Se guarda el cliente
        clientes.append(cliente)

        # Se guarda el resultado.
        print("\nPRUEBA 1: Cliente creado correctamente.")


    except Exception as error:

        # Se muestra el error sin detener el programa.
        print(f"\nPRUEBA 1 FALLIDA: {error}")
    # ..........................................
    # PRUEBA 2: CREAR UNA SALA.
    # ..........................................
    try:
        # Se crea una sala con capacidad para 20 personas.
        sala = ReservaSala(
            "Sala de reuniones",
            50000,
            20
        )
        # Guardamos la sala.
        servicios.append(sala)
        # Mostramos el resultado.
        print("\nPRUEBA 2: Sala creada correctamente.")
    except Exception as error:
        
        # Se captura cualquier error.
        print(f"\nPRUEBA 2 FALLIDA: {error}")

    # ..........................................
    # PRUEBA 3: CREAR UN EQUIPO.
    # ..........................................

    try:

        # Se crea un equipo para alquilar.
        equipo = AlquilerEquipo(
            "Alquiler de portátil",
            30000,
            "Portátil",
            10000
        )
        # Se guarda el equipo.
        servicios.append(equipo)

        # se muestra el resultado.
        print("\nPRUEBA 3: Equipo creado correctamente.")

    except Exception as error:

        # Se captura el error.
        print(f"\nPRUEBA 3 FALLIDA: {error}")

    # ..........................................
    # PRUEBA 4: CREAR UNA ASESORÍA.
    # ..........................................
    try:

        # Se crea una asesoría especializada.
        asesoria = AsesoriaEspecializada(
            "Asesoría tecnológica",
            80000,
            "Desarrollo de software",
            "senior"
        )
        # Se guarda la asesoría.
        servicios.append(asesoria)

        # Se muestra el resultado.
        print("\nPRUEBA 4: Asesoría creada correctamente.")

    except Exception as error:

        # Se captura el error.
        print(f"\nPRUEBA 4 FALLIDA: {error}")
    # ..........................................
    # PRUEBA 5: PROCESAR UNA RESERVA CORRECTA.
    # ..........................................


    try:
        # Se crea una reserva con el cliente y la sala.
        reserva_correcta = Reserva(
            cliente,
            sala,
            3
        )


        # Se guarda la reserva.
        reservas.append(reserva_correcta)
      
        #Se procesa la reserva y se calcula su costo.
        costo = reserva_correcta.procesar()

        # Se muestra el resultado.
        print("\nPRUEBA 5: Reserva procesada correctamente.")

        # Se muestra el costo calculado.
        print(f"Costo de la reserva: ${costo:,.2f}")

        # Se muestra los datos de la reserva.
        reserva_correcta.mostrar_reserva()

    except Exception as error:

        # Se captura cualquier error.
        print(f"\nPRUEBA 5 FALLIDA: {error}")
    # ..........................................
    # PRUEBA 6: CLIENTE CON CORREO INCORRECTO.
    # ..........................................
    try:
        # Se crea un cliente con correo inválido.
        cliente_invalido = Cliente(
            "Maria Lopez",
            "87654321",
            "correo_incorrecto"
        )

        # Si se crea, se guarda en la lista.
        clientes.append(cliente_invalido)
      
        print("\nPRUEBA 6: Cliente creado.")

    except Exception as error:


        # Se captura el error de validación.
        print("\nPRUEBA 6: Error solucionado correctamente.")

        # Se muestra el motivo del error.
        print(f"Motivo: {error}")
    # ..........................................
    # PRUEBA 7: SERVICIO CON PRECIO NEGATIVO.
    # ..........................................
    try:
        # Se intenta crear una sala con precio negativo.
        servicio_invalido = ReservaSala(
            "Sala inválida",
            -50000,
            10
        )
        # Si se crea, se guarda en la lista.
        servicios.append(servicio_invalido)

        # Este mensaje no debería aparecer.
        print("\nPRUEBA 7: Servicio creado.")

    except ServicioInvalidoError as error:

        # Se captura el error del precio.
        print("\nPRUEBA 7: Precio negativo rechazado.")

        # Se muestra el motivo.
        print(f"Motivo: {error}")
      
    except Exception as error:

        #Se captura cualquier otro error.
        print(f"\nPRUEBA 7: Error solucionado: {error}")
    # ...............................................
    # PRUEBA 8: RESERVAR UN SERVICIO NO DISPONIBLE.
    # ...............................................
    try:
        # Se crea un servicio que no está disponible.
        sala_no_disponible = ReservaSala(
            "Sala ocupada",
            60000,
            15,
            disponible=False
        )

        # Se guarda el servicio.
        servicios.append(sala_no_disponible)

        # Se intenta reservar el servicio no disponible.
        reserva_invalida = Reserva(
            cliente,
            sala_no_disponible,
            2
        )

        # Se guarda la reserva.
        reservas.append(reserva_invalida)
        # Se intenta procesarla.
        reserva_invalida.procesar()
        # Este mensaje no debería aparecer.
        print("\nPRUEBA 8: Reserva procesada.")
    except Exception as error:

        # Se captura el error de disponibilidad.
        print("\nPRUEBA 8: Servicio no disponible detectado.")
        # Se muestra el motivo.
        print(f"Motivo: {error}")
    # .........................................
    # PRUEBA 9: RESERVA CON DURACIÓN CERO.
    # .........................................
    try:

        # Se intenta crear una reserva con duración cero.
        reserva_duracion_cero = Reserva(
            cliente,
            sala,
            0
        )

        # Este mensaje no debería aparecer.
        print("\nPRUEBA 9: Reserva creada.")


    except Exception as error:

        # Se captura el error de duración.
        print("\nPRUEBA 9: Duración inválida rechazada.")

        # Se muestra el motivo.
        print(f"Motivo: {error}")
    # .........................................
    # PRUEBA 10: CANCELAR UNA RESERVA DOS VECES.
    # ..........................................
    try:
        # Se crea una nueva reserva válida.
        reserva_cancelada = Reserva(
            cliente,
            sala,
            1
        )
        # Se guarda la reserva.
        reservas.append(reserva_cancelada)

        # Se cancela la reserva por primera vez.
        reserva_cancelada.cancelar()

        # Se intenta cancelarla nuevamente.
        reserva_cancelada.cancelar()

        # Este mensaje no debería aparecer.
        print("\nPRUEBA 10: Reserva cancelada.")

    except Exception as error:

        # Se captura el error de operación no permitida.
        print("\nPRUEBA 10: Cancelación repetida rechazada.")
      
        # Se muestra el motivo.
        print(f"Motivo: {error}")
    # ............................................
    # RESUMEN DE LA SIMULACIÓN.
    # ............................................

    # Se muestra el título del resumen.
    print("\n******************************************")
    print(" Resumen de la simulacion")
    print("********************************************")

    # Se muestra la cantidad de clientes.
    print(f"Clientes registrados: {len(clientes)}")

    # Se muestra la cantidad de servicios.
    print(f"Servicios registrados: {len(servicios)}")

    # Se muestra la cantidad de reservas.
    print(f"Reservas registradas: {len(reservas)}")

    # Se registra el final de las pruebas.
    registrar_evento(
        "Finalizó la simulación de las diez pruebas"
    )
    # Se devuelve las listas para que main.py las pueda utilizar.
    return {
        "clientes": clientes,
        "servicios": servicios,
        "reservas": reservas
    }

if __name__ == "__main__":
    ejecutar_simulacion()
