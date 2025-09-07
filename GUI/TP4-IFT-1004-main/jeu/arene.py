"""
La classe Arène

Représente la zone où les dés sont lancés
"""


class Arene:
    """ Représente la zone de jeu où les dés sont lancés.

    Attributes:
        dimension (int): La dimension, largeur comme hauteur, de l'Arene.
        des (dict): Les dés présents sur l'arène, sous la forme de paires <emplacement, dé>
                    où emplacement est un tuple de coordonnées (x,y) et dé est une istance de la classe Dé.
        mode_affichage (int): Le mode d'affichage (1 pour [X,2,3,4,5,6] ou 2 pour [X,⚁,⚂,⚃,⚄,⚅])
    """

    def __init__(self, dimension, de_initial, mode_affichage):
        """
        Constructeur de la classe Arene.
        Le dé initial est centré et sa valeur ne doit pas être X.

        Args:
            dimension (int): La dimension, largeur comme hauteur, de l'Arene.
            de_initial (De): L'unique dé présent dans l'arène au départ
            mode_affichage (int): Le mode d'affichage (1 pour [X,2,3,4,5,6] ou 2 pour [X,⚁,⚂,⚃,⚄,⚅])
        """
        self.dimension = dimension
        de_initial.lancer()
        while de_initial.valeur == 1:
            de_initial.lancer()
        self.des = {(self.dimension // 2, self.dimension // 2): de_initial}
        self.mode_affichage = mode_affichage

    def dans_arene(self, emplacement):
        """
        Vérifie si un emplacement est inclus dans l'arène.
        Un emplacement (x, y) est dans l'arène s'il se trouve entre (0,0)
        et (d-1, d-1) inclusivement, où d est la dimension de l'arène

        Args:
            emplacement ((int, int)): Coordonnées dont on veut vérifier l'inclusion

        Returns:
            bool: True si l'emplacement est dans l'arène, False sinon
        """
        return 0 <= emplacement[0] < self.dimension and 0 <= emplacement[1] < self.dimension

    def effectuer_lancer(self, lancer):
        """
        Obtient la trajectoire du lancer (Lancer.trajectoire), relance les
        dés accrochés (Arene.relancer_des_accroches) au passage pour tous les
        emplacements de la trajectoire excepté le dernier, puis place le dé du
        lancer au dernier emplacement de la trajectoire (Arene.placer_nouveau_de).

        Args:
            lancer (Lancer): contient les informations sur le lancer à effectuer
        """
        self.relancer_des_accroches(lancer.trajectoire[:-1])
        self.placer_nouveau_de(lancer.de, lancer.trajectoire[-1])

    def relancer_des_accroches(self, trajectoire):
        """
        Pour chaque emplacement de la trajectoire, relancer le dé (De.lancer) qui
        se trouve à cet emplacement, s'il y en a un.

        Args:
            trajectoire (list): Liste des coordonnées où l'on doit relancer
        """
        for emplacement in trajectoire:
            if emplacement in self.des:
                self.des[emplacement].lancer()

    def placer_nouveau_de(self, de, emplacement_final):
        """
        Si l'emplacement final est dans l'arène (Arene.dans_arene),
        on lance le dé (De.lancer) et on l'ajoute dans le dictionnaire de dés
        à l'emplacement final.

        Important: Si un dé est déjà présent à cet emplacement, ce dernier est retiré
        pour laisser place au nouveau dé.

        Args:
            de (De): Le dé à ajouter
            emplacement_final ((int, int)): Les coordonnées où ajouter le dé
        """
        if self.dans_arene(emplacement_final):
            de.lancer()
            self.des[emplacement_final] = de

    def effectuer_plusieurs_lancers(self, liste_lancers):
        """
        Effectue chaque lancer (Arene.effectuer_lancer) de la liste de lancers.

        Args:
            liste_lancers (list): La liste de lancers à effectuer
        """
        for lancer in liste_lancers:
            self.effectuer_lancer(lancer)

    def rangement(self, joueur_en_cours):
        """
        Il s'agit d'enlever les dés de l'arène, suivant les règles du jeu:
          - On retire d'abord tous les X (Arene.retirer_les_x)
          - On compte combien des autres valeurs sont présentes (Arene.compter_valeurs)
          - On retire les dés non uniques (Arene.retirer_correspondances)
        On retourne ensuite un booléen indiquant si une correspondance
        a eu lieu (Arene.correspondance_existe)

        Args:
            joueur_en_cours (Joueur): le joueur qui vient de lancer

        Returns:
            bool: True si une correspondance a eu lieu, False sinon.
        """
        self.retirer_les_x()
        comptes = self.compter_valeurs()
        self.retirer_correspondances(comptes, joueur_en_cours)
        return self.correspondance_existe(comptes)

    def retirer_les_x(self):
        """
        Parmi toutes les entrées du dictionnaire de dés, retire
        (Arene.retirer_de) celles dont la valeur est 1.

        Astuce: commencez par identifier les emplacements avec les X en les mettant
        dans une liste, puis retirez-les dans un deuxième temps, car faire des suppressions
        dans un dictionnaire en même temps que l'on itère dessus est déconseillé.
        """
        a_retirer_X = []
        for emplacement in self.des.keys():
            valeur_de = self.des[emplacement].valeur
            if valeur_de == 1:
                a_retirer_X.append(emplacement)
        for emplacement in a_retirer_X:
            self.retirer_de(emplacement)

    def compter_valeurs(self):
        """
        Retourne un dictionnaire associant les numéros 2, 3, 4, 5 et 6
        au nombre de dés ayant ces valeurs.

        Exemple: si l'arène contient 3 dés (un 5 et deux 3),
        alors on retourne {2:0, 3:2, 4:0, 5:1, 6:0}

        Returns:
            dict: Le dictionnaire associant valeurs de dés et nombre d'occurence
        """
        comptes = {
            2: 0, 3: 0, 4: 0, 5: 0, 6: 0
        }
        for de in self.des.values():
            valeur_de = de.valeur
            comptes[valeur_de] += 1
        return comptes

    def retirer_correspondances(self, comptes, joueur_en_cours):
        """
        Parmi toutes les entrées du dictionnaire de dés, rend au joueur
        (Arene.rendre_au_joueur) celles dont la valeur est présente plus d'une fois.

        Astuce: commencez par identifier les emplacements des dés à enlever en les mettant
        dans une liste, puis retirez-les dans un deuxième temps, car faire des suppressions
        dans un dictionnaire en même temps que l'on itère dessus est déconseillé.

        Args:
            comptes (dict): Nombre d'occurences de chaque valeur de dé
            joueur_en_cours (Joueur): le joueur à qui rendre les dés

        """
        a_retirer_correspondance = []
        for emplacement in self.des.keys():
            valeur_de = self.des[emplacement].valeur
            if comptes[valeur_de] > 1:
                a_retirer_correspondance.append(emplacement)
        for emplacement in a_retirer_correspondance:
            self.rendre_au_joueur(emplacement, joueur_en_cours)

    def correspondance_existe(self, comptes):
        """
        Indique s'il existe une valeur présente plus d'une fois sur l'arène.

        Args:
            comptes (dict): Un dictionnaire indiquant, pour chaque valeur
                de dé de 2 à 6, combien sont présents sur l'arène.

        Returns:
            bool: True si une valeur de dé est là plus d'une fois, False sinon.
        """
        for compte in comptes.values():
            if compte > 1:
                return True
        return False

    def est_vide(self):
        """
        Vérifie si l'arène est vide.

        Returns:
            bool: True si aucun dé n'est présent, False sinon.
        """
        return len(self.des) == 0

    def retirer_de(self, emplacement):
        """
        Retire un dé définitivement. Utilisez le mot-clé del.

        Args:
            emplacement ((int, int)): L'emplacement du dé à éliminer.
        """
        del self.des[emplacement]

    def rendre_au_joueur(self, emplacement, joueur):
        """
        Rend le dé situé à l'emplacement au joueur (Joueur.rendre_de),
        et retire le dé de l'arène (Arene.retirer_de). L'ordre des appels est important!

        Args:
            emplacement ((int, int)): L'emplacement du dé à rendre
            joueur (Joueur): Le joueur à qui rendre le dé
        """
        de = self.des[emplacement]
        joueur.rendre_de(de)
        self.retirer_de(emplacement)

    def afficher_de(self, emplacement):
        """
        Donne la représentation en chaîne de caractères du dé situé à l'emplacement
        spécifié en paramètre, selon le mode d'affichage.

        Args:
            emplacement ((int, int)): L'emplacement du dé à afficher

        Returns:
            str: La chaîne représentant le dé
        """
        return self.des[emplacement].affichage_string(self.mode_affichage)
