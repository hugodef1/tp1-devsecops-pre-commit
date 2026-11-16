Travail demandé
- Identifiez les problèmes de qualité du code.
le mdp est en clair dans le code
- Identifiez les risques de sécurité.
quelqu'un pourrait trouver ce code
- Expliquez pourquoi eval() est dangereux lorsqu'il est utilisé sur une entrée non fiable.
Car on peut répondre d'une formule comme 2+2 mais on peut également lancer une attaque qui s'executera avec les bons droits.
- Expliquez pourquoi un mot de passe ne doit pas être stocké dans le code source.
Parce que quelqu'un pourrait le récuperer.
- Proposez une première correction, sans installer encore de hook.
password = os.environ.get("APP_PASSWORD")
le mdp n'est plus en clair.
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

Le paquet concerné. python-dotenv
La version installée ou résolue. 1.2.4
L'identifiant de vulnérabilité, lorsqu'il est fourni.
La version corrigée disponible, si elle existe.
L'impact potentiel sur l'application.
L'action envisagée.Maintenir l'audit automatique dans pre-commit et en CI pour détecter toute future faille publiée, et verrouiller la version saine dans requirements.txt
