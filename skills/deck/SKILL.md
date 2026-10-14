---
name: deck
description: Orchestre une équipe d'agents qui construit un deck de conseil (.pptx, fond blanc, boxes grises) à partir des priorités du lecteur. Cadrage avec l'utilisateur, lecture des sources (takeaways d'abord), recherche, ghost deck, storyboard visuel, revues Minto et logical writing à chaque porte, génération du fichier. Utiliser quand l'utilisateur demande un deck, des slides, une présentation, une réponse RFP en slides, ou tape /deck.
argument-hint: "[besoin, destinataire, documents joints]"
---

# Orchestrateur deck-conseil

Tu orchestres l'équipe. Tu mènes toi-même le cadrage avec l'utilisateur et tu valides chaque porte. Tu délègues la production et les revues.

`SKILL_DIR` désigne le dossier de ce fichier. Passe son chemin absolu à chaque agent.

## Quatre principes gouvernent tout le pipeline

1. **Le deck part des priorités du lecteur.** Les sources fournissent les preuves ; elles ne dictent ni l'ordre ni les titres. Un deck qui suit l'ordre des documents résume ; un deck qui suit l'ordre des questions du lecteur répond.
2. **Minto et le logical writing s'appliquent à chaque niveau** : deck, slide, bloc, phrase. Chaque agent producteur les applique en écrivant ; le reviewer les contrôle à chaque porte. Règles : `references/minto.md` et `references/logical-writing.md`.
3. **Aucun chiffre sans source nommée.** Aucun ratio, prix ou total reconstitué présenté comme une donnée. Une information manquante reste signalée comme manquante.
4. **Aucun contenu de slide avant validation du ghost deck.**

## Le dossier de travail porte les échanges entre agents

Crée `deck-<sujet-court>/` dans le répertoire courant. Chaque agent lit uniquement les fichiers dont il a besoin et écrit un seul livrable. Ce découpage évite de recharger les sources à chaque étape et limite les tokens.

| Fichier | Auteur | Lecteurs |
|---|---|---|
| `00-brief.md` | toi (cadrage) | tous |
| `01-sources.md` | lecteur-sources | architecte, directeur-visuel |
| `02-recherche.md` | chercheur | architecte, directeur-visuel |
| `03-ghost-deck.md` | architecte | directeur-visuel, reviewer |
| `04-storyboard.json` | directeur-visuel | reviewer, constructeur |
| `revues/porte{1,2,3}-v{n}.md` | reviewer | toi, l'agent qui corrige |
| `deck.pptx`, `rendu/` | constructeur | toi, l'utilisateur |

## Mode d'exécution

- **Outil Agent disponible (Claude Code avec le plugin)** : délègue chaque étape au sous-agent nommé (`lecteur-sources`, `chercheur`, `architecte-ghost-deck`, `directeur-visuel`, `reviewer`, `constructeur`, préfixés `deck-conseil:` selon l'affichage). Dans chaque prompt de délégation, donne : `SKILL_DIR`, le dossier de travail, les fichiers à lire, le fichier à écrire, et pour une correction le chemin de la revue. Lance lecteur-sources et chercheur en parallèle.
- **Pas d'outil Agent (claude.ai)** : joue chaque rôle toi-même, dans l'ordre, en relisant `roles/<rôle>.md` juste avant l'étape. Pour une revue, relis uniquement les fichiers produits, jamais ton propre raisonnement : le reviewer juge le livrable, pas l'intention.

Les sous-agents ne parlent pas à l'utilisateur. Toute question à l'utilisateur passe par toi.

## Le pipeline compte huit étapes et trois portes

**0. Cadrage (toi).** Suis `roles/cadrage.md`. Pose en un seul message les questions dont la réponse manque (AskUserQuestion si disponible). Ne demande jamais ce que la demande ou les documents disent déjà. Écris `00-brief.md`, puis fais valider le brief en une ligne par l'utilisateur.

**1. Matière.** Si l'utilisateur a fourni des documents : `lecteur-sources` → `01-sources.md`. Si le brief liste des questions de recherche : `chercheur` → `02-recherche.md`. En parallèle. Si aucune des deux n'est nécessaire, passe à l'étape 2.

**2. Ghost deck.** `architecte-ghost-deck` → `03-ghost-deck.md`.

**3. Porte 1 : narratif.** `reviewer` en mode `ghost` → `revues/porte1-v{n}.md`. Verdict « À reprendre » : renvoie l'architecte vers la revue. Trois tours au plus ; au-delà, tranche toi-même et note le point ouvert. Puis applique tes critères de validation (plus bas). Montre ensuite à l'utilisateur l'idée directrice et la liste des titres, et attends son feu vert : corriger un titre ici coûte une ligne, le corriger après le storyboard coûte une slide.

**4. Storyboard.** `directeur-visuel` → `04-storyboard.json` (format : `references/schema-storyboard.md`).

**5. Porte 2 : slides.** Lance `python3 SKILL_DIR/scripts/lint_storyboard.py <dossier>/04-storyboard.json`. Toute ERREUR repart au directeur visuel avant revue. Puis `reviewer` en mode `storyboard`. Boucle de correction, trois tours au plus.

**6. Porte 3 : écriture.** `reviewer` en mode `final`, phrase par phrase. Le directeur visuel applique les corrections dans le JSON. Relance le linter.

**7. Construction.** `constructeur` → `deck.pptx` et `rendu/`. Il corrige les débordements signalés.

**8. Livraison.** Donne à l'utilisateur le fichier, la liste des titres finale, et les points ouverts : informations manquantes, chiffres retirés faute de source, désaccords non tranchés.

## Tes critères pour valider le ghost deck

Tu valides seulement si chaque réponse est oui :
- L'idée directrice répond à la question principale du lecteur notée dans le brief.
- Les titres lus seuls, à la suite, racontent l'histoire complète.
- Chaque titre répond à une question du lecteur, dans l'ordre de priorité du brief.
- La réponse ou la recommandation arrive dans les trois premières slides de contenu.
- Le deck s'ouvre sur une slide qui dit pourquoi le travail existe et ce qu'il vise, et le SCQA apparaît sur les slides.
- Aucune idée ne revient d'une slide à l'autre.
- Chaque titre trouve ses preuves dans `01-sources.md` ou `02-recherche.md`, ou la preuve manquante figure dans les points ouverts.

## Ce que tu ne fais pas

- Tu ne réécris pas toi-même un livrable d'agent : tu le renvoies avec la revue et une consigne précise. Exception : le mode claude.ai, où tu joues tous les rôles.
- Tu ne sautes aucune porte, même sous pression de délai : tu réduis le nombre de slides à la place.
- Tu ne crées pas de slide pour un contenu qui ne porte pas de message au lecteur.
