"""
La classe Dé.

Représente un dé à 6 faces.
"""

from random import randint


class De:
    """ Représente un dé à 6 faces.

    Attributes:
        valeur (int): Un nombre de 1 à 6 inclusivement.
    """
    def __init__(self):
        """
        Constructeur de la classe De.
        Avant d'être lancé, sa valeur est None.
        """
        self.valeur = None

    def affichage_string(self, mode):
        """
        Donne la représentation en chaîne de caractères de la valeur
        du dé, selon le mode [2,3,4,5,6] ou [⚁,⚂,⚃,⚄,⚅].
        Si sa valeur est 1, on affiche X peu importe le mode.

        Args:
            mode (int): Le mode (1 pour [2,3,4,5,6], 2 pour [⚁,⚂,⚃,⚄,⚅]).

        Returns:
            str: La représentation de la valeur du dé.
        """
        if self.valeur == 1:
            return "X"
        elif mode == 1:
            return str(self.valeur)
        elif mode == 2:
            return chr(9855 + self.valeur)

    def lancer(self):
        """
        Modifie aléatoirement la valeur du dé.
        """
        self.valeur = randint(1, 6)

    def ranger(self):
        """
        Met la valeur du dé à None.
        """
        self.valeur = None
