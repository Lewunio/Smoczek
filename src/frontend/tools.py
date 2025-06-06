import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

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

def load_photo(path:str,size_x:int,size_y:int)->PhotoImage:
    """
    Funkcja ładowania zdjęć

    Args:
        path(str): ścieżka do zdjęcia
        size_x(int): wymiar x
        size_y(int): wymiar y

    Returns:
        PhotoImage: Przygotowane zdjęcie
    """
    logo_img = Image.open(path).resize((size_x,size_y))
    return ImageTk.PhotoImage(logo_img)