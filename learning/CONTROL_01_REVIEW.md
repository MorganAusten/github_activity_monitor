Tu as une compréhension réelle du système, mais certains points sont encore compris “par comportement observé” plutôt que par contrat précis entre les composants. C’est exactement ce que ce contrôle devait révéler.

## Note : **15 / 20**

Le niveau est bon pour l’étape actuelle. Tu n’es pas encore autonome sur tous les diagnostics backend, mais PostgreSQL, transactions et migrations commencent à être compris plutôt qu’appliqués mécaniquement.

| Question         |    Note | Évaluation                                                                                      |
| ---------------- | ------: | ----------------------------------------------------------------------------------------------- |
| 1. Architecture  | 1.5 / 2 | Responsabilités comprises, mais tu n’as pas donné ce que chaque composant **ne doit pas faire** |
| 2. PostgreSQL    |   2 / 2 | Très bon                                                                                        |
| 3. Transaction   |   2 / 2 | Correct                                                                                         |
| 4. Modèle / SQL  |   1 / 2 | Tu identifies le décalage, mais pas précisément le comportement Python                          |
| 5. Configuration | 1.5 / 2 | `.env` compris, `.venv` à préciser                                                              |
| 6. Migrations    |   3 / 3 | Très bon raisonnement                                                                           |
| 7. Debug         |   1 / 2 | Bonne piste, mais ton diagnostic exact n’est pas celui indiqué par l’erreur                     |
| 8. Tests         | 1.5 / 2 | `finally` compris, identifiants uniques oubliés                                                 |
| 9. Métier        |   1 / 2 | Bonne analyse du problème, mauvaise définition de la mesure de succès                           |
| 10. Autonomie    | 0.5 / 1 | Bonne attitude, mais procédure trop vague                                                       |

### 1. Architecture — plutôt acquis

Tes responsabilités sont correctes.

Par exemple :

```text
postgresql_client
→ établir une connexion

snapshot_repository
→ écrire/supprimer des snapshots

snapshot_reader
→ lire les snapshots

migration_runner
→ maintenir le schéma à la bonne version
```

Ce qui manquait était la notion de **frontière de responsabilité**.

Par exemple, `postgresql_client.py` ne devrait pas connaître `snapshot_repository`. Le reader ne devrait pas créer les tables. Le migration runner ne devrait pas récupérer les dépôts GitHub.

C’est important parce qu’en architecture, savoir ce qu’un composant **ne fait pas** est presque aussi important que savoir ce qu’il fait.

### 2. `UNIQUE` + `ON CONFLICT` — acquis

Ta réponse est bonne.

Tu as compris les deux niveaux :

```text
UNIQUE
→ la base garantit l'intégrité

ON CONFLICT DO NOTHING
→ l'application définit quoi faire lorsqu'un doublon est détecté
```

Et surtout ton observation sur le rollback est pertinente : sans gestion du conflit, une violation de contrainte ferait échouer la transaction.

C’est une notion backend importante : **ne pas compter uniquement sur le code Python pour garantir l’intégrité des données**.

### 3. Transactions — acquis

Ta réponse :

> toute l'opération est annulée, donc aussi 003

est correcte avec notre structure actuelle.

C’est même un point subtil.

Avec une seule transaction :

```text
003 réussit
INSERT 003 réussit
004 échoue
        ↓
ROLLBACK
        ↓
003 annulée
INSERT 003 annulé
004 annulée
```

Donc la base revient à son état précédent.

Tu commences ici à raisonner en termes d’**atomicité**, même si on n’a pas encore beaucoup utilisé ce terme.

### 4. Modèle Python ↔ SQL — fragile

Tu as identifié le risque général, mais il faut être plus précis.

Si le modèle devient :

```python
RepositorySnapshot(
    repository_id,
    owner,
    name,
    language,
    description,
    stars,
    captured_at,
)
```

mais que le `SELECT` retourne toujours seulement :

```text
repository_id
owner
name
language
stars
captured_at
```

alors Python ne va pas magiquement mettre :

```python
description = None
```

Le type :

```python
str | None
```

signifie :

> la valeur peut être une `str` ou `None`.

Il ne signifie pas :

> cet argument est facultatif.

Pour qu'il soit facultatif à la construction, il faudrait une valeur par défaut, par exemple `description: str | None = None`, avec les contraintes d’ordre propres aux dataclasses.

Avec notre mapping positionnel, tu pourrais surtout avoir :

* mauvais nombre d’arguments ;
* `stars` placé dans `description` ;
* `captured_at` placé dans `stars` ;
* `IndexError` selon la façon dont tu lis le tuple ;
* `TypeError` à la construction.

Ton bon réflexe était cependant :

> regarder le nombre et la position des valeurs.

À conserver.

### 5. `.venv` / `.env` — presque acquis

Ta définition du `.env` est bonne.

Pour `.venv`, cette partie est à corriger :

> s'assurer que notre programme est exécuté depuis le bon endroit

Ce n’est pas vraiment ça.

Le `.venv` isole **l’environnement Python du projet** :

```text
version/interpréteur Python
+
packages installés
+
leurs versions
```

Par exemple :

```text
psycopg
pytest
requests
python-dotenv
```

Le `.venv` lui-même n’est généralement pas envoyé sur Git non plus. Sur une autre machine, on le recrée puis on réinstalle les dépendances.

Et pour choisir la base :

```text
.env
↓
POSTGRES_DB=...
↓
os.getenv("POSTGRES_DB")
↓
psycopg.connect(dbname=...)
↓
base utilisée
```

Ce n’est donc pas le `.venv` qui sélectionne PostgreSQL.

### 6. Migrations — très bien acquis

C’est une de tes meilleures réponses.

Tu as correctement identifié :

