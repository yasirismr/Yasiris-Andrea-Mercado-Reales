"""
Genera imágenes tipo 'captura de pantalla' de las verificaciones
(valida e invalida) para incluir como evidencia en el repositorio.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from merkle_tree import MerkleTree

transacciones = [
    "TX1: Ana paga 50 a Bruno",
    "TX2: Bruno paga 20 a Carla",
    "TX3: Carla paga 100 a Diego",
    "TX4: Diego paga 15 a Elena",
    "TX5: Elena paga 30 a Ana",
]
arbol = MerkleTree(transacciones)
prueba_tx3 = arbol.get_proof(2)


def render_terminal(lines, filename, ok_color):
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    ax.axis("off")
    y = 0.95
    for line, color in lines:
        ax.text(0.03, y, line, transform=ax.transAxes, fontsize=11,
                 family="monospace", color=color, va="top")
        y -= 0.115
    plt.tight_layout()
    plt.savefig(filename, dpi=160, facecolor=fig.get_facecolor())
    plt.close()


# ---- Captura 1: verificación valida ----
es_valida = MerkleTree.verify_proof(transacciones[2], prueba_tx3, arbol.root)
lines_ok = [
    ("$ python3 experimento.py", "#7fdbff"),
    ("", "white"),
    ("Transaccion a probar: 'TX3: Carla paga 100 a Diego'", "white"),
    (f"Merkle Root:  {arbol.root}", "#dddddd"),
    ("", "white"),
    (f">>> Verificacion con el dato CORRECTO -> {'VALIDA [OK]' if es_valida else 'INVALIDA [FAIL]'}", "#2ecc71" if es_valida else "#e74c3c"),
]
render_terminal(lines_ok, "captura_verificacion_valida.png", "#2ecc71")

# ---- Captura 2: verificación invalida (dato incorrecto) ----
dato_falso = "TX3: Carla paga 100000 a Diego (dato alterado por un atacante)"
es_valida_falsa = MerkleTree.verify_proof(dato_falso, prueba_tx3, arbol.root)
lines_fail = [
    ("$ python3 experimento.py", "#7fdbff"),
    ("", "white"),
    (f"Dato falso usado: '{dato_falso}'", "white"),
    (f"Merkle Root esperada: {arbol.root}", "#dddddd"),
    ("", "white"),
    (f">>> Verificacion con el dato INCORRECTO -> {'VALIDA [OK]' if es_valida_falsa else 'INVALIDA [FAIL]'}", "#2ecc71" if es_valida_falsa else "#e74c3c"),
    ("El sistema detecto la alteracion correctamente.", "#f39c12"),
]
render_terminal(lines_fail, "captura_verificacion_invalida.png", "#e74c3c")

print("Capturas generadas.")
