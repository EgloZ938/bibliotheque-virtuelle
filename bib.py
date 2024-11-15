# Import des modules nécessaires
from colorama import init, Fore, Back, Style  # Pour les couleurs dans le terminal
import os      # Pour les opérations système (clear screen)
import time    # Pour les délais d'affichage

# Initialisation de colorama pour les couleurs dans le terminal
init()

class Book:
    """
    Classe représentant un livre.
    Gère les informations et l'état d'un livre dans la bibliothèque.
    """
    def __init__(self, name, author, content):
        """
        Initialise un nouveau livre avec ses attributs de base.
        Tous les attributs sont privés pour l'encapsulation.
        """
        self.__name = name            # Titre du livre
        self.__author = author        # Auteur du livre
        self.__content = content      # Contenu/texte du livre
        self.__available = True       # État de disponibilité (True = disponible à l'achat)

    # Propriétés pour accéder aux attributs privés en lecture seule
    @property
    def name(self):
        """Retourne le titre du livre"""
        return self.__name
    
    @property
    def author(self):
        """Retourne l'auteur du livre"""
        return self.__author
    
    @property
    def content(self):
        """Retourne le contenu du livre"""
        return self.__content
    
    @property
    def available(self):
        """Retourne l'état de disponibilité du livre"""
        return self.__available
    
    def set_availability(self, status):
        """Modifie l'état de disponibilité du livre"""
        self.__available = status

    def __str__(self):
        """
        Retourne une représentation textuelle du livre avec des couleurs.
        Rouge pour les livres achetés, Vert pour les disponibles.
        """
        status = f'{Fore.RED}(Déjà acheté){Style.RESET_ALL}' if not self.__available else f'{Fore.GREEN}(Disponible){Style.RESET_ALL}'
        return f"{Fore.CYAN}'{self.__name}'{Style.RESET_ALL} par {Fore.YELLOW}{self.__author}{Style.RESET_ALL} {status}"

class Lib:
    """
    Classe gérant la bibliothèque.
    Stocke et gère la collection de livres.
    """
    def __init__(self):
        """Initialise une nouvelle bibliothèque vide"""
        self.__books = {}            # Dictionnaire des livres {id: Book}
        self.__current_id = 1        # Compteur pour générer les IDs uniques
    
    def add_book(self, name, author, content):
        """
        Ajoute un nouveau livre à la bibliothèque.
        Retourne l'ID attribué au livre.
        """
        book = Book(name, author, content)
        self.__books[self.__current_id] = book
        self.__current_id += 1
        return self.__current_id - 1

    def list_books(self):
        """Retourne un dictionnaire de tous les livres avec leur ID"""
        return {id: str(book) for id, book in self.__books.items()}

    def get_book(self, book_id):
        """Récupère un livre par son ID. Retourne None si non trouvé."""
        return self.__books.get(book_id)

    def update_book(self, book_id, name, author, content):
        """
        Met à jour les informations d'un livre existant.
        Conserve son état de disponibilité.
        """
        if book_id in self.__books:
            old_availability = self.__books[book_id].available
            self.__books[book_id] = Book(name, author, content)
            self.__books[book_id].set_availability(old_availability)
            return True
        return False

    def delete_book(self, book_id):
        """Supprime un livre par son ID. Retourne True si succès."""
        return self.__books.pop(book_id, None) is not None

