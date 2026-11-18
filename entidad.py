"""
Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación (213023) - Fase 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Christian Melo Amaya

Define la clase abstracta Entidad (abstracción). Es la base de Cliente,
Servicio y Reserva: toda entidad tiene un id y debe implementar describir().
"""
from abc import ABC, abstractmethod  # herramientas para crear clases abstractas


class Entidad(ABC):
    """Base de Cliente y Servicio: toda entidad tiene un id y sabe describirse."""

    def __init__(self, identificador):
        self._id = identificador  # identificador único (atributo privado por convención)

    def get_id(self):
        """Devuelve el identificador de la entidad."""
        return self._id  # solo lectura: no hay set_id a propósito

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe devolver su descripción en texto."""

    def __str__(self):
        return self.describir()  # al imprimir el objeto se muestra su descripción
