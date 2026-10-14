# Logical writing : règles d'écriture appliquées à chaque phrase

Ces règles codifient la pratique de rédaction de conseil de l'auteur du projet. Aucune méthode publiée ne porte ce nom ; le socle sourcé reste Minto (`minto.md`). Elles s'appliquent à tout texte produit par l'équipe : titres, blocs, notes, livrables intermédiaires.

## Structure
1. **Chaque paragraphe, bloc ou section répond à une question.** Si on ne peut pas formuler la question, le bloc n'a pas de raison d'être.
2. **Chaque titre de paragraphe, de bloc ou de graphique contient l'idée principale de ce qu'il surmonte.** Le texte dessous détaille cette idée. « Coûts » est une étiquette ; « Les coûts de conformité doublent en trois ans » est une idée.
3. **Idée, analyse, conclusion.** Une phrase porte une seule affirmation.
4. **Réponse d'abord.** La conclusion précède les arguments, à chaque niveau.

## Phrase
5. **Voix active, toujours.** Le sujet fait l'action. « La banque réduit ses délais » et non « Les délais sont réduits ». Si l'acteur est inconnu, cherche-le ; s'il reste inconnu, dis-le.
6. **Chaque mot sert.** Retire ce qui ne change pas le sens.
7. **Pas d'adverbe de modulation** : seulement, uniquement, déjà, désormais, maintenant, plus de, juste, vraiment, très, et leurs équivalents anglais (only, now, already, more than). Ils affaiblissent l'affirmation. Un chiffre précis remplace « plus de ».
8. **Pas de tournure « ne pas X mais Y » ni « non pas X mais Y ».** Affirme Y.
9. **Pas de tiret long ni de demi-cadratin.** Une virgule, un point ou deux phrases.
10. **Pas d'échafaudage rhétorique** ni d'intensif creux (« il est essentiel de noter que », « véritable », « clé »).
11. **Vocabulaire simple, dans le registre du lecteur.** Pas de jargon qu'il n'emploie pas.

## Titres de slides
12. Une phrase affirmative, complète, éventuellement longue. Pas de point-virgule, pas d'incise, pas de question, pas de sous-titre : s'il faut un sous-titre, le titre n'est pas bon.
13. Le titre porte la conclusion ou la tension, jamais le sujet.
14. Hiérarchie limitée à trois niveaux : titre de slide, titre de bloc, texte ou liste.

## Chiffres
15. Tout chiffre renvoie à une source nommée, avec son unité, son périmètre et sa date.
16. Aucun ratio, prix ou total reconstitué présenté comme une donnée.

## Exemples de réécriture

| Avant | Après | Règle |
|---|---|---|
| Une refonte du processus KYC a été engagée | La banque refond son processus KYC | 5 |
| Ce n'est pas un sujet technique mais un sujet d'organisation | Le sujet relève de l'organisation | 8 |
| Synthèse des enjeux | Trois enjeux réglementaires imposent une décision avant juin | 2, 13 |
| Les coûts représentent déjà plus de 20 % du budget | Les coûts représentent 23 % du budget (source, 2025) | 7, 15 |
| Contexte : forte croissance ; risques multiples | Le marché croît de 12 % par an et expose la banque à trois risques | 12 |

## Contrôle automatique
`scripts/lint_storyboard.py` détecte une partie de ces défauts (voix passive probable, adverbes, tirets, points-virgules, titres de blocs réduits à une étiquette, chiffres sans source). Il ne remplace pas la relecture : le passif français prend des formes qu'une expression régulière manque, et un titre peut respecter toutes les règles sans porter d'idée.
