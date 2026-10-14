# deck-conseil

Une équipe d'agents Claude qui construit des decks de conseil en partant des priorités du lecteur, puis prouve chaque réponse par les sources. Le rendu final : un .pptx éditable sur fond blanc, boxes grises, une seule couleur d'accent.

```
/deck-conseil:deck Note de cadrage pour le COMEX sur la refonte KYC, à partir des 3 PDF joints
```

## Le pipeline sépare la réflexion de la mise en forme

```
Cadrage avec l'utilisateur (orchestrateur)
   │  objectif, lecteur, questions du lecteur par priorité
   ├──► lecteur-sources ──► takeaways d'abord, faits avec page source
   └──► chercheur ────────► faits datés et sourcés
            ▼
   architecte-ghost-deck ─► idée directrice, SCQA, pyramide, titres
            ▼
   PORTE 1  reviewer (narratif) + validation orchestrateur + feu vert utilisateur
            ▼
   directeur-visuel ─────► contenu des blocs + gabarit par slide (JSON)
            ▼
   PORTE 2  linter + reviewer (couverture du titre, périmètre, gabarit)
   PORTE 3  reviewer (logical writing phrase par phrase)
            ▼
   constructeur ─────────► deck.pptx, rendu PNG, correction des débordements
```

Trois choix structurent l'outil :

- **Minto et le logical writing ne forment pas des étapes.** Ce sont deux références (`skills/deck/references/`) que chaque agent applique en écrivant, et que le reviewer contrôle à chaque porte, du deck jusqu'à la phrase.
- **Le reviewer n'a pas produit ce qu'il juge.** Il tourne dans un contexte séparé, avec le brief du lecteur comme étalon.
- **Les agents échangent par fichiers** (`00-brief.md` → `04-storyboard.json`). Chaque agent lit uniquement ce dont il a besoin, ce qui limite les tokens et laisse une trace relisible.

## Quatorze gabarits encodent les relations logiques classiques du conseil

`colonnes`, `lignes`, `puces`, `progression` (boxes croissantes avec flèche), `chevrons`, `matrice` 2x2, `tableau` avec Harvey balls, `graphique_texte`, `waterfall`, `avant_apres`, `timeline`, `arbre` (issue tree), `recommandation`, `couverture`. Le directeur visuel choisit le gabarit d'après la relation entre les blocs (`references/gabarits.md`). Graphiques natifs PowerPoint, donc éditables.

Démonstration : `examples/demo-gabarits/` (storyboard JSON et deck généré).

## Installation

**Claude Code (recommandé : agents séparés)**
```bash
claude plugin marketplace add <votre-compte>/deck-conseil
claude plugin install deck-conseil@deck-conseil
```
Puis dans une session : `/deck-conseil:deck <votre besoin>`. Prérequis : Python 3.9+ et `pip install python-pptx`. LibreOffice et poppler sont optionnels, pour le contrôle visuel du rendu.

**claude.ai (mode séquentiel)**
```bash
python3 tools/package_skill.py   # crée dist/deck.zip
```
Téléversez `dist/deck.zip` dans les paramètres de Claude, section Skills, avec l'exécution de code activée. Sans sous-agents, l'orchestrateur joue chaque rôle à la suite en relisant son fichier de rôle avant chaque étape.

**Scripts seuls**
```bash
python3 skills/deck/scripts/lint_storyboard.py storyboard.json
python3 skills/deck/scripts/build_deck.py storyboard.json -o deck.pptx
python3 skills/deck/scripts/render_check.py deck.pptx rendu/
```

## Organisation du repo

```
.claude-plugin/          manifeste du plugin et de la marketplace
agents/                  sous-agents Claude Code (générés depuis les rôles)
skills/deck/
  SKILL.md               orchestrateur : pipeline, portes, critères de validation
  roles/                 un fichier par rôle : source unique des prompts
  references/            « Consulting Brain » : Minto, logical writing, gabarits, graphiques, format JSON
  scripts/               générateur .pptx, linter, rendu PNG
tools/                   synchronisation rôles → agents, empaquetage claude.ai
examples/                deck de démonstration
```

Pour modifier un agent, éditez `skills/deck/roles/<rôle>.md` puis lancez `python3 tools/sync_agents.py`.

## Adapter à une charte d'entreprise

La charte tient dans les constantes en tête de `build_deck.py` (couleurs, police, marges) et dans `meta.accent` du storyboard. Pour ajouter des exemples internes (propositions gagnées, battle cards), créez un dossier `references/exemples-internes/` hors du repo public et citez-le dans le rôle de l'architecte.

## Limites connues

- Le linter repère une voix passive probable par expression régulière : il manque des formes et signale des faux positifs. La porte 3 reste nécessaire.
- L'ajustement du texte estime la largeur des caractères. Le rendu LibreOffice diffère légèrement de PowerPoint ; le constructeur contrôle les débordements sur le rendu.
- Les chiffres des slides de graphiques de la démonstration sont fictifs.

## Crédits

L'architecture s'inspire de [enterprise-ai-skills](https://github.com/sruthir28/enterprise-ai-skills) (chaîne stratège, constructeur, critique) et de [pyramid-principle](https://github.com/tyroneross/pyramid-principle) (règles canoniques en un seul endroit). Le code et les prompts de ce repo sont originaux.

Licence MIT.
