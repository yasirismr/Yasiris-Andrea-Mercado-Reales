# Laboratorio 1 — Matriz de 100.000 x 100.000 en disco duro

**Estudiante:** [ESCRIBE AQUÍ TU NOMBRE COMPLETO]
**Curso:** Estructuras de Datos y Laboratorios
**Profesor:** Diego

## Enunciado

Escribir una matriz de 100.000 x 100.000 en disco duro.
Entregable: mostrar la matriz creada.

## Objetivo de esta solución

No basta con "que funcione": el código debe resolver explícitamente tres
problemas técnicos de escala:

1. **Consumo excesivo de RAM.**
2. **Escritura lenta a disco.**
3. **Optimización en la manipulación, creación, almacenamiento y lectura de datos.**

La matriz completa tiene `100.000 × 100.000 = 10.000.000.000` (diez mil
millones) de celdas. Si se guardara con el tipo de dato por defecto de
Python/NumPy (`float64`, 8 bytes por celda) pesaría **~80 TB**, y crearla
como un arreglo normal en memoria agotaría la RAM de cualquier computador
de uso común de inmediato. Por eso toda la solución gira en torno a nunca
tener la matriz completa en memoria, ni al crearla ni al leerla.

## ¿Por qué funciona? (resumen de las decisiones de diseño)

| Problema | Cómo se resuelve | Dónde |
|---|---|---|
| Consumo excesivo de RAM | La matriz se escribe **por bloques de filas** (no fila por fila ni completa), reutilizando el mismo buffer en memoria | `src/matrix_writer.py` |
| Consumo excesivo de RAM | Cada celda ocupa 1 byte (no 8), reduciendo el tamaño total de ~80 TB a ~9.3 GB | `src/config.py` |
| Escritura lenta a disco | Se agrupan varias filas en un solo `write()` en vez de una llamada al sistema operativo por fila (100.000 syscalls → ~50 syscalls) | `src/matrix_writer.py` |
| Escritura lenta a disco | Se preasigna el tamaño final del archivo (`truncate` + `posix_fallocate`) antes de escribir, evitando que el sistema de archivos lo vaya agrandando y fragmentando poco a poco | `src/matrix_writer.py` |
| Optimización de lectura | **Registros de longitud fija:** cada fila mide siempre lo mismo en bytes, así que la posición de cualquier fila se calcula con `indice * TAM_REGISTRO`, sin recorrer el archivo | `src/matrix_reader.py` |
| Optimización de lectura | **Acceso directo (`seek`)** para lecturas puntuales, y **memory-mapped file (`mmap`)** para acceso aleatorio repetido y muy rápido | `src/matrix_reader.py` |
| Verificación de resultados | Comprobación del tamaño exacto del archivo + muestreo de filas (inicio, medio, fin y aleatorias) sin leer el archivo completo | `src/verify.py` |

## Estructura del repositorio

```
laboratorio1-estructura-datos/
├── README.md              <- este archivo
├── requirements.txt        <- dependencias (ninguna externa; solo librería estándar)
├── .gitignore               <- excluye el archivo de datos generado (pesa varios GB)
├── main.py                  <- punto de entrada: crea, verifica y muestra la matriz completa
├── test_rapido.py           <- misma solución pero con una matriz 1.000x1.000, para probar en segundos
├── data/                    <- aquí se genera matriz_gigante.dat (no se sube a GitHub)
│   └── .gitkeep
└── src/
    ├── __init__.py
    ├── config.py             <- parámetros centrales (dimensiones, tamaño de bloque, rutas)
    ├── matrix_writer.py       <- crea la matriz en disco (resuelve RAM y velocidad de escritura)
    ├── matrix_reader.py       <- lee filas/celdas por acceso directo y por mmap; muestra la matriz
    └── verify.py               <- verifica que el archivo generado sea correcto y completo
```

### Descripción de cada archivo

- **`src/config.py`** — Define `FILAS`, `COLUMNAS`, `BYTES_POR_CELDA`, el
  `TAM_REGISTRO` (tamaño fijo de una fila en bytes) y `FILAS_POR_BLOQUE`
  (cuántas filas se acumulan en memoria antes de escribir a disco). Cambiar
  el tamaño de la matriz solo requiere editar este archivo.

- **`src/matrix_writer.py`** — Contiene `crear_matriz()`, que genera el
  archivo en disco por bloques, preasigna el espacio total y usa `fsync`
  para garantizar que los datos quedaron físicamente escritos.

- **`src/matrix_reader.py`** — Contiene tres formas de leer datos sin
  cargar el archivo completo: `leer_fila_seek()` (acceso directo clásico),
  `leer_celda_seek()` (acceso a una sola celda) y la clase
  `MatrizMemoryMapped` (lectura/escritura vía `mmap`). También incluye
  `mostrar_muestra()`, que es la función que resuelve el entregable
  ("mostrar la matriz creada").

- **`src/verify.py`** — Verifica que el archivo tenga el tamaño exacto
  esperado y que una muestra representativa de filas (inicio, medio, fin
  y aleatorias) tenga el contenido correcto. Es la forma de **comprobar
  el contenido del archivo generado** sin tener que leerlo completo.

- **`main.py`** — Orquesta todo el proceso: revisa espacio en disco,
  crea la matriz de 100.000x100.000, la verifica y la muestra.

- **`test_rapido.py`** — Corre exactamente el mismo pipeline pero con una
  matriz de 1.000x1.000, para validar en segundos que el código funciona
  antes de lanzar la versión completa (que tarda varios minutos y ocupa
  ~9.3 GB).

## Cómo ejecutar

### 1. Clonar y entrar al repositorio
```bash
git clone <url-del-repo>
cd laboratorio1-estructura-datos
```

### 2. (Opcional pero recomendado) Prueba rápida primero
```bash
python test_rapido.py
```
Esto crea una matriz de 1.000x1.000 en segundos y confirma que todo el
pipeline (crear → verificar → mostrar) funciona correctamente.

### 3. Ejecutar el laboratorio completo (100.000 x 100.000)
```bash
python main.py
```

**Requisito:** al menos ~10 GB de espacio libre en disco. El script
verifica esto automáticamente al inicio y avisa si no hay suficiente
espacio.

### 4. Verificar el archivo generado por separado
```bash
python -m src.verify
```

## Cómo se verifica el contenido del archivo generado

`main.py` y `src/verify.py` comprueban dos cosas, sin leer el archivo
completo:

1. **Tamaño exacto:** `os.path.getsize()` debe coincidir con
   `FILAS * TAM_REGISTRO` byte por byte. Si coinciden, se confirma que
   la matriz tiene sus 10.000.000.000 celdas completas, no una versión
   truncada.
2. **Contenido por muestreo:** se leen ~23 filas (la primera, la del
   medio, la última y 20 aleatorias) por acceso directo, y se valida que
   cada una mida exactamente `TAM_REGISTRO` bytes y contenga el valor
   esperado en todas sus celdas.

## Resultados esperados (con la configuración por defecto)

- Tamaño del archivo: **~9.31 GB**
- Tiempo de creación: depende del disco, pero típicamente unos pocos
  minutos en un SSD (mucho más lento en HDD mecánico o almacenamiento en
  red)
- Acceso a cualquier fila (por `seek` o `mmap`): **tiempo constante**,
  independiente de si es la fila 0 o la fila 99.999
