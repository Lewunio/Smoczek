import tkinter as tk
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 300
GROUND_Y = 250
OBSTACLE_INTERVAL = 2000  # ms
INITIAL_SPEED = 10

class DinoGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack()

        self.dino = self.canvas.create_rectangle(50, GROUND_Y - 50, 90, GROUND_Y, fill="black")
        self.dino_y = GROUND_Y
        self.is_jumping = False
        self.jump_velocity = 0
        self.root.bind("<space>", self.jump)

        self.obstacles = []
        self.game_running = True
        self.speed = INITIAL_SPEED

        self.score = 0
        self.final_score = None  # <--- Zmienna na wynik końcowy
        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Wynik: {self.score}", font=("Arial", 14), fill="black")

        self.spawn_obstacle()
        self.update_game()
        self.increase_speed()

    def jump(self, event=None):
        if not self.is_jumping and self.game_running:
            self.is_jumping = True
            self.jump_velocity = -15

    def spawn_obstacle(self):
        if not self.game_running:
            return
        x = WINDOW_WIDTH
        height_units = random.randint(1, 3)
        height = 20 * height_units
        y = GROUND_Y
        obstacle = self.canvas.create_rectangle(x, y - height, x + 20, y, fill="green")
        self.obstacles.append(obstacle)
        self.root.after(OBSTACLE_INTERVAL, self.spawn_obstacle)

    def update_game(self):
        if not self.game_running:
            return

        # Skok dinozaura
        if self.is_jumping:
            self.canvas.move(self.dino, 0, self.jump_velocity)
            self.dino_y += self.jump_velocity
            self.jump_velocity += 1
            if self.dino_y >= GROUND_Y:
                self.dino_y = GROUND_Y
                self.canvas.coords(self.dino, 50, GROUND_Y - 50, 90, GROUND_Y)
                self.is_jumping = False

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

        self.root.after(30, self.update_game)

    def check_collision(self, dino, obstacle):
        dino_coords = self.canvas.bbox(dino)
        obs_coords = self.canvas.bbox(obstacle)
        return (dino_coords[2] > obs_coords[0] and
                dino_coords[0] < obs_coords[2] and
                dino_coords[3] > obs_coords[1] and
                dino_coords[1] < obs_coords[3])

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
                                text="GAME OVER", font=("Arial", 24), fill="red")
        self.show_game_over_options()

    def show_game_over_options(self):
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.5, rely=0.6, anchor="center")

        retry_btn = tk.Button(frame, text="Zagraj ponownie", command=self.restart_game)
        retry_btn.pack(side="left", padx=10)

        quit_btn = tk.Button(frame, text="Zamknij", command=self.quit_game)
        quit_btn.pack(side="right", padx=10)

        self.retry_frame = frame

    def restart_game(self):
        self.retry_frame.destroy()
        self.canvas.delete("all")

        self.dino = self.canvas.create_rectangle(50, GROUND_Y - 50, 90, GROUND_Y, fill="black")
        self.dino_y = GROUND_Y
        self.is_jumping = False
        self.jump_velocity = 0
        self.obstacles = []
        self.speed = INITIAL_SPEED
        self.score = 0  # <--- ZEROWANIE
        self.game_running = True

        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Wynik: {self.score}", font=("Arial", 14), fill="black")

        self.spawn_obstacle()
        self.update_game()
        self.increase_speed()

    def increase_speed(self):
        if self.game_running:
            self.speed += 0.5
            self.root.after(5000, self.increase_speed)

    def quit_game(self):
        self.final_score = self.score  # <--- Zapamiętanie wyniku
        print(f"Wynik końcowy: {self.final_score}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dino Gra")
    game = DinoGame(root)
    root.mainloop()

    # Po zamknięciu gry możemy jeszcze odczytać wynik:
    print("Z gry uzyskano wynik:", game.final_score)