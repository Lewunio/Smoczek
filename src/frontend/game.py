import tkinter as tk
import random
from traceback import print_tb

from PIL import Image, ImageTk
from src.backend.pet import Pet

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
GROUND_Y = 500
OBSTACLE_INTERVAL = 2000  # ms
INITIAL_SPEED = 10

class DinoGame:
    def __init__(self, root,pet:Pet):
        self.pet = pet
        self.root = root
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.title("Dino Gra")

        # Tło
        self.bg_image_pil = Image.open("assets/backgrounds/cave.png")
        self.bg_resized = self.bg_image_pil.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(self.bg_resized)

        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")
        self.canvas.tag_lower("background")
        self.root.bg_photo = self.bg_photo

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

    def jump(self, event=None):
        if not self.is_jumping and self.game_running:
            self.is_jumping = True
            self.jump_velocity = -25  # wyższy skok

    def spawn_obstacle(self):
        if not self.game_running:
            return
        x = WINDOW_WIDTH
        height_units = random.randint(1, 3)
        height = 40 * height_units  # większe przeszkody
        y = GROUND_Y
        obstacle = self.canvas.create_rectangle(x, y - height, x + 40, y, fill="brown")
        self.obstacles.append(obstacle)
        self.root.after(OBSTACLE_INTERVAL, self.spawn_obstacle)

    def update_game(self):
        if not self.game_running:
            return

        # Grawitacja i skok
        if self.is_jumping:
            self.jump_velocity += 1.5  # szybciej opada
            self.dino_y += self.jump_velocity
            if self.dino_y >= GROUND_Y:
                self.dino_y = GROUND_Y
                self.is_jumping = False
            self.canvas.coords(self.dino, self.dino_x, self.dino_y - 40)

        # Ruch przeszkód
        for obstacle in list(self.obstacles):
            self.canvas.move(obstacle, -self.speed, 0)
            coords = self.canvas.coords(obstacle)
            if coords[2] < 0:
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
        return (dino_coords[2] > obs_coords[0] and
                dino_coords[0] < obs_coords[2] and
                dino_coords[3] > obs_coords[1] and
                dino_coords[1] < obs_coords[3])

    def game_over(self):
        self.game_running = False
        self.game_over_text = self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
                                                      text="GAME OVER", font=("Arial", 36, "bold"), fill="red")

        for _ in range(int(self.final_score/10+1)):
            self.pet.play()
        self.show_game_over_options()

    def show_game_over_options(self):
        self.retry_frame = tk.Frame(self.root, bg="white")
        self.retry_frame.place(relx=0.5, rely=0.6, anchor="center")

        retry_btn = tk.Button(self.retry_frame, text="Zagraj ponownie", command=self.restart_game)
        retry_btn.pack(side="left", padx=10)

        quit_btn = tk.Button(self.retry_frame, text="Zamknij", command=self.quit_game)
        quit_btn.pack(side="right", padx=10)

    def restart_game(self):
        self.retry_frame.destroy()

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