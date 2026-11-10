# Assistant IA local pour documents hospitaliers

Prototype d'assistant qui répond aux questions d'agents d'un établissement de santé **à partir de ses documents internes**, avec un modèle de langage qui tourne **en local** (aucune donnée ne quitte l'ordinateur), un **contrôle d'accès par rôle** et un **journal d'audit**.

> **Projet de démonstration.** Tous les documents et toutes les « données patients » sont **fictifs** (créés pour l'occasion). Aucune donnée réelle n'est utilisée. Ce n'est pas un dispositif médical et il n'a pas été validé juridiquement.

## Ce que fait le projet

| Fonction | Principe |
|---|---|
| **IA locale** | Modèle open source servi par [Ollama](https://ollama.com) sur le poste. Aucune API externe. |
| **Recherche documentaire (RAG)** | Recherche BM25 dans les documents, puis réponse du modèle limitée aux extraits retrouvés, avec citation de la source. |
| **Contrôle d'accès** | Deux rôles (`stagiaire`, `referent`). Le filtre est appliqué **avant** la recherche : un document réservé n'atteint jamais le modèle. |
| **Abstention** | Si rien de pertinent n'est trouvé, le modèle n'est pas appelé et l'assistant le dit, au lieu d'inventer. |
| **Journal d'audit** | Chaque question est enregistrée (rôle, sources, durée, modèle) dans une base SQLite. |
| **Pseudonymisation** | Démonstration sur des comptes rendus fictifs : noms, NIR, téléphones, e-mails, dates remplacés par des jetons. |
| **Évaluation** | 12 questions avec mesure : bon document retrouvé, information présente, source citée, abstention, fuite. |

Aucune bibliothèque externe : Python et Ollama suffisent.

## Installation (Windows, PowerShell)

1. Installer [Ollama](https://ollama.com), puis télécharger un petit modèle : `ollama pull qwen2.5:1.5b`
2. Dans le dossier du projet :

```powershell
python test_assistant.py                                   # 11 tests, sans Ollama
python ask.py stagiaire "Combien de caractères pour un mot de passe ?"
python ask.py referent                                     # mode conversation
python ask.py --audit                                      # derniers échanges
python pseudonymize.py                                     # démonstration de pseudonymisation
python evaluate.py                                         # évaluation complète -> evaluation_<modèle>_<prompt>.md
python evaluate.py --no-llm                                # évaluation de la recherche seule
```

Pour tester la variante 2 du prompt : `$env:RAG_PROMPT = "v2"`. Pour changer de modèle : `$env:OLLAMA_MODEL = "llama3.2:3b"` (variables d'environnement, sans modifier le code).

## Architecture

```
question + rôle
      │
      ▼
 filtre d'accès (rôle → niveaux de confidentialité autorisés)
      │
      ▼
 recherche BM25 (retrieval.py)  ──► rien de pertinent ? → « je ne trouve pas » (le modèle n'est pas appelé)
      │
      ▼
 prompt = consignes + extraits autorisés  ──► Ollama (llm.py, local)
      │
      ▼
 réponse + sources  ──► journal d'audit (audit.py)
```

## Adapter à un autre établissement

Remplacer les fichiers de `data/documents/` (en-tête `Titre`, `Accès: public` ou `restreint`, puis le texte), adapter `data/eval_questions.json`, et choisir le modèle adapté au matériel disponible.

## Résultats de l'évaluation

Mesures sur 10 questions avec réponse et 2 questions sans réponse permise, sur un PC portable de 2015 (8 Go de RAM, sans carte graphique), avec le modèle `qwen2.5:1.5b` servi par Ollama. Les rapports complets, réponses du modèle comprises, sont dans les fichiers `evaluation_*.md`.

| Modèle | Prompt | Document retrouvé | Information correcte | Source citée par le modèle | Abstention correcte | Fuites d'information réservée | Durée moyenne |
|---|---|---|---|---|---|---|---|
| qwen2.5:1.5b | v1 (consigne seule) | 10/10 | 9/10 | 4/10 | 2/2 | 0 | 6,7 à 8,0 s |
| qwen2.5:1.5b | v2 (consigne + un exemple de citation) | 10/10 | 10/10 | 6/10 | 1/2 | 0 | 7,9 à 9,0 s |

Deux exécutions successives du prompt v2 ont donné exactement les mêmes scores. La première requête est plus longue (environ 24 s), car le modèle doit se charger en mémoire.

### Ce que ces mesures montrent

- **La recherche fonctionne** : le bon document est retrouvé dans 10 cas sur 10, et le filtre d'accès n'a laissé passer aucun document réservé.
- **Ajouter un exemple au prompt (v2) améliore la citation des sources (4 à 6 sur 10) et l'exactitude (9 à 10 sur 10), mais dégrade l'abstention (2 sur 2 à 1 sur 2).**
- **Erreur observée** : à la question « Quel est le poste du chef du service informatique ? » posée avec le rôle `stagiaire` (qui n'a pas accès à l'annuaire), le modèle v2 répond « 4500, [incident_securite] ». Ce numéro est celui de la ligne d'assistance en cas d'incident, pas celui du chef de service. Il n'y a pas de fuite (la bonne réponse est dans un document réservé), mais c'est une réponse fausse, présentée avec une source. Une citation ne garantit donc pas qu'une réponse est correcte : c'est pourquoi l'assistant affiche les extraits sources, pour que l'utilisateur vérifie.
- **Limite de la mesure** : 12 questions seulement, et les réglages ont été comparés sur ces mêmes questions. Ces chiffres montrent une tendance sur ce prototype, pas une performance générale.

## Limites connues

- **Petits modèles** : un modèle de 1 à 3 milliards de paramètres, sur un PC sans carte graphique, est lent et se trompe plus souvent en français. L'évaluation sert à mesurer ces erreurs, pas à les cacher. Un établissement utiliserait un serveur adapté.
- **Recherche par mots-clés** : BM25 ne comprend pas les synonymes. Piste : comparer avec une recherche sémantique (embeddings) et mesurer le gain.
- **Pseudonymisation par règles** : elle ne détecte pas les noms sans titre (« M. », « Mme », « Dr »). Piste : la compléter par un modèle de reconnaissance d'entités et un contrôle humain.
- **Rôles** : le rôle est choisi en ligne de commande. En production : authentification et annuaire de l'établissement.
- **Évaluation** : 12 questions, vérification des réponses par mots-clés. Insuffisant pour juger la qualité réelle ; une validation par des référents métier serait nécessaire.
- **Cadre réglementaire** : projet technique réalisé par une étudiante, sans validation juridique (RGPD, secret médical, hébergement de données de santé).

## Auteure

Sharyn Janice Djiodop Foka · [LinkedIn](https://www.linkedin.com/in/sharyn-foka) · [GitHub](https://github.com/Sharynjanice) · [Portfolio](https://portfoliosharyn.vercel.app)