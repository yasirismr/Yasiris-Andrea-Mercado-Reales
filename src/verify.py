"""
verify.py
----------
Verifica que el archivo generado sea correcto y consistente, sin
necesidad de leerlo completo en memoria.

Comprobaciones realizadas:
  1. El tamaño del archivo en disco coincide EXACTAMENTE con el
     tamaño esperado (FILAS * TAM_REGISTRO). Esto confirma que la
     matriz tiene de verdad 100.000 x 100.000 elementos, y no una
     versión truncada o incompleta.
  2. Una muestra de filas (inicio, medio, fin y varias aleatorias)
     tiene el largo correcto (TAM_REGISTRO bytes) y el valor esperado
     en sus celdas, usando acceso directo (sin leer filas de más).
  3. Reporta cualquier inconsistencia encontrada.
"""

import os
import random

from . import config
from .matrix_reader import leer_fila_seek


def verificar_tamano_archivo() -> bool:
    tamano_esperado = config.FILAS * config.TAM_REGISTRO
    tamano_real = os.path.getsize(config.FILENAME)

    print("Verificación de tamaño:")
    print(f"  Esperado: {tamano_esperado:,} bytes ({tamano_esperado / (1024**3):.2f} GB)")
    print(f"  Real:     {tamano_real:,} bytes ({tamano_real / (1024**3):.2f} GB)")

    ok = tamano_esperado == tamano_real
    print(f"  Resultado: {'OK' if ok else 'FALLA - tamaños no coinciden'}")
    return ok


def verificar_filas(valor_esperado: int, n_muestras: int = 20) -> bool:
    """
    Revisa varias filas (fijas + aleatorias) para confirmar:
      - que cada registro leído mide exactamente TAM_REGISTRO bytes
      - que las celdas contienen el valor esperado
    Se hace por muestreo (no fila por fila) porque revisar las 100.000
    filas completas sería lento y, para este laboratorio, innecesario:
    una muestra representativa ya detecta errores de escritura.
    """
    indices = {0, config.FILAS // 2, config.FILAS - 1}
    indices.update(random.sample(range(config.FILAS), min(n_muestras, config.FILAS)))

    print(f"\nVerificación de contenido ({len(indices)} filas muestreadas):")
    todo_ok = True
    for idx in sorted(indices):
        fila = leer_fila_seek(idx)
        largo_ok = len(fila) == config.TAM_REGISTRO
        valores_ok = all(b == valor_esperado for b in fila)
        estado = "OK" if (largo_ok and valores_ok) else "FALLA"
        if estado == "FALLA":
            todo_ok = False
        print(f"  Fila {idx:>7}: largo={len(fila)} valores_correctos={valores_ok} -> {estado}")

    return todo_ok


def verificar_todo(valor_esperado: int = config.VALOR_RELLENO) -> None:
    print("=" * 60)
    print("VERIFICACIÓN DEL ARCHIVO GENERADO")
    print("=" * 60)

    if not os.path.exists(config.FILENAME):
        print(f"ERROR: no existe el archivo {config.FILENAME}. Corre matrix_writer.py primero.")
        return

    ok_tamano = verificar_tamano_archivo()
    ok_filas = verificar_filas(valor_esperado)

    print("\n" + "=" * 60)
    if ok_tamano and ok_filas:
        print("RESULTADO FINAL: el archivo es válido y consistente.")
    else:
        print("RESULTADO FINAL: se encontraron inconsistencias, revisar arriba.")
    print("=" * 60)


if __name__ == "__main__":
    verificar_todo()
