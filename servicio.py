"""
Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación (213023) - Fase 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Christian Melo Amaya y Eduardo Luis Flores Molina

Define la clase abstracta Servicio y sus tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada (herencia y polimorfismo).
Cada hija sobrescribe calcular_costo, describir y validar_parametros.
calcular_costo tiene parámetros opcionales de impuesto y descuento (sobrecarga),
y calcular_costo_seguro usa try/except/else/finally con encadenamiento.
"""
from abc import abstractmethod  # para marcar métodos que los hijos deben implementar

from entidad import Entidad  # Servicio es una Entidad
from excepciones import (  # errores propios que usa este módulo
    SoftwareFJError, ServicioInvalidoError, ServicioNoDisponibleError,
    ParametroFaltanteError, CalculoInconsistenteError,
)
from logger_config import registrar_evento  # para anotar eventos


def es_numero(valor):
    """True si es int o float (y no un booleano)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


class Servicio(Entidad):
    """Clase abstracta: define lo que todo servicio debe saber hacer."""

    _contador = 0  # cuenta los servicios creados para generar ids

    def __init__(self, nombre, precio_base, disponible=True):
        self._nombre = nombre  # nombre del servicio
        self._precio_base = precio_base  # tarifa por unidad de tiempo
        self._disponible = disponible  # si se puede reservar
        self.validar_parametros()  # cada hijo agrega sus propias validaciones
        Servicio._contador += 1  # solo se cuenta si todo fue válido
        super().__init__(f"SRV-{Servicio._contador:03d}")  # id tipo SRV-001
        registrar_evento(f"Servicio creado: {self._id} - {self._nombre}")  # rastro en el log

    # ---------- métodos abstractos (los hijos los sobrescriben) ----------
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """Calcula el costo. Sobrecargado con parámetros opcionales:
        calcular_costo(2) | calcular_costo(2, impuesto=0.19) | calcular_costo(2, descuento=0.1)."""

    @abstractmethod
    def validar_parametros(self):
        """Validaciones comunes; los hijos la extienden con super().validar_parametros()."""
        if self._nombre is None or self._precio_base is None:  # faltantes
            raise ParametroFaltanteError("El servicio requiere nombre y precio base")
        if not isinstance(self._nombre, str) or not self._nombre.strip():  # nombre vacío
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío")
        if not es_numero(self._precio_base) or self._precio_base <= 0:  # precio positivo
            raise ServicioInvalidoError(f"El precio base debe ser un número mayor a 0 (recibido: {self._precio_base})")
        if not isinstance(self._disponible, bool):  # disponibilidad booleana
            raise ServicioInvalidoError("La disponibilidad debe ser True o False")

    # ---------- métodos comunes ----------
    def describir(self):
        """Descripción base; los hijos la amplían."""
        estado = "disponible" if self._disponible else "NO disponible"  # texto del estado
        return f"[{self._id}] {self._nombre} | base: ${self._precio_base:,.2f} | {estado}"

    def get_nombre(self):
        return self._nombre  # nombre del servicio

    def get_precio_base(self):
        return self._precio_base  # tarifa base

    def esta_disponible(self):
        return self._disponible  # True o False

    def set_disponible(self, disponible):
        if not isinstance(disponible, bool):  # validación
            raise ServicioInvalidoError("La disponibilidad debe ser True o False")
        self._disponible = disponible  # actualiza el estado

    def verificar_disponibilidad(self):
        """Lanza error si el servicio no se puede reservar (lo usa Reserva)."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no está disponible")

    def _validar_duracion(self, duracion):
        """La duración debe ser un número mayor a 0."""
        if duracion is None:  # parámetro faltante
            raise ParametroFaltanteError("La duración es obligatoria")
        if not es_numero(duracion) or duracion <= 0:  # positiva
            raise ServicioInvalidoError(f"La duración debe ser un número mayor a 0 (recibido: {duracion})")

    def _aplicar_ajustes(self, subtotal, impuesto, descuento):
        """Aplica descuento e impuesto al subtotal y revisa que el resultado sea coherente."""
        if not es_numero(impuesto) or not 0 <= impuesto <= 1:  # impuesto entre 0 y 1
            raise CalculoInconsistenteError(f"Impuesto inválido: {impuesto} (use un valor entre 0 y 1)")
        if not es_numero(descuento) or not 0 <= descuento < 1:  # descuento entre 0 y 1
            raise CalculoInconsistenteError(f"Descuento inválido: {descuento} (use un valor entre 0 y 1)")
        total = subtotal * (1 - descuento) * (1 + impuesto)  # primero descuento, luego impuesto
        if total <= 0:  # un costo nunca debe ser 0 o negativo
            raise CalculoInconsistenteError(f"El costo calculado es inconsistente: {total}")
        return round(total, 2)  # redondea a 2 decimales

    def calcular_costo_seguro(self, duracion, impuesto=0.0, descuento=0.0):
        """Calcula el costo capturando errores (try/except/else/finally + encadenamiento)."""
        try:
            costo = self.calcular_costo(duracion, impuesto, descuento)  # intenta calcular
        except SoftwareFJError as error:  # si algo falla...
            raise CalculoInconsistenteError(  # ...lo encadena con "from" para conservar la causa
                f"No se pudo calcular el costo de '{self._nombre}'") from error
        else:  # se ejecuta solo si NO hubo error
            registrar_evento(f"Costo calculado para {self._id}: ${costo:,.2f}")
            return costo
        finally:  # se ejecuta siempre
            registrar_evento(f"Fin del cálculo de costo para {self._id}")


