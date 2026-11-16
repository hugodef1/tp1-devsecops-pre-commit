# TP1 — Sécuriser un dépôt Python avec les hooks `pre-commit`

## 1. Analyse initiale du code (`app.py`)

### Problèmes de qualité du code
* Le mot de passe est écrit en clair directement dans le code source (`password = "demo-secret-123"`) et la variable n'est même pas utilisée dans la fonction.
* Le module `os` est importé inutilement.

### Risques de sécurité
* **Fuite de secret (Hardcoded Secret) :** Toute personne ayant accès au dépôt Git, aux artefacts de build ou aux logs peut récupérer le mot de passe en clair.
* **Exécution de code arbitraire (RCE) :** L'utilisation de `eval()` sur une saisie utilisateur permet d'exécuter n'importe quelle commande Python sur la machine.

### Pourquoi `eval()` est-il dangereux sur une entrée non fiable ?
La fonction `eval()` interprète et exécute la chaîne de caractères saisie comme du véritable code Python. Si un utilisateur entre une expression simple comme `2 + 2`, cela fonctionne, mais un attaquant peut tout aussi bien injecter du code malveillant (ex. : `__import__('os').system(...)`) qui s'exécutera avec les droits du processus de l'application.

### Pourquoi un mot de passe ne doit-il pas être stocké dans le code source ?
Parce que le code source est versionné, partagé entre développeurs et souvent hébergé sur des plateformes distantes : un mot de passe inscrit en dur reste visible dans l'historique des commits et peut être récupéré et exploité par n'importe qui ayant accès au dépôt.

### Première correction proposée (avant mise en place des hooks)
Le mot de passe est retiré du code pour être lu via une variable d'environnement, et `eval()` est remplacé par `ast.literal_eval()` afin de n'autoriser que l'évaluation de structures de données simples :

```python
import ast
import os

def get_message():
    # Récupération sécurisée depuis l'environnement (si nécessaire)
    password = os.environ.get("APP_PASSWORD")

    user_input = input("Entrez une valeur ou expression littérale : ")
    try:
        # Évaluation sécurisée (uniquement chaînes, nombres, tuples, listes, dicts, booléens)
        result = ast.literal_eval(user_input)
        return f"Résultat : {result}"
    except (ValueError, SyntaxError):
        return "Entrée invalide ou non autorisée."
```

---

## 2. Audit des dépendances (`pip-audit`)

Résultat de l'analyse sur `requirements.txt` :

* **Paquet concerné :** `python-dotenv`
* **Version installée ou résolue :** `1.2.4`
* **Identifiant de vulnérabilité :** Aucun (aucune vulnérabilité connue détectée)
* **Version corrigée disponible :** Non applicable
* **Impact potentiel sur l'application :** Aucun risque connu identifié sur cette dépendance à ce jour.
* **Action envisagée :** Maintenir l'audit automatique dans `pre-commit` et en CI pour détecter toute future faille publiée, et verrouiller la version saine dans `requirements.txt`.

---

## 3. Adaptation des contrôles à NOVA SERVICES

### Réponses aux questions d'adaptation

