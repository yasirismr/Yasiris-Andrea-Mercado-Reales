"""
Experimento del Laboratorio 2 - Árbol de Merkle
"""

from merkle_tree import MerkleTree, sha256


def linea(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


# ----------------------------------------------------------------------
# 1. Crear 5 transacciones simuladas
# ----------------------------------------------------------------------
linea("1. TRANSACCIONES SIMULADAS")
transacciones = [
    "TX1: Ana paga 50 a Bruno",
    "TX2: Bruno paga 20 a Carla",
    "TX3: Carla paga 100 a Diego",
    "TX4: Diego paga 15 a Elena",
    "TX5: Elena paga 30 a Ana",
]
for i, tx in enumerate(transacciones):
    print(f"  [{i}] {tx}")

# ----------------------------------------------------------------------
# 2. Construir el árbol y mostrar la raíz
# ----------------------------------------------------------------------
linea("2. CONSTRUCCIÓN DEL ÁRBOL Y MERKLE ROOT")
arbol = MerkleTree(transacciones)
arbol.print_tree()
print(f"\n>>> MERKLE ROOT ORIGINAL: {arbol.root}")

# ----------------------------------------------------------------------
# 3. Modificar una transacción y demostrar que la raíz cambia
# ----------------------------------------------------------------------
linea("3. MODIFICACIÓN DE UNA TRANSACCIÓN")
transacciones_modificadas = transacciones.copy()
original_tx3 = transacciones_modificadas[2]
transacciones_modificadas[2] = "TX3: Carla paga 999999 a Diego"  # dato alterado

print(f"  Transacción original [2]: {original_tx3}")
print(f"  Transacción modificada [2]: {transacciones_modificadas[2]}")

arbol_modificado = MerkleTree(transacciones_modificadas)
print(f"\n>>> MERKLE ROOT ORIGINAL:   {arbol.root}")
print(f">>> MERKLE ROOT MODIFICADO: {arbol_modificado.root}")

if arbol.root != arbol_modificado.root:
    print("\n✅ La raíz CAMBIÓ tras modificar una sola transacción, como se esperaba.")
else:
    print("\n❌ ERROR: la raíz no cambió (esto no debería ocurrir).")

# ----------------------------------------------------------------------
# 4. Generar prueba de inclusión para la transacción 3 (índice 2) y verificar
# ----------------------------------------------------------------------
linea("4. PRUEBA DE INCLUSIÓN PARA LA TRANSACCIÓN 3 (índice 2)")
indice_tx3 = 2
prueba_tx3 = arbol.get_proof(indice_tx3)

print(f"  Transacción a probar: '{transacciones[indice_tx3]}'")
print(f"  Prueba de inclusión (hash hermano, posición):")
for h, pos in prueba_tx3:
    print(f"    - {h}  ({pos})")

es_valida = MerkleTree.verify_proof(transacciones[indice_tx3], prueba_tx3, arbol.root)
print(f"\n>>> Verificación con el dato CORRECTO -> {'VÁLIDA ✅' if es_valida else 'INVÁLIDA ❌'}")
assert es_valida, "La prueba debería ser válida"

# ----------------------------------------------------------------------
# 5. Verificar con un dato incorrecto -> debe fallar
# ----------------------------------------------------------------------
linea("5. VERIFICACIÓN CON UN DATO INCORRECTO (debe fallar)")
dato_falso = "TX3: Carla paga 100000 a Diego (dato alterado por un atacante)"
print(f"  Dato falso usado para la verificación: '{dato_falso}'")

es_valida_falsa = MerkleTree.verify_proof(dato_falso, prueba_tx3, arbol.root)
print(f"\n>>> Verificación con el dato INCORRECTO -> {'VÁLIDA ✅' if es_valida_falsa else 'INVÁLIDA ❌'}")
assert not es_valida_falsa, "La prueba con dato falso NO debería ser válida"

linea("EXPERIMENTO FINALIZADO CORRECTAMENTE")
