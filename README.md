# Ranking : Outil de recherche en Python

Il s'agit d'un moteur de recherche de documents qui utilise l'algorithme BM25 pour récupérer des documents pertinents en fonction de la requête de l'utilisateur. Il prend en charge les opérateurs AND et OR pour combiner les termes de la requête.

## Installation

Installez les dépendances requises à l'aide de pip :

    ```
    pip install -r requirements.txt
    ```

## Utilisation

1. Assurez-vous que vos documents sont indexés et prêts. Les documents doivent être au format JSON.
2. Définissez vos fichiers d'index et leurs coefficients associés dans le dictionnaire `index_files` dans le fichier `main.py`.
3. Exécutez le fichier `main.py` :

    ```
    python main.py
    ```

4. Entrez votre requête lorsqu'on vous le demande. Vous pouvez utiliser les opérateurs AND ou OR pour combiner les termes de la requête.
5. Visualisez les résultats affichés dans la console.

## Fonctionnalités

- Algorithme BM25 pour le classement des documents.
- Prise en charge des opérateurs AND et OR dans les requêtes.
- Fichiers d'index et coefficients personnalisables.