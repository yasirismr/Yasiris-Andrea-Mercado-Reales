"""
main.py
--------
Laboratorio 1 - Estructuras de Datos
Punto de entrada del proyecto: crea la matriz de 100.000 x 100.000
en disco, la verifica y muestra una muestra representativa de su
contenido (el entregable del laboratorio).

Ejecutar desde la raíz del repositorio con:
    python main.py
"""

import os
import shutil

from src import config
from src.matrix_writer import crear_matriz
from src.matrix_reader import mostrar_muestra, MatrizMemoryMapped
from src.verify import verificar_todo


def verificar_espacio_disco() -> None:
    """Chequea que haya espacio libre suficiente antes de escribir ~9.3 GB."""
    total, usado, libre = shutil.disk_usage(os.path.dirname(config.DATA_DIR) or ".")
    libre_gb = libre / (1024 ** 3)
    necesario_gb = (config.FILAS * config.TAM_REGISTRO) / (1024 ** 3)

    print(f"Espacio libre en disco: {libre_gb:.2f} GB")
    print(f"Espacio necesario:      {necesario_gb:.2f} GB")

    if libre_gb < necesario_gb * 1.1:  # margen de seguridad del 10%
        print("\nADVERTENCIA: puede que no haya suficiente espacio libre.")
        print("Considera reducir config.FILAS / config.COLUMNAS para probar primero.")


def demo_mmap() -> None:
    """Muestra el uso del lector con memory-mapped file para acceso puntual rápido."""
    print("\n--- Demo de acceso con mmap ---")
    centro = config.FILAS // 2
    ultima = config.FILAS - 1
    with MatrizMemoryMapped() as m:
        print("Celda (0, 0):", m.obtener_celda(0, 0))
        print(f"Celda ({centro}, {centro}):", m.obtener_celda(centro, centro))
        print(f"Celda ({ultima}, {ultima}):", m.obtener_celda(ultima, ultima))


def main() -> None:
    print("=" * 60)
    print("LABORATORIO 1 - MATRIZ 100.000 x 100.000 EN DISCO")
    print("=" * 60)

    verificar_espacio_disco()

    print("\nPaso 1: creando la matriz en disco...")
    crear_matriz()

    print("\nPaso 2: verificando integridad del archivo generado...")
    verificar_todo()

    print("\nPaso 3: mostrando la matriz creada (entregable)...")
    mostrar_muestra()

    demo_mmap()


if __name__ == "__main__":
    main()
