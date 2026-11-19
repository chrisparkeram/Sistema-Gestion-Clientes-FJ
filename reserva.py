"""
EJERCICIO 1: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
SERVICIOS Y RESERVAS
Curso: Programación (213023)
Fase: 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Autor: Christian Melo Amaya y Eduardo Luis Flores Molina
Descripción: El archivo reserva.py es el encargado de controlar el proceso de las reservas
dentro del proyecto, esto permite una realcion correcta entre los clientes y los servicios. En este archivo
se aplican abstraccion, herencia, polimorfismo, encapsulacion y manejo de excepciones. Adicional a esto 
en este archivo se calculan los costos, operaciones y cancelaciones realizadas de manera correcta.
"""


#Tomamos la clase abstracta que representa las entidades, esto se encuentra en el archivo entidad.py.
#Esto lo necesitamos porque la clase reserva va a heredar de Entidad
from entidad import Entidad

# Tomamos la clase Cliente para validar el objeto cliente, esto se encuentra en el archivo cliente.py.
#Esta clase se necesita para verificar que la reserva se encuentra asociada a un cliente valido.
from cliente import Cliente

# Tomamos la clase Servicio para validar el servicio, esto se encuentra en el archivo servicio.py.
#Tambien lo necesitamos para verificar que el servicio que se quiere reservar sea de servicio del proyecto
from servicio import Servicio

#Tomamos las excepciones que ya existen en excepciones.py.Esto funciona cuando se intenta crear
#una reserva incorrecta y cuando se intenta realizar una operacion que no esta permitida
from excepciones import (
    SoftwareFJError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)

# Importamos las funciones para registrar eventos y errores, es decir guardar las 
# operaciones realizadas y regitra los errores que se presenta
from logger_config import registrar_evento, registrar_error

# Creamos la clase Reserva, que hereda de Entidad.
class Reserva(Entidad):


    #Se crea este contador el cual permite contar cuantas reservas  se han creado
    _contador = 0


    # Cuando se crea una reserva  se ejecuta esta funcion: recibe cliente, servicio y duración.
    def __init__(self, cliente, servicio, duracion):


        # Verificamos que el cliente sea un objeto Cliente. esto es una validacion, si el cliente
        # no es un objeto cliente, el sistema rechaza la operacion.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "El cliente debe ser un objeto de la clase Cliente"
            )


        # Verificamos que el servicio sea un objeto Servicio.
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "El servicio debe ser un objeto de la clase Servicio"
            )

        # Ahora validamos si el servicio es valido
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise ReservaInvalidaError(
                "La duración debe ser un número mayor que cero"
            )


        # Se guarda el cliente asociado a la reserva.
        self._cliente = cliente


        # Se guarda el servicio solicitado.
        self._servicio = servicio


        # Se guarda la duración de la reserva.
        self._duracion = duracion


        # Toda reserva comienza en estado pendiente.
        self._estado = "pendiente"


        # Inicializamos el costo sin calcular.
        self._costo = None


        # Aumentamos el contador de reservas.
        Reserva._contador += 1


        # Creamos el identificador único de la reserva.
        identificador = f"RES-{Reserva._contador:03d}"


        # Llamamos al constructor de la clase Entidad.
        super().__init__(identificador)


        # Registramos la creación de la reserva.
        registrar_evento(
            f"Reserva creada: {self._id}"
        )


    # Método para procesar la reserva.
    def procesar(self):

        # Solo se pueden procesar reservas pendientes.
        if self._estado != "pendiente":
            raise OperacionNoPermitidaError(
                "La reserva no se encuentra pendiente"
            )

        # Intentamos verificar disponibilidad y calcular el costo.
        try:

            # Comprobamos que el servicio esté disponible.
            self._servicio.verificar_disponibilidad()

            # Calculamos el costo utilizando el método seguro.
            costo_calculado = self._servicio.calcular_costo_seguro(
                self._duracion
            )

        # Capturamos cualquier error producido durante el proceso.
        except Exception as error:

            # Registramos el error en el archivo de logs.
            registrar_error(
                f"Error al procesar la reserva {self._id}",
                error
            )
            # Lanzamos una excepción nueva conservando la causa original.
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva"
            ) from error
        # Se ejecuta cuando no ocurrió ningún error.
        else:
            # Se guarda el costo calculado.
            self._costo = costo_calculado

            # Se confirma la reserva.
            self.confirmar()

            # Se informa que el proceso terminó correctamente.
            registrar_evento(
                f"Reserva procesada correctamente: {self._id}"
            )

            # Se devuelve el costo de la reserva.
            return self._costo

        # Se ejecuta siempre, haya ocurrido un error o no.
        finally:

            #Se registra la finalización del procesamiento.
            registrar_evento(
                f"Finalizó el procesamiento de {self._id}"
            )

    # Método para confirmar una reserva.
    def confirmar(self):

        # Solo se puede confirmar si está pendiente.
        if self._estado != "pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes"
            )

        # Se cambia el estado a confirmacion.
        self._estado = "confirmada"

        # Se registra el cambio de estado.
        registrar_evento(
            f"Reserva confirmada: {self._id}"
        )

    # Método para cancelar una reserva.
    def cancelar(self):


        # No se permite cancelar una reserva ya cancelada.
        if self._estado == "cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada"
            )

        # Se cambia el estado a cancelada.
        self._estado = "cancelada"

        # Se registra la cancelación.
        registrar_evento(
            f"Reserva cancelada: {self._id}"
        )

    # Método para mostrar la información de la reserva.
    def mostrar_reserva(self):

        # Se obtiene el costo o se muestra que aún no existe.
        costo_mostrar = (
            f"${self._costo:,.2f}"
            if self._costo is not None
            else "Pendiente de cálculo"
        )

        # Se muestra los datos principales de la reserva.
        print("\n***************INFORMACIÓN DE RESERVA **************")


        # Se muestra el identificador.
        print(f"Identificador: {self._id}")


        # Se muestra los datos del cliente.
        print(f"Cliente: {self._cliente.get_nombre()}")


        # Se muestra el nombre del servicio.
        print(f"Servicio: {self._servicio.get_nombre()}")

        # Se muestra la duración.
        print(f"Duración: {self._duracion}")

        # Se muestra el estado actual.
        print(f"Estado: {self._estado}")

        # Se muestra el costo.
        print(f"Costo: {costo_mostrar}")

        # Se cierra  la presentación.
        print("**************************************")

    # Se implementa el método abstracto de Entidad.
    def describir(self):
        # Se devuelve una descripción de la reserva.
        return (
            f"[{self._id}] "
            f"Cliente: {self._cliente.get_nombre()} | "
            f"Servicio: {self._servicio.get_nombre()} | "
            f"Estado: {self._estado}"
        )
