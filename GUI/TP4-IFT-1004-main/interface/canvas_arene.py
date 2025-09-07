"""
Ce module contient la classe CanvasArene, qui permet de dessiner l'ensemble de l'arène
et de gérer les clics.
"""
from math import ceil, floor
from tkinter import Canvas, ALL, LAST

# Cette constante donne la hauteur totale de l'arène, en pixels.
DIMENSION_BASE = 300


class CanvasArene(Canvas):
    def __init__(self, master, arene):
        """
        Constructeur de la classe CanvasArene. Attribue les dimensions en pixels
        en fonction des dimensions de l'arène, dessine l'arène dans l'interface
        et associe le clic de souris à la méthode selectionner_case.

        Args:
            master (Tk): Le widget TKinter dans lequel le canvas s'intègre.
            arene (Arene): L'arène des GlaDéateurs à afficher.
        """
        self.arene = arene
        self.dimension_canvas = DIMENSION_BASE
        super().__init__(master, width=self.dimension_canvas + 1,
                         height=self.dimension_canvas + 1,
                         borderwidth=0, highlightthickness=0)

        self.suite_clic = None
        self.coordonnees_cliquables = lambda coordonnees: False
        self.dimension_case = self.dimension_canvas // self.arene.dimension
        self.bind("<Button-1>", self.selectionner_case)
        self.dessiner_canvas(lambda: None)

    def pixel_vers_coordonnees(self, x, y):
        """
        Cette méthode convertit la position d'un clic en coordonnées de l'arène.

        Args:
            x: La position du clic, en x (de haut en bas)
            y: La position du clic, en y (de gauche à droite)

        Returns:
            tuple: Les coordonnées de la case cliquée.
        """
        return x // self.dimension_case, y // self.dimension_case

    def coordonnees_vers_pixels(self, x, y, milieu=False):
        """
        Cette méthode des coordonnées de l'arène en position en pixels

        Args:
            x (int): La coordonnée en x
            y (int): La coordonnée en y
            milieu (bool): Si True, le centre de la case est retourné.
                           Si False, le coin haut-gauche est retourné.

        Returns:
            tuple: La position en pixels.
        """
        if milieu:
            return (x + 0.5) * self.dimension_case, (y + 0.5) * self.dimension_case
        else:
            return x * self.dimension_case, y * self.dimension_case

    def selectionner_case(self, event):
        """
        Cette méthode prend en argument un clic de souris sur le canvas, et actionne
        la fonction définie comme devant faire suite au clic (self.suite_clic), dont
        l'argument est en coordonnées plutôt qu'en pixels.

        Args:
            event (tkinter.Event): L'événement correspondant au clic

        """
        x, y = event.y, event.x  # nos coordonnées sont transposées par rapport aux pixels
        coordonnees = self.pixel_vers_coordonnees(x, y)
        if self.suite_clic is not None and self.coordonnees_cliquables(coordonnees):
            self.suite_clic(coordonnees)

    def dessiner_canvas(self, suite):
        """
        Cette méthode dessine l'arène.

        Args:
            suite (fonction): La suite du programme
        """
        self.delete(ALL)
        for i in range(self.arene.dimension ** 2):
            x, y = i // self.arene.dimension, i % self.arene.dimension
            haut, gauche = self.coordonnees_vers_pixels(x, y)
            bas, droite = self.coordonnees_vers_pixels(x + 1, y + 1)
            if self.coordonnees_cliquables((x, y)):
                remplissage = 'pink'
            else:
                remplissage = 'white'
            self.create_rectangle(gauche, haut, droite, bas,
                                  outline='gray', fill=remplissage, width=1)
            if (x, y) in self.arene.des:
                self.dessiner_de((x, y), gauche + 5, haut + 5, droite - 5, bas - 5)

        self.create_rectangle(0, 0, self.dimension_canvas, self.dimension_canvas,
                              outline='black', width=5)
        suite()

    def dessiner_de(self, coordonnees, gauche, haut, droite, bas):
        self.create_rectangle(gauche, haut, droite, bas, fill='white',
                              outline='black', width=3)
        texte_de = self.arene.afficher_de(coordonnees)
        if texte_de.isnumeric() or texte_de == 'X':
            self.create_text((gauche + droite) // 2, (haut + bas) // 2, fill='black',
                             font="Times 20 bold", text=texte_de)
        else:
            #### DÉBUT DÉFI DESSINER DÉS ####
            # Commencez par supprimer la ligne du raise.
            l = (droite - gauche) // 10
            if texte_de == "⚁":
                self.create_oval(gauche+l, haut+l, gauche+3*l, haut+3*l, fill="black")
                self.create_oval(gauche+7*l, haut+7*l, gauche+9*l, haut+9*l, fill="black")
            if texte_de == "⚂":
                self.create_oval(gauche + l, haut + l, gauche + 3 * l, haut + 3 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + 7 * l, gauche + 9 * l, haut + 9 * l, fill="black")
                self.create_oval(gauche + 4 * l, haut + 4 * l, gauche + 6 * l, haut + 6 * l, fill="black")
            if texte_de == "⚃":
                self.create_oval(gauche + l, haut + l, gauche + 3 * l, haut + 3 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + 7 * l, gauche + 9 * l, haut + 9 * l, fill="black")
                self.create_oval(gauche + l, haut + 7 * l, gauche + 3 * l, haut + 9 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + l, gauche + 9 * l, haut + 3 * l, fill="black")
            if texte_de == "⚄":
                self.create_oval(gauche + l, haut + l, gauche + 3 * l, haut + 3 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + 7 * l, gauche + 9 * l, haut + 9 * l, fill="black")
                self.create_oval(gauche + l, haut + 7 * l, gauche + 3 * l, haut + 9 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + l, gauche + 9 * l, haut + 3 * l, fill="black")
                self.create_oval(gauche + 4 * l, haut + 4 * l, gauche + 6 * l, haut + 6 * l, fill="black")
            if texte_de == "⚅":
                self.create_oval(gauche + l, haut + l, gauche + 3 * l, haut + 3 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + 7 * l, gauche + 9 * l, haut + 9 * l, fill="black")
                self.create_oval(gauche + l, haut + 7 * l, gauche + 3 * l, haut + 9 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + l, gauche + 9 * l, haut + 3 * l, fill="black")
                self.create_oval(gauche + l, haut + 4 * l, gauche + 3 * l, haut + 6 * l, fill="black")
                self.create_oval(gauche + 7 * l, haut + 4 * l, gauche + 9 * l, haut + 6 * l, fill="black")
            #### FIN DÉFI DESSINER DÉS ####

    def permettre_clics(self, case_cliquable, suite_clic):
        """
        Cette méthode associe une fonction à exécuter à ce qui doit arriver suite
        à un clic, pour les cases où le clic est permis.

        Args:
            case_cliquable (fonction): Fonction qui détermine si des coordonnées sont cliquables
            suite_clic (fonction): Fonction à exécuter suite au clic d'une cases
        """
        self.coordonnees_cliquables = case_cliquable
        self.suite_clic = suite_clic
        self.dessiner_canvas(lambda: None)

    def afficher_lancer(self, lancer, temps_attente, suite):
        """
        Désactive les clics et affiche le lancer.

        Args:
            lancer (Lancer): le lancer à afficher
            temps_attente (int): Temps en millisecondes avant d'exécuter la suite
            suite (fonction): la suite du programme
        """
        self.suite_clic = None
        self.coordonnees_cliquables = lambda _: False
        traj = lancer.trajectoire
        for i in range(len(traj) - 1):
            x1, y1 = traj[i]
            x2, y2 = traj[i + 1]
            self.create_line(*self.coordonnees_vers_pixels(y1, x1, True),
                             *self.coordonnees_vers_pixels(y2, x2, True),
                             arrow=LAST)
        self.after(temps_attente, suite)
