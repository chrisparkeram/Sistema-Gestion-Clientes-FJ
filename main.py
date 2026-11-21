"""
EJERCICIO 1: SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES,
SERVICIOS Y RESERVAS
Curso: Programación (213023)
Fase: 4
Tema: Programación orientada a objetos y manejo avanzado de excepciones
Autor: Christian Melo Amaya y Eduardo Luis Molina
Descripción: Este archivo es el principal del proyecto Software.FJ. Su funcion es conectar y coordinar
los diferentes modulos del sistema.
En el inicio importa de los demas archivos del programa herramientas necesarias y configurar el registro
de eventos. Luego se ejecuta la funcion simulacion, en donde se realiza 10 pruebas del proyecto.
Este programa utiliza  ciclos For, para recorrer las listas y mostrar los clientes, servicios y reservas registrados,
igualmanera  muestra donde esta el archivo logs, donde quedan guardados los eventos y errores.
"""

# Se importa el módulo os para obtener la ubicacon del archivo log.
import os

# Se improta la función que ejecuta las diez pruebas. este se encuentra en el archivo simulacion.py
from simulacion import ejecutar_simulacion

# Se importa las funciones de configuración del registro. Este se encunetra en el archivo logger_confi
from logger_config import configurar_logger, ARCHIVO_LOG

# Creamos la función principal del proyecto.
def main():

    # Se muestra el encabezado del Programa.
    print("\n*************************************************")
    print(" Software FJ")
    print(" SISTEMA INTEGRAL DE CLIENTES, SERVICIOS Y RESERVAS")
    print("***************************************************")

    # Por medio del try el programa ejecutara instrucciones que se encuentra dentro de este

    try:
        # Se configura el archivo de registros.
        configurar_logger()

        # Se informa que el sistema inició correctamente.
        print("\n*******************")
        print("INICIAMOS PROGRAMA...")
        print("*********************")

        # Se ejecuta las diez pruebas, que realizamos en simulacion.py
        datos = ejecutar_simulacion()

        # Clientes.
        print("\n//////////// CLIENTES REGISTRADOS ///////////////")

        # Recorremos todos los clientes registrados.Recorriendo con el ciclo FOR todos los clientes almacenados en la lista
        for cliente in datos["clientes"]:

            # Se muestra la información de cada cliente.
            print(cliente.describir())

        # Se muestra el título de servicios.
        print("\n///////////////SERVICIOS REGISTRADOS////////////////")

        # Se recorre todos los servicios registrados.
        for servicio in datos["servicios"]:


            # Se muestra la descripción de cada servicio.
            print(servicio.describir())

        # Se muestra el título de reservas.
        print("\n**************** RESERVAS REGISTRADAS *****************")

        # Se muestra todas las reservas registradas.
        for reserva in datos["reservas"]:

            # Se muestra la descripción de cada reserva.
            print(reserva.describir())

        # Se muestra el mensaje de finalización del programa.
        print("\n*******************************")
        print(" EJECUCIÓN DEL SISTEMA FINALIZADA")
        print("**********************************")

        # Se indica la ubicación del archivo de registros.
        print("\nArchivo de registros generado:")

        # Se muestra la ruta completa del archivo log. este se encuentra en logger_config.py
        print(os.path.abspath(ARCHIVO_LOG))

        #Este codigo captura excepciones que estan dentro de las instrucciones  protegida por el try.
    except Exception as error:
        # validacion de error inesperado del programa.
        print(f"\nError general del sistema: {error}")

        # Se registra el error en el archivo de logs.
        from logger_config import registrar_error

        # Se guarda el detalle del error.
        registrar_error(
            "Error general durante la ejecución de main",
            error
        )
     # Se verifica que el archivo se ejecute directamente.
if __name__ == "__main__":

    # Se ejecuta la función principal.
    main()
