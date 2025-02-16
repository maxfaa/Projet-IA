"""
Module qui gère l'interface graphique du jeu des alumettes
"""
from tkinter import PhotoImage
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class GameView(ctk.CTk):
    """
    Interface graphique des alumettes

    Attributes:
        controller : instance de GameController
        buttons (list): liste de boutons
        message_label : affichage des messages
        canvas : zone des alumettes
        buttons_frame = zone des boutons
        torch_image = fichier de la torche minecraft
    """
    def __init__(self, controller):
        """
        initialisation de gameView
        Args:
            controller; instance de GameController
        """
        super().__init__()
        self.controller = controller
        self.title("Jeu des allumettes")
        self.minsize(800, 500)
        self.maxsize(800, 500)

        self.message_label = ctk.CTkLabel(
            self,
            text="",
            font=("OCR A Extended",20, "bold"),
            text_color="#32CD32"
            )
        self.message_label.pack(pady=20)

        self.canvas = ctk.CTkCanvas(self, width=725, height=325,bg= "#323232")
        self.canvas.pack()

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=5)

        self.buttons = []
        self.buttons_create()

        self.torch_image = PhotoImage(file="games/torches/images/Torche.gif")
        #permet de mettre les torches minecraft en gif (pas encore résolu, elles bougent pas :/)
        #self.torch_image = self.torch_image.subsample(2,2)
        #divise par deux la taille de la torche, en x et y

        self.update_view()

    def update_view(self):
        """
        Met à jour l'affichage de l'écran en supprimant et en refaisant les alumettes
        """
        self.canvas.delete("all")
        self.draw_matches(self.controller.get_nb_torchs())
        self.message_label.configure(text=self.controller.get_status_message())

    def draw_matches(self, count):
        """
        Createur d'alumettes en fonction du nombre count
        Args: 
            count : nombre d'alumettes
        """
        for i in range(count):
            pos_x = 80 + i * 40
            self.canvas.create_image(pos_x, 150, image=self.torch_image)

    def end_game(self):
        """
        efface les boutons précédents et fait le bouton "recommencer"
        """
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="Recommencer",
            command=self.controller.reset_game
            )
        reset_button.pack(padx=10, pady=20)

    def reset(self):
        """
        Réinitialise le jeu en supprimant les boutons précédents et
        fait le boutons de choix d'alumettes. Met à jour la vue
        """
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        self.buttons_create()
        self.update_view()

    def buttons_create(self):
        """
        Créateur de boutons de choix d'alumettes, pour éviter la redondance
        """
        for i in range(1, 4):
            button = ctk.CTkButton(
                self.buttons_frame,
                text=f"Prendre {i}",
                command=lambda n=i: self.controller.handle_human_move(n)
                )
            button.pack(side="left", padx=10, pady=20)
            self.buttons.append(button)
