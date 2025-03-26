import pygame
import random
import os
import tkinter as tk
from tkinter import filedialog, colorchooser

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 500, 600
PLAYER_SIZE = 50
BLOCK_SIZE = 50
SPEED = 5
BLOCK_SPEED = 5  # Initial block speed
SPEED_INCREMENT = 1  # How much the block speed increases
SCORE_THRESHOLD = 1000  # Increase speed and spawn more blocks every 1000 points
HIGH_SCORE_FILE = "high_score.txt"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
background_color = WHITE

# Load images
def load_image(path, size):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, size)

def load_settings():
    global player_img, block_img, background_color
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            player_path = lines[0].strip()
            block_path = lines[1].strip()
            color_values = tuple(map(int, lines[2].strip().split(',')))
            background_color = color_values
            player_img = load_image(player_path, (PLAYER_SIZE, PLAYER_SIZE))
            block_img = load_image(block_path, (BLOCK_SIZE, BLOCK_SIZE))
    else:
        player_img = load_image(r"C:\Users\bolt\Pictures\ASCII Art\car.jpg", (PLAYER_SIZE, PLAYER_SIZE))
        block_img = load_image(r"C:\Users\bolt\Pictures\Camera Roll\large_user_6750003_651.jpg", (BLOCK_SIZE, BLOCK_SIZE))

load_settings()

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Load high score
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Player setup
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 10

# Blocks list
blocks = []

# Home screen
def home_screen():
    while True:
        screen.fill(background_color)
        draw_text("Dodge the Blocks", WIDTH // 2, HEIGHT // 4, BLACK, center=True)
        draw_text("Press P to Play", WIDTH // 2, HEIGHT // 2, BLACK, center=True)
        draw_text("Press S for Settings", WIDTH // 2, HEIGHT // 2 + 50, BLACK, center=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return
                if event.key == pygame.K_s:
                    settings_screen()

# Settings screen
def settings_screen():
    global player_img, block_img, background_color
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    while True:
        screen.fill(WHITE)
        draw_text("Settings", WIDTH // 2, HEIGHT // 4, BLACK, center=True)
        draw_text("Press 1 to Change Player Image", WIDTH // 2, HEIGHT // 2, BLACK, center=True)
        draw_text("Press 2 to Change Block Image", WIDTH // 2, HEIGHT // 2 + 50, BLACK, center=True)
        draw_text("Press 3 to Change Background Color", WIDTH // 2, HEIGHT // 2 + 100, BLACK, center=True)
        draw_text("Press B to Go Back", WIDTH // 2, HEIGHT // 2 + 150, BLACK, center=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return
                if event.key == pygame.K_1:
                    player_path = filedialog.askopenfilename(title="Select Player Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
                    if player_path:
                        player_img = load_image(player_path, (PLAYER_SIZE, PLAYER_SIZE))
                if event.key == pygame.K_2:
                    block_path = filedialog.askopenfilename(title="Select Block Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
                    if block_path:
                        block_img = load_image(block_path, (BLOCK_SIZE, BLOCK_SIZE))
                if event.key == pygame.K_3:
                    color = colorchooser.askcolor(title="Choose Background Color")[0]
                    if color:
                        background_color = tuple(map(int, color))
                
                with open("settings.txt", "w") as file:
                    file.write(f"{player_img.get_at((0, 0))}\n")  # Save path or relevant data
                    file.write(f"{block_img.get_at((0, 0))}\n")  # Save path or relevant data
                    file.write(f"{','.join(map(str, background_color))}")

    root.quit()

def reset_game():
    global player_x, blocks, score, BLOCK_SPEED
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    blocks = []
    score = 0
    BLOCK_SPEED = 5  # Reset speed to initial value

def draw_text(text, x, y, color=BLACK, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Collision detection
def check_collision():
    global blocks
    for block in blocks:
        if (player_x < block[0] + BLOCK_SIZE and player_x + PLAYER_SIZE > block[0]) and (player_y < block[1] + BLOCK_SIZE and player_y + PLAYER_SIZE > block[1]):
            return True  # Collision detected
    return False

# Main game loop
running = True
clock = pygame.time.Clock()
score = 0
high_score = load_high_score()
font = pygame.font.Font(None, 36)

home_screen()  # Show home screen before starting the game

while running:
    screen.fill(background_color)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= SPEED
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
        player_x += SPEED

    # Block mechanics
    if random.randint(1, 30) == 1:
        block_x = random.randint(0, WIDTH - BLOCK_SIZE)
        blocks.append([block_x, 0])

    for block in blocks:
        block[1] += BLOCK_SPEED
        screen.blit(block_img, (block[0], block[1]))

    screen.blit(player_img, (player_x, player_y))
    blocks = [block for block in blocks if block[1] < HEIGHT]

    # Check collision with blocks
    if check_collision():
        high_score = max(high_score, score)  # Update high score if needed
        save_high_score(high_score)
        reset_game()
        home_screen()  # Go back to home screen after dying

    # Increase block spawn rate and speed every 1000 points
    score += 1
    if score % SCORE_THRESHOLD == 0:
        BLOCK_SPEED += SPEED_INCREMENT  # Increase block speed
        # Increase the block spawn rate
        for _ in range(2):  # Add two more blocks every 1000 points
            block_x = random.randint(0, WIDTH - BLOCK_SIZE)
            blocks.append([block_x, 0])

    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"High Score: {high_score}", 10, 40)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
