"""
Point d'entrée du TP3.

Les dés, l'arène, les joueurs, et la partie y sont générés.
"""

from joueur import Joueur
from arene import Arene
from de import De
from gladeateur import Gladeateur


def demander_entier(nom_entier, valeur_defaut, entier_minimum=None, entier_maximum=None):
    """
    Cette fonction permet de demander à l'utilisateur un entier entre des bornes, possiblement
    absentes, avec validation de l'entrée. Elle inclut aussi une valeur par défaut si l'utilisateur
    n'entre rien.

    Args:
        nom_entier (str): Le nom de l'entier à choisir
        valeur_defaut (int): La valeur à prendre si rien n'est écrit
        entier_minimum (int, optional): La borne inférieure. Défaut: None (pas de borne inférieure)
        entier_maximum (int, optional): La borne supérieure. Défaut: None (pas de borne inférieure)

    Returns:
        int: L'entier entré par l'utilisateur
    """
    entree_invalide = True
    entier = None
    while entree_invalide:
        entree = input("Veuillez entrer {} [{} par défaut]: ".format(nom_entier, valeur_defaut))
        if entree == "":
            return valeur_defaut
        elif not entree.isnumeric():
            print("Entrée invalide: {} doit être un entier.".format(nom_entier))
        else:
            entier = int(entree)
            entier_trop_petit = entier_minimum is not None and entier < entier_minimum
            entier_trop_grand = entier_maximum is not None and entier > entier_maximum
            if entier_trop_petit:
                print(
                    "Entrée invalide: {} doit être un entier plus grand ou égal à {}. "
                        .format(nom_entier, entier_minimum))
            elif entier_trop_grand:
                print(
                    "Entrée invalide: {} doit être un entier plus petit ou égal à {}. "
                        .format(nom_entier, entier_maximum))
            entree_invalide = entier_trop_petit or entier_trop_grand
    return entier


print("Bienvenue aux GlaDÉateurs !!!")

#######################
# CRÉATION DE L'ARÈNE #
#######################

mode_affichage = demander_entier(
    "le mode d'affichage parmi: les numéros (1) ou les icônes (2)", 1, 1, 2)
dimension = demander_entier("la dimension de l'arène", 5, 3)
arene = Arene(dimension, De(), mode_affichage)

########################
# CRÉATION DES JOUEURS #
########################

n_joueurs = demander_entier("le nombre de joueurs", 2, 2, 5)
n_des_par_joueur = demander_entier("le nombre de dés par joueur", 10, 1, 15)

joueurs = []
for i in range(n_joueurs):
    des = []
    for j in range(n_des_par_joueur):
        des.append(De())
    joueurs.append(Joueur(i + 1, des, arene))

#########################
# CRÉATION DE LA PARTIE #
#########################

glad = Gladeateur(joueurs, arene)
input("Appuyez sur Entrée pour débuter...")
glad.jouer_partie()