```text
base : 000 → 003
repo : 000 → 005

donc :
→ exécuter 004
→ enregistrer 004
→ exécuter 005
→ enregistrer 005
```

Et tu as donné deux bonnes raisons de ne pas modifier une vieille migration :

1. elle est déjà enregistrée comme appliquée ;
2. les migrations suivantes peuvent dépendre de l’état qu’elle avait créé.

Il y en a une troisième importante : deux installations pourraient alors avoir toutes deux `"002"` enregistrée, mais **des schémas différents**.

C’est catastrophique à diagnostiquer.

Donc :

```text
migration appliquée
→ on ne la réécrit plus
→ nouvelle modification = nouvelle migration
```

Très bon acquis.

### 7. Diagnostic de `failed to resolve host 'POSTGRES_HOST'` — partiellement acquis

Tu as pensé au `.env`, ce qui est pertinent.

Mais lis littéralement l’erreur :

```text
failed to resolve host 'POSTGRES_HOST'
```

Elle dit que Psycopg essaie réellement de contacter une machine appelée :

```text
POSTGRES_HOST
```

Donc mon hypothèse principale serait :

> j’ai passé le **nom de la variable d’environnement** au lieu de sa valeur.

Typiquement :

```python
postgres_host = "POSTGRES_HOST"
```

au lieu de :

```python
postgres_host = os.getenv("POSTGRES_HOST")
```

Si la variable était simplement absente, avec notre validation actuelle on devrait normalement obtenir notre `ValueError` avant d’arriver ici.

C’est une compétence de debug à renforcer : **exploiter chaque mot du message d’erreur avant de chercher au hasard**.

### 8. Tests d’intégration — presque acquis

Ton explication du `finally` est correcte :

```text
test réussi → nettoyage
test échoué → nettoyage quand même
```

Ce qui manquait : pourquoi générer des IDs uniques.

Supposons qu’un ancien test ait crashé avant son cleanup et laissé :

```text
repository_id = 123
```

Si le prochain test réutilise `123`, il dépend de données provenant d’une exécution précédente.

Avec un ID généré pour chaque test :

```text
test A → ID 178603...
test B → ID 178604...
```

ils interfèrent beaucoup moins entre eux.

Le principe est :

> un test doit contrôler ses propres données et dépendre le moins possible de l’état préexistant.

### 9. Valeur métier — bon début, mais un point essentiel manque

Ton analyse utilisateur/processus/risques est bonne.

Tu as notamment compris que le coût ne se limite pas à 45 minutes :

```text
temps humain
+
erreurs potentielles
+
décisions basées sur de mauvaises données
```

Très important pour ton futur positionnement freelance.

Mais ici :

> mesure de succès : ça dépend de quelqu'un

ce n’est pas une mesure de succès.

Il fallait transformer le problème en indicateurs mesurables.

Par exemple :

```text
Temps avant :
45 minutes / jour

Temps après :
5 minutes de vérification humaine

Gain :
40 minutes / jour

Fiabilité :
80/80 dépôts traités

Erreurs de copie :
0 erreur manuelle de transcription

Disponibilité :
rapport prêt avant 9h
```

C’est précisément là que tu passes de :

> « j’ai fait un script Python »

à :

> « j’ai réduit de 89 % le temps consacré à cette tâche et supprimé une catégorie d’erreurs manuelles ».

C’est central pour ton objectif freelance.

### 10. Diagnostic autonome — raisonnement correct mais trop abstrait

Ta stratégie :

> localiser → comprendre → corriger → retester

est saine.

Mais un développeur backend autonome doit transformer ça en procédure concrète.

Par exemple :

```text
1. Lire la traceback et trouver la première erreur utile.
2. Identifier la couche : configuration, connexion, SQL, mapping, application.
3. Reproduire le problème isolément.
4. Vérifier la modification récente et l'état PostgreSQL/migrations.
5. Corriger puis lancer le test ciblé avant toute la suite pytest.
```

Dire seulement « je cherche où ça plante » est encore trop général.

---

## Ton niveau actuel par compétence

| Compétence               | État actuel                                            |
| ------------------------ | ------------------------------------------------------ |
| Python général           | **intermédiaire en progression**                       |
| PostgreSQL fondamental   | **en bonne acquisition**                               |
| SQL                      | **fondamentaux acquis, pratique encore limitée**       |
| Transactions             | **comprises conceptuellement**                         |
| Migrations               | **bonne compréhension**                                |
| Tests                    | **bases solides, stratégie de test à développer**      |
| Architecture             | **bonne intuition, frontières à renforcer**            |
| Debug                    | **fonctionnel, manque encore de méthode systématique** |
| HTTP / API               | **déjà commencé, à approfondir**                       |
| Backend web              | **pas encore réellement abordé**                       |
| Automatisation           | **premières briques, pas encore n8n/orchestration**    |
| IA via API               | **pas encore abordée sérieusement**                    |
| Déploiement / monitoring | **pas encore abordés**                                 |
| Valeur métier            | **bonne intuition, quantification à renforcer**        |
| Autonomie                | **en progression, encore besoin d’accompagnement**     |

Donc non, on n’est évidemment pas encore à « expert backend automation IA ». Mais **le parcours reste cohérent avec cet objectif**.

Ce que je veux éviter maintenant, c’est de continuer à empiler PostgreSQL pendant 30 heures. On a appris suffisamment de stockage pour continuer à faire évoluer le système et rencontrer de nouveaux problèmes réels.

### Ton seul prochain objectif

Je veux que tu corriges uniquement les **questions 4, 7 et 9** avec ce que tu viens de comprendre, sans recopier mes formulations.

Ce sont les trois domaines que ce contrôle révèle comme les plus intéressants à consolider : **contrat données/code, diagnostic, valeur métier**.
