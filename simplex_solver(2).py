"""
simplex_solver.py
-----------------
Résolution automatique de problèmes de Programmation Linéaire
par la méthode du Simplexe (maximisation, forme standard).

Projet  : Optimisation de la vente dans un mini-supermarché
Auteure : Andof Sara — G8
Encadré par : Pr. Abdelati REHA & Pr. Yassine SAFSOUF
EMSI Marrakech — Année Universitaire 2025-2026
"""

import numpy as np


# ────────────────────────────────────────────────────────────────
#  SOLVEUR SIMPLEXE
# ────────────────────────────────────────────────────────────────

def simplex_solver(c, A, b, var_names):
    """
    Résout un problème de maximisation linéaire par la méthode du Simplexe.

    Paramètres
    ----------
    c         : list[float]  — coefficients de la fonction objectif
    A         : list[list]   — matrice des contraintes (≤)
    b         : list[float]  — membres droits des contraintes
    var_names : list[str]    — noms des variables de décision

    Retourne
    --------
    solution  : list[float]  — valeurs optimales de toutes les variables
    z_opt     : float        — valeur optimale de Z
    """

    n_vars = len(c)
    n_cons = len(b)

    slack_names = [f'E{i+1}' for i in range(n_cons)]
    all_names   = var_names + slack_names

    # ── Construction du tableau initial ──────────────────────────
    tableau = np.zeros((n_cons + 1, n_vars + n_cons + 1))

    # Ligne L0 : coefficients négatifs de la fonction objectif
    for j, coef in enumerate(c):
        tableau[0][j] = -coef

    # Lignes de contraintes + variables d'écart
    for i in range(n_cons):
        for j in range(n_vars):
            tableau[i+1][j] = A[i][j]
        tableau[i+1][n_vars + i] = 1.0   # variable d'écart Ei
        tableau[i+1][-1] = b[i]          # membre droit

    basis = list(range(n_vars, n_vars + n_cons))   # base initiale = variables d'écart

    iteration = 0

    # ── Affichage du tableau initial ─────────────────────────────
    _print_tableau(tableau, all_names, basis, iteration)

    # ── Boucle Simplexe ──────────────────────────────────────────
    while True:
        # Test d'optimalité : existe-t-il un coefficient négatif en L0 ?
        pivot_col = -1
        min_val   = -1e-9
        for j in range(len(all_names)):
            if tableau[0][j] < min_val:
                min_val, pivot_col = tableau[0][j], j

        if pivot_col == -1:
            break   # Tous les coefficients ≥ 0 → optimum atteint

        # Choix de la variable sortante (ratio minimum positif)
        ratios = [
            (tableau[i][-1] / tableau[i][pivot_col], i)
            for i in range(1, n_cons + 1)
            if tableau[i][pivot_col] > 1e-9
        ]

        if not ratios:
            print("Problème non borné — pas de solution optimale finie.")
            return None, None

        _, pivot_row = min(ratios)

        print(f"\n  Variable entrante : {all_names[pivot_col]}")
        print(f"  Variable sortante : {all_names[basis[pivot_row - 1]]}")
        print(f"  Pivot             : {tableau[pivot_row][pivot_col]:.4g}\n")

        # Pivotage (élimination de Gauss)
        tableau[pivot_row] /= tableau[pivot_row][pivot_col]
        basis[pivot_row - 1] = pivot_col

        for i in range(n_cons + 1):
            if i != pivot_row:
                tableau[i] -= tableau[i][pivot_col] * tableau[pivot_row]

        iteration += 1
        _print_tableau(tableau, all_names, basis, iteration)

    # ── Extraction de la solution ─────────────────────────────────
    solution = [0.0] * len(all_names)
    for i, idx in enumerate(basis):
        solution[idx] = tableau[i + 1][-1]

    return solution, tableau[0][-1]


# ────────────────────────────────────────────────────────────────
#  AFFICHAGE DU TABLEAU
# ────────────────────────────────────────────────────────────────

