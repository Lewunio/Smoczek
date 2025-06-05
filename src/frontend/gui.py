import os.path
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox
from src.backend.pet import Pet
from src.backend.save import save_game, load_game

chosen_species_package = None
required_food = None
play_time_required = None

def window(root, pet):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Zwierzak GUI")
    WIDTH, HEIGHT = 1400, 800

    # tło jaskini

    bg_path = "src/frontend/assets/backgrounds/cave.png"
    bg_image = Image.open(bg_path).resize((WIDTH, HEIGHT))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    root.bg_photo = bg_photo  # referencja, żeby nie usunęło z pamięci

    # === ZWIERZAK ===
    pet_image_path = f"src/frontend/assets/{pet.species}/static_pet.png"
    pet_img = Image.open(pet_image_path).resize((300, 300))  # rozmiar możesz zmienić
    pet_photo = ImageTk.PhotoImage(pet_img)
    canvas.pet_photo = pet_photo  # zapamiętaj referencję
    canvas.create_image(WIDTH // 2, HEIGHT // 2, image=pet_photo)

    # === INFOKA ===
    info_frame = tk.Frame(root, bg="#ffffff")
    canvas.create_window(50, 50, anchor="nw", window=info_frame)

    name_label = tk.Label(info_frame, text="", bg="#ffffff", font=("Arial", 14))
    species_label = tk.Label(info_frame, text="", bg="#ffffff", font=("Arial", 14))
    birth_label = tk.Label(info_frame, text="", bg="#ffffff", font=("Arial", 14))
    happy_label = tk.Label(info_frame, text="", bg="#ffffff", font=("Arial", 14))
    hunger_label = tk.Label(info_frame, text="", bg="#ffffff", font=("Arial", 14))
    tired_label = tk.Label(info_frame, text="", bg="#ffffff", font=("Arial", 14))
    exp_label = tk.Label(info_frame, text="", bg="#ffffff", font=("Arial", 14))

    for label in [name_label, species_label, birth_label, happy_label, hunger_label, tired_label, exp_label]:
        label.pack(anchor="w")

    def update_labels():
        name_label.config(text=f"Imię: {pet.name}")
        species_label.config(text=f"Gatunek: {pet.species}")
        birth_label.config(text=f"Urodzony: {pet.birth}")
        happy_label.config(text=f"❤️ Szczęście: {pet.happy}/100")
        hunger_label.config(text=f"🍗 Głód: {pet.hunger}/100")
        tired_label.config(text=f"😴 Zmęczenie: {pet.tired}/100")
        exp_label.config(text=f"⭐ Doświadczenie: {pet.exp}")

    def decay_stats():
        pet.update_stats()
        update_labels()
        root.after(3000, decay_stats)

    # === PRZYCISKI ===
    button_frame = tk.Frame(root, pady=10, bg="#ffffff")
    canvas.create_window(WIDTH // 2, HEIGHT - 100, anchor="center", window=button_frame)

    tk.Button(button_frame, text="😴 Śpij", command=pet.sleep, width=10).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="🍗 Jedz", command=pet.eat, width=10).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="🎮 Baw się", command=pet.play, width=10).grid(row=0, column=2, padx=5)

    update_labels()
    decay_stats()

def choose_egg(root, start_game_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Wybierz swojego podopiecznego")
    WIDTH, HEIGHT = 1400, 800

    bg_path = "src/frontend/assets/backgrounds/cave.png"
    bg_image = Image.open(bg_path).resize((WIDTH, HEIGHT))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    root.bg_photo = bg_photo  # żeby nie wyczyściło obrazka z pamięci

    placeholder_text = "Podaj imie zwierzaka"
    entry_width = 30

    # Tworzymy ramkę do trzymania entry
    # === POLA TEKSTOWE ===
    placeholder_texts = [
        "Podaj imie zwierzaka",
        "Ilość pożywienia do przeżycia",
        "Czas zabawy (w sekundach)"
    ]
    entries = []

    for i, placeholder in enumerate(placeholder_texts):
        frame = tk.Frame(canvas, width=300, height=75, bg="black")
        frame.pack_propagate(False)  # nie dopuszcza, żeby Frame zmniejszył się do rozmiaru Entry

        entry = tk.Entry(
            frame,
            font=("Arial", 20, "italic"),
            fg="gray",
            bg="black",
            insertbackground="white",
            bd=4,
            relief="ridge",
            justify="center"
        )
        entry.insert(0, placeholder)
        entry.pack(fill="both", expand=True)

        canvas.create_window(WIDTH // 2, 100 + i * 90, window=frame)

        def make_focus_in(entry_ref=entry, ph=placeholder):
            return lambda e: (
                entry_ref.delete(0, tk.END),
                entry_ref.config(font=("Arial", 20, "normal"), fg="white")
            ) if entry_ref.get() == ph else None

        def make_focus_out(entry_ref=entry, ph=placeholder):
            return lambda e: (
                entry_ref.insert(0, ph),
                entry_ref.config(font=("Arial", 20, "italic"), fg="gray")
            ) if entry_ref.get().strip() == "" else None

        entry.bind("<FocusIn>", make_focus_in())
        entry.bind("<FocusOut>", make_focus_out())

        entries.append(entry)

    root.after(100, lambda: entries[0].focus_force())

    # === Jajka ===
    egg_images = []
    egg_ids = []

    start_x = 400
    gap = 200

    species_packages = ["reddragon", "fenix", "gryf", "tiger"]

    for i in range(4):
        path = f"src/frontend/assets/eggs/egg{i+1}.png"
        img = Image.open(path).resize((200, 200))
        photo = ImageTk.PhotoImage(img)
        egg_images.append(photo)

        x = start_x + i * gap
        y = 600

        egg_id = canvas.create_image(x, y, image=photo, anchor="center")
        egg_ids.append((egg_id, i))

    canvas.egg_images = egg_images

    def on_click(event):
        global chosen_species_package
        clicked = canvas.find_closest(event.x, event.y)[0]
        for egg_id, species_index in egg_ids:
            if clicked == egg_id:
                name = entries[0].get().strip()
                food_str = entries[1].get().strip()
                play_str = entries[2].get().strip()

                if name == "" or name == placeholder_texts[0]:
                    messagebox.showwarning("Błąd", "Podaj imię zwierzaka!")
                    return
                if not food_str.isdigit():
                    messagebox.showwarning("Błąd", "Podaj poprawną ilość pożywienia (liczba całkowita)!")
                    return
                if not play_str.isdigit():
                    messagebox.showwarning("Błąd", "Podaj poprawny czas zabawy (liczba całkowita w sekundach)!")
                    return

                global chosen_species_package, required_food, play_time_required
                chosen_species_package = species_packages[species_index]
                required_food = int(food_str)
                play_time_required = int(play_str)
                pet = Pet(name, chosen_species_package)
                window(root, pet)

    canvas.bind("<Button-1>", on_click)


def make_image_button(canvas, x, y, text, command, image):
    width = 400
    height = 75
    ramka = canvas.create_rectangle(
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
    return [canvas.create_window(x,y,window=button), ramka]
def menu():
    root = tk.Tk()
    root.title("Menu Główne")
    root.attributes("-topmost", True)
    WIDTH, HEIGHT = 1400, 800
    root.geometry(f"{WIDTH}x{HEIGHT}")

    # srodek ekraniu
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (WIDTH // 2)
    y = (screen_height // 2) - (HEIGHT // 2)
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    bg_path = "src/frontend/assets/backgrounds/menu.png"
    bg_image = Image.open(bg_path).resize((WIDTH, HEIGHT))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0,0,image=bg_photo, anchor="nw")
    canvas.bg_photo = bg_photo

    #logo
    logo_path = "src/frontend/assets/icons/logo.png"
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
    btn_path = "src/frontend/assets/backgrounds/button_background.png"
    btn_img = Image.open(btn_path).resize((400, 75))
    btn_photo = ImageTk.PhotoImage(btn_img)
    canvas.btn_photo = btn_photo  # zapamiętaj referencję!

    make_image_button(canvas, WIDTH // 2, 400, "Nowa gra", lambda: choose_egg(root, start_game_callback=lambda pet: window(root, pet)), btn_photo)
    make_image_button(canvas, WIDTH // 2, 525, "Wczytaj grę", load_existing_game, btn_photo)
    make_image_button(canvas, WIDTH // 2, 650, "Wyjście", root.destroy, btn_photo)

    root.mainloop()

    def game():
        pass
