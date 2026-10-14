"""Catalogue des gabarits : champs obligatoires et titres de blocs soumis au logical writing.

Ce fichier sert de source unique au générateur (build_deck.py) et au linter (lint_storyboard.py).
"""

# layout -> (champs obligatoires, relation logique encodée)
LAYOUTS = {
    "couverture": (["titre"], "Page de garde"),
    "colonnes": (["blocs"], "Arguments parallèles (2 à 4 piliers)"),
    "lignes": (["blocs"], "Arguments empilés, chacun avec son détail à droite"),
    "puces": (["points"], "Simple énumération sans autre relation"),
    "progression": (["blocs"], "Montée en maturité ou feuille de route, de gauche à droite"),
    "chevrons": (["etapes"], "Processus séquentiel"),
    "matrice": (["axe_x", "axe_y", "quadrants"], "Positionnement selon deux critères"),
    "tableau": (["colonnes", "lignes"], "Comparaison d'options sur plusieurs critères"),
    "graphique_texte": (["graphique", "blocs"], "Donnée chiffrée et sa lecture"),
    "waterfall": (["etapes"], "Écart entre deux valeurs, décomposé"),
    "avant_apres": (["avant", "apres"], "Situation actuelle contre cible"),
    "timeline": (["phases"], "Calendrier de mise en œuvre"),
    "arbre": (["racine", "branches"], "Décomposition d'un tout (issue tree)"),
    "recommandation": (["recommandation", "piliers"], "Recommandation et ses conditions ou raisons"),
}

# Champs dont les éléments portent un "titre" qui doit énoncer une idée (logical writing).
# Les titres d'étapes, de phases, de quadrants ou d'en-têtes de tableau restent des étiquettes.
IDEA_TITLE_FIELDS = {
    "colonnes": ["blocs"],
    "lignes": ["blocs"],
    "progression": ["blocs"],
    "graphique_texte": ["blocs"],
    "waterfall": ["blocs"],
    "avant_apres": ["avant", "apres"],
    "recommandation": ["piliers"],
}

HARVEY = {"[0]": "○", "[1]": "◔", "[2]": "◑", "[3]": "◕", "[4]": "●"}
