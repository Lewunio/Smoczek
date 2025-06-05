import tkinter as tk
import random

from PIL import Image, ImageTk
from src.backend.pet import Pet
from gui import make_image_button

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
GROUND_Y = 700
OBSTACLE_INTERVAL = 2000  # ms
INITIAL_SPEED = 10

class DinoGame:
    def __init__(self, root_given,pet_given:Pet):

        self.ui_elements = []
        self.pet = pet_given
        self.root = root_given
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.title("Dino Gra")
        self.root.protocol("WM_DELETE_WINDOW", self.disable_close)
        # Tło
        self.bg_image_pil = Image.open("assets/backgrounds/game_cave.png")
        self.bg_resized = self.bg_image_pil.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(self.bg_resized)

        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")
        self.canvas.tag_lower("background")
        self.root.bg_photo = self.bg_photo

        button_bg = Image.open("assets/backgrounds/button_background.png").resize((400, 75))
        self.button_image = ImageTk.PhotoImage(button_bg)

        #Obstacles img

        self.big_spike_img = ImageTk.PhotoImage(
            Image.open("assets/items/big_spike.png").resize((100,150))
        )
        self.mid_spike_img = ImageTk.PhotoImage(
            Image.open("assets/items/mid_spike.png").resize((100, 100))
        )
        self.rock_img = ImageTk.PhotoImage(
            Image.open("assets/items/rock.png").resize((50,50))
        )
        self.obstacle_imgs = [self.big_spike_img, self.mid_spike_img, self.rock_img]
        # Dinozaur – większy, przesunięty do środka
        original_img = Image.open("assets/reddragon/running_pet.png")
        resized_img = original_img.resize((80, 80), Image.Resampling.LANCZOS)
        self.dino_img = ImageTk.PhotoImage(resized_img)
        self.root.dino_img = self.dino_img
        self.dino_x = 300
        self.dino_y = GROUND_Y
        self.dino = self.canvas.create_image(self.dino_x, self.dino_y - 40, image=self.dino_img)

        # Skok
        self.is_jumping = False
        self.jump_velocity = 0
        self.root.bind("<space>", self.jump)

        # Stan gry
        self.obstacles = []
        self.game_running = True
        self.speed = INITIAL_SPEED
        self.score = 0
        self.final_score = 0
        self.game_over_text = None

        self.score_text = self.canvas.create_text(WINDOW_WIDTH // 2, 40, anchor="n",
                                                  text=f"Wynik: {self.score}",
                                                  font=("Arial", 24, "bold"), fill="white")

        self.spawn_obstacle()
        self.update_game()
        self.increase_speed()

    def disable_close(self):
        pass
    def jump(self, event=None):
        if not self.is_jumping and self.game_running:
            self.is_jumping = True
            self.jump_velocity = -25  # wyższy skok


    def spawn_obstacle(self):
        if not self.game_running:
            return
        x = WINDOW_WIDTH
        y = GROUND_Y
        rand = random.randint(0, 2)
        obstacle = self.canvas.create_image(x, y+5  , image=self.obstacle_imgs[rand], anchor="sw")
        self.obstacles.append(obstacle)
        self.root.after(OBSTACLE_INTERVAL, self.spawn_obstacle)

    def update_game(self):
        if not self.game_running:
            return

        # Grawitacja i skok
        if self.is_jumping:
            self.jump_velocity += 1.7  # szybciej opada
            self.dino_y += self.jump_velocity
            if self.dino_y >= GROUND_Y:
                self.dino_y = GROUND_Y
                self.is_jumping = False
            self.canvas.coords(self.dino, self.dino_x, self.dino_y - 40)

        # Ruch przeszkód
        for obstacle in list(self.obstacles):
            self.canvas.move(obstacle, -self.speed, 0)
            coords = self.canvas.coords(obstacle)

            x = coords[0]
            if x < -100:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Wynik: {self.score}")

        # Kolizje
        for obstacle in self.obstacles:
            if self.check_collision(self.dino, obstacle):
                self.game_over()
                return

        self.root.after(10, self.update_game)  # ultra płynność

    def check_collision(self, dino, obstacle):
        dino_coords = self.canvas.bbox(dino)
        obs_coords = self.canvas.bbox(obstacle)
        tolerance = 10

        return (
                dino_coords[2] - tolerance > obs_coords[0] + tolerance and
                dino_coords[0] + tolerance < obs_coords[2] - tolerance and
                dino_coords[3] - tolerance > obs_coords[1] + tolerance and
                dino_coords[1] + tolerance < obs_coords[3] - tolerance
        )

    def game_over(self):
        self.game_running = False
        self.game_over_text = self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
                                                      text="GAME OVER", font=("Arial", 36, "bold"), fill="red")

        for _ in range(self.score//5+1):
            self.pet.play()
        self.show_game_over_options()

    def show_game_over_options(self):
        # Wczytanie tła przycisków

        self.root.button_image = self.button_image  # zabezpieczenie przed GC

        # Pozycje przycisków na środku
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2 + 80

        # Przyciski: „Zagraj ponownie” i „Zamknij”
        bt1 = make_image_button(self.canvas, center_x - 220, center_y,
                               "Zagraj ponownie", self.restart_game, self.button_image)
        self.ui_elements.extend(bt1)  # placeholder

        bt2 = make_image_button(self.canvas, center_x + 220, center_y,
                               "Zamknij", self.quit_game, self.button_image)
        self.ui_elements.extend(bt2)  # placeholder

    def restart_game(self):
        for i in self.ui_elements:
            self.canvas.delete(i)  # najprościej: usuń wszystko z canvas
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

        self.spawn_obstacle()
        self.update_game()
        self.increase_speed()

    def increase_speed(self):
        if self.game_running:
            self.speed += 1.5  # szybciej rośnie prędkość
            self.root.after(3000, self.increase_speed)  # częstsze przyspieszanie

    def quit_game(self):
        self.final_score = self.score
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    pet = Pet(name="sss",species="ss",happy=20)
    game = DinoGame(root,pet)
    root.mainloop()
    print("Z gry uzyskano wynik:", game.final_score)
    print(pet.__str__())