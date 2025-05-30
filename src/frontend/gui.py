import tkinter as tk
from tkinter import simpledialog, messagebox
from src.backend.pet import Pet
from src.backend.save import save_game, load_game

def window(pet):

    root = tk.Tk()
    root.title("Zwierzak GUI")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    # Labels
    name_label = tk.Label(frame, text="")
    species_label = tk.Label(frame, text="")
    birth_label = tk.Label(frame, text="")
    happy_label = tk.Label(frame, text="")
    hunger_label = tk.Label(frame, text="")
    tired_label = tk.Label(frame, text="")
    exp_label = tk.Label(frame, text="")

    def update_labels():
        name_label.config(text=f"Imię: {pet.name}")
        species_label.config(text=f"Gatunek: {pet.species}")
        birth_label.config(text=f"Urodzony: {pet.birth}")
        happy_label.config(text=f"❤️ Szczęście: {pet.happy}/100")
        hunger_label.config(text=f"🍗 Głód: {pet.hunger}/100")
        tired_label.config(text=f"😴 Zmęczenie: {pet.tired}/100")
        exp_label.config(text=f"⭐ Doświadczenie: {pet.exp}")

    for label in [name_label, species_label, birth_label, happy_label, hunger_label, tired_label, exp_label]:
        label.pack(anchor="w")

    # Buttons
    button_frame = tk.Frame(root, pady=10)
    button_frame.pack()

    tk.Button(button_frame, text="😴 Śpij", command=pet.sleep, width=10).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="🍗 Jedz", command=pet.eat, width=10).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="🎮 Baw się", command=pet.play, width=10).grid(row=0, column=2, padx=5)

    update_labels()
    root.mainloop()
def menu():
    root = tk.Tk()
    root.title("Menu Główne")
    root.geometry("300x200")

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

    tk.Label(root, text="🐾 Witaj w grze Zwierzak! 🐾", pady=20).pack()

    tk.Button(root, text="🆕 Nowa gra", command=start_new_game, width=20).pack(pady=5)
    tk.Button(root, text="📂 Wczytaj grę", command=load_existing_game, width=20).pack(pady=5)
    tk.Button(root, text="❌ Wyjście", command=root.destroy, width=20).pack(pady=5)

    root.mainloop()