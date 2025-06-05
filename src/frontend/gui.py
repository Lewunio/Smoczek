import os.path
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox
from src.backend.pet import Pet
from src.backend.save import save_game, load_game


# def window(pet):
#
#     root = tk.Tk()
#     root.title("Zwierzak GUI")
#
#
#     bg_path = os.path.join("src", "frontend", "assets", "backgrounds", "cave.png")
#     bg_image = Image.open(bg_path)
#     bg_photo = ImageTk.PhotoImage(bg_image)
#
#     canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height)
#     canvas.pack()
#     canvas.create_image(0,0,image=bg_photo, anchor="nw")
#
#
#     name_label = tk.Label(root, text="", bg="#ffffff", font=("Arial",14))
#     name_label_window = canvas.create_window(50,50, anchor="nw", window=name_label)
#
#     # Labels
#     name_label = tk.Label(frame, text="")
#     species_label = tk.Label(frame, text="")
#     birth_label = tk.Label(frame, text="")
#     happy_label = tk.Label(frame, text="")
#     hunger_label = tk.Label(frame, text="")
#     tired_label = tk.Label(frame, text="")
#     exp_label = tk.Label(frame, text="")
#
#     def update_labels():
#         name_label.config(text=f"Imię: {pet.name}")
#         species_label.config(text=f"Gatunek: {pet.species}")
#         birth_label.config(text=f"Urodzony: {pet.birth}")
#         happy_label.config(text=f"❤️ Szczęście: {pet.happy}/100")
#         hunger_label.config(text=f"🍗 Głód: {pet.hunger}/100")
#         tired_label.config(text=f"😴 Zmęczenie: {pet.tired}/100")
#         exp_label.config(text=f"⭐ Doświadczenie: {pet.exp}")
#
#     def decay_stats():
#         pet.update_stats()
#         update_labels()
#         root.after(3000, decay_stats)
#
#     for label in [name_label, species_label, birth_label, happy_label, hunger_label, tired_label, exp_label]:
#         label.pack(anchor="w")
#
#     # Buttons
#     button_frame = tk.Frame(root, pady=10)
#     button_frame.pack()
#
#     tk.Button(button_frame, text="😴 Śpij", command=pet.sleep, width=10).grid(row=0, column=0, padx=5)
#     tk.Button(button_frame, text="🍗 Jedz", command=pet.eat, width=10).grid(row=0, column=1, padx=5)
#     tk.Button(button_frame, text="🎮 Baw się", command=pet.play, width=10).grid(row=0, column=2, padx=5)
#
#     update_labels()
#     decay_stats()
#     root.mainloop()

def make_image_button(canvas, x, y, text, command, image):
    width = 400
    height = 75
    canvas.create_rectangle(
        x - width // 2 - 4, y - height // 2 - 4,
        x + width // 2 + 4, y + height // 2 + 4,
        outline="#4c2306", width=6  # kolor i grubość obramowania
    )


    button = tk.Button(
        canvas,
        text=text,
        image=image,
        compound="center",
        font=("Arial", 30, "bold"),
        fg="#4c2406",
        borderwidth=0,
        highlightthickness=0,
        command=command
    )
    canvas.create_window(x,y,window=button)
def menu():
    root = tk.Tk()
    root.title("Menu Główne")
    WIDTH, HEIGHT = 1000, 800
    root.geometry(f"{WIDTH}x{HEIGHT}")

    bg_path = os.path.join("frontend", "assets", "backgrounds", "menu.png")
    bg_image = Image.open(bg_path).resize((WIDTH, HEIGHT))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0,0,image=bg_photo, anchor="nw")
    canvas.bg_photo = bg_photo

    #logo
    logo_path = os.path.join("frontend", "assets","icons", "logo.png")
    logo_img = Image.open(logo_path).resize((500,400))
    logo_photo = ImageTk.PhotoImage(logo_img)
    canvas.logo_photo = logo_photo
    canvas.create_image(WIDTH//2,200,image=logo_photo, anchor="center")

    def start_new_game():
        name = simpledialog.askstring("Nowa gra", "Podaj imię zwierzaka:")
        if not name:
            return
        species = simpledialog.askstring("Nowa gra", "Podaj gatunek:")
        if not species:
            return
        pet = Pet(name, species)
        root.destroy()
        window(pet)

    def load_existing_game():
        try:
            pet = load_game()
            root.destroy()
            window(pet)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać gry:\n{e}")

    button_style = {
        "bg": "#ffffff",
        "fg": "#333333",
        "font": ("Arial", 12, "bold"),
        "width": 20,
        "relief": "raised"
    }
    btn_path = os.path.join("frontend", "assets", "backgrounds", "button_background.png")
    btn_img = Image.open(btn_path).resize((400, 75))
    btn_photo = ImageTk.PhotoImage(btn_img)
    canvas.btn_photo = btn_photo  # zapamiętaj referencję!

    make_image_button(canvas, WIDTH // 2, 400, "Nowa gra", start_new_game, btn_photo)
    make_image_button(canvas, WIDTH // 2, 525, "Wczytaj grę", load_existing_game, btn_photo)
    make_image_button(canvas, WIDTH // 2, 650, "Wyjście", root.destroy, btn_photo)

    root.mainloop()

    def game():
        pass
