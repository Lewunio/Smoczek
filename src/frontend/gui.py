import os.path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox
from src.backend.pet import Pet
from src.backend.save import save_game, load_game
from .tools import make_image_button
from .game import DinoGame

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
    canvas.is_sleeping = False
    canvas.bg_id = canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    root.bg_photo = bg_photo  # referencja, żeby nie usunęło z pamięci

    # === ZWIERZAK ===
    pet_image_path = f"src/frontend/assets/{pet.species}/static_pet.png"
    pet_img = Image.open(pet_image_path).resize((400, 400))  # rozmiar możesz zmienić
    pet_photo = ImageTk.PhotoImage(pet_img)
    canvas.pet_photo = pet_photo  # zapamiętaj referencję
    canvas.pet_image_id = canvas.create_image(720, 480, image=pet_photo)

    def change_pet_image(image_path, duration_ms=1000):
        new_img = Image.open(image_path).resize((400, 400))
        new_photo = ImageTk.PhotoImage(new_img)
        canvas.pet_photo = new_photo
        canvas.itemconfig(canvas.pet_image_id, image=new_photo)

        # Po upływie czasu wróć do podstawowego obrazka
        def revert_image():
            static_path = f"src/frontend/assets/{pet.species}/static_pet.png"
            static_img = Image.open(static_path).resize((400, 400))
            static_photo = ImageTk.PhotoImage(static_img)
            canvas.pet_photo = static_photo
            canvas.itemconfig(canvas.pet_image_id, image=static_photo)

        canvas.after(duration_ms, revert_image)

    def update_labels():
        canvas.itemconfig(canvas.exp_value_text, text=str(int(pet.exp)))
        canvas.itemconfig(canvas.hunger_value_text, text=f"{int(pet.hunger)} / {int(pet.hunger_level)}")
        canvas.itemconfig(canvas.tired_value_text, text=f"{int(pet.tired)} / 100")


    def decay_stats():
        pet.update_stats()
        update_labels()
        root.after(3000, decay_stats)


    # === PRZYCISKI ===
    # === PRZYCISKI-GRAFIKI ===
    meat_icon = ImageTk.PhotoImage(Image.open("src/frontend/assets/items/meat_in_frame.png").resize((150, 150)))
    game_icon = ImageTk.PhotoImage(Image.open("src/frontend/assets/items/game.png").resize((150, 150)))
    sleep_icon = ImageTk.PhotoImage(Image.open("src/frontend/assets/items/sleep.png").resize((150, 150)))

    canvas.meat_icon = meat_icon
    canvas.game_icon = game_icon
    canvas.sleep_icon = sleep_icon

    button_y = HEIGHT - 100
    button_spacing = 150
    button_start_x = WIDTH // 2 - button_spacing

    canvas.create_image(button_start_x, button_y, image=sleep_icon, anchor="center", tags="sleep")
    canvas.create_image(WIDTH // 2, button_y, image=meat_icon, anchor="center", tags="eat")
    canvas.create_image(WIDTH // 2 + button_spacing, button_y, image=game_icon, anchor="center", tags="play")

    def on_icon_click(event):
        item = canvas.find_closest(event.x, event.y)[0]
        tags = canvas.gettags(item)
        if "sleep" in tags:
            pet.sleep()
            canvas.is_sleeping = not canvas.is_sleeping

            new_bg_path = (
                "src/frontend/assets/backgrounds/cave_night.png"
                if canvas.is_sleeping
                else "src/frontend/assets/backgrounds/cave.png"
            )
            new_bg = Image.open(new_bg_path).resize((WIDTH, HEIGHT))
            new_bg_photo = ImageTk.PhotoImage(new_bg)
            canvas.bg_photo = new_bg_photo
            canvas.itemconfig(canvas.bg_id, image=new_bg_photo)
            new_pet_image_path = (
                f"src/frontend/assets/{pet.species}/sleep_pet.png"
                if canvas.is_sleeping
                else f"src/frontend/assets/{pet.species}/static_pet.png"
            )
            pet_img = Image.open(new_pet_image_path).resize((400, 400))
            pet_photo = ImageTk.PhotoImage(pet_img)
            canvas.pet_photo = pet_photo
            canvas.itemconfig(canvas.pet_image_id, image=pet_photo)


        elif "eat" in tags:
            if not pet.sleeping:
                pet.eat()
                eating_path = f"src/frontend/assets/{pet.species}/eating_pet.png"
                if os.path.exists(eating_path):
                    change_pet_image(eating_path, 1000)
        elif "play" in tags:
            if not pet.sleeping:
                game(root,pet)
        update_labels()

    canvas.tag_bind("sleep", "<Button-1>", on_icon_click)
    canvas.tag_bind("eat", "<Button-1>", on_icon_click)
    canvas.tag_bind("play", "<Button-1>", on_icon_click)


    exp_icon = ImageTk.PhotoImage(Image.open("src/frontend/assets/icons/exp.png").resize((120, 120)))
    canvas.exp_icon = exp_icon  # referencja żeby nie znikło

    # === HUNGER (GŁÓD) W LEWYM GÓRNYM ROGU ===
    hunger_icon = ImageTk.PhotoImage(Image.open("src/frontend/assets/icons/hungry_icon.png").resize((80, 80)))
    canvas.hunger_icon = hunger_icon  # zapamiętaj referencję

    # Dodaj ikonkę głodu
    canvas.create_image(30, 30, image=hunger_icon, anchor="nw")

    # Dodaj tekst głodu
    canvas.hunger_value_text = canvas.create_text(
        130, 50,
        text=f"{pet.hunger} / {pet.hunger_level}",
        fill="white",
        font=("Arial", 26, "bold"),
        anchor="w"
    )


    # pozycja w prawym górnym rogu
    canvas.create_image(WIDTH - 180, 30, image=exp_icon, anchor="ne")
    canvas.exp_value_text = canvas.create_text(WIDTH - 100, 80, text=str(int(pet.exp)), fill="white",
                                               font=("Arial", 38, "bold"), anchor="ne")

    # === TIRED (ZMĘCZENIE) PONIŻEJ GŁODU ===
    tired_icon = ImageTk.PhotoImage(Image.open("src/frontend/assets/icons/grey_hungry_icon.png").resize((80, 80)))
    canvas.tired_icon = tired_icon  # zapamiętaj referencję

    canvas.create_image(30, 130, image=tired_icon, anchor="nw")  # niżej o 100px

    canvas.tired_value_text = canvas.create_text(
        130, 150,
        text=f"{int(pet.tired)} / 100",
        fill="white",
        font=("Arial", 26, "bold"),
        anchor="w"
    )

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

    species_packages = ["reddragon", "tiger", "fenix", "gryf"]

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

                chosen_species_package = species_packages[species_index]
                required_food = int(food_str)
                play_time_required = int(play_str)
                pet = Pet(name=name, species=chosen_species_package, hunger_level=required_food)
                start_game_callback(pet)

    canvas.bind("<Button-1>", on_click)



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



    btn_path = "src/frontend/assets/backgrounds/button_background.png"
    btn_img = Image.open(btn_path).resize((400, 75))
    btn_photo = ImageTk.PhotoImage(btn_img)
    canvas.btn_photo = btn_photo  # zapamiętaj referencję!

    make_image_button(canvas, WIDTH // 2, 400, "Nowa gra", lambda: choose_egg(root, start_game_callback=lambda pet: window(root, pet)), btn_photo)
    make_image_button(canvas, WIDTH // 2, 525, "Wczytaj grę", lambda: load_existing_game(root), btn_photo)
    make_image_button(canvas, WIDTH // 2, 650, "Wyjście", root.destroy, btn_photo)

    root.mainloop()
def load_existing_game(root):
    try:
        pet = load_game()
        window(root,pet)
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wczytać gry:\n{e}")
def game(root, pet):
    DinoGame(root,pet)
    window(root,pet)
