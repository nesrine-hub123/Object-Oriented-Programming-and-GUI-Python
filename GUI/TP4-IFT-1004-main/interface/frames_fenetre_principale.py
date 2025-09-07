"""
Module contenant des frames utilitaires présents dans la fenêtre principale.
"""

from tkinter import Frame, Label, Button, Scale, VERTICAL, IntVar

from interface.joueur_ordinateur import JoueurOrdinateur


class FrameDescription(Frame):
    def __init__(self, master):
        """
        Constructeur de la classe FrameDescription. Affiche un descriptif
        de ce qui se passe dans le jeu.

        Args:
            master (Tk): La fenêtre dans laquelle ce frame s'insert.
        """
        super().__init__(master)
        self.label_description = Label(self, text="")
        self.label_description.grid(row=0, column=0)

    def populer(self, texte, temps_attente, suite):
        """
        Cette méthode affiche les informations sur le jeu.

        Args:
            texte (str): Le message à afficher
            temps_attente (int): Temps en millisecondes avant d'exécuter la suite
            suite (fonction): La fonction à exécuter après
        """
        self.label_description['text'] = texte
        self.after(temps_attente, suite)

    def vider(self):
        """
        Cette méthode enlève l'affichage.
        """
        self.label_description['text'] = ""


class FrameJoueurActif(Frame):
    def __init__(self, master):
        """
        Constructeur de la classe FrameJoueurActif. Affiche les informations relatives au
        joueur dont c'est le tour.

        Args:
            master (Tk): La fenêtre dans laquelle ce frame s'insert.
        """
        super().__init__(master)

        self.label_nom_joueur = Label(self, text="")
        self.label_nombre_des = Label(self, text="")

        self.label_nom_joueur.grid(row=0, column=0)
        self.label_nombre_des.grid(row=1, column=0)

        self.clic_bouton = lambda: None
        self.bouton_terminer_tour = Button(
            self, text="Terminer le tour", command=self.appui_bouton)
        self.bouton_terminer_tour.grid(row=1, column=1)
        self.bouton_terminer_tour["state"] = "disabled"

        self.couleurs = [
            'blue', 'green', 'red', 'orange', 'purple'
        ]

    def populer(self, joueur):
        """
        Ajoute les informations d'un joueur dans le frame.

        Args:
            joueur (Joueur): le joueur dont c'est le tour
        """
        self.label_nom_joueur["text"] = f"Joueur # {joueur.numero_joueur}"
        self.label_nombre_des["text"] = f"{len(joueur.des)} dés"
        self.label_nom_joueur["fg"] = self.couleurs[joueur.numero_joueur - 1]
        self.label_nombre_des["fg"] = self.couleurs[joueur.numero_joueur - 1]

    def activer_bouton(self, fonction):
        """
        Permet de cliquer sur le bouton fin du tour, et associe la fonction au clic.

        Args:
            fonction (fonction): La fonction à exécuter suite au clic de bouton
        """
        self.bouton_terminer_tour["state"] = "normal"
        self.clic_bouton = fonction

    def appui_bouton(self):
        """
        Effectue la fonction à exécuter suite au clic de bouton, et grise le bouton.
        """
        self.bouton_terminer_tour["state"] = "disabled"
        self.clic_bouton()


class FrameTableauJoueurs(Frame):
    def __init__(self, master):
        super().__init__(master)

        #### DÉBUT DÉFI TABLEAU DES JOUEURS ####
        # Une partie du code pour ce défi se trouve dans le constructeur,
        # le reste dans la méthode mise_a_jour

        # Initialization du tableau
        self.label_joueur_1 = Label(self, text="")
        self.label_joueur_2 = Label(self, text="")
        self.label_joueur_3 = Label(self, text="")
        self.label_joueur_4 = Label(self, text="")
        self.label_joueur_5 = Label(self, text="")

        # Placement des elements
        self.label_joueur_1.grid(row=0, column=0)
        self.label_joueur_2.grid(row=1, column=0)
        self.label_joueur_3.grid(row=2, column=0)
        self.label_joueur_4.grid(row=3, column=0)
        self.label_joueur_5.grid(row=4, column=0)

    def mise_a_jour(self):
        # Donne le nombre de dés de chaque joueur si il est encore en vie
        if len(self.master.joueurs[0].des) != 0:
            self.label_joueur_1["text"] = f"Joueur # 1 : {len(self.master.joueurs[0].des)} dés"
        else:
            self.label_joueur_1["text"] = f"Joueur # 1 : ÉLIMINÉ"

        if len(self.master.joueurs[1].des) != 0:
            self.label_joueur_2["text"] = f"Joueur # 2 : {len(self.master.joueurs[1].des)} dés"
        else:
            self.label_joueur_2["text"] = f"Joueur # 2 : ÉLIMINÉ"

        if len(self.master.joueurs) >= 3 and len(self.master.joueurs[2].des) != 0:
            self.label_joueur_3["text"] = f"Joueur # 3 : {len(self.master.joueurs[2].des)} dés"
        elif len(self.master.joueurs) >= 3:
            self.label_joueur_3["text"] = f"Joueur # 3 : ÉLIMINÉ"

        if len(self.master.joueurs) >= 4 and len(self.master.joueurs[3].des) != 0:
            self.label_joueur_4["text"] = f"Joueur # 4 : {len(self.master.joueurs[3].des)} dés"
        elif len(self.master.joueurs) >= 4:
            self.label_joueur_4["text"] = f"Joueur # 4 : ÉLIMINÉ"

        if len(self.master.joueurs) == 5 and len(self.master.joueurs[4].des) != 0:
            self.label_joueur_5["text"] = f"Joueur # 4 : {len(self.master.joueurs[4].des)} dés"
        elif len(self.master.joueurs) == 5:
            self.label_joueur_5["text"] = f"Joueur # 4 : ÉLIMINÉ"

        # Couleurs du texte
        self.label_joueur_1["fg"] = self.master.frame_joueur.couleurs[0]
        self.label_joueur_2["fg"] = self.master.frame_joueur.couleurs[1]
        self.label_joueur_3["fg"] = self.master.frame_joueur.couleurs[2]
        self.label_joueur_4["fg"] = self.master.frame_joueur.couleurs[3]
        self.label_joueur_5["fg"] = self.master.frame_joueur.couleurs[4]
        #### FIN DÉFI TABLEAU DES JOUEURS ####


class FrameTempsAttente(Frame):
    def __init__(self, master):
        super().__init__(master)
        #### DÉBUT DÉFI TEMPS ATTENTE ####
        self.a = IntVar()
        self.slider = Scale(master, orient=VERTICAL,
                            from_=500, to=10, variable=self.a)
        self.slider.grid(row=2, column=2)
        self.master.gestionnaire_io.temps_attente = self.valeur_slider

    def valeur_slider(self):
        return self.a.get()
        #### FIN DÉFI TEMPS ATTENTE ####
