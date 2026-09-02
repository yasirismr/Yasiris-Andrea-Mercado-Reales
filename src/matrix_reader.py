"""
matrix_reader.py
------------------
Lee la matriz creada en disco sin cargarla completa en memoria.

Ofrece dos estrategias de lectura, ambas O(1) respecto al tamaño de
la matriz (no dependen de cuántas filas tenga el archivo):

1) ACCESO DIRECTO CLÁSICO (seek + read)
   Se calcula la posición exacta de una fila con:
       posicion = indice_fila * TAM_REGISTRO
   y se salta directo ahí con f.seek(posicion), sin leer las filas
   anteriores. Es el mecanismo clásico de "registros de longitud fija"
   de Estructuras de Datos.

2) MEMORY-MAPPED FILE (mmap)
   El módulo mmap del sistema operativo "mapea" el archivo de disco
   como si fuera un bloque de memoria, pero el sistema operativo solo
   trae a RAM las páginas (fragmentos) que realmente se consultan, y
   las libera automáticamente si hace falta memoria. Esto da acceso
   aleatorio muy rápido sin que nosotros administremos manualmente
   buffers ni posiciones, y sin el riesgo de cargar el archivo completo.
"""

import mmap
import os

from . import config


def leer_fila_seek(indice_fila: int) -> bytes:
    """
    Lee una fila usando acceso directo clásico (seek + read).

    Solo se leen TAM_REGISTRO bytes del disco, sin importar si la
    fila pedida es la primera o la última de la matriz: el costo es
    siempre el mismo (acceso directo, no secuencial).
    """
    if not (0 <= indice_fila < config.FILAS):
        raise IndexError(f"Fila fuera de rango: {indice_fila}")

    with open(config.FILENAME, "rb") as f:
        posicion = indice_fila * config.TAM_REGISTRO
        f.seek(posicion)
        return f.read(config.TAM_REGISTRO)


def leer_celda_seek(fila: int, columna: int) -> int:
    """
    Lee una única celda (fila, columna) sin leer la fila completa.

    Esto lleva el acceso directo un paso más allá: no solo saltamos
    a la fila correcta, sino directamente al byte exacto de la celda.
    """
    if not (0 <= fila < config.FILAS) or not (0 <= columna < config.COLUMNAS):
        raise IndexError(f"Celda fuera de rango: ({fila}, {columna})")

    with open(config.FILENAME, "rb") as f:
        posicion = fila * config.TAM_REGISTRO + columna * config.BYTES_POR_CELDA
        f.seek(posicion)
        return f.read(config.BYTES_POR_CELDA)[0]


class MatrizMemoryMapped:
    """
    Envuelve el archivo con mmap para dar acceso tipo matriz[fila][columna]
    con muy baja latencia y sin cargar el archivo completo en RAM.

    Uso recomendado con 'with' para asegurar que se cierra el mapeo:

        with MatrizMemoryMapped() as m:
            valor = m.obtener_celda(50_000, 50_000)
            fila = m.obtener_fila(0)
    """

    def __init__(self):
        self._file = open(config.FILENAME, "r+b")
        self._mmap = mmap.mmap(self._file.fileno(), 0)  # 0 = mapear el archivo completo

    def obtener_fila(self, indice_fila: int) -> bytes:
        inicio = indice_fila * config.TAM_REGISTRO
        fin = inicio + config.TAM_REGISTRO
        return self._mmap[inicio:fin]

    def obtener_celda(self, fila: int, columna: int) -> int:
        pos = fila * config.TAM_REGISTRO + columna * config.BYTES_POR_CELDA
        return self._mmap[pos]

    def escribir_celda(self, fila: int, columna: int, valor: int) -> None:
        pos = fila * config.TAM_REGISTRO + columna * config.BYTES_POR_CELDA
        self._mmap[pos] = valor

    def close(self):
        self._mmap.flush()
        self._mmap.close()
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def mostrar_muestra(n_filas: int = 5, n_cols: int = 10) -> None:
    """
    Entregable del laboratorio: 'mostrar' la matriz creada.

    Imprimir los 10.000 millones de valores es inviable (tardaría horas
    y no aportaría nada legible). En su lugar se muestra:
      - Las dimensiones y tamaño reales del archivo.
      - Una muestra representativa (esquina superior izquierda).
      - Una fila del centro y una del final, leídas por acceso directo,
        para demostrar que TODA la matriz existe, no solo el inicio.
    """
    tamano = os.path.getsize(config.FILENAME)
    print("=== Matriz creada en disco ===")
    print(f"Dimensiones: {config.FILAS:,} filas x {config.COLUMNAS:,} columnas")
    print(f"Total de elementos: {config.FILAS * config.COLUMNAS:,}")
    print(f"Tamaño en disco: {tamano / (1024 ** 3):.2f} GB")

    print(f"\nMuestra (primeras {n_filas} filas, primeras {n_cols} columnas):")
    for i in range(n_filas):
        fila = leer_fila_seek(i)
        print(f"  Fila {i}: {list(fila[:n_cols])} ...")

    fila_centro = config.FILAS // 2
    fila_final = config.FILAS - 1
    print(f"\nFila del centro ({fila_centro}): {list(leer_fila_seek(fila_centro)[:n_cols])} ...")
    print(f"Última fila     ({fila_final}): {list(leer_fila_seek(fila_final)[:n_cols])} ...")


if __name__ == "__main__":
    mostrar_muestra()
