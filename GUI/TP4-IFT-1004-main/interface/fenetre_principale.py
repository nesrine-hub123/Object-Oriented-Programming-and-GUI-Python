"""
Module contenant la classe FenetrePrincipale et ses classes utilitaires FrameAttaque
et FrameJoueurActif. Cette fenêtre permet de jouer au jeu.
"""

from tkinter import Tk, Button, Label, messagebox

from jeu.gladeateur import Gladeateur
from interface.joueur_ordinateur import JoueurOrdinateur
from interface.gestionnaire_io_interface import GestionnaireIOInterface
from interface.canvas_arene import CanvasArene
from interface.fenetre_introduction import FenetreIntroduction
from interface.frames_fenetre_principale import FrameDescription, FrameJoueurActif, FrameTableauJoueurs, \
    FrameTempsAttente


class FenetrePrincipale(Tk):
    def __init__(self):
        """
        Constructeur de la classe FenetrePrincipale.
        Cette classe gère l'instance de GlaDéateurs, les joueurs et l'arène.
        """
        super().__init__()

        self.title("Les GlaDÉateurs")
        self.label_bienvenue = Label(text="Bienvenue aux GlaDéateurs!")
        self.bouton_commencer = Button(text="Commencer", width=20, command=self.lancer_fenetre_introduction)
        self.label_bienvenue.grid(row=0, column=0, padx=10, pady=10)
        self.bouton_commencer.grid(row=1, column=0, padx=10, pady=10)

    def lancer_fenetre_introduction(self):
        """
        Ouvre la fenêtre où l'on inscrit les paramètres de la partie.
        """
        fenetre_introduction = FenetreIntroduction(self)
        self.wait_window(fenetre_introduction)
        arene, joueurs = fenetre_introduction.obtenir_donnees()
        if arene is not None and joueurs is not None:
            self.demarrer(arene, joueurs)

    def demarrer(self, arene, joueurs):
        """
        Lance une partie.

        Args:
            arene (Arene): L'arène de la partie
            joueurs (list): La liste des joueurs
        """
        self.label_bienvenue.destroy()
        self.bouton_commencer.destroy()

        self.joueurs = joueurs
        self.arene = arene

        self.canvas_arene = CanvasArene(self, arene)
        self.canvas_arene.grid(row=0, column=0, padx=20, pady=20)

        self.frame_description = FrameDescription(self)
        self.frame_description.grid(row=1, column=0, padx=10, pady=10)

        self.frame_joueur = FrameJoueurActif(self)
        self.frame_joueur.grid(row=2, column=0, padx=10, pady=10)

        self.joueur_index = 0
        self.joueur_actuel = joueurs[self.joueur_index]

        self.gestionnaire_io = GestionnaireIOInterface(self, self.canvas_arene, self.frame_description)

        self.frame_tableau_joueurs = FrameTableauJoueurs(self)
        self.frame_temps_attente = FrameTempsAttente(self)
        self.frame_tableau_joueurs.grid(row=0, column=1, padx=10, pady=10)
        self.frame_temps_attente.grid(row=1, column=1, padx=10, pady=10)

        self.gladeateur = Gladeateur(joueurs, arene, self.gestionnaire_io)
        self.gladeateur.jouer_partie()

    def est_joueur_ordi(self):
        """
        Cette méthode indique s'il s'agit d'un joueur ordinateur

        Returns:
            bool: True s'il s'agit d'un ordinateur, False si joueur humain
        """
        return isinstance(self.joueur_actuel, JoueurOrdinateur)

    def redessiner(self, temps_attente, suite):
        """
        Cette méthode active le redessinage de l'arène, et déclenche
        la suite.

        Args:
            temps_attente (int): Temps en millisecondes avant d'exécuter la suite
            suite (fonction): La fonction à exécuter suite au redessinage
        """

        self.canvas_arene.dessiner_canvas(lambda: None)
        self.frame_description.vider()

        if not self.est_joueur_ordi():
            temps_attente = 0
        self.after(temps_attente, suite)

    def afficher_joueur(self, joueur, temps_attente, suite):
        """
        Cette méthode affiche le joueur en cours

        Args:
            joueur (Joueur): Le joueur à afficher
            temps_attente (int): Temps en millisecondes avant d'exécuter la suite
            suite (fonction): La fonction à exécuter suite à l'affichage du joueur
        """
        self.frame_tableau_joueurs.mise_a_jour()
        self.frame_joueur.populer(joueur)
        self.redessiner(temps_attente, suite)

    def afficher_gagnant(self, joueur):
        """
        Affiche le gagnant de la partie.
        """
        messagebox.showinfo("Fin de la partie", f"Victoire du {str(joueur)}")
        self.canvas_arene.permettre_clics(lambda _: None, None)
        self.frame_joueur.populer(joueur)
