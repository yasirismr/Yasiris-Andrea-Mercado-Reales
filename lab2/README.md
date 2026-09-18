# Yasiris Andrea Mercado Reales Laboratorio 2 — Árbol de Merkle (Merkle Tree)

Implementación de un Árbol de Merkle en Python usando SHA-256, con un experimento
completo que crea transacciones simuladas, construye el árbol, demuestra la
propiedad de integridad (cambio de raíz ante una modificación) y genera/verifica
una prueba de inclusión (Merkle Proof).

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `merkle_tree.py` | Código fuente: clase `MerkleTree` (construcción, raíz, prueba de inclusión y verificación). |
| `experimento.py` | Script que ejecuta el experimento completo pedido en el enunciado. |
| `diagrama.py` | Genera el diagrama gráfico del árbol (`merkle_tree_diagram.png`). |
| `capturas.py` | Genera las imágenes de evidencia de las verificaciones válida/inválida. |
| `Lab2_Merkle_Tree.ipynb` | **Notebook de Google Colab** con todo el código, explicaciones y resultados ya ejecutados. |
| `merkle_tree_diagram.png` | Diagrama del árbol construido (gráfico). |
| `captura_verificacion_valida.png` | Captura de la verificación con dato correcto (válida). |
| `captura_verificacion_invalida.png` | Captura de la verificación con dato incorrecto (inválida). |

## Especificación implementada

- Cada **hoja** contiene el hash SHA-256 de un bloque de datos (transacción).
- Cada **nodo interno** contiene el hash SHA-256 de la concatenación de sus dos hijos (`SHA256(left + right)`).
- Si el número de nodos en un nivel es **impar**, el último nodo se **duplica** para poder emparejarlo.
- La **raíz (Merkle Root)** es el hash que representa la integridad de todo el conjunto de datos.



## Diseño del árbol (5 transacciones)

Con 5 transacciones, el árbol queda así (el Nivel 1 tiene 3 nodos → impar → se
duplica el último para el cálculo del Nivel 2):

```
                                   RAÍZ (Merkle Root)
                                   [3589b5bb..]
                                  /                \
                        [813b205d..]         [fa9c3fe2..]
                        /          \                 \
              [65de03ee..]  [3d5d2857..]      [fb40366a..]
               /      \      /      \         (dup) /
        [21af4847..][a55c56fc..][89c914d5..][b624272e..]  [6ae4711d..]
          TX1      TX2      TX3      TX4         TX5
```

Ver también `merkle_tree_diagram.png` para la versión gráfica a color.

## Resumen del experimento

1. **5 transacciones simuladas** (`TX1`…`TX5`) representando pagos entre personas.
2. **Construcción del árbol**: se calcula el hash SHA-256 de cada transacción (hojas),
   y se combinan de a pares hacia arriba hasta obtener la **Merkle Root**.
3. **Modificación de una transacción** (`TX3`): al cambiar un solo carácter del dato,
   la Merkle Root resultante es **completamente distinta** (efecto avalancha de SHA-256),
   demostrando que el árbol detecta cualquier alteración en los datos.
4. **Prueba de inclusión para TX3**: se genera la lista de hashes hermanos
   (`get_proof`) necesarios para reconstruir la raíz partiendo únicamente de `TX3`,
   sin necesitar las demás transacciones completas.
5. **Verificación**:
   - Con el dato **correcto** → la raíz recalculada coincide con la Merkle Root → **VÁLIDA**.
   - Con un dato **incorrecto** (alterado) → la raíz recalculada no coincide → **INVÁLIDA**.

## Resultados obtenidos (ejemplo de ejecución)

- Merkle Root original:
  `3589b5bb7945794e0d4687d167d1be9a787f7faf0f08089c70e86f089c262a93`
- Merkle Root tras modificar TX3:
  `f7f9ddd22d0dc11e08450458de4512d82d8e6190dd8582c8f923d5c35d35e298`
- Verificación de TX3 con dato correcto: **VÁLIDA**
- Verificación de TX3 con dato incorrecto: **INVÁLIDA**

Ver `captura_verificacion_valida.png` y `captura_verificacion_invalida.png` para
la evidencia visual de ambos casos.

## Uso de IA generativa

De acuerdo con el código de honor del curso, se declara explícitamente el uso de
IA generativa (Claude, Anthropic) en este entregable:

- **Qué se usó de la IA**: se le pidio un codigo base y se trabajo encima de el, se probo codigo con nuestros propios datos
- **Qué no vino de la IA**: Revisión y depuración del codigo los datos de las 5 transacciones simuladas y el
  enunciado/especificación del laboratorio, provistos por el estudiante/docente.
- **Responsabilidad**: el estudiante ha revisado, ejecutado y comprende algunas 
  partes del código entregado (construcción del árbol, generación de la Merkle
  Root, generación y verificación de la prueba de inclusión) y puede explicar
  cualquier elemento de la entrega.

## Complejidad

- Construcción del árbol: `O(n)` en tiempo y espacio, para `n` transacciones.
- Prueba de inclusión y verificación: `O(log₂ n)` hashes, en lugar de recorrer
  todas las `n` transacciones — esta es la principal ventaja del Árbol de Merkle
  (usado en Bitcoin, Git, IPFS, certificados de transparencia, etc.).
