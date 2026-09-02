"""
config.py
---------
Parámetros centrales del laboratorio. Todo el proyecto lee de aquí,
así que para cambiar el tamaño de la matriz o el comportamiento del
buffer, solo hay que tocar este archivo.
"""

import os

# ----------------------------------------------------------------------
# Dimensiones de la matriz
# ----------------------------------------------------------------------
FILAS = 100_000
COLUMNAS = 100_000

# Cada celda se guarda como 1 byte (entero sin signo 0-255).
# Con float64 (8 bytes/celda) la matriz pesaría ~80 TB -> inviable.
# Con 1 byte/celda pesa ~9.31 GB -> cabe en un disco normal.
BYTES_POR_CELDA = 1

# Tamaño de un "registro" = una fila completa. Es FIJO: todas las filas
# ocupan siempre lo mismo en disco. Esto es lo que permite el acceso
# directo (random access) por cálculo de posición en vez de recorrer
# el archivo secuencialmente.
TAM_REGISTRO = COLUMNAS * BYTES_POR_CELDA

# ----------------------------------------------------------------------
# Nombre y ubicación del archivo de datos
# ----------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
FILENAME = os.path.join(DATA_DIR, "matriz_gigante.dat")

# ----------------------------------------------------------------------
# Tamaño del buffer de escritura (soluciona "escritura lenta a disco")
# ----------------------------------------------------------------------
# En vez de hacer f.write() una vez por cada fila (100.000 llamadas al
# sistema operativo, muy lento por la sobrecarga de cada syscall),
# acumulamos varias filas en memoria y las escribimos juntas.
#
# FILAS_POR_BLOQUE = 2000  ->  2000 * 100.000 bytes = ~190 MB por bloque
# Esto es un punto intermedio seguro entre:
#   - Consumo de RAM (no cargamos las 100.000 filas, solo 2000)
#   - Velocidad de escritura (pocas llamadas grandes en vez de muchas pequeñas)
FILAS_POR_BLOQUE = 2000

# Valor de relleno por defecto para las celdas (puede sobrescribirse)
VALOR_RELLENO = 7