class ReservaSala(Servicio):
    """Reserva de salas: se cobra por hora."""

    def __init__(self, nombre, precio_base, capacidad, disponible=True):
        self._capacidad = capacidad  # personas que caben (se guarda antes de validar)
        super().__init__(nombre, precio_base, disponible)  # el padre valida y asigna id

    def validar_parametros(self):
        super().validar_parametros()  # validaciones comunes
        if not isinstance(self._capacidad, int) or isinstance(self._capacidad, bool) or self._capacidad <= 0:
            raise ServicioInvalidoError(f"La capacidad debe ser un entero mayor a 0 (recibido: {self._capacidad})")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        self._validar_duracion(duracion)  # duración en horas
        subtotal = self._precio_base * duracion  # tarifa por hora
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return f"{super().describir()} | Sala para {self._capacidad} personas (por hora)"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por día más un depósito fijo."""

    def __init__(self, nombre, precio_base, tipo_equipo, deposito=0, disponible=True):
        self._tipo_equipo = tipo_equipo  # ej. "Portátil", "Proyector"
        self._deposito = deposito  # valor fijo que se suma al alquiler
        super().__init__(nombre, precio_base, disponible)

    def validar_parametros(self):
        super().validar_parametros()  # validaciones comunes
        if not isinstance(self._tipo_equipo, str) or not self._tipo_equipo.strip():
            raise ServicioInvalidoError("El tipo de equipo no puede estar vacío")
        if not es_numero(self._deposito) or self._deposito < 0:
            raise ServicioInvalidoError(f"El depósito debe ser un número mayor o igual a 0 (recibido: {self._deposito})")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        self._validar_duracion(duracion)  # duración en días
        if int(duracion) != duracion:  # los días deben ser enteros
            raise ServicioInvalidoError("Los días de alquiler deben ser un número entero")
        subtotal = self._precio_base * duracion + self._deposito  # tarifa diaria + depósito
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return f"{super().describir()} | Equipo: {self._tipo_equipo}, depósito ${self._deposito:,.2f} (por día)"


class AsesoriaEspecializada(Servicio):
    """Asesorías: se cobra por sesión, con recargo si el asesor es senior."""

    RECARGO_SENIOR = 0.25  # 25% extra por asesor senior
    NIVELES = ("junior", "senior")  # niveles permitidos

    def __init__(self, nombre, precio_base, especialidad, nivel="junior", disponible=True):
        self._especialidad = especialidad  # ej. "Ciberseguridad"
        self._nivel = nivel  # "junior" o "senior"
        super().__init__(nombre, precio_base, disponible)

    def validar_parametros(self):
        super().validar_parametros()  # validaciones comunes
        if not isinstance(self._especialidad, str) or not self._especialidad.strip():
            raise ServicioInvalidoError("La especialidad no puede estar vacía")
        if self._nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"El nivel debe ser uno de {self.NIVELES} (recibido: {self._nivel})")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        self._validar_duracion(duracion)  # duración en sesiones
        subtotal = self._precio_base * duracion  # tarifa por sesión
        if self._nivel == "senior":  # recargo para asesores senior
            subtotal *= 1 + self.RECARGO_SENIOR
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return f"{super().describir()} | Asesoría de {self._especialidad}, nivel {self._nivel} (por sesión)"
