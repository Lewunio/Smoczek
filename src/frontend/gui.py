import os.path
import tkinter as tk
from tkinter import messagebox
from src.backend.pet import Pet
from src.backend.save import save_game, load_game
from .tools import make_image_button, load_photo
from .game import DinoGame

WIDTH, HEIGHT = 1400, 800

def window(root:tk.Tk, pet:Pet):
    """
    Główne okno gry

    Args:
        root (tk.Tk): Okno gry
        pet (Pet): Postać gry
    """
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Zwierzak GUI")



    def save_on_close():
        """
        Zapisywanie przy zamykaniu
        """
        should_save = messagebox.askyesno("Zamknij grę", "Czy chcesz zapisać grę przed wyjściem?",parent=root)
        if should_save:
            save_game(pet)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", save_on_close)
    # tło jaskini

    bg_photo = load_photo("src/frontend/assets/backgrounds/cave.png", WIDTH, HEIGHT)
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    canvas.is_sleeping = False
    canvas.bg_id = canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    root.bg_photo = bg_photo  # referencja, żeby nie usunęło z pamięci

    # === ZWIERZAK ===
    pet_photo = load_photo(f"src/frontend/assets/{pet.species}/static_pet.png", 400, 400)
    canvas.pet_photo = pet_photo  # zapamiętaj referencję
    canvas.pet_image_id = canvas.create_image(WIDTH//2, 480, image=pet_photo)
    #=== IMIE ===
    canvas.name_text = canvas.create_text(
        WIDTH//2, 200,
        text=pet.name,
        fill="#8a3115",
        font=("Papyrus",120,"bold"),
        anchor="s",
    )

    def change_pet_image(image_path, duration_ms=1000):
        """Zmiana zdjęcia czasowo"""
        new_photo = load_photo(image_path, 400, 400)
        canvas.pet_photo = new_photo
        canvas.itemconfig(canvas.pet_image_id, image=new_photo)

        def revert_image():
            """Po upływie czasu wróć do podstawowego obrazka"""
            static_photo = load_photo(f"src/frontend/assets/{pet.species}/static_pet.png", 400, 400)
            canvas.pet_photo = static_photo
            canvas.itemconfig(canvas.pet_image_id, image=static_photo)

        canvas.after(duration_ms, lambda: (revert_image(), update_labels()))

    def update_labels():
        """
        Funkcja aktualizująca dane w GUI
        """
        canvas.itemconfig(canvas.exp_value_text, text=str(int(pet.exp)))
        canvas.itemconfig(canvas.hunger_value_text, text=f"{int(pet.hunger)} / {int(pet.hunger_level)}")
        canvas.itemconfig(canvas.tired_value_text, text=f"{int(pet.tired)} / 100")
        canvas.itemconfig(canvas.happy_icon_text, text=f"{int(pet.happy)} / {int(pet.happy_level)}")

        hunger_percent = pet.hunger / pet.hunger_level if pet.hunger_level > 0 else 1
        tired_percent = pet.tired / 100 if pet.tired is not None else 1

        if canvas.is_sleeping:
            new_pet_image_path = f"src/frontend/assets/{pet.species}/sleep_pet.png"
            if os.path.exists(new_pet_image_path):
                sleep_photo = load_photo(new_pet_image_path, 400, 400)
                canvas.pet_photo = sleep_photo
                canvas.itemconfig(canvas.pet_image_id, image=sleep_photo)
            return

        image_path = f"src/frontend/assets/{pet.species}/static_pet.png"

        if hunger_percent <= 0.3 and tired_percent <= 0.3:
            test_path = f"src/frontend/assets/{pet.species}/hungry_tired_pet.png"
            if os.path.exists(test_path):
                image_path = test_path
        elif hunger_percent <= 0.3:
            test_path = f"src/frontend/assets/{pet.species}/hungry_pet.png"
            if os.path.exists(test_path):
                image_path = test_path
        elif tired_percent <= 0.3:
            test_path = f"src/frontend/assets/{pet.species}/tired_pet.png"
            if os.path.exists(test_path):
                image_path = test_path

        status_photo = load_photo(image_path, 400, 400)
        canvas.pet_photo = status_photo
        canvas.itemconfig(canvas.pet_image_id, image=status_photo)

    def decay_stats():
        """
        Obniżanie statów zwierzaka
        """
        if not canvas.winfo_exists():
            return  # Canvas już nie istnieje – zakończ
        pet.update_stats()
        update_labels()
        root.after(3000, decay_stats)


    # === PRZYCISKI ===
    # === PRZYCISKI-GRAFIKI ===

    meat_icon = load_photo("src/frontend/assets/items/meat_in_frame.png",150, 150)
    game_icon = load_photo("src/frontend/assets/items/game.png", 150, 150)
    sleep_icon = load_photo("src/frontend/assets/items/sleep.png", 150, 150)

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
        """Zachowanie po kliknięciu ikony"""
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
            new_bg_photo = load_photo(new_bg_path, WIDTH, HEIGHT)
            canvas.bg_photo = new_bg_photo
            canvas.itemconfig(canvas.bg_id, image=new_bg_photo)
            new_pet_image_path = (
                f"src/frontend/assets/{pet.species}/sleep_pet.png"
                if canvas.is_sleeping
                else f"src/frontend/assets/{pet.species}/static_pet.png"
            )
            pet_photo2 = load_photo(new_pet_image_path, 400, 400)
            canvas.pet_photo = pet_photo2
            canvas.itemconfig(canvas.pet_image_id, image=pet_photo2)

            update_labels()

        elif "eat" in tags:
            if pet.can_eat:
                pet.eat()
                eating_path = f"src/frontend/assets/{pet.species}/eating_pet.png"
                if os.path.exists(eating_path):
                    change_pet_image(eating_path, 1000)
                    root.after(1000, update_labels)
                else:
                    update_labels()
            else:
                update_labels()
        elif "play" in tags:
            if not pet.sleeping:
                game(root,pet)
            update_labels()

    canvas.tag_bind("sleep", "<Button-1>", on_icon_click)
    canvas.tag_bind("eat", "<Button-1>", on_icon_click)
    canvas.tag_bind("play", "<Button-1>", on_icon_click)


    exp_icon = load_photo("src/frontend/assets/icons/exp.png", 120, 120)
    canvas.exp_icon = exp_icon  # referencja żeby nie znikło

    # === HUNGER (GŁÓD) W LEWYM GÓRNYM ROGU ===
    hunger_icon = load_photo("src/frontend/assets/icons/hungry_icon.png",80,80)
    canvas.hunger_icon = hunger_icon  # zapamiętaj referencję

    # Dodaj ikonkę głodu
    canvas.create_image(30, 30, image=hunger_icon, anchor="nw")
    # tutaj
    # Dodaj tekst głodu
    canvas.hunger_value_text = canvas.create_text(
        120, 68,
        text=f"{pet.hunger} / {pet.hunger_level}",
        fill="#efaa32",
        font=("Papyrus", 46, "bold"),
        anchor="w"
    )


    # pozycja w prawym górnym rogu
    canvas.create_image(WIDTH - 180, 30, image=exp_icon, anchor="ne")
    canvas.exp_value_text = canvas.create_text(WIDTH - 120, 80, text=str(int(pet.exp)), fill="#06acc5",
                                               font=("Arial", 38, "bold"), anchor="ne")

    # === TIRED (ZMĘCZENIE) PONIŻEJ GŁODU ===
    tired_icon = load_photo("src/frontend/assets/icons/zmeczenie.png", 80, 80)
    canvas.tired_icon = tired_icon  # zapamiętaj referencję

    canvas.create_image(30, 130, image=tired_icon, anchor="nw")  # niżej o 100px

    canvas.tired_value_text = canvas.create_text(
        120, 173, #tutaj
        text=f"{int(pet.tired)} / 100",
        fill="#efaa32",
        font=("Papyrus", 46, "bold"),
        anchor="w"
    )
    # === HAPPY (SZCZESCIE) PONIZEJ ZMECZENIA ===
    happy_icon = load_photo("src/frontend/assets/icons/happy.png", 80, 80)
    canvas.happy_icon = happy_icon  # zapamiętaj referencję

    canvas.create_image(30, 216, image=happy_icon, anchor="nw")  # niżej o 100px

    canvas.happy_icon_text = canvas.create_text(
        120, 260,  # tutaj
        text=f"{int(pet.happy)} / {int(pet.happy_level)}",
        fill="#efaa32",
        font=("Papyrus", 46, "bold"),
        anchor="w"
    )

    update_labels()
    decay_stats()


def choose_egg(root, start_game_callback):
    """
    Tworzenie zwierzaka

    Args:
        root (tkinter.Tk): Okno gry
        start_game_callback: wywołanie głównej gry
    """
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Wybierz swojego podopiecznego")


    bg_photo = load_photo("src/frontend/assets/backgrounds/cave.png", WIDTH, HEIGHT)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    root.bg_photo = bg_photo  # żeby nie wyczyściło obrazka z pamięci


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
        photo = load_photo(f"src/frontend/assets/eggs/egg{i+1}.png", 200, 200)
        egg_images.append(photo)

        x = start_x + i * gap
        y = 600

        egg_id = canvas.create_image(x, y, image=photo, anchor="center")
        egg_ids.append((egg_id, i))

    canvas.egg_images = egg_images

    def on_click(event):
        """
        Jak gra ma się zachować po kliknięciu jajka
        Wczutje dane z okienek
        """
        clicked = canvas.find_closest(event.x, event.y)[0]
        for id_egg, species_index in egg_ids:
            if clicked == id_egg:
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

                pet = Pet(name=name, species=species_packages[species_index], hunger_level=int(food_str), happy_level=int(play_str))
                start_game_callback(pet)

    canvas.bind("<Button-1>", on_click)



def menu():
    """
    Tworzenie okna gry i uruchamianie menu
    Gracz może wybrać co chce zrobić
    Ustawia przyciski i ładuje grafiki menu
    """
    root = tk.Tk()
    root.title("Menu Główne")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    root.geometry(f"{WIDTH}x{HEIGHT}")

    # srodek ekraniu
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (WIDTH // 2)
    y = (screen_height // 2) - (HEIGHT // 2)
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    #tło menu
    bg_photo = load_photo("src/frontend/assets/backgrounds/menu.png", WIDTH, HEIGHT)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0,0,image=bg_photo, anchor="nw")
    canvas.bg_photo = bg_photo

    #logo
    logo_photo = load_photo("src/frontend/assets/icons/logo.png", 500, 400)
    canvas.logo_photo = logo_photo
    canvas.create_image(WIDTH//2,200,image=logo_photo, anchor="center")

    #przyciski
    btn_photo = load_photo("src/frontend/assets/backgrounds/button_background.png", 400, 75)
    canvas.btn_photo = btn_photo  # zapamiętaj referencję!

    make_image_button(canvas, WIDTH // 2, 400, "Nowa gra", lambda: choose_egg(root, start_game_callback=lambda pet: window(root, pet)), btn_photo)
    make_image_button(canvas, WIDTH // 2, 525, "Wczytaj grę", lambda: load_existing_game(root), btn_photo)
    make_image_button(canvas, WIDTH // 2, 650, "Wyjście", root.destroy, btn_photo)

    root.mainloop()
def load_existing_game(root:tk.Tk):
    """
    Zachowanie przycisku do ładowania gry
    Korzyta z load_game a następnie przechodzi do okna gry

    Args:
        root (tk.Tk): Okno gry
    """
    try:
        pet = load_game()
        window(root,pet)
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wczytać gry:\n{e}")
def game(root:tk.Tk, pet:Pet):
    """
    Zachowanie przycisku ładowania zabawy

    Odpala nowy toplevel i po zakończeniu gry cofa do głownego okna

    Args:
        root(tk.Tk): Okno gry
        pet(Dane zwierzaka):
    """
    root.update_idletasks()  # odśwież dane geometryczne
    geometry = root.geometry()  # np. "1400x800+100+200"
    size, x, y = geometry.split('+')
    x, y = int(x), int(y)

    # Ukryj główne okno
    root.withdraw()

    # Utwórz nowe okno gry
    game_window = tk.Toplevel(root)
    game_window.title("DinoGame")
    game_window.geometry(f"1400x800+{x}+{y}")

    def back_to_main():
        root.deiconify()
        window(root, pet)

    # Przekazanie callbacku do DinoGame
    DinoGame(game_window, pet, on_close_callback=back_to_main)