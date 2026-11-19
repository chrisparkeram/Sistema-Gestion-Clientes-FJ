"""
Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Curso: Programación (213023) - Fase 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Christian Melo Amaya y Eduardo Luis Flores Molina

Configura el archivo de registro (software_fj.log) donde queda anotado cada
evento importante y cada error del sistema. Ofrece tres funciones:
configurar_logger, registrar_evento y registrar_error. Lo usan todos los demás módulos.
"""
import logging  # módulo estándar de Python para escribir logs

NOMBRE_LOGGER = "software_fj"  # nombre interno del logger
ARCHIVO_LOG = "software_fj.log"  # archivo donde se guardan los registros


def configurar_logger(archivo=ARCHIVO_LOG):
    """Crea (o reutiliza) el logger que escribe en un archivo de texto."""
    logger = logging.getLogger(NOMBRE_LOGGER)  # obtiene el logger por nombre
    logger.setLevel(logging.DEBUG)  # registra todos los niveles
    if not logger.handlers:  # evita duplicar líneas si ya está configurado
        manejador = logging.FileHandler(archivo, encoding="utf-8")  # escribe en el archivo
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # fecha | nivel | mensaje
        manejador.setFormatter(formato)  # aplica el formato al manejador
        logger.addHandler(manejador)  # conecta el manejador al logger
    return logger  # devuelve el logger listo para usar


def registrar_evento(mensaje):
    """Anota un evento normal (por ejemplo, una reserva confirmada)."""
    configurar_logger().info(mensaje)  # nivel INFO


def registrar_error(mensaje, excepcion=None):
    """Anota un error; si hay excepción, agrega su tipo y su causa encadenada."""
    if excepcion is not None:  # si nos pasan la excepción original
        mensaje = f"{mensaje} | {type(excepcion).__name__}: {excepcion}"  # agrega tipo y texto
        if excepcion.__cause__ is not None:  # si el error venía encadenado (raise ... from ...)
            mensaje += f" | causa: {type(excepcion.__cause__).__name__}: {excepcion.__cause__}"  # agrega la causa
    configurar_logger().error(mensaje)  # nivel ERROR
