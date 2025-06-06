import tkinter as tk
import random
from src.backend.pet import Pet
from .tools import make_image_button, load_photo

# Stałe konfiguracyjne gry
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
GROUND_Y = 700
OBSTACLE_INTERVAL = 2000  # ms
INITIAL_SPEED = 30
P_SIZE = 200
O_SIZE = 100
JUMP_HEIGHT = -50
DOWN_SPEED = 3
TOLERANCE = 40  # tolerancja kolizji

class DinoGame:
    def __init__(self, root_given:tk.Toplevel, pet_given:Pet,on_close_callback=None):
        """
        Inicjalizacja podstawowych zmiennych i ustawień okna gry
        Ładowanie zdjęć

        Args:
            root_given(tk.Toplevel): Okno gry
            pet_given(Pet): Postać gry
            on_close_callback: callback function
        """
        self.on_close_callback = on_close_callback
        self.ui_elements = []
        self.pet = pet_given
        self.root = root_given
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.title("Dino Gra")
        self.root.protocol("WM_DELETE_WINDOW", self.disable_close)

        # Ustawienie tła
        self.bg_photo = load_photo("src/frontend/assets/backgrounds/game_cave.png",WINDOW_WIDTH, WINDOW_HEIGHT)

        self.canvas = tk.Canvas(root_given, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")
        self.canvas.tag_lower("background")
        self.root.bg_photo = self.bg_photo

        # Game over - ikonka
        self.game_over_img = load_photo("src/frontend/assets/items/gameover.png",300,300)
        # Przyciski – tło
        self.button_image = load_photo("src/frontend/assets/backgrounds/button_background.png", 400, 75)

        # Wczytanie grafik przeszkód
        self.big_spike_img = load_photo("src/frontend/assets/items/big_spike.png",O_SIZE * 2, O_SIZE * 3)
        self.mid_spike_img = load_photo("src/frontend/assets/items/mid_spike.png",O_SIZE * 2, O_SIZE * 2)
        self.rock_img = load_photo("src/frontend/assets/items/rock.png",O_SIZE, O_SIZE)
        self.obstacle_imgs = [self.big_spike_img, self.mid_spike_img, self.rock_img]

        # Wczytanie grafiki dinozaura

        self.dino_img = load_photo(f"src/frontend/assets/{self.pet.species}/running_pet.png", P_SIZE, P_SIZE)
        self.root.dino_img = self.dino_img  # zapobiega GC
        self.dino_x = 300
        self.dino_y = GROUND_Y
        self.dino = self.canvas.create_image(self.dino_x, self.dino_y - 40, image=self.dino_img)

        # Parametry skoku
        self.is_jumping = False
        self.jump_velocity = 0
        self.root.bind("<space>", self.jump)

        # Inicjalizacja stanu gry
        self.obstacles = []
        self.obstacle_after_id = None
        self.game_running = True
        self.speed = INITIAL_SPEED
        self.score = 0
        self.final_score = 0
        self.game_over_text = None

        # Tekst wyniku
        self.score_text = self.canvas.create_text(WINDOW_WIDTH // 2, 40, anchor="n",
                                                  text=f"Wynik: {self.score}",
                                                  font=("Arial", 24, "bold"), fill="white")

        self.spawn_obstacle()
        self.update_game()
        self.increase_speed()

    def disable_close(self):
        """Zmiana funkcji wychodzenia(przycisk X)"""
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()

    def jump(self, event=None):
        """Obsługa skoku po naciśnięciu spacji"""
        if not self.is_jumping and self.game_running:
            self.is_jumping = True
            self.jump_velocity = JUMP_HEIGHT

    def spawn_obstacle(self):
        """Generowanie nowej przeszkody"""
        if not self.game_running:
            return
        x = WINDOW_WIDTH
        y = GROUND_Y
        rand = random.randint(0, 2)
        obstacle = self.canvas.create_image(x, y + 70, image=self.obstacle_imgs[rand], anchor="sw")
        self.obstacles.append(obstacle)
        self.obstacle_after_id = self.root.after(OBSTACLE_INTERVAL, self.spawn_obstacle)

    def update_game(self):
        """Główna pętla aktualizacji gry (grawitacja, kolizje, przeszkody)"""
        if not self.game_running:
            return

        # Obsługa grawitacji/skoku
        if self.is_jumping:
            self.jump_velocity += DOWN_SPEED
            self.dino_y += self.jump_velocity
            if self.dino_y >= GROUND_Y:
                self.dino_y = GROUND_Y
                self.is_jumping = False
            self.canvas.coords(self.dino, self.dino_x, self.dino_y - 40)

        # Przesuwanie i usuwanie przeszkód
        for obstacle in list(self.obstacles):
            self.canvas.move(obstacle, -self.speed, 0)
            coords = self.canvas.coords(obstacle)
            x = coords[0]
            if x < -100:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Wynik: {self.score}")

        # Sprawdzenie kolizji
        for obstacle in self.obstacles:
            if self.check_collision(self.dino, obstacle):
                self.game_over()
                return

        # Harmonogram następnej klatki
        self.root.after(10, self.update_game)


    def check_collision(self, dino, obstacle):
        """
        Detekcja kolizji z tolerancją

        Args:
            dino: Postać
            obstacle: Przeszkoda
        """
        dino_coords = self.canvas.bbox(dino)
        obs_coords = self.canvas.bbox(obstacle)
        tolerance = TOLERANCE

        return (
            dino_coords[2] - tolerance > obs_coords[0] + tolerance and
            dino_coords[0] + tolerance < obs_coords[2] - tolerance and
            dino_coords[3] - tolerance > obs_coords[1] + tolerance and
            dino_coords[1] + tolerance < obs_coords[3] - tolerance
        )

    def game_over(self):
        """Obsługa końca gry"""
        self.game_running = False
        self.game_over_text = self.canvas.create_image(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100,
                                                       image=self.game_over_img, anchor="center")

        # Zwiększenie radości smoka
        for _ in range(self.score // 3 + 1):
            self.pet.play()

        self.show_game_over_options()


    def show_game_over_options(self):
        """Wyświetlenie przycisków końca gry"""
        self.root.button_image = self.button_image  # zabezpieczenie przed GC
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2 + 80

        bt1 = make_image_button(self.canvas, center_x - 220, center_y,
                                "Zagraj ponownie", self.restart_game, self.button_image)
        self.ui_elements.extend(bt1)

        bt2 = make_image_button(self.canvas, center_x + 220, center_y,
                                "Zamknij", self.quit_game, self.button_image)
        self.ui_elements.extend(bt2)

    def restart_game(self):
        """Restartowanie gry"""
        for i in self.ui_elements:
            self.canvas.delete(i)
        self.ui_elements.clear()

        for obstacle in self.obstacles:
            self.canvas.delete(obstacle)
        self.obstacles.clear()

        self.canvas.delete(self.dino)
        self.canvas.delete(self.score_text)
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)

        self.dino_y = GROUND_Y
        self.dino = self.canvas.create_image(self.dino_x, self.dino_y - 40, image=self.dino_img)
        self.is_jumping = False
        self.jump_velocity = 0
        self.speed = INITIAL_SPEED
        self.score = 0
        self.game_running = True
        self.game_over_text = None

        self.score_text = self.canvas.create_text(WINDOW_WIDTH // 2, 40, anchor="n",
                                                  text=f"Wynik: {self.score}",
                                                  font=("Arial", 24, "bold"), fill="white")
        if self.obstacle_after_id:
            self.root.after_cancel(self.obstacle_after_id)
            self.obstacle_after_id = None

        self.spawn_obstacle()
        self.update_game()
        self.increase_speed()

    def increase_speed(self):
        """Zwiększanie prędkości gry co pewien czas"""
        if self.game_running:
            self.speed += 1.5
            self.root.after(3000, self.increase_speed)

    def quit_game(self):
        """Wyjście z gry"""
        self.final_score = self.score
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()


# if __name__ == "__main__":
#     root = tk.Tk()
#     pet = Pet(name="sss", species="ss", happy=20)
#     game = DinoGame(root, pet)
#     root.mainloop()
#     print("Z gry uzyskano wynik:", game.final_score)
#     print(pet.__str__())