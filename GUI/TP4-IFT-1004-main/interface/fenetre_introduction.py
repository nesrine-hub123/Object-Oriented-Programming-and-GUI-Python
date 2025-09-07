"""
Module contenant la classe FenetreIntroduction et ses classes
utilitaires FrameArene et FrameJoueurs.
"""

from tkinter import IntVar, Button, Label, Entry, Frame, messagebox, RIDGE, Toplevel, \
    Checkbutton, END

from jeu.arene import Arene
from jeu.de import De
from interface.joueur_ordinateur import JoueurOrdinateur
from interface.joueur_humain_tk import JoueurHumainTk

import os


class FrameArene(Frame):
    def __init__(self, master):
        """
        Constructeur de la classe FrameArene. Cette classe gère le menu
        de création de l'arène.

        Args:
            master (Frame): Le widget TKinter dans lequel la frame s'intègre.
        """
        super().__init__(master, borderwidth=1, relief=RIDGE)

        self.frame_dimension_carre = Frame(self)
        self.label_dimension_carre = Label(
            self.frame_dimension_carre, text="Dimension d'un côté: ")
        self.entry_dimension_carre = Entry(self.frame_dimension_carre, width=5)
        self.label_dimension_carre.grid(row=0, column=0)
        self.entry_dimension_carre.grid(row=0, column=1)
        self.frame_dimension_carre.grid(row=1, column=0, padx=5, pady=2)

        self.frame_nombre_des = Frame(self)
        self.label_nombre_des = Label(
            self.frame_nombre_des, text="Nombre de dés par joueur: ")
        self.entry_nombre_des = Entry(self.frame_nombre_des, width=5)
        self.label_nombre_des.grid(row=0, column=0)
        self.entry_nombre_des.grid(row=0, column=1)
        self.frame_nombre_des.grid(row=2, column=0, padx=5, pady=2)

        self.mode_var = IntVar(value=0)
        self.mode_checkbutton = Checkbutton(
            self, text="Dés dessinés", variable=self.mode_var)
        self.mode_checkbutton.grid(row=4, column=0, padx=5, pady=2)

    def obtenir_arene(self):
        """
        Cette méthode crée une arène en fonction des paramètres déterminés dans le frame.

        Returns:
            Arene: L'arène créée.
        """
        try:
            dimension = int(self.entry_dimension_carre.get())
            if dimension < 3:
                raise ValueError
        except ValueError:
            raise ValueError("La dimension doit être un entier >= 3 !")
        return Arene(dimension, De(), self.mode_var.get() + 1)

    def obtenir_nombre_des(self):
        """
        Cette fonction lit le nombre de dés inscrit dans l'entry correspondant
        Lance un exception si ce qui est inscrit n'est pas un entier valide.

        Returns:
            int: Le nombre de dés.
        """
        try:
            nb_des = int(self.entry_nombre_des.get())
            if nb_des < 1 or nb_des > 15:
                raise ValueError
            return nb_des
        except ValueError:
            raise ValueError(
                "Le nombre de dés doit être un entier entre 1 et 15 !")


class FrameJoueurs(Frame):
    def __init__(self, master):
        """
        Constructeur de la classe FrameJoueurs. Cette classe gère le menu
        du choix des joueurs.

        Args:
            master (Frame): Le widget TKinter dans lequel la frame s'intègre.
        """
        super().__init__(master, borderwidth=1, relief=RIDGE)
        label_joueurs = Label(self, text="Sélectionnez les joueurs")
        label_joueurs.grid(row=0, column=0, padx=10, pady=10)
        self.boutons_joueur = []
        frame_boutons = Frame(self)
        frame_boutons.grid(row=1, column=0)
        for i in range(5):
            bouton_joueur = Button(frame_boutons, text="Inactif", width=8, font='sans 12',
                                   command=lambda c=i: self.changer_type_joueur(c))
            bouton_joueur.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.boutons_joueur.append(bouton_joueur)

    def obtenir_joueurs(self, arene, nb_des_par_joueur, fenetre_jeu):
        """
        Cette méthode crée les joueurs en fonction du contenu des boutons.

        Returns:
            list: La liste des joueurs
        """
        joueurs = []
        n_des_joueurs = 30
        n_joueurs = sum(map(lambda bouton: int(
            bouton['text'] != 'Inactif'), self.boutons_joueur))

        for i, bouton_joueur in enumerate(self.boutons_joueur):
            des = [De() for _ in range(nb_des_par_joueur)]
            if bouton_joueur['text'] == "Humain":
                joueurs.append(JoueurHumainTk(i + 1, des, arene, fenetre_jeu))
            elif bouton_joueur['text'] == "Ordinateur":
                joueurs.append(JoueurOrdinateur(i + 1, des, arene))
        if len(joueurs) < 2:
            raise ValueError("Trop peu de joueurs!")
        return joueurs

    def changer_type_joueur(self, i):
        """
        Cette fonction permet de modifier le contenu du bouton dont
        le numéro est en paramètres.

        Args:
            i (int): Le numéro du bouton à modifier
        """
        if self.boutons_joueur[i]['text'] == "Inactif":
            self.boutons_joueur[i]['text'] = "Humain"
        elif self.boutons_joueur[i]['text'] == "Humain":
            self.boutons_joueur[i]['text'] = "Ordinateur"
        else:
            self.boutons_joueur[i]['text'] = "Inactif"


class FenetreIntroduction(Toplevel):
    def __init__(self, master):
        """
        Constructeur de la classe FenetreIntroduction. Cette classe permet
        de choisir les paramètres de la partie et de démarrer la partie.
        """
        super().__init__(master)
        self.master = master
        self.transient(master)
        self.grab_set()

        self.title("Paramètres de la partie...")
        self.arene = None
        self.joueurs = None

        self.label_introduction = Label(
            self, text="Bienvenue aux GlaDÉateurs!")

        self.label_introduction.grid(row=0, column=0, padx=10, pady=10)

        self.frame_frame = Frame(self)
        self.frame_arene = FrameArene(self.frame_frame)
        self.frame_arene.grid(row=0, column=0, padx=10, pady=10)
        self.frame_joueurs = FrameJoueurs(self.frame_frame)
        self.frame_joueurs.grid(row=0, column=1, padx=10, pady=10)
        self.frame_frame.grid(row=1, column=0)

        self.button_frame = Frame(self)
        self.bouton_remplissage_auto = Button(self.button_frame, text="Paramètres par défaut",
                                              command=self.remplissage_auto)
        self.bouton_commencer = Button(
            self.button_frame, text="Commencer!", command=self.commencer)
        self.bouton_remplissage_auto.grid(row=2, column=0, padx=10, pady=10)
        self.bouton_commencer.grid(row=2, column=1, padx=10, pady=10)
        self.button_frame.grid(row=2, column=0)

    def commencer(self):
        """
        Cette méthode crée la fenêtre principale en fonction des paramètres dans les frames.
        """
        try:
            self.arene = self.frame_arene.obtenir_arene()
            self.joueurs = self.frame_joueurs.obtenir_joueurs(self.arene, self.frame_arene.obtenir_nombre_des(),
                                                              self.master)
            self.grab_release()
            self.master.focus_set()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def obtenir_donnees(self):
        """
        Retourne l'arène et les joueurs.

        Returns:
            Arene: L'arène créée
            list: La liste de joueurs créés
        """
        return self.arene, self.joueurs

    def remplissage_auto(self):
        try:
            self.obtenir_infos_remplissage()
        except NotImplementedError:
            messagebox.showerror(
                "Erreur", "Le défi Fichier de configuration n'a pas été réalisé encore")
        except FileNotFoundError:
            messagebox.showerror(
                "Erreur", "Aucun fichier de configuration trouvé")
        except KeyError:
            messagebox.showerror(
                "Erreur", "Il manque un des champs obligatoires")
        except ValueError:
            messagebox.showerror(
                "Erreur", "Un des champs n'a pas le bon format")

    def obtenir_infos_remplissage(self):
        #### DÉBUT DÉFI LECTURE FICHIER CONFIG ####
        # Test de presence du ficher
        try:
            lignes_config = open("./interface/config.txt").readlines()
        except FileNotFoundError:
            print("Fichier inexistant")

        # Initialization des variable
        dimension = lignes_config[0].split(":")[1].rstrip()
        n_des = lignes_config[1].split(":")[1].rstrip()
        dessiner = lignes_config[2].split(":")[1].rstrip()
        joueurs = lignes_config[3].split(":")[1].rstrip().split(",")

        # Test pour s'assure que tous les varibles sont non nuls
        if len(dimension) == 0 or len(n_des) == 0 or len(dessiner) == 0 or len(joueurs) == 0:
            raise KeyError

        # Test sur les proprietes des variables
        try:
            int(dimension)
        except ValueError:
            print("la dimension n'est pas un entier")

        try:
            int(n_des)
        except ValueError:
            print("le nombre de des n'est pas un entier")

        if dessiner == "oui":
            dessiner = True
        elif dessiner == "non":
            dessiner = False
        else:
            raise ValueError

        if len(joueurs) < 2 or len(joueurs) > 5:
            raise ValueError

        # Insertition des valeurs dans l'interface
        self.frame_arene.entry_dimension_carre.delete(0, "end")
        self.frame_arene.entry_dimension_carre.insert(END, dimension)

        self.frame_arene.entry_nombre_des.delete(0, "end")
        self.frame_arene.entry_nombre_des.insert(END, n_des)

        if dessiner:
            self.frame_arene.mode_var.set(1)
        else:
            self.frame_arene.mode_var.set(0)

        for i in range(len(joueurs)):
            self.frame_joueurs.boutons_joueur[i]['text'] = joueurs[i]

        for i in range(5 - len(joueurs)):
            self.frame_joueurs.boutons_joueur[len(
                joueurs) + i]['text'] = "Inactif"
        #### FIN DÉFI LECTURE FICHIER CONFIG ####
