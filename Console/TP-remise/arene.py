"""
La classe Arène

Représente la zone où les dés sont lancés
"""

import colorama
from de import De
from lancer import Lancer
from joueur import Joueur


class Arene:
    """ Représente la zone de jeu où les dés sont lancés.

    Attributes:
        dimension (int): La dimension, largeur comme hauteur, de l'Arene.
        des (dict): Les dés présents sur l'arène, sous la forme de paires <emplacement, dé>
                    où emplacement est un tuple de coordonnées (x,y) et dé est une istance de la classe Dé.
        mode_affichage (int): Le mode d'affichage (1 pour [X,2,3,4,5,6] ou 2 pour [X,⚁,⚂,⚃,⚄,⚅])
    """
    def __init__(self, dimension: int, de_initial: De, mode_affichage: int):
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

    def dans_arene(self, emplacement: tuple):
        """
        Vérifie si un emplacement est inclus dans l'arène.
        Un emplacement (x, y) est dans l'arène s'il se trouve entre (0,0)
        et (d-1, d-1) inclusivement, où d est la dimension de l'arène

        Args:
            emplacement ((int, int)): Coordonnées dont on veut vérifier l'inclusion

        Returns:
            bool: True si l'emplacement est dans l'arène, False sinon
        """
        # Torben
        result = False

        if (emplacement[0] < self.dimension and
            emplacement[1] < self.dimension):
            result = True

        return result


    def effectuer_lancer(self, lancer: Lancer):
        """
        Obtient la trajectoire du lancer (Lancer.trajectoire), relance les
        dés accrochés (Arene.relancer_des_accroches) au passage pour tous les
        emplacements de la trajectoire excepté le dernier, puis place le dé du
        lancer au dernier emplacement de la trajectoire (Arene.placer_nouveau_de).

        Args:
            lancer (Lancer): contient les informations sur le lancer à effectuer
        """
        self.relancer_des_accroches(lancer.trajectoire)
        self.placer_nouveau_de(De(), lancer.trajectoire[-1])


        

    def relancer_des_accroches(self, trajectoire: list):
        """
        Pour chaque emplacement de la trajectoire, relancer le dé (De.lancer) qui
        se trouve à cet emplacement, s'il y en a un.

        Args:
            trajectoire (list): Liste des coordonnées où l'on doit relancer
        """
        # Torben
        for i in self.des:
            if i in trajectoire:
                self.des[i].lancer()


    def placer_nouveau_de(self, de: De, emplacement_final: tuple):
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
        # Torben
        if (self.dans_arene(emplacement_final)):
            de.lancer()
            self.des[emplacement_final] = de

        # TODO retirer le de si il y en a deja un


    def effectuer_plusieurs_lancers(self, liste_lancers: list):
        """
        Effectue chaque lancer (Arene.effectuer_lancer) de la liste de lancers.

        Args:
            liste_lancers (list): La liste de lancers à effectuer
        """
        # Torben
        for i in liste_lancers:
            self.effectuer_lancer(i)


    def rangement(self, joueur_en_cours: Joueur):
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
        # Torben
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
        # Torben
        liste_a_retirer = []
        for i in self.des:
            if self.des[i].valeur == 1:
                liste_a_retirer.append(i)
        
        for i in liste_a_retirer:
            del self.des[i]


    def compter_valeurs(self):
        """
        Retourne un dictionnaire associant les numéros 2, 3, 4, 5 et 6
        au nombre de dés ayant ces valeurs.

        Exemple: si l'arène contient 3 dés (un 5 et deux 3),
        alors on retourne {2:0, 3:2, 4:0, 5:1, 6:0}

        Returns:
            dict: Le dictionnaire associant valeurs de dés et nombre d'occurence
        """
        # Torben
        resultat = {2:0, 3:0, 4:0, 5:0, 6:0}
        # TODO possible lambda function
        for i in self.des:
            if self.des[i].valeur == 2:
                resultat[2] += 1
            elif self.des[i].valeur == 3:
                resultat[3] += 1
            elif self.des[i].valeur == 4:
                resultat[4] += 1
            elif self.des[i].valeur == 5:
                resultat[5] += 1
            elif self.des[i].valeur == 6:
                resultat[6] += 1

        return resultat




    def retirer_correspondances(self, comptes: dict, joueur_en_cours: Joueur):
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
        # Torben
        liste_a_rendre = []
        for i in comptes:
            if comptes[i] > 1:
                for j in self.des:
                    if self.des[j].valeur == i:
                        liste_a_rendre.append(j)

        for i in liste_a_rendre:
            self.rendre_au_joueur(i, joueur_en_cours)



    def correspondance_existe(self, comptes: dict):
        """
        Indique s'il existe une valeur présente plus d'une fois sur l'arène.

        Args:
            comptes (dict): Un dictionnaire indiquant, pour chaque valeur
                de dé de 2 à 6, combien sont présents sur l'arène.

        Returns:
            bool: True si une valeur de dé est là plus d'une fois, False sinon.
        """
        # Torben
        for i in comptes:
            if comptes[i] > 1:
                return True
        
        return False

    def est_vide(self):
        """
        Vérifie si l'arène est vide.

        Returns:
            bool: True si aucun dé n'est présent, False sinon.
        """
        # Torben
        if self.des == {}:
            return True
        else:
            return False

    def retirer_de(self, emplacement: tuple):
        """
        Retire un dé définitivement. Utilisez le mot-clé del.

        Args:
            emplacement ((int, int)): L'emplacement du dé à éliminer.
        """
        del self.des[emplacement]

    def rendre_au_joueur(self, emplacement: tuple, joueur: Joueur):
        """
        Rend le dé situé à l'emplacement au joueur (Joueur.rendre_de),
        et retire le dé de l'arène (Arene.retirer_de). L'ordre des appels est important!

        Args:
            emplacement ((int, int)): L'emplacement du dé à rendre
            joueur (Joueur): Le joueur à qui rendre le dé
        """
        joueur.rendre_de(self.des[emplacement])
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

    def affichage_string(self, lancer=None):
        """
        Donne la représentation en chaîne de caractères de l'arène, en affichant la
        trajectoire d'un lancer au besoin

        Args:
            lancer (optionel): Une liste correspondand à une trajectoire

        Returns:
            str: la représentation en chaîne de caractères
        """
        if lancer is None:
            trajectoire = []
        elif type(lancer) is list:
            trajectoire = lancer
        else:
            trajectoire = lancer.trajectoire

        ligne_exterieure = '{:s}  |'
        for x in list(range(self.dimension)):
            ligne_exterieure += '{:^3d}'.format(x)
        ligne_exterieure += "|  {:s}\n"

        ligne_interieure = "----" + "|" + "-" * 3 * self.dimension + "|----\n"

        m = "\n"
        m += ligne_exterieure.format('NO', 'NE')
        m += ligne_interieure
        for i in range(self.dimension):
            m += "{:>3d} |".format(i)
            for j in range(self.dimension):
                if (i, j) in trajectoire:
                    m += colorama.Back.LIGHTYELLOW_EX + colorama.Fore.RED

                if (i, j) in self.des:
                    m += "{:^3s}".format(self.afficher_de((i, j)))
                else:
                    m += "   "

                if (i, j) in trajectoire:
                    m += colorama.Fore.RESET + colorama.Back.RESET

            m += "| {:<3d} \n".format(i)
        m += ligne_interieure
        m += ligne_exterieure.format('SO', 'SE')
        return m

    def __str__(self):
        """
        Pour afficher l'arène'.

        Returns:
            str: la représentation en chaîne de caractères
        """
        return self.affichage_string()


# Le code suivant peut être exécuté pour afficher des exemples d'arènes, lorsque la classe « De » sera complétée
if __name__ == '__main__':
    arene_1 = Arene(5, De(), 1)
    arene_2 = Arene(15, De(), 2)
    print(arene_1)
    print(arene_2)