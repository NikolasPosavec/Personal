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
SCORE_THRESHOLD = 1000  # Increase speed every 1000 points
HIGH_SCORE_FILE = "high_score.txt"
SETTINGS_FILE = "settings.txt"

# Default colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
background_color = WHITE

# Initialize default images
default_player_img = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
default_player_img.fill(RED)
default_block_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
default_block_img.fill(BLACK)

# Load images
def load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        if size == (PLAYER_SIZE, PLAYER_SIZE):
            return default_player_img
        return default_block_img

def load_settings():
    global player_img, block_img, background_color
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                lines = [line.strip() for line in file.readlines()]
                if len(lines) >= 3:
                    player_path = lines[0] if lines[0] != "None" else None
                    block_path = lines[1] if lines[1] != "None" else None
                    try:
                        color_values = tuple(map(int, lines[2].split(',')))
                        background_color = color_values
                    except (ValueError, IndexError):
                        background_color = WHITE
                    
                    player_img = load_image(player_path, (PLAYER_SIZE, PLAYER_SIZE)) if player_path else default_player_img
                    block_img = load_image(block_path, (BLOCK_SIZE, BLOCK_SIZE)) if block_path else default_block_img
                else:
                    raise ValueError("Settings file incomplete")
    except Exception as e:
        print(f"Error loading settings: {e}")
        player_img = default_player_img
        block_img = default_block_img
        background_color = WHITE

load_settings()

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Load high score
def load_high_score():
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                content = file.read().strip()
                return int(content) if content else 0
        return 0
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Initialize high score
high_score = load_high_score()

# Player setup
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 10

# Blocks list
blocks = []

# Font setup
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=BLACK, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

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
    
    while True:
        screen.fill(background_color)
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
                    root = tk.Tk()
                    root.withdraw()
                    player_path = filedialog.askopenfilename(
                        title="Select Player Image", 
                        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
                    )
                    root.destroy()
                    if player_path:
                        player_img = load_image(player_path, (PLAYER_SIZE, PLAYER_SIZE))
                if event.key == pygame.K_2:
                    root = tk.Tk()
                    root.withdraw()
                    block_path = filedialog.askopenfilename(
                        title="Select Block Image", 
                        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
                    )
                    root.destroy()
                    if block_path:
                        block_img = load_image(block_path, (BLOCK_SIZE, BLOCK_SIZE))
                if event.key == pygame.K_3:
                    root = tk.Tk()
                    root.withdraw()
                    color = colorchooser.askcolor(title="Choose Background Color")
                    root.destroy()
                    if color[0]:
                        background_color = tuple(map(int, color[0]))

        # Save settings
        with open(SETTINGS_FILE, "w") as file:
            file.write(f"{player_path if 'player_path' in locals() else 'None'}\n")
            file.write(f"{block_path if 'block_path' in locals() else 'None'}\n")
            file.write(f"{','.join(map(str, background_color))}\n")

def reset_game():
    global player_x, blocks, score, BLOCK_SPEED, high_score
    player_x = WIDTH // 2 - PLAYER_SIZE // 2
    blocks = []
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    score = 0
    BLOCK_SPEED = 5  # Reset speed to initial value

# Main game variables
running = True
clock = pygame.time.Clock()
score = 0

home_screen()  # Show home screen before starting the game

while running:
    screen.fill(background_color)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                home_screen()

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

    for block in blocks[:]:
        block[1] += BLOCK_SPEED
        screen.blit(block_img, (block[0], block[1]))
        
        # Check for collisions
        if (player_x < block[0] + BLOCK_SIZE and
            player_x + PLAYER_SIZE > block[0] and
            player_y < block[1] + BLOCK_SIZE and
            player_y + PLAYER_SIZE > block[1]):
            reset_game()
            break

    # Remove blocks that are off screen
    blocks = [block for block in blocks if block[1] < HEIGHT]
    
    # Draw player and update score
    screen.blit(player_img, (player_x, player_y))
    score += 1

    # Increase difficulty
    if score % SCORE_THRESHOLD == 0:
        BLOCK_SPEED += SPEED_INCREMENT

    # Display scores
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"High Score: {high_score}", 10, 40)

    pygame.display.flip()
    clock.tick(60)

# Save high score when quitting
if score > high_score:
    save_high_score(score)
pygame.quit()