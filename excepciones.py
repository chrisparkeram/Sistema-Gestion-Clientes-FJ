"""
Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación (213023) - Fase 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Christian Melo Amaya

Define las excepciones personalizadas del sistema. Todas heredan de
SoftwareFJError y se anotan solas en el log al crearse. Cubren datos inválidos,
parámetros faltantes, servicios no disponibles, reservas incorrectas,
operaciones no permitidas y cálculos inconsistentes.
"""
from logger_config import registrar_error  # cada error creado queda registrado en el log


class SoftwareFJError(Exception):
    """Excepción base: todas las demás heredan de ella."""

    def __init__(self, mensaje):
        super().__init__(mensaje)  # guarda el mensaje en la excepción
        registrar_error(f"{type(self).__name__}: {mensaje}")  # lo anota en el archivo de logs


class ClienteInvalidoError(SoftwareFJError):
    """Datos de cliente inválidos (nombre, documento o correo)."""


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros de servicio inválidos (precio negativo, nombre vacío, etc.)."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se intentó usar un servicio que no está disponible."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio (llegó None)."""


class ReservaInvalidaError(SoftwareFJError):
    """Intento de reserva incorrecto (datos de la reserva inválidos)."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación no permitida (por ejemplo, cancelar una reserva ya cancelada)."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de costos dio un resultado inconsistente o no pudo hacerse."""