class BookShop:
    """
    Classe principale gérant l'interface utilisateur de la bibliothèque.
    Gère l'affichage et les interactions avec l'utilisateur.
    """
    def __init__(self):
        """Initialise la boutique avec une nouvelle bibliothèque"""
        self.__lib = Lib()

    def clear_screen(self):
        """Nettoie l'écran du terminal (compatible Windows/Unix)"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, text):
        """
        Affiche un en-tête stylé avec des bordures.
        Args:
            text (str): Texte à afficher dans l'en-tête
        """
        width = 60
        print(f"\n{Fore.BLUE}{'='*width}")
        print(text.center(width))
        print(f"{'='*width}{Style.RESET_ALL}\n")

    def display_book_content(self, book):
        """
        Affiche le contenu d'un livre de manière stylée.
        Format: Titre en haut, contenu au milieu, auteur en bas.
        Args:
            book (Book): Le livre à afficher
        """
        self.clear_screen()
        width = 60
        
        # En-tête avec le titre du livre
        print(f"\n{Fore.BLUE}{'='*width}")
        print(f"{Fore.YELLOW}{book.name.center(width)}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*width}{Style.RESET_ALL}\n")
        
        # Formatage et affichage du contenu
        paragraphs = book.content.split('\n')
        for paragraph in paragraphs:
            words = paragraph.split()
            current_line = ""
            # Découpage du texte en lignes de maximum 40 caractères
            for word in words:
                if len(current_line) + len(word) + 1 <= 40:
                    current_line += word + " "
                else:
                    print(current_line.center(width))
                    current_line = word + " "
            if current_line:
                print(current_line.center(width))
            print()
        
        # Pied de page avec l'auteur
        print(f"{Fore.BLUE}{'='*width}")
        print(f"{Fore.YELLOW}Écrit par {book.author}".center(width))
        print(f"{Fore.BLUE}{'='*width}{Style.RESET_ALL}\n")
        
        input(f"{Fore.GREEN}Appuyez sur Entrée pour revenir au menu...{Style.RESET_ALL}")

    def run(self):
        """
        Démarre l'interface interactive de la bibliothèque.
        Boucle principale du programme.
        """
        # Définition des commandes disponibles
        commands = {
            "1": ("Créer un livre", self.__create_book),
            "2": ("Lister les livres", self.__list_books),
            "3": ("Mettre à jour un livre", self.__update_book),
            "4": ("Supprimer un livre", self.__delete_book),
            "5": ("Afficher le détail d'un livre", self.__show_book_details),
            "6": ("Acheter un livre", self.__buy_book),
            "7": ("Lire un livre", self.__read_book),
            "8": ("Retourner un livre", self.__return_book),
            "q": ("Quitter", None)
        }

        while True:
            self.clear_screen()
            self.print_header("BIBLIOTHÈQUE VIRTUELLE")
            
            # Affichage du menu
            print(f"{Fore.CYAN}Commandes disponibles:{Style.RESET_ALL}")
            for key, (desc, _) in commands.items():
                print(f"{Fore.GREEN}{key}{Style.RESET_ALL}: {desc}")
            
            # Saisie et traitement du choix utilisateur
            choice = input(f"\n{Fore.YELLOW}Entrez votre choix: {Style.RESET_ALL}").lower()
            
            if choice == 'q':
                self.clear_screen()
                print(f"\n{Fore.GREEN}Merci d'avoir utilisé la bibliothèque virtuelle!{Style.RESET_ALL}\n")
                break
                
            if choice in commands:
                commands[choice][1]()  # Exécute la fonction associée à la commande
            else:
                print(f"{Fore.RED}Commande invalide{Style.RESET_ALL}")
                time.sleep(1)

    def __create_book(self):
        """
        Gère la création d'un nouveau livre.
        Demande à l'utilisateur le titre, l'auteur et le contenu du livre.
        """
        self.clear_screen()
        self.print_header("CRÉATION D'UN LIVRE")
        
        # Collecte des informations du livre
        name = input(f"{Fore.YELLOW}Nom du livre: {Style.RESET_ALL}")
        author = input(f"{Fore.YELLOW}Auteur: {Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Contenu (appuyez sur Entrée deux fois pour terminer):{Style.RESET_ALL}")
        
        # Lecture du contenu multi-lignes
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        content = "\n".join(lines)
        
        # Création du livre et confirmation
        book_id = self.__lib.add_book(name, author, content)
        print(f"\n{Fore.GREEN}Livre créé avec l'ID: {book_id}{Style.RESET_ALL}")
        time.sleep(2)

    def __list_books(self):
        """
        Affiche la liste de tous les livres dans la bibliothèque.
        Montre l'ID, le titre, l'auteur et la disponibilité de chaque livre.
        """
        self.clear_screen()
        self.print_header("LISTE DES LIVRES")
        
        books = self.__lib.list_books()
        if not books:
            print(f"{Fore.RED}Aucun livre disponible{Style.RESET_ALL}")
        else:
            for id, book in books.items():
                print(f"ID {Fore.GREEN}{id}{Style.RESET_ALL}: {book}")
        
        input(f"\n{Fore.YELLOW}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def __update_book(self):
        """
        Permet la mise à jour des informations d'un livre existant.
        Vérifie l'existence du livre avant la mise à jour.
        Gère les erreurs de saisie d'ID.
        """
        self.clear_screen()
        self.print_header("MISE À JOUR D'UN LIVRE")
        
        try:
            book_id = int(input(f"{Fore.YELLOW}ID du livre à modifier: {Style.RESET_ALL}"))
            name = input(f"{Fore.YELLOW}Nouveau nom: {Style.RESET_ALL}")
            author = input(f"{Fore.YELLOW}Nouvel auteur: {Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Nouveau contenu (appuyez sur Entrée deux fois pour terminer):{Style.RESET_ALL}")
            
            # Lecture du nouveau contenu
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            content = "\n".join(lines)
            
            # Tentative de mise à jour
            if self.__lib.update_book(book_id, name, author, content):
                print(f"\n{Fore.GREEN}Livre mis à jour{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Livre non trouvé{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}ID invalide{Style.RESET_ALL}")
        
        time.sleep(2)

    def __delete_book(self):
        """
        Gère la suppression d'un livre.
        Vérifie l'existence du livre avant la suppression.
        Gère les erreurs de saisie d'ID.
        """
        self.clear_screen()
        self.print_header("SUPPRESSION D'UN LIVRE")
        
        try:
            book_id = int(input(f"{Fore.YELLOW}ID du livre à supprimer: {Style.RESET_ALL}"))
            if self.__lib.delete_book(book_id):
                print(f"\n{Fore.GREEN}Livre supprimé{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Livre non trouvé{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}ID invalide{Style.RESET_ALL}")
        
        time.sleep(2)

    def __show_book_details(self):
        """
        Affiche les détails d'un livre spécifique.
        Montre toutes les informations disponibles sur le livre.
        Gère les erreurs de saisie d'ID.
        """
        self.clear_screen()
        self.print_header("DÉTAILS DU LIVRE")
        
        try:
            book_id = int(input(f"{Fore.YELLOW}ID du livre: {Style.RESET_ALL}"))
            book = self.__lib.get_book(book_id)
            if book:
                print(f"\nDétails du livre:\n{book}")
            else:
                print(f"\n{Fore.RED}Livre non trouvé{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}ID invalide{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

    def __buy_book(self):
        """
        Gère l'achat d'un livre.
        Vérifie la disponibilité du livre avant l'achat.
        Empêche l'achat multiple du même livre.
        """
        self.clear_screen()
        self.print_header("ACHAT D'UN LIVRE")
        
        try:
            book_id = int(input(f"{Fore.YELLOW}ID du livre à acheter: {Style.RESET_ALL}"))
            book = self.__lib.get_book(book_id)
            if book:
                if book.available:
                    book.set_availability(False)
                    print(f"\n{Fore.GREEN}Livre acheté avec succès{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}Vous avez déjà acheté ce livre{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Livre non trouvé{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}ID invalide{Style.RESET_ALL}")
        
        time.sleep(2)

    def __read_book(self):
        """
        Permet la lecture d'un livre acheté.
        Vérifie que le livre existe et a été acheté avant d'autoriser la lecture.
        Affiche le contenu du livre de manière formatée.
        """
        self.clear_screen()
        self.print_header("LECTURE D'UN LIVRE")
        
        try:
            book_id = int(input(f"{Fore.YELLOW}ID du livre à lire: {Style.RESET_ALL}"))
            book = self.__lib.get_book(book_id)
            if book:
                if not book.available:  # Vérifie si le livre a été acheté
                    self.display_book_content(book)
                else:
                    print(f"\n{Fore.RED}Vous devez d'abord acheter ce livre pour pouvoir le lire{Style.RESET_ALL}")
                    time.sleep(2)
            else:
                print(f"\n{Fore.RED}Livre non trouvé{Style.RESET_ALL}")
                time.sleep(2)
        except ValueError:
            print(f"\n{Fore.RED}ID invalide{Style.RESET_ALL}")
            time.sleep(2)

    def __return_book(self):
        """
        Gère le retour d'un livre acheté.
        Vérifie que le livre existe et a été acheté avant d'autoriser le retour.
        """
        self.clear_screen()
        self.print_header("RETOUR D'UN LIVRE")
        
        try:
            book_id = int(input(f"{Fore.YELLOW}ID du livre à retourner: {Style.RESET_ALL}"))
            book = self.__lib.get_book(book_id)
            if book:
                if not book.available:  # Vérifie si le livre a été acheté
                    book.set_availability(True)
                    print(f"\n{Fore.GREEN}Livre retourné avec succès{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}Ce livre n'a pas été acheté{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Livre non trouvé{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}ID invalide{Style.RESET_ALL}")
        
        time.sleep(2)

# Point d'entrée du programme
if __name__ == '__main__':
    shop = BookShop()    # Crée une instance de la boutique
    shop.run()           # Lance l'interface interactive