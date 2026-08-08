# Point exact de reprise

## Situation

Le dernier contrôle a identifié trois zones prioritaires à consolider avant de poursuivre la roadmap :

1. contrat données ↔ code ;
2. diagnostic ;
3. valeur métier.

Le mentor précédent avait explicitement décidé de ne pas continuer à empiler PostgreSQL et de ne pas sauter vers FastAPI/n8n/IA avant cette consolidation.

## Ticket actuel — unique

Reprendre les questions 4, 7 et 9 du Contrôle 1 et demander à l'utilisateur de les reformuler avec ses propres mots, sans recopier la correction.

### Question 4 — Modèle / SQL

Contexte :
`RepositorySnapshot` reçoit un champ :

```python
description: str | None
```

mais le `SELECT` reste :

```sql
SELECT repository_id, owner, name, language, stars, captured_at
```

Objectif :
- expliquer les problèmes possibles ;
- décrire le diagnostic ;
- vérifier la compréhension de `str | None` vs argument facultatif ;
- raisonner sur nombre et ordre des colonnes/arguments.

### Question 7 — Debug

Erreur :

```text
psycopg.OperationalError:
failed to resolve host 'POSTGRES_HOST'
```

Objectif :
- demander l'hypothèse principale ;
- demander comment la vérifier ;
- vérifier que l'utilisateur exploite littéralement le message d'erreur.

Point à faire émerger :
Psycopg essaie réellement de résoudre un hôte nommé `POSTGRES_HOST`, ce qui suggère notamment que le nom de la variable d'environnement a pu être passé au lieu de sa valeur.

### Question 9 — Valeur métier

Cas :

> Chaque matin, quelqu'un copie les statistiques GitHub de 80 dépôts dans Excel. Cela prend environ 45 minutes et il y a régulièrement des erreurs.

Demander d'identifier :
- utilisateur ;
- processus actuel ;
- coût/perte ;
- risques ;
- résultat attendu ;
- mesure de succès.

Objectif de consolidation :
la mesure de succès ne doit pas rester vague ; elle doit devenir observable et si possible quantifiée.

## Comportement du mentor

Ne pas redonner immédiatement les réponses ci-dessus.

Commencer par demander à l'utilisateur de répondre de nouveau aux trois questions avec ses mots.
Analyser ensuite sa réponse.
Donner des indices uniquement si nécessaire.
Une fois les trois notions suffisamment consolidées, mettre à jour `LEARNING_STATE.md` et définir UN seul prochain objectif basé sur le repo réel.

## Critère de sortie de ce ticket

On peut passer à la suite si l'utilisateur montre qu'il peut :
- prévoir un décalage modèle/SQL et diagnostiquer sa cause ;
- extraire une hypothèse précise d'un message d'erreur ;
- proposer au moins une mesure de succès concrète pour un processus métier automatisé.
