"""
La classe JoueurOrdinateur

Hérite de Joueur et contient une "intelligence artificielle" extrêmement rudimentaire.
"""

from random import randint, choice
from jeu.joueur import Joueur
from jeu.lancer import ANGLES


#### DÉBUT DÉFI JOUEUR ORDINATEUR ####

class JoueurOrdinateur(Joueur):  # N'oubliez pas d'hériter de Joueur !!
    def __init__(self, numero_joueur, des_initiaux, arene):
        super().__init__(numero_joueur, des_initiaux, arene)

    def decision_continuer(self):
        decision = randint(1, 4)
        if decision == 4:
            return False
        return True

    def choisir_coordonnees(self):
        return randint(0, self.arene.dimension - 1), \
               randint(0, self.arene.dimension - 1)

    def choisir_angle(self):

        return choice(list(ANGLES.keys()))

    def choisir_puissance(self):
        return randint(1, max(1, self.arene.dimension // 4))
    # Écrivez les 4 méthodes demandées.

#### FIN DÉFI JOUEUR ORDINATEUR ####
