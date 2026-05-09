# 🛒 Optimisation de la Vente dans un Mini-Supermarché

**Matières :** Programmation Linéaire / Python  
**Étudiante :** Andof Sara — Groupe G8  
**Encadrants :** Pr. Abdelati REHA & Pr. Yassine SAFSOUF  
**Établissement :** EMSI Marrakech — 3ème année Génie Informatique & Réseaux  
**Année Universitaire :** 2025-2026

---

## 📌 Description du Projet

Ce projet applique les méthodes d'optimisation de la **Programmation Linéaire** à un cas concret : la maximisation du profit d'un mini-supermarché vendant des sandwichs, des boissons et des gâteaux.

Le projet est structuré en trois parties :

- **Partie 1** — Modélisation et résolution par la méthode graphique (2 variables)
- **Partie 2** — Modélisation et résolution par la méthode du Simplexe (3 variables)
- **Partie 3** — Implémentation Python de l'algorithme du Simplexe

---

## 📂 Structure du Dépôt

```
mini-supermarche-optimization/
│
├── README.md
├── rapport/
│   └── Andof_Sara_G8.docx       # Rapport complet (Parties 1, 2 et 3)
└── src/
    └── simplex_solver.py         # Programme Python — Méthode du Simplexe
```

---

## ▶️ Lancer le Programme

### Prérequis
```bash
pip install numpy
```

### Exécution
```bash
python src/simplex_solver.py
```

Deux modes sont disponibles :

| Mode | Description |
|------|-------------|
| `1` | Saisie interactive — résoudre n'importe quel problème |
| `2` | Démonstration directe avec le problème du mini-supermarché |

---

## 📊 Résultats Optimaux

| Variable | Valeur | Description |
|----------|--------|-------------|
| x₁ | 25 unités/jour | Sandwichs |
| x₂ | 50 unités/jour | Boissons |
| x₃ | 0 unités/jour  | Gâteaux (non rentables) |
| **Z\*** | **275 DH/jour** | **Profit maximum** |

---

## 🛠️ Technologies Utilisées

- **Python 3.x**
- **NumPy** — calcul matriciel
- **Microsoft Excel** (Solveur) — validation des résultats
- **GeoGebra** — méthode graphique
