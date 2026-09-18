"""
Genera un diagrama visual (PNG) del Árbol de Merkle construido
con las 5 transacciones del experimento.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from merkle_tree import MerkleTree

transacciones = [
    "TX1: Ana paga 50 a Bruno",
    "TX2: Bruno paga 20 a Carla",
    "TX3: Carla paga 100 a Diego",
    "TX4: Diego paga 15 a Elena",
    "TX5: Elena paga 30 a Ana",
]

arbol = MerkleTree(transacciones)

# Reconstruimos la estructura completa (incluyendo la duplicación del nivel impar)
# para dibujar el árbol tal como se calculó internamente.
levels_padded = []
for lvl in arbol.levels:
    lvl2 = lvl[:]
    if len(lvl2) % 2 == 1 and len(lvl2) > 1:
        lvl2 = lvl2 + [lvl2[-1] + " (dup)"]
    levels_padded.append(lvl2)

fig, ax = plt.subplots(figsize=(14, 9))
ax.axis("off")

n_levels = len(arbol.levels)
y_gap = 1.0

positions = {}  # (level, index) -> (x, y)

# Calculamos posiciones de abajo (hojas) hacia arriba (raíz)
level_widths = [len(lvl) for lvl in arbol.levels]
max_width = max(level_widths)

for li, level in enumerate(arbol.levels):
    y = li * y_gap
    count = len(level)
    total_width = max_width
    spacing = total_width / count
    for i in range(count):
        x = (i + 0.5) * spacing
        positions[(li, i)] = (x, y)

# Dibujar conexiones (nodo -> padre)
for li in range(n_levels - 1):
    level = arbol.levels[li]
    padded = level[:]
    duplicated_idx = None
    if len(padded) % 2 == 1:
        duplicated_idx = len(padded)  # el índice duplicado (virtual)
        padded = padded + [padded[-1]]
    for i in range(0, len(padded), 2):
        parent_i = i // 2
        x1, y1 = positions[(li, i if i < len(level) else i - 1)]
        # para el nodo duplicado usamos la misma posición visual que el original
        if i >= len(level):
            x1, y1 = positions[(li, len(level) - 1)]
        if i + 1 < len(level):
            x2, y2 = positions[(li, i + 1)]
        else:
            x2, y2 = positions[(li, len(level) - 1)]  # duplicado
        x3, y3 = positions[(li + 1, parent_i)]
        ax.plot([x1, x3], [y1, y3], color="gray", linewidth=1, zorder=1)
        ax.plot([x2, x3], [y2, y3], color="gray", linewidth=1, zorder=1)

# Dibujar nodos
colors_by_level = ["#a8d8ea", "#aa96da", "#fcbad3", "#ffffd2", "#c3f584"]
labels_tx = transacciones

for li, level in enumerate(arbol.levels):
    color = colors_by_level[li % len(colors_by_level)]
    for i, h in enumerate(level):
        x, y = positions[(li, i)]
        w, hgt = 0.85, 0.32
        rect = mpatches.FancyBboxPatch(
            (x - w / 2, y - hgt / 2), w, hgt,
            boxstyle="round,pad=0.02,rounding_size=0.05",
            linewidth=1.2, edgecolor="black", facecolor=color, zorder=2
        )
        ax.add_patch(rect)
        short_hash = h[:10] + "..." + h[-6:]
        ax.text(x, y, short_hash, ha="center", va="center", fontsize=7.5, zorder=3, family="monospace")

        if li == 0:
            ax.text(x, y - 0.28, f"H(TX{i+1})", ha="center", va="top", fontsize=8, color="#333333")

# Etiquetas de nivel
level_names = [f"Nivel {i} (hojas)" if i == 0 else (f"Raíz (Merkle Root)" if i == n_levels - 1 else f"Nivel {i}") for i in range(n_levels)]
for li in range(n_levels):
    ax.text(-0.6, li * y_gap, level_names[li], ha="right", va="center", fontsize=10, fontweight="bold")

# Transacciones originales debajo de las hojas
for i, tx in enumerate(transacciones):
    x, y = positions[(0, i)]
    ax.text(x, y - 0.5, tx, ha="center", va="top", fontsize=7, style="italic", rotation=0, wrap=True)

ax.set_xlim(-1.5, max_width + 0.5)
ax.set_ylim(-1.0, (n_levels - 1) * y_gap + 0.6)
ax.set_title("Árbol de Merkle - 5 transacciones (SHA-256)\nNivel 1 tiene número impar de nodos -> se duplica el último", fontsize=12, fontweight="bold")

plt.tight_layout()
plt.savefig("merkle_tree_diagram.png", dpi=180)
print("Diagrama guardado en merkle_tree_diagram.png")
print(f"Merkle Root: {arbol.root}")
