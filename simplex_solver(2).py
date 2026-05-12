# simplex_solver.py
# Projet : Optimisation de la vente dans un mini-supermarche
# Auteure : Andof Sara - G8
# EMSI Marrakech - 2025-2026

import numpy as np

def simplex_solver(c, A, b, var_names):
    n_vars = len(c)
    n_cons = len(b)
    slack_names = [f'E{i+1}' for i in range(n_cons)]
    all_names   = var_names + slack_names

    tableau = np.zeros((n_cons + 1, n_vars + n_cons + 1))
    for j, coef in enumerate(c):
        tableau[0][j] = -coef
    for i in range(n_cons):
        for j in range(n_vars):
            tableau[i+1][j] = A[i][j]
        tableau[i+1][n_vars + i] = 1.0
        tableau[i+1][-1] = b[i]

    basis = list(range(n_vars, n_vars + n_cons))
    print_tableau(tableau, all_names, basis, 0)

    iteration = 0
    while True:
        pivot_col = -1
        min_val   = -1e-9
        for j in range(len(all_names)):
            if tableau[0][j] < min_val:
                min_val, pivot_col = tableau[0][j], j
        if pivot_col == -1:
            break

        ratios = [
            (tableau[i][-1] / tableau[i][pivot_col], i)
            for i in range(1, n_cons + 1)
            if tableau[i][pivot_col] > 1e-9
        ]
        if not ratios:
            print("Probleme non borne.")
            return None, None

        _, pivot_row = min(ratios)
        print(f"\n  Variable entrante : {all_names[pivot_col]}")
        print(f"  Variable sortante : {all_names[basis[pivot_row - 1]]}")
        print(f"  Pivot             : {tableau[pivot_row][pivot_col]:.4g}\n")

        tableau[pivot_row] /= tableau[pivot_row][pivot_col]
        basis[pivot_row - 1] = pivot_col
        for i in range(n_cons + 1):
            if i != pivot_row:
                tableau[i] -= tableau[i][pivot_col] * tableau[pivot_row]

        iteration += 1
        print_tableau(tableau, all_names, basis, iteration)

    solution = [0.0] * len(all_names)
    for i, idx in enumerate(basis):
        solution[idx] = tableau[i + 1][-1]
    return solution, tableau[0][-1]


def print_tableau(tableau, all_names, basis, iteration):
    col_width = 10
    print(f"\n{'─'*65}")
    print(f"  TABLEAU {iteration}")
    print(f"{'─'*65}")
    col_names = all_names + ['b']
    header = "  Base   |" + "".join(f"{n:>{col_width}}" for n in col_names)
    print(header)
    print("  " + "-" * (len(header) - 2))
    row = "  L0      |"
    for val in tableau[0]:
        row += f"{val:>{col_width}.4g}"
    print(row)
    n_cons = tableau.shape[0] - 1
    for i in range(1, n_cons + 1):
        base_var = all_names[basis[i - 1]]
        row = f"  {base_var:<7} |"
        for val in tableau[i]:
            row += f"{val:>{col_width}.4g}"
        print(row)
    print(f"\n  Z = {tableau[0][-1]:.4g}")


def resolution_mini_supermarche():
    """
    Chapitre 2 - Probleme exact du rapport :
    Maximiser Z = 5x1 + 3x2 + 4x3
    Contraintes :
      2x1 + x2 + 3x3 <= 100  (Farine)
       x1 + x2        <= 80  (Viande)
       x1              <= 40  (Demande sandwichs)
            x2         <= 50  (Demande boissons)
                  x3   <= 30  (Demande gateaux)
    Solution attendue : x1=25, x2=50, x3=0, Z*=275
    """
    print("=" * 65)
    print("  PROBLEME : Mini-Supermarche (3 variables - Chapitre 2)")
    print("=" * 65)
    print("\n  Maximiser Z = 5x1 + 3x2 + 4x3\n")
    print("  Contraintes :")
    print("    2x1 + x2 + 3x3 <= 100  (Farine)")
    print("     x1 + x2        <= 80  (Viande)")
    print("     x1              <= 40  (Demande sandwichs)")
    print("          x2         <= 50  (Demande boissons)")
    print("                x3   <= 30  (Demande gateaux)\n")

    var_names = ['x1', 'x2', 'x3']
    c = [5, 3, 4]
    A = [
        [2, 1, 3],
        [1, 1, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    b = [100, 80, 40, 50, 30]

    solution, z_opt = simplex_solver(c, A, b, var_names)

    if solution is not None:
        print("\n" + "=" * 65)
        print("  SOLUTION OPTIMALE")
        print("=" * 65)
        print(f"  x1 (sandwichs) = {solution[0]:.4g} unites/jour")
        print(f"  x2 (boissons)  = {solution[1]:.4g} unites/jour")
        print(f"  x3 (gateaux)   = {solution[2]:.4g} unites/jour")
        print(f"\n  Profit optimal Z* = {z_opt:.4g} DH/jour")
        print("=" * 65)


def saisie_interactive():
    print("=" * 65)
    print("  SOLVEUR SIMPLEXE - Saisie interactive")
    print("=" * 65)
    n_vars = int(input("\nNombre de variables : "))
    n_cons = int(input("Nombre de contraintes : "))
    var_names = [input(f"  Nom variable {i+1} : ") for i in range(n_vars)]
    print("\nCoefficients de la fonction objectif :")
    c = [float(input(f"  Coef de {v} : ")) for v in var_names]
    print("\nContraintes (<=) :")
    A, b = [], []
    for i in range(n_cons):
        print(f"  Contrainte {i+1} :")
        row = [float(input(f"    Coef de {v} : ")) for v in var_names]
        A.append(row)
        b.append(float(input(f"    Membre droit b{i+1} : ")))
    solution, z_opt = simplex_solver(c, A, b, var_names)
    if solution is not None:
        print("\n" + "=" * 65)
        print("  SOLUTION OPTIMALE")
        print("=" * 65)
        for j, name in enumerate(var_names):
            print(f"  {name} = {solution[j]:.4g}")
        print(f"\n  Z* = {z_opt:.4g}")
        print("=" * 65)


if __name__ == '__main__':
    print("\nChoisissez un mode :")
    print("  1 - Saisie interactive")
    print("  2 - Resolution Mini-Supermarche (Chapitre 2)")
    choix = input("\nVotre choix (1 ou 2) : ").strip()
    if choix == '2':
        resolution_mini_supermarche()
    else:
        saisie_interactive()
