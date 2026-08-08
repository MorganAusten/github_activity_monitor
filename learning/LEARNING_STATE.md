# État d'apprentissage — GitHub Activity Monitor

Dernière mise à jour de migration : 2026-08-08.

## Contexte

L'utilisateur a environ 2 à 3 ans d'expérience en C++, C#, Unreal Engine et Unity.
Il connaît déjà :
- programmation orientée objet ;
- architecture/modularité de base ;
- débogage ;
- états/événements ;
- résolution de problèmes.

Son apprentissage backend Python a commencé depuis environ une semaine au moment de cette migration.

Rythme récent :
- généralement au moins 1 à 2 h par jour ;
- certaines journées jusqu'à 4 à 5 h.

## Autonomie observée

L'utilisateur estime avoir écrit environ 70 % du code lui-même.

Mode d'aide utilisé jusque-là :
- tickets de plus en plus autonomes ;
- tentative personnelle d'abord ;
- indices si nécessaire ;
- aide sur des fonctions/bibliothèques encore inconnues ;
- recommandations ponctuelles de structure et noms de fichiers ;
- revue de code et correction après tentative.

L'utilisateur pense pouvoir refaire globalement ce qu'il a déjà construit sans IA, mais :
- plus lentement ;
- avec probablement plusieurs erreurs ;
- avec besoin de diagnostic.

Interprétation : compréhension réelle en cours de consolidation ; éviter de confondre exposition et maîtrise.

## Évaluation objective — Contrôle 1

Note : 15/20.

### État par compétence

| Compétence | État actuel |
|---|---|
| Python général | intermédiaire en progression |
| PostgreSQL fondamental | en bonne acquisition |
| SQL | fondamentaux acquis, pratique encore limitée |
| Transactions | comprises conceptuellement |
| Migrations | bonne compréhension |
| Tests | bases solides, stratégie à développer |
| Architecture | bonne intuition, frontières à renforcer |
| Debug | fonctionnel, méthode systématique à renforcer |
| HTTP / API | commencé, à approfondir |
| Backend web | pas encore réellement abordé |
| Automatisation | premières briques, pas encore n8n/orchestration |
| IA via API | pas encore abordée sérieusement |
| Déploiement / monitoring | pas encore abordés |
| Valeur métier | bonne intuition, quantification à renforcer |
| Autonomie | en progression, encore accompagnée |

## Acquis relativement solides

### PostgreSQL — contraintes et idempotence
Comprend :
- `UNIQUE (repository_id, captured_at)` comme garantie d'intégrité au niveau base ;
- `ON CONFLICT (...) DO NOTHING` comme comportement applicatif face au doublon ;
- l'idée qu'on ne doit pas compter uniquement sur Python pour protéger l'intégrité.

### Transactions
Comprend qu'avec une transaction englobante :
- une migration précédente réussie peut être rollback si une migration suivante échoue ;
- les écritures dans `schema_migrations` sont également concernées ;
- la notion d'atomicité commence à être comprise.

### Migrations
Bonne compréhension :
- exécuter uniquement les migrations absentes ;
- enregistrer les migrations appliquées ;
- ne pas modifier une ancienne migration déjà appliquée en production ;
- créer une nouvelle migration pour une nouvelle évolution.

## En consolidation

### Architecture / frontières
Les responsabilités principales sont comprises :
- client PostgreSQL → connexion ;
- repository → écriture/suppression ;
- reader → lecture ;
- migration runner → évolution du schéma.

À renforcer :
- expliciter ce que chaque composant ne doit pas faire ;
- raisonner par frontière de responsabilité.

### Modèle Python ↔ SQL
Fragile :
- différence entre `str | None` et un argument réellement facultatif avec valeur par défaut ;
- conséquences d'un `SELECT` désynchronisé du modèle ;
- nombre et ordre des valeurs ;
- erreurs possibles : mauvais nombre d'arguments, décalage positionnel, `TypeError`, `IndexError`.

### Configuration
`.env` globalement compris.
`.venv` à consolider :
- environnement Python isolé ;
- interpréteur/packages/versions ;
- ce n'est pas ce qui choisit la base PostgreSQL.

### Debug
Bon réflexe général, mais manque de précision.
Compétence à renforcer :
- lire littéralement le message d'erreur ;
- extraire l'information avant de multiplier les hypothèses ;
- identifier la couche fautive ;
- reproduire de façon isolée ;
- vérifier la modification récente ;
- lancer d'abord le test ciblé.

### Tests d'intégration
Comprend `try/finally` pour garantir le nettoyage.
À renforcer :
- IDs uniques pour éviter l'interférence entre exécutions ;
- chaque test doit contrôler ses propres données ;
- réduire la dépendance à l'état préexistant.

### Valeur métier
Bonne intuition sur :
- utilisateur ;
- processus ;
- temps humain ;
- erreurs ;
- risques de décision.

À renforcer :
- transformer le résultat en métriques ;
- temps avant/après ;
- taux/catégorie d'erreurs ;
- complétude ;
- délai de disponibilité ;
- gain quantifiable.

## Flux système compris

API GitHub
→ requête/réponse HTTP
→ JSON
→ mapping vers `Repository`
→ filtrage / rapport
→ création de `RepositorySnapshot`
→ PostgreSQL
→ lecture / historique

Important : parler en termes de protocole.
Le `GitHubClient` encapsule l'échange HTTP ; il ne remplace pas conceptuellement HTTP/API.

Les migrations appartiennent à l'initialisation/évolution de l'environnement de données, pas au flux métier principal exécuté nécessairement à chaque traitement.

## Règle de mise à jour

Ne mettre une compétence en "acquise" qu'après preuve :
1. l'utilisateur peut l'expliquer ;
2. il peut modifier une implémentation ;
3. il peut diagnostiquer une panne ;
4. il peut transférer le principe à un autre cas.

Mettre à jour ce fichier seulement après une observation significative, pas après chaque petite réussite.
