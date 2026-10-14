# Format du storyboard (`04-storyboard.json`)

Exemple complet : `examples/demo-gabarits/04-storyboard.json` dans le repo.

```json
{
  "meta": {"titre": "Nom du deck", "accent": "1F4E79", "police": "Arial"},
  "slides": [ { "layout": "...", "titre": "...", "source": "...", "notes": "...", "...": "champs du gabarit" } ]
}
```

## Champs communs à toutes les slides
| Champ | Obligatoire | Rôle |
|---|---|---|
| `layout` | oui | Un gabarit de la liste ci-dessous |
| `titre` | oui | Le titre validé au ghost deck, mot pour mot |
| `source` | si la slide contient un chiffre | Affichée en pied de slide, préfixée de « Source : » |
| `notes` | non | Notes orateur : ce qui se dit en plus, points ouverts |

Un **bloc** s'écrit `{"titre": "idée du bloc", "points": ["détail", "détail"], "accent": false}`.

## Champs par gabarit
| `layout` | Champs | Remarques |
|---|---|---|
| `couverture` | `titre`, `contexte` | `contexte` : destinataire, date |
| `colonnes` | `blocs` (2 à 4), `synthese` (optionnel) | `synthese` : bandeau sous les colonnes ; à n'utiliser que s'il ajoute une information |
| `lignes` | `blocs` (2 à 5), `largeur_titres` (pouces, défaut 3,6) | Titre de bloc à gauche, points à droite |
| `puces` | `points`, `titre_bloc` (optionnel) | |
| `progression` | `blocs` (2 à 5), `axe` (libellé de la flèche), `accent_derniere` (défaut vrai) | Boxes croissantes de gauche à droite |
| `chevrons` | `etapes` : `[{titre, points}]` (2 à 6) | Les titres d'étapes restent courts (1 à 2 mots) |
| `matrice` | `axe_x`, `axe_y` : `{label, bas, haut}` ; `quadrants` : 4 blocs dans l'ordre haut-gauche, haut-droite, bas-gauche, bas-droite ; `commentaire` (blocs, optionnel) | `accent: true` sur le quadrant que le titre désigne |
| `tableau` | `colonnes` (en-têtes), `lignes` (listes de cellules), `colonne_accent` (index, optionnel), `legende`, `largeur_premiere_colonne` | Cellule `"[0]"` à `"[4]"` : Harvey ball de 0 à 4 quarts |
| `graphique_texte` | `graphique` : `{titre, type: barres \| barres_h \| courbe, categories, series: [{nom, valeurs}], unite, format, accent: [index]}` ; `blocs` (1 à 3) ; `part_graphique` (défaut 0,6) | `accent` : index des catégories en couleur, les autres en gris |
| `waterfall` | `etapes` : `[{label, valeur, total}]` ; `titre_graphique`, `unite`, `format`, `blocs` (optionnel) | `total: true` pour les barres de départ et d'arrivée ; les autres valeurs sont des variations signées |
| `avant_apres` | `avant`, `apres` (blocs), `transition` (optionnel) | |
| `timeline` | `phases` : `[{periode, titre, points}]` (2 à 6) | |
| `arbre` | `racine` (texte), `branches` : `[{texte, feuilles: []}]` (2 à 4) | |
| `recommandation` | `recommandation` (texte), `piliers` (blocs, 2 à 4) | |

`format` suit la syntaxe Excel (`"0"`, `"0.0"`) ; `unite` s'ajoute après le nombre (`" %"`, `" Md€"`).
