"""
matrix_writer.py
-----------------
Crea la matriz de FILAS x COLUMNAS directamente en disco duro.

Problemas que resuelve y cómo:

1) CONSUMO EXCESIVO DE RAM
   No se crea nunca un arreglo con las 10.000.000.000 celdas en
   memoria (eso pediría del orden de ~9-80 GB de RAM según el tipo
   de dato, y colapsaría casi cualquier equipo). En su lugar, se
   mantiene en RAM solo un BLOQUE de filas a la vez (ver
   config.FILAS_POR_BLOQUE), se escribe ese bloque a disco y se
   descarta antes de generar el siguiente.

2) ESCRITURA LENTA A DISCO
   Escribir fila por fila (100.000 llamadas a f.write) es lento
   porque cada llamada implica una transición al sistema operativo
   (syscall) con su propia sobrecarga. Aquí se agrupan varias filas
   en un solo objeto de bytes (un "bloque") y se hace UNA escritura
   por bloque, reduciendo drásticamente el número de syscalls.
   Además:
     - Se preasigna el tamaño final del archivo con ftruncate/
       posix_fallocate antes de escribir, para que el sistema de
       archivos reserve el espacio de una sola vez y no tenga que
       ir agrandando el archivo fragmento a fragmento.
     - Se abre el archivo en modo binario con buffering explícito.

3) OPTIMIZACIÓN DE MANIPULACIÓN / CREACIÓN / ALMACENAMIENTO
   - Se usan "registros de longitud fija": cada fila mide siempre
     TAM_REGISTRO bytes. Esto permite luego calcular la posición de
     cualquier fila con una simple multiplicación (indice * TAM_REGISTRO),
     sin tener que leer el archivo para saber dónde empieza cada fila.
   - Los bloques se generan con bytes(...) que crea el buffer en una
     sola operación de bajo nivel, en vez de construirlo elemento por
     elemento con listas o bucles de Python (mucho más lento).
"""

import os
import time

from . import config


def _preasignar_archivo(ruta: str, tamano_bytes: int) -> None:
    """
    Reserva el espacio total del archivo en disco de una sola vez.

    Esto evita que el sistema de archivos tenga que ir extendiendo el
    archivo fragmento a fragmento en cada escritura (lo cual fragmenta
    el archivo en disco y hace la escritura y lectura posterior más
    lentas). Es el equivalente a "avisarle al disco" cuánto espacio
    necesitaremos antes de empezar a llenarlo.
    """
    with open(ruta, "wb") as f:
        f.truncate(tamano_bytes)
        if hasattr(os, "posix_fallocate"):
            # posix_fallocate reserva espacio físico real (no solo lógico),
            # lo que reduce la fragmentación en sistemas Linux/Mac.
            try:
                os.posix_fallocate(f.fileno(), 0, tamano_bytes)
            except OSError:
                # Algunos sistemas de archivos (p.ej. algunos montajes de red)
                # no soportan fallocate; el truncate ya deja el archivo listo.
                pass


def crear_matriz(valor: int = config.VALOR_RELLENO, mostrar_progreso: bool = True) -> None:
    """
    Crea la matriz completa en disco, bloque por bloque.

    Parameters
    ----------
    valor : int
        Valor (0-255) con el que se llena cada celda.
    mostrar_progreso : bool
        Si True, imprime avance cada cierto número de filas.
    """
    os.makedirs(config.DATA_DIR, exist_ok=True)

    tamano_total = config.FILAS * config.TAM_REGISTRO
    _preasignar_archivo(config.FILENAME, tamano_total)

    # Un bloque = varias filas idénticas concatenadas. Se genera UNA sola
    # vez y se reutiliza para todos los bloques (no se reconstruye en
    # cada iteración), ahorrando tiempo de CPU.
    filas_por_bloque = config.FILAS_POR_BLOQUE
    bloque = bytes([valor]) * (config.TAM_REGISTRO * filas_por_bloque)

    inicio = time.time()

    with open(config.FILENAME, "r+b", buffering=1024 * 1024) as f:  # buffer de E/S de 1 MB
        fila_actual = 0
        while fila_actual < config.FILAS:
            filas_restantes = config.FILAS - fila_actual
            if filas_restantes >= filas_por_bloque:
                f.write(bloque)
                fila_actual += filas_por_bloque
            else:
                # Último bloque, puede ser más pequeño que el resto
                bloque_final = bytes([valor]) * (config.TAM_REGISTRO * filas_restantes)
                f.write(bloque_final)
                fila_actual += filas_restantes

            if mostrar_progreso and fila_actual % (filas_por_bloque * 5) == 0:
                pct = (fila_actual / config.FILAS) * 100
                print(f"  Progreso: {fila_actual:,}/{config.FILAS:,} filas ({pct:.1f}%)")

        f.flush()
        os.fsync(f.fileno())  # fuerza la escritura física a disco antes de continuar

    duracion = time.time() - inicio
    tamano_real = os.path.getsize(config.FILENAME)

    print("\nMatriz creada correctamente.")
    print(f"  Archivo: {config.FILENAME}")
    print(f"  Tiempo total: {duracion:.2f} s")
    print(f"  Tamaño en disco: {tamano_real / (1024 ** 3):.2f} GB")
    print(f"  Velocidad promedio: {(tamano_real / (1024 ** 2)) / duracion:.1f} MB/s")


if __name__ == "__main__":
    crear_matriz()