def _print_tableau(tableau, all_names, basis, iteration):
    """Affiche le tableau Simplexe courant de façon lisible."""
    col_width = 10
    header = f"\n{'─'*60}\n  TABLEAU {iteration}\n{'─'*60}"
    print(header)

    # En-tête des colonnes
    col_names = all_names + ['b']
    header_row = "  Base  |" + "".join(f"{n:>{col_width}}" for n in col_names)
    print(header_row)
    print("  " + "─" * (len(header_row) - 2))

    # Ligne L0
    row_str = "  L0     |"
    for val in tableau[0]:
        row_str += f"{val:>{col_width}.4g}"
    print(row_str)

    # Lignes de contraintes
    n_cons = tableau.shape[0] - 1
    for i in range(1, n_cons + 1):
        base_var = all_names[basis[i - 1]]
        row_str  = f"  {base_var:<6} |"
        for val in tableau[i]:
            row_str += f"{val:>{col_width}.4g}"
        print(row_str)

    print(f"\n  Z = {tableau[0][-1]:.4g}")


# ────────────────────────────────────────────────────────────────
#  PROGRAMME PRINCIPAL
# ────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Solveur Simplexe — Maximisation")
    print("  Projet : Optimisation Mini-Supermarché")
    print("=" * 60)

    # ── Saisie interactive ────────────────────────────────────────
    n_vars = int(input("\nNombre de variables de décision : "))
    n_cons = int(input("Nombre de contraintes           : "))

    var_names = [input(f"  Nom variable {i+1} : ") for i in range(n_vars)]

    print("\nCoefficients de la fonction objectif (à maximiser) :")
    c = [float(input(f"  Coef de {v} : ")) for v in var_names]

    print("\nMatrice des contraintes (≤) :")
    A, b = [], []
    for i in range(n_cons):
        print(f"  Contrainte {i+1} :")
        row = [float(input(f"    Coef de {v} : ")) for v in var_names]
        A.append(row)
        b.append(float(input(f"    Membre droit b{i+1} : ")))

    # ── Résolution ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  RÉSOLUTION PAR LA MÉTHODE DU SIMPLEXE")
    print("=" * 60)

    solution, z_opt = simplex_solver(c, A, b, var_names)

    # ── Affichage des résultats ───────────────────────────────────
    if solution is not None:
        print("\n" + "=" * 60)
        print("  SOLUTION OPTIMALE")
        print("=" * 60)
        for j, name in enumerate(var_names):
            print(f"  {name} = {solution[j]:.4g}")
        print(f"\n  Z* = {z_opt:.4g}")
        print("=" * 60)


# ────────────────────────────────────────────────────────────────
#  APPLICATION AU PROBLÈME DU MINI-SUPERMARCHÉ
# ────────────────────────────────────────────────────────────────

def demo_mini_supermarche():
    """
    Application directe au problème étudié (Chapitre 2) :
      Maximiser Z = 5x1 + 3x2 + 4x3
      Sous les contraintes :
        2x1 + x2 + 3x3 ≤ 100   (Farine)
          x1 + x2       ≤  80   (Viande)
          x1            ≤  40   (Demande sandwichs)
               x2       ≤  50   (Demande boissons)
                    x3  ≤  30   (Demande gâteaux)
    """
    print("\n" + "=" * 60)
    print("  DÉMONSTRATION — Mini-Supermarché (3 variables)")
    print("=" * 60)

    var_names = ['x1 (sandwichs)', 'x2 (boissons)', 'x3 (gâteaux)']
    c  = [5, 3, 4]
    A  = [
        [2, 1, 3],   # Farine
        [1, 1, 0],   # Viande
        [1, 0, 0],   # Demande sandwichs
        [0, 1, 0],   # Demande boissons
        [0, 0, 1],   # Demande gâteaux
    ]
    b  = [100, 80, 40, 50, 30]

    solution, z_opt = simplex_solver(c, A, b, var_names)

    if solution is not None:
        print("\n" + "=" * 60)
        print("  RÉSULTATS")
        print("=" * 60)
        labels = ['Sandwichs (x1)', 'Boissons  (x2)', 'Gâteaux   (x3)']
        for j, label in enumerate(labels):
            print(f"  {label} = {solution[j]:.4g} unités/jour")
        print(f"\n  Profit optimal Z* = {z_opt:.4g} DH/jour")
        print("=" * 60)


# ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("\nChoisissez un mode :")
    print("  1 — Saisie interactive (résoudre votre propre problème)")
    print("  2 — Démonstration Mini-Supermarché")
    choix = input("\nVotre choix (1 ou 2) : ").strip()

    if choix == '2':
        demo_mini_supermarche()
    else:
        main()
