# Bibliothèque Virtuelle

Un système de gestion de bibliothèque en ligne de commande permettant d'acheter et lire des livres virtuels.

## Fonctionnalités

- Création de livres
- Listage des livres disponibles
- Mise à jour des informations des livres
- Suppression de livres
- Affichage des détails d'un livre
- Achat de livres
- Lecture des livres achetés

## Configuration

### Prérequis

- Python 3.8 ou supérieur
- Package `colorama` pour l'interface colorée

### Installation

1. Créez un environnement virtuel :
```bash
python -m venv env
```

2. Activez l'environnement virtuel :
```bash
# Sur Unix/MacOS
source env/bin/activate

# Sur Windows
env\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install colorama
```

## Structure du Projet

Le projet est organisé autour de trois classes principales :

- `Book` : Représente un livre avec ses attributs (titre, auteur, contenu)
- `Lib` : Gère la collection de livres et leurs opérations CRUD
- `BookShop` : Interface utilisateur et logique d'interaction

## Utilisation

1. Lancez le programme :
```bash
python bib.py
```

2. Menu des commandes :
- `1` : Créer un livre
- `2` : Lister les livres
- `3` : Mettre à jour un livre
- `4` : Supprimer un livre
- `5` : Afficher le détail d'un livre
- `6` : Acheter un livre
- `7` : Lire un livre
- `q` : Quitter

## Interface

L'interface utilise les couleurs suivantes :
- 🟢 Vert : Succès et commandes disponibles
- 🔴 Rouge : Erreurs et livres non disponibles
- 🔵 Bleu : Bordures décoratives
- 🟡 Jaune : Prompts et texte important
- 🔶 Cyan : Titres et informations

## Caractéristiques Techniques

- Encapsulation des données avec des attributs privés
- Gestion des erreurs pour les entrées invalides
- Interface utilisateur interactive et colorée
- Système de gestion d'état pour les livres (disponible/acheté)
- Formatage automatique du texte pour la lecture

## Licence

Ce projet est sous licence libre.