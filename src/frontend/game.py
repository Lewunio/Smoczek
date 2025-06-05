import tkinter as tk
import random
from PIL import Image, ImageTk

OBSTACLE_INTERVAL = 2000  # ms
INITIAL_SPEED = 10

class DinoGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x800")
        self.root.update()

        self.window_width = self.root.winfo_width()
        self.window_height = self.root.winfo_height()
        self.ground_y = int(self.window_height * 0.3125)

        # Tło
        self.bg_image_pil = Image.open("assets/backgrounds/cave.png")
        self.bg_resized = self.bg_image_pil.resize((self.window_width, self.window_height))
        self.bg_photo = ImageTk.PhotoImage(self.bg_resized)

        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")
        self.canvas.tag_lower("background")
        self.root.bg_photo = self.bg_photo

        # Dinozaur
        original_img = Image.open("assets/reddragon/running_pet.png")
        resized_img = original_img.resize((40, 40), Image.Resampling.LANCZOS)
        self.dino_img = ImageTk.PhotoImage(resized_img)
        self.root.dino_img = self.dino_img  # chroni przed garbage collection
        self.dino = self.canvas.create_image(70, self.ground_y - 25, image=self.dino_img)
        self.dino_y = self.ground_y

        # Ruch
        self.is_jumping = False
        self.jump_velocity = 0
        self.root.bind("<space>", self.jump)

        # Stan gry
        self.obstacles = []
        self.game_running = True
        self.speed = INITIAL_SPEED
        self.score = 0
        self.final_score = None

        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Wynik: {self.score}", font=("Arial", 14), fill="black")

        self.spawn_obstacle()
        self.update_game()
        self.increase_speed()

        self.root.bind("<Configure>", self.on_resize)
        self.on_resize(tk.Event())  # wymuś ustawienie po starcie

    def jump(self, event=None):
        if not self.is_jumping and self.game_running:
            self.is_jumping = True
            self.jump_velocity = -15

    def spawn_obstacle(self):
        if not self.game_running or self.ground_y is None:
            return
        x = self.window_width
        height_units = random.randint(1, 3)
        height = 20 * height_units
        y = self.ground_y
        obstacle = self.canvas.create_rectangle(x, y - height, x + 20, y, fill="brown")
        self.obstacles.append(obstacle)
        self.root.after(OBSTACLE_INTERVAL, self.spawn_obstacle)

    def update_game(self):
        if not self.game_running:
            return

        if self.is_jumping:
            self.canvas.move(self.dino, 0, self.jump_velocity)
            self.dino_y += self.jump_velocity
            self.jump_velocity += 1
            if self.dino_y >= self.ground_y:
                self.dino_y = self.ground_y
                self.canvas.coords(self.dino, 70, self.ground_y - 25)
                self.is_jumping = False

        for obstacle in list(self.obstacles):
            self.canvas.move(obstacle, -self.speed, 0)
            coords = self.canvas.coords(obstacle)
            if coords[2] < 0:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Wynik: {self.score}")

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
        self.canvas.create_text(self.window_width // 2, self.window_height // 2 - 30,
                                text="GAME OVER", font=("Arial", 24), fill="red")
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

        self.dino = self.canvas.create_image(70, self.ground_y - 25, image=self.dino_img)
        self.dino_y = self.ground_y
        self.is_jumping = False
        self.jump_velocity = 0
        self.speed = INITIAL_SPEED
        self.score = 0
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
        self.final_score = self.score
        print(f"Wynik końcowy: {self.final_score}")
        self.root.destroy()

    def on_resize(self, event):
        self.window_width = self.root.winfo_width()
        self.window_height = self.root.winfo_height()
        self.ground_y = int(self.window_height * 0.3125)

        self.canvas.config(width=self.window_width, height=self.window_height)
        self.canvas.delete("background")

        self.bg_resized = self.bg_image_pil.resize((self.window_width, self.window_height))
        self.bg_photo = ImageTk.PhotoImage(self.bg_resized)
        self.root.bg_photo = self.bg_photo

        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")
        self.canvas.tag_lower("background")

        self.canvas.coords(self.dino, 70, self.dino_y - 25)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dino Gra")
    game = DinoGame(root)
    root.mainloop()
    print("Z gry uzyskano wynik:", game.final_score)