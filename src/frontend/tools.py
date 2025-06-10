import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def make_image_button(canvas, x, y, text, command, image):
    """
    Tworzy przycisk graficzny z tekstem i obramowaniem na podanym kanwie.

    Przycisk jest osadzony na obrazie, z centralnym tekstem, a wokół dodana jest ramka.

    Args:
        canvas (tk.Canvas): Obiekt kanwy, na której zostanie utworzony przycisk.
        x (int): Pozycja X (środek przycisku).
        y (int): Pozycja Y (środek przycisku).
        text (str): Tekst wyświetlany na przycisku.
        command (Callable): Funkcja wywoływana po kliknięciu.
        image (tk.PhotoImage): Obraz tła przycisku.

    Returns:
        list: Lista zawierająca ID utworzonego przycisku i ramki na kanwie.
    """
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
    Ładuje i skaluje obrazek do podanych wymiarów.

    Args:
        path (str): Ścieżka do pliku graficznego.
        size_x (int): Szerokość w pikselach.
        size_y (int): Wysokość w pikselach.

    Returns:
        PhotoImage: Obiekt obrazka gotowy do użycia w Tkinterze.
    """
    logo_img = Image.open(path).resize((size_x,size_y))
    return ImageTk.PhotoImage(logo_img)