"""
Laboratorio 2 - Árbol de Merkle
Implementación de un Árbol de Merkle con SHA-256.

Reglas:
- Cada hoja = SHA-256 de un bloque de datos (transacción).
- Cada nodo interno = SHA-256 de la concatenación de sus dos hijos.
- Si un nivel tiene un número impar de elementos, el último se duplica.
- La raíz (Merkle Root) representa la totalidad del conjunto de datos.
"""

import hashlib


def sha256(data: str) -> str:
    """Devuelve el hash SHA-256 (hexadecimal) de una cadena de texto."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class MerkleTree:
    def __init__(self, transactions):
        if not transactions:
            raise ValueError("Se necesita al menos una transacción para construir el árbol.")
        self.transactions = list(transactions)
        self.levels = []  # levels[0] = hojas, levels[-1] = [raíz]
        self._build_tree()

    # ------------------------------------------------------------------
    # Construcción del árbol
    # ------------------------------------------------------------------
    def _build_tree(self):
        # Nivel 0: hash de cada transacción (hojas)
        leaves = [sha256(tx) for tx in self.transactions]
        self.levels = [leaves]

        current_level = leaves
        while len(current_level) > 1:
            # Si el nivel es impar, se duplica el último elemento
            if len(current_level) % 2 == 1:
                current_level = current_level + [current_level[-1]]

            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1]
                parent_hash = sha256(left + right)
                next_level.append(parent_hash)

            self.levels.append(next_level)
            current_level = next_level

    @property
    def root(self):
        """Merkle Root: hash raíz que representa todo el conjunto de datos."""
        return self.levels[-1][0]

    # ------------------------------------------------------------------
    # Prueba de inclusión (Merkle Proof)
    # ------------------------------------------------------------------
    def get_proof(self, index):
        """
        Genera la prueba de inclusión (lista de hashes hermanos y su
        posición 'left'/'right') para la hoja en la posición `index`.
        """
        if index < 0 or index >= len(self.transactions):
            raise IndexError("Índice de transacción fuera de rango.")

        proof = []
        idx = index

        # Recorremos todos los niveles excepto la raíz
        for level in self.levels[:-1]:
            level_padded = level[:]
            if len(level_padded) % 2 == 1:
                level_padded.append(level_padded[-1])

            is_right_node = (idx % 2 == 1)  # nodo actual es el hijo derecho?
            sibling_index = idx - 1 if is_right_node else idx + 1
            sibling_hash = level_padded[sibling_index]

            # Si el nodo actual es izquierdo, el hermano va a la derecha
            # al concatenar, y viceversa.
            position = "left" if is_right_node else "right"
            proof.append((sibling_hash, position))

            idx = idx // 2

        return proof

    # ------------------------------------------------------------------
    # Verificación de una prueba de inclusión
    # ------------------------------------------------------------------
    @staticmethod
    def verify_proof(data, proof, root):
        """
        Verifica que `data` (el bloque de datos original, sin hashear)
        pertenece al árbol cuya raíz es `root`, usando la prueba `proof`
        generada por get_proof().
        """
        computed_hash = sha256(data)

        for sibling_hash, position in proof:
            if position == "right":
                computed_hash = sha256(computed_hash + sibling_hash)
            else:  # position == "left"
                computed_hash = sha256(sibling_hash + computed_hash)

        return computed_hash == root

    # ------------------------------------------------------------------
    # Utilidades de visualización
    # ------------------------------------------------------------------
    def print_tree(self):
        """Imprime el árbol nivel por nivel (raíz al final)."""
        for i, level in enumerate(self.levels):
            label = "Raíz" if i == len(self.levels) - 1 else f"Nivel {i}"
            print(f"\n{label}:")
            for h in level:
                print(f"  {h}")
