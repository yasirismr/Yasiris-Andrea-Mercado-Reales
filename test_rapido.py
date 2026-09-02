"""
test_rapido.py
----------------
Prueba rápida del pipeline completo con una matriz reducida
(1.000 x 1.000 en vez de 100.000 x 100.000), para validar que todo
funciona en segundos antes de correr la versión completa (que puede
tardar varios minutos y ocupar ~9.3 GB en disco).

No modifica config.py: sobreescribe los valores en memoria solo para
esta ejecución.

Ejecutar con:
    python test_rapido.py
"""

from src import config

# Sobrescribimos las dimensiones ANTES de importar los módulos que las usan,
# para que todos los cálculos (TAM_REGISTRO, etc.) se hagan con el tamaño chico.
config.FILAS = 1_000
config.COLUMNAS = 1_000
config.TAM_REGISTRO = config.COLUMNAS * config.BYTES_POR_CELDA
config.FILENAME = config.FILENAME.replace("matriz_gigante.dat", "matriz_prueba.dat")

from src.matrix_writer import crear_matriz          # noqa: E402
from src.matrix_reader import mostrar_muestra        # noqa: E402
from src.verify import verificar_todo                 # noqa: E402

if __name__ == "__main__":
    print(f"Probando con matriz reducida: {config.FILAS} x {config.COLUMNAS}\n")
    crear_matriz()
    verificar_todo()
    mostrar_muestra()
