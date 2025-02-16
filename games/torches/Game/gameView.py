import customtkinter as ctk
from tkinter import Canvas, PhotoImage

ctk.set_appearance_mode("dark")     
ctk.set_default_color_theme("green")

class GameView(ctk.CTk):
    def __init__(self, controller)-> None:
        super().__init__()
        self.controller = controller
        self.title("Jeu des allumettes")
        self.minsize(800, 500)
        self.maxsize(800, 500)

        self.message_label = ctk.CTkLabel(self, text="", font=("OCR A Extended", 20, "bold"), text_color="#32CD32")
        self.message_label.pack(pady=20)
        
        self.canvas = Canvas(self, width=725, height=325)
        self.canvas.pack()
        
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(pady=5)
        
        self.buttons = []
        self.buttons_create()
        
        self.torch_image = PhotoImage(file="games/torches/images/Torche.gif") # permet de mettre les torches minecraft en gif (mais pas encore résolu, elles bougent pas :/)
        #self.torch_image = self.torch_image.subsample(2,2) #divise par deux la taille de la torche, en x et y

        self.update_view()
    
    def update_view(self)-> None:
        self.canvas.delete("all")
        self.draw_matches(self.controller.get_nb_matches())
        self.message_label.configure(text=self.controller.get_status_message())
    
    def draw_matches(self, count: int)-> None:
        for i in range(count):
            x = 80 + i * 40
            self.canvas.create_image(x, 150, image=self.torch_image)
            
    def end_game(self)-> None: 
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        reset_button = ctk.CTkButton(self.buttons_frame, text="Recommencer", command=self.controller.reset_game)
        reset_button.pack(padx=10, pady=20)
    
    def reset(self)-> None:
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        self.buttons_create()
        self.update_view()

    def buttons_create(self)-> None: # pour éviter de se répéter dans le reset et le init
        for i in range(1, 4):
            button = ctk.CTkButton(self.buttons_frame, text=f"Prendre {i}", command=lambda n=i: self.controller.handle_human_move(n))
            button.pack(side="left", padx=10, pady=20)
            self.buttons.append(button)