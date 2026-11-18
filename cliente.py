"""
Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación (213023) - Fase 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Christian Melo Amaya

Define la clase Cliente (encapsulación): sus datos personales son privados y
se manejan con getters, setters y validaciones robustas de nombre, documento
y correo. Hereda de Entidad.
"""
import re  # expresiones regulares para validar nombre y correo

from entidad import Entidad  # clase abstracta de la que hereda
from excepciones import ClienteInvalidoError, ParametroFaltanteError  # errores propios
from logger_config import registrar_evento  # para anotar eventos

PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+( [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$")  # solo letras y espacios
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")  # algo@dominio.ext


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos son privados y solo se cambian validados."""

    _contador = 0  # cuenta los clientes creados para generar ids

    def __init__(self, nombre, documento, correo):
        self._nombre = None  # se declaran privados; los setters los validan
        self._documento = None
        self._correo = None
        self.set_nombre(nombre)  # valida y guarda el nombre
        self.set_documento(documento)  # valida y guarda el documento
        self.set_correo(correo)  # valida y guarda el correo
        Cliente._contador += 1  # solo se cuenta si todo fue válido
        super().__init__(f"CLI-{Cliente._contador:03d}")  # id tipo CLI-001
        registrar_evento(f"Cliente creado: {self._id} - {self._nombre}")  # deja rastro en el log

    # ---------- getters y setters ----------
    def get_nombre(self):
        return self._nombre  # devuelve el nombre

    def set_nombre(self, nombre):
        self.validar_nombre(nombre)  # si no es válido, lanza error y no guarda
        self._nombre = nombre.strip()  # guarda sin espacios sobrantes

    def get_documento(self):
        return self._documento  # devuelve el documento

    def set_documento(self, documento):
        self.validar_documento(documento)  # valida antes de guardar
        self._documento = str(documento).strip()  # se guarda como texto

    def get_correo(self):
        return self._correo  # devuelve el correo

    def set_correo(self, correo):
        self.validar_correo(correo)  # valida antes de guardar
        self._correo = correo.strip().lower()  # el correo se guarda en minúscula

    # ---------- validaciones ----------
    def validar_nombre(self, nombre):
        """El nombre debe ser texto con solo letras y espacios (mínimo 2 letras)."""
        if nombre is None:  # parámetro faltante
            raise ParametroFaltanteError("El nombre del cliente es obligatorio")
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:  # tipo y largo
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 2 letras")
        if not PATRON_NOMBRE.match(nombre.strip()):  # solo letras y espacios
            raise ClienteInvalidoError(f"El nombre '{nombre}' contiene caracteres no permitidos")

    def validar_documento(self, documento):
        """El documento debe tener solo dígitos, entre 5 y 12."""
        if documento is None:  # parámetro faltante
            raise ParametroFaltanteError("El documento del cliente es obligatorio")
        texto = str(documento).strip()  # acepta número o texto
        if not (texto.isascii() and texto.isdigit()):  # solo 0-9
            raise ClienteInvalidoError(f"El documento '{texto}' debe contener solo números")
        if not 5 <= len(texto) <= 12:  # largo razonable
            raise ClienteInvalidoError("El documento debe tener entre 5 y 12 dígitos")

    def validar_correo(self, correo):
        """El correo debe tener formato usuario@dominio.ext."""
        if correo is None:  # parámetro faltante
            raise ParametroFaltanteError("El correo del cliente es obligatorio")
        if not isinstance(correo, str) or not PATRON_CORREO.match(correo.strip()):  # formato
            raise ClienteInvalidoError(f"El correo '{correo}' no tiene un formato válido")

    # ---------- presentación ----------
    def describir(self):
        """Texto con los datos del cliente (implementa el método abstracto)."""
        return f"[{self._id}] {self._nombre} | Doc: {self._documento} | Correo: {self._correo}"

    def mostrar_datos(self):
        """Imprime los datos del cliente en pantalla."""
        print(self.describir())