1. **Contrôles communs à tous les dépôts :**
   Les contrôles d'hygiène générale et de prévention des fuites de données s'appliquent à tous les projets (API, outil d'administration, scripts) :
   * Détection des secrets (`detect-secrets`) pour bloquer l'ajout accidentel de mots de passe ou clés API.
   * Vérifications de formatage et d'intégrité (`trailing-whitespace`, `end-of-file-fixer`, `check-added-large-files`, `check-yaml`).

2. **Contrôles spécifiques à Python :**
   * Analyse statique de sécurité (SAST) avec **Bandit**.
   * Exécution des tests unitaires avec **pytest**.
   * Audit des vulnérabilités des dépendances avec **pip-audit**.
   * *(Optionnel)* Un formateur ou linter Python comme Ruff ou Black.

3. **Contrôles bloquants avant le commit :**
   Les vérifications rapides et critiques qui empêchent une erreur évidente d'entrer dans l'historique Git local :
   * `detect-secrets` (évite d'enregistrer un secret dans l'historique local).
   * `bandit` (détection rapide des failles critiques comme `eval()`).
   * Hooks de formatage (`check-yaml`, `check-added-large-files`, etc.).
   * Tests unitaires rapides (`pytest` sur les fonctions critiques).

4. **Contrôles exécutés uniquement en CI :**
   Les vérifications plus lentes, dépendantes du réseau ou trop lourdes pour le poste local :
   * Audit complet des dépendances (`pip-audit`), qui interroge des bases en ligne et peut ralentir les commits locaux.
   * Suites de tests longues (intégration, bout en bout, charge).
   * Analyses approfondies (scans d'images Docker, analyses SAST complètes).

5. **Éviter qu'une exception à `detect-secrets` ne masque un véritable secret :**
   * Exiger une revue humaine systématique (via Pull Request) pour toute modification du fichier `.secrets.baseline` ou tout commentaire `# pragma: allowlist secret`.
   * Justifier chaque exception (ex. : identifiant de test fictif) et interdire d'ajouter un vrai secret au baseline.
   * Imposer la révocation et le renouvellement immédiat de tout vrai secret découvert, puis sa suppression du code.

6. **Responsable de la mise à jour des versions des hooks :**
   Le **référent technique (Tech Lead)** ou le **référent DevSecOps / Sécurité** de l'équipe, via une mise à jour périodique et contrôlée (`pre-commit autoupdate`) testée avant déploiement sur la branche principale.

7. **Prouver qu'un développeur a corrigé une vulnérabilité :**
   * **Historique Git :** Un commit dédié référençant le correctif (mise à jour de version dans `requirements.txt` ou refactorisation du code).
   * **Logs de la pipeline CI :** Un rapport d'exécution réussi (`pre-commit run --all-files`, `pytest`, `pip-audit`) sur la Pull Request associée.
   * **Revue de code :** La validation par un pair avant la fusion sur `main`.

8. **Traiter une dépendance vulnérable sans correctif disponible :**
   * **Évaluer l'exploitabilité réelle :** Vérifier si la fonction vulnérable de la bibliothèque est réellement utilisée par l'application.
   * **Mettre en place des mesures compensatoires :** Filtrer strictement les entrées utilisateur en amont, restreindre l'accès réseau ou isoler le service.
   * **Remplacer la bibliothèque :** Migrer vers une alternative maintenue si le risque est trop élevé.
   * **Documenter l'acceptation temporaire du risque :** Enregistrer une exception formalisée, approuvée par le responsable sécurité, avec une date de réexamen régulière.

---

### Livrable complémentaire — Politique interne de sécurisation du code (NOVA SERVICES)

> **1. Contrôles obligatoires**  
> Tout dépôt applicatif doit embarquer à sa racine un fichier `.pre-commit-config.yaml` versionné intégrant : le contrôle de formatage et de taille des fichiers, la détection de secrets (`detect-secrets`), l'analyse statique de sécurité (`bandit` pour Python), l'exécution des tests unitaires (`pytest`) et l'audit des dépendances (`pip-audit`).
>
> **2. Répartition des contrôles (Local vs CI)**  
> * **En local (avant chaque commit) :** Formatage YAML/fins de ligne, taille des fichiers, `detect-secrets`, `bandit` et tests unitaires rapides.  
> * **En intégration continue (CI sur chaque Pull Request) :** Réexécution complète de `pre-commit run --all-files`, suite complète de tests (`pytest`) et audit des dépendances (`pip-audit`).
>
> **3. Conditions de blocage**  
> Tout échec sur la détection de secret, sur une vulnérabilité de sévérité moyenne ou haute détectée par Bandit (`-ll`), ou sur un test unitaire bloque immédiatement le commit local ainsi que la fusion de la Pull Request vers la branche `main`.
>
> **4. Traitement des faux positifs**  
> Lorsqu'un outil signale une alerte non pertinente (ex. : chaîne aléatoire de test dans `detect-secrets`), le développeur doit analyser l'alerte avant de l'ajouter au fichier `.secrets.baseline` ou d'utiliser une directive d'exclusion. Toute modification du baseline doit être justifiée dans la description de la Pull Request.
>
> **5. Responsable de la validation des exceptions**  
> Aucune exception de sécurité (contournement d'une règle SAST ou acceptation d'une dépendance vulnérable sans correctif) ne peut être validée par son auteur. Toute dérogation doit être examinée et approuvée par le Responsable Sécurité (RSSI / Référent DevSecOps) et fait l'objet d'un réexamen trimestriel.
>
> **6. Procédure de mise à jour des outils**  
> Les versions des hooks et des outils d'analyse sont épinglées dans `.pre-commit-config.yaml` et `requirements-dev.txt`. Le référent technique effectue une mise à jour mensuelle via `pre-commit autoupdate`, valide la non-régression sur l'ensemble du dépôt et soumet la mise à jour via une Pull Request dédiée.

---

## 4. Indicateurs de suivi de la sécurité

| Indicateur | Ce qu'il mesure | Source de données | Propriétaire | Fréquence | Seuil d'alerte & Action déclenchée |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Taux de dépôts configurés** | Part des dépôts actifs disposant d'un fichier `.pre-commit-config.yaml` à jour. | Plateforme Git (GitLab / GitHub API) | Référent DevSecOps | Mensuelle | **Seuil :** < 100 % des dépôts actifs.<br>**Action :** Déploiement du modèle standard sur les dépôts manquants. |
| **Taux de contrôles CI réussis** | Part des exécutions de pipelines CI terminées sans échec de sécurité ou de test. | Logs de la chaîne CI/CD | Tech Lead | Hebdomadaire | **Seuil :** < 85 % de réussite.<br>**Action :** Rappel sur l'installation locale (`pre-commit install`) ou sensibilisation de l'équipe. |
| **Nombre de secrets détectés** | Volume d'alertes remontées par `detect-secrets` à qualifier (vrais secrets vs faux positifs). | Rapports CI `detect-secrets` & commits sur `.secrets.baseline` | Responsable Sécurité | Hebdomadaire | **Seuil :** ≥ 1 vrai secret détecté.<br>**Action :** Révocation immédiate du secret, purge de l'historique Git et sensibilisation. |
| **Nombre de vulnérabilités de dépendances ouvertes** | Volume de CVE identifiées par `pip-audit` restant à corriger. | Rapports CI `pip-audit` | Tech Lead / Sécurité | Hebdomadaire | **Seuil :** > 0 faille Critique ou Haute.<br>**Action :** Création d'un ticket prioritaire de mise à jour de dépendance. |
| **Délai médian de correction** | Temps écoulé entre la détection d'une vulnérabilité et la validation de son correctif. | Gestionnaire de tickets & historique Git | Responsable Sécurité | Mensuelle | **Seuil :** > 7 jours (Critique) ou > 30 jours (Moyenne).<br>**Action :** Escalade auprès des chefs de projet pour planifier la remédiation. |
| **Nombre d'exceptions actives** | Nombre de dérogations (baseline ou dépendances non corrigées) encore actives. | Registre des exceptions & `.secrets.baseline` | Responsable Sécurité | Trimestrielle | **Seuil :** Augmentation continue ou exception > 3 mois.<br>**Action :** Revue obligatoire pour confirmer le maintien ou exiger la suppression de l'exception. |

---

## 5. Questions de compréhension

1. **Qu'est-ce qu'un hook `pre-commit` ?**  
   C'est un script automatisé déclenché par Git juste avant la création d'un commit local. Il vérifie le code modifié (formatage, sécurité, tests) et bloque le commit si l'un des contrôles échoue.

2. **Quelle différence existe-t-il entre un contrôle local et un contrôle CI ?**  
   Le **contrôle local** s'exécute sur le poste du développeur avant le commit ; il offre un retour immédiat mais peut être désactivé ou contourné (par exemple avec `--no-verify` ou `core.hooksPath=/dev/null`). Le **contrôle CI** s'exécute sur un serveur centralisé lors de l'envoi du code (Push / Pull Request) ; il est obligatoire, non contournable et garantit que tout le code intégré respecte les règles de sécurité.

3. **Pourquoi faut-il versionner `.pre-commit-config.yaml` ?**  
   Versionner ce fichier dans Git permet de partager exactement les mêmes règles et versions d'outils avec toute l'équipe de développement ainsi qu'avec le serveur d'intégration continue (CI), garantissant ainsi la reproductibilité des contrôles.

4. **Pourquoi `detect-secrets` peut-il produire des faux positifs ?**  
   Parce qu'il s'appuie sur des expressions régulières (mots-clés comme `password`, `token`) et sur le calcul d'entropie (chaînes de caractères très aléatoires). Il peut donc signaler par erreur un identifiant technique, un hash de test ou une chaîne aléatoire qui n'est pas un véritable secret.

5. **Pourquoi un baseline ne doit-il pas servir à ignorer des secrets réels ?**  
   Le fichier `.secrets.baseline` est versionné et lisible dans le dépôt Git. Y inscrire un vrai secret ne fait que masquer l'alerte tout en laissant le secret exposé dans le code et dans l'historique Git ; un vrai secret doit impérativement être supprimé du code et révoqué.

6. **Quel risque présente l'utilisation de `eval()` sur une entrée non fiable ?**  
   `eval()` interprète et exécute la chaîne fournie comme du code Python. Si l'entrée provient d'un utilisateur malveillant, celui-ci peut injecter des commandes système arbitraires (exécution de code à distance / RCE), lire des fichiers sensibles ou compromettre le serveur.

7. **Pourquoi un fichier `.env` doit-il être exclu du dépôt ?**  
   Le fichier `.env` contient les véritables valeurs sensibles (mots de passe, clés API) propres à l'environnement local d'exécution. L'exclure via `.gitignore` empêche sa publication sur le dépôt distant et évite la fuite des identifiants.

8. **Pourquoi le fait de déplacer un secret dans une variable d'environnement ne suffit-il pas à sécuriser sa gestion ?**  
   Bien que cela retire le secret du code source, une variable d'environnement reste lisible en clair par tous les processus enfants, peut fuiter dans les logs d'erreur ou les dumps mémoire, et n'offre ni chiffrement au repos, ni contrôle d'accès fin, ni rotation automatique (contrairement à un coffre-fort de secrets comme HashiCorp Vault ou AWS Secrets Manager).

9. **Quelle différence existe-t-il entre une analyse de code et un audit des dépendances ?**  
   * **Analyse de code (SAST, ex. : Bandit) :** Inspecte le code source écrit par les développeurs de l'entreprise pour détecter des failles de programmation (ex. : `eval()`, injections SQL).
   * **Audit des dépendances (SCA, ex. : `pip-audit`) :** Vérifie les bibliothèques tierces importées dans le projet afin d'identifier si leurs versions contiennent des vulnérabilités publiques connues (CVE).

10. **Pourquoi faut-il exécuter les tests dans la CI même si un hook local existe ?**  
    Un développeur peut oublier d'installer les hooks (`pre-commit install`), contourner leur exécution locale, ou disposer d'un environnement local différent de la production. La CI garantit que les tests sont systématiquement exécutés dans un environnement propre et isolé avant toute intégration.

11. **Comment empêcher réellement les pushes directs sur `main` ?**  
    Il faut configurer des **règles de protection de branche** directement côté serveur sur la plateforme Git (GitHub / GitLab) : interdire les pushes directs sur `main`, imposer le passage par une Pull Request / Merge Request, exiger la réussite des contrôles CI et demander au moins une approbation de revue de code.

12. **Quels indicateurs permettraient de suivre l'efficacité du dispositif ?**  
    On peut suivre le taux de dépôts équipés de hooks, le taux de réussite des pipelines CI, le nombre de secrets détectés, le volume de vulnérabilités ouvertes sur les dépendances, le délai médian de correction des failles et le nombre d'exceptions actives.
