import pygame
import random
import os
import tkinter as tk
from tkinter import filedialog, colorchooser
import time
import json

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 500, 600
PLAYER_SIZE = 50
BLOCK_SIZE = 50
BASE_SPEED = 5
BASE_BLOCK_SPEED = 5
SPEED_INCREMENT = 1
SCORE_THRESHOLD = 1000
HIGH_SCORE_FILE = "high_score.txt"
COINS_FILE = "coins.txt"
SETTINGS_FILE = "settings.txt"
UPGRADES_FILE = "upgrades.json"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (80, 80, 80)
GOLD = (255, 215, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

# Initialize default images
default_player_img = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
default_player_img.fill(RED)
default_block_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
default_block_img.fill(BLACK)

# Global variables
player_img = default_player_img
block_img = default_block_img
background_color = WHITE
high_score = 0
coins = 0.0  # Initialize as float to support decimal coins
score = 0
paused = False
control_scheme = "arrows"  # Can be "arrows", "wasd", or "mouse"

# Upgrades system
upgrades = {
    "player_speed": {"level": 0, "max_level": 5, "cost": [100, 200, 300, 400, 500], "effect": [0.5, 1.0, 1.5, 2.0, 2.5]},
    "block_speed": {"level": 0, "max_level": 5, "cost": [100, 200, 300, 400, 500], "effect": [-0.5, -1.0, -1.5, -2.0, -2.5]},
    "player_size": {"level": 0, "max_level": 5, "cost": [150, 300, 450, 600, 750], "effect": [-5, -10, -15, -20, -25]},
    "coin_multiplier": {"level": 0, "max_level": 5, "cost": [200, 400, 600, 800, 1000], "effect": [0.2, 0.4, 0.6, 0.8, 1.0]}
}

# Load images function
def load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        if size == (PLAYER_SIZE, PLAYER_SIZE):
            return default_player_img
        return default_block_img

# Load all game data
def load_data():
    global player_img, block_img, background_color, high_score, coins, upgrades, control_scheme
    
    # Load settings
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                lines = [line.strip() for line in file.readlines()]
                if len(lines) >= 4:
                    player_path = lines[0] if lines[0] != "None" else None
                    block_path = lines[1] if lines[1] != "None" else None
                    try:
                        color_values = tuple(map(int, lines[2].split(',')))
                        background_color = color_values
                    except (ValueError, IndexError):
                        background_color = WHITE
                    control_scheme = lines[3] if len(lines) > 3 and lines[3] in ["arrows", "wasd", "mouse"] else "arrows"
                    
                    player_img = load_image(player_path, (PLAYER_SIZE, PLAYER_SIZE)) if player_path else default_player_img
                    block_img = load_image(block_path, (BLOCK_SIZE, BLOCK_SIZE)) if block_path else default_block_img
    except Exception as e:
        print(f"Error loading settings: {e}")

    # Load high score
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                content = file.read().strip()
                high_score = int(content) if content else 0
    except (FileNotFoundError, ValueError, PermissionError):
        high_score = 0

    # Load coins
    try:
        if os.path.exists(COINS_FILE):
            with open(COINS_FILE, "r") as file:
                content = file.read().strip()
                coins = float(content) if content else 0.0
    except (FileNotFoundError, ValueError, PermissionError):
        coins = 0.0

    # Load upgrades
    try:
        if os.path.exists(UPGRADES_FILE):
            with open(UPGRADES_FILE, "r") as file:
                loaded_upgrades = json.load(file)
                for key in upgrades:
                    if key in loaded_upgrades:
                        upgrades[key]["level"] = loaded_upgrades[key]["level"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

# Initialize game data
load_data()

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Create surfaces for overlays
pause_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pause_overlay.fill((255, 255, 255, 128))
game_over_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
game_over_overlay.fill((0, 0, 0, 0))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_GRAY, hover_color=GRAY, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2, border_radius=5)
        
        font = pygame.font.Font(None, 28)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")

def save_coins():
    try:
        with open(COINS_FILE, "w") as file:
            file.write(str(coins))
    except Exception as e:
        print(f"Error saving coins: {e}")

def save_upgrades():
    try:
        upgrade_data = {key: {"level": upgrades[key]["level"]} for key in upgrades}
        with open(UPGRADES_FILE, "w") as file:
            json.dump(upgrade_data, file)
    except Exception as e:
        print(f"Error saving upgrades: {e}")

def save_settings():
    try:
        with open(SETTINGS_FILE, "w") as file:
            player_path = "None" if player_img == default_player_img else "player.png"
            block_path = "None" if block_img == default_block_img else "block.png"
            file.write(f"{player_path}\n")
            file.write(f"{block_path}\n")
            file.write(f"{','.join(map(str, background_color))}\n")
            file.write(f"{control_scheme}\n")
    except Exception as e:
        print(f"Error saving settings: {e}")

# Font setup
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)

def draw_text(text, x, y, color=BLACK, center=False, font_type=font):
    text_surface = font_type.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_coin_counter():
    coin_text = f"Coins: {round(coins, 1)}"  # Display with 1 decimal place
    coin_surface = font.render(coin_text, True, GOLD)
    coin_rect = coin_surface.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(coin_surface, coin_rect)

# Calculate game stats based on upgrades
def get_player_speed():
    return BASE_SPEED + (upgrades["player_speed"]["effect"][upgrades["player_speed"]["level"] - 1] if upgrades["player_speed"]["level"] > 0 else 0)

def get_block_speed():
    return BASE_BLOCK_SPEED + (upgrades["block_speed"]["effect"][upgrades["block_speed"]["level"] - 1] if upgrades["block_speed"]["level"] > 0 else 0)

def get_player_size():
    return PLAYER_SIZE + (upgrades["player_size"]["effect"][upgrades["player_size"]["level"] - 1] if upgrades["player_size"]["level"] > 0 else 0)

def get_coin_multiplier():
    return 1 + (upgrades["coin_multiplier"]["effect"][upgrades["coin_multiplier"]["level"] - 1] if upgrades["coin_multiplier"]["level"] > 0 else 0)

# Settings screen
def settings_screen():
    global player_img, block_img, background_color, coins, control_scheme
    
    back_button = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "Back")
    arrows_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 40, "Arrow Keys", 
                         color=GREEN if control_scheme == "arrows" else LIGHT_GRAY)
    wasd_button = Button(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 40, "WASD Keys",
                        color=GREEN if control_scheme == "wasd" else LIGHT_GRAY)
    mouse_button = Button(WIDTH//2 - 100, HEIGHT//2 + 150, 200, 40, "Mouse Control",
                         color=GREEN if control_scheme == "mouse" else LIGHT_GRAY)
    player_img_button = Button(WIDTH//2 - 100, HEIGHT//2 - 90, 200, 40, "Player Image")
    block_img_button = Button(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 40, "Block Image")
    bg_color_button = Button(WIDTH//2 - 100, HEIGHT//2 + 10, 200, 40, "Background Color")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(background_color)
        draw_text("Settings", WIDTH // 2, 50, BLACK, center=True, font_type=large_font)
        
        # Update button colors
        arrows_button.color = GREEN if control_scheme == "arrows" else LIGHT_GRAY
        wasd_button.color = GREEN if control_scheme == "wasd" else LIGHT_GRAY
        mouse_button.color = GREEN if control_scheme == "mouse" else LIGHT_GRAY
        
        # Check hover states
        arrows_button.check_hover(mouse_pos)
        wasd_button.check_hover(mouse_pos)
        mouse_button.check_hover(mouse_pos)
        player_img_button.check_hover(mouse_pos)
        block_img_button.check_hover(mouse_pos)
        bg_color_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        
        # Draw buttons
        draw_text("Control Scheme:", WIDTH // 2, HEIGHT//2 + 20, BLACK, center=True)
        arrows_button.draw(screen)
        wasd_button.draw(screen)
        mouse_button.draw(screen)
        
        draw_text("Customization:", WIDTH // 2, HEIGHT//2 - 120, BLACK, center=True)
        player_img_button.draw(screen)
        block_img_button.draw(screen)
        bg_color_button.draw(screen)
        
        back_button.draw(screen)
        draw_coin_counter()
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if back_button.is_clicked(mouse_pos, event):
                save_settings()
                return
            
            if arrows_button.is_clicked(mouse_pos, event):
                control_scheme = "arrows"
            if wasd_button.is_clicked(mouse_pos, event):
                control_scheme = "wasd"
            if mouse_button.is_clicked(mouse_pos, event):
                control_scheme = "mouse"
            
            if player_img_button.is_clicked(mouse_pos, event):
                root = tk.Tk()
                root.withdraw()
                player_path = filedialog.askopenfilename(
                    title="Select Player Image", 
                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
                )
                root.destroy()
                if player_path:
                    player_img = load_image(player_path, (PLAYER_SIZE, PLAYER_SIZE))
            
            if block_img_button.is_clicked(mouse_pos, event):
                root = tk.Tk()
                root.withdraw()
                block_path = filedialog.askopenfilename(
                    title="Select Block Image", 
                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
                )
                root.destroy()
                if block_path:
                    block_img = load_image(block_path, (BLOCK_SIZE, BLOCK_SIZE))
            
            if bg_color_button.is_clicked(mouse_pos, event):
                root = tk.Tk()
                root.withdraw()
                color = colorchooser.askcolor(title="Choose Background Color")
                root.destroy()
                if color[0]:
                    background_color = tuple(map(int, color[0]))

# Upgrade menu
def upgrades_menu():
    global coins
    
    back_button = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "Back")
    
    # Create upgrade buttons
    upgrade_buttons = {}
    y_pos = 150
    for upgrade in upgrades:
        upgrade_buttons[upgrade] = Button(WIDTH//2 + 100, y_pos, 150, 40, "Upgrade", GREEN, (0, 150, 0))
        y_pos += 60
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(background_color)
        draw_text("Upgrades Shop", WIDTH // 2, 50, BLACK, center=True, font_type=large_font)
        draw_coin_counter()
        
        y_pos = 150
        for upgrade, data in upgrades.items():
            # Draw upgrade info
            level = data["level"]
            max_level = data["max_level"]
            effect = data["effect"][level] if level < max_level else data["effect"][-1]
            
            # Upgrade name and level
            upgrade_name = upgrade.replace("_", " ").title()
            level_text = f"{upgrade_name} (Level {level}/{max_level})"
            draw_text(level_text, WIDTH//2 - 200, y_pos)
            
            # Upgrade effect
            effect_text = f"Effect: {effect}"
            if upgrade == "player_speed":
                effect_text = f"Speed +{effect}"
            elif upgrade == "block_speed":
                effect_text = f"Block Speed {effect}"
            elif upgrade == "player_size":
                effect_text = f"Size {effect}px"
            elif upgrade == "coin_multiplier":
                effect_text = f"Multiplier +{effect}x"
            draw_text(effect_text, WIDTH//2 - 200, y_pos + 25)
            
            # Upgrade button
            if level < max_level:
                cost = data["cost"][level]
                button_text = f"Upgrade ({cost})"
                upgrade_buttons[upgrade].text = button_text
                upgrade_buttons[upgrade].rect.y = y_pos
                upgrade_buttons[upgrade].check_hover(mouse_pos)
                upgrade_buttons[upgrade].draw(screen)
            else:
                draw_text("MAX LEVEL", WIDTH//2 + 100, y_pos + 20, center=True)
            
            y_pos += 60
        
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if back_button.is_clicked(mouse_pos, event):
                return
            
            for upgrade, button in upgrade_buttons.items():
                if upgrades[upgrade]["level"] < upgrades[upgrade]["max_level"]:
                    if button.is_clicked(mouse_pos, event):
                        cost = upgrades[upgrade]["cost"][upgrades[upgrade]["level"]]
                        if coins >= cost:
                            coins -= cost
                            upgrades[upgrade]["level"] += 1
                            save_coins()
                            save_upgrades()

# Home screen
def home_screen():
    play_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Play")
    settings_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "Settings")
    upgrades_button = Button(WIDTH//2 - 100, HEIGHT//2 + 140, 200, 50, "Upgrades")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(background_color)
        draw_text("Dodge the Blocks", WIDTH // 2, HEIGHT // 4, BLACK, center=True, font_type=large_font)
        
        play_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        upgrades_button.check_hover(mouse_pos)
        
        play_button.draw(screen)
        settings_button.draw(screen)
        upgrades_button.draw(screen)
        draw_coin_counter()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if play_button.is_clicked(mouse_pos, event):
                return True
            if settings_button.is_clicked(mouse_pos, event):
                settings_screen()
            if upgrades_button.is_clicked(mouse_pos, event):
                upgrades_menu()

def reset_game():
    global player_x, blocks, score, BLOCK_SPEED, high_score, coins
    
    # Calculate coins earned with multiplier
    base_coins = score // 100
    coins_earned = base_coins * get_coin_multiplier()
    coins += coins_earned
    save_coins()
    
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    
    player_x = WIDTH // 2 - get_player_size() // 2
    blocks = []
    score = 0
    BLOCK_SPEED = get_block_speed()
    return round(coins_earned, 1)  # Return coins earned rounded to 1 decimal

def show_countdown():
    player_size = get_player_size()
    for i in range(3, 0, -1):
        screen.fill(background_color)
        for block in blocks:
            screen.blit(block_img, (block[0], block[1]))
        screen.blit(pygame.transform.scale(player_img, (player_size, player_size)), (player_x, HEIGHT - player_size - 10))
        draw_text(f"Score: {score}", 10, 40)
        draw_text(f"High Score: {high_score}", 10, 70)
        draw_coin_counter()
        screen.blit(pause_overlay, (0, 0))
        draw_text(str(i), WIDTH // 2, HEIGHT // 2, BLACK, center=True, font_type=large_font)
        pygame.display.flip()
        time.sleep(1)
    
    screen.fill(background_color)
    for block in blocks:
        screen.blit(block_img, (block[0], block[1]))
    screen.blit(pygame.transform.scale(player_img, (player_size, player_size)), (player_x, HEIGHT - player_size - 10))
    draw_text(f"Score: {score}", 10, 40)
    draw_text(f"High Score: {high_score}", 10, 70)
    draw_coin_counter()
    screen.blit(pause_overlay, (0, 0))
    draw_text("GO!", WIDTH // 2, HEIGHT // 2, BLACK, center=True, font_type=large_font)
    pygame.display.flip()
    time.sleep(0.5)

def show_game_over(player_x, player_y, blocks, score, high_score):
    alpha = 0
    fade_speed = 5
    
    coins_earned = reset_game()
    
    try_again_button = Button(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50, "Try Again")
    home_button = Button(WIDTH//2 - 100, HEIGHT//2 + 120, 200, 50, "Go Home")
    
    while alpha < 180:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.fill(background_color)
        for block in blocks:
            screen.blit(block_img, (block[0], block[1]))
        player_size = get_player_size()
        screen.blit(pygame.transform.scale(player_img, (player_size, player_size)), (player_x, player_y))
        draw_text(f"Score: {score}", 10, 40)
        draw_text(f"High Score: {high_score}", 10, 70)
        draw_coin_counter()
        
        alpha = min(alpha + fade_speed, 180)
        game_over_overlay.fill((0, 0, 0, alpha))
        screen.blit(game_over_overlay, (0, 0))
        
        draw_text("GAME OVER", WIDTH // 2, HEIGHT // 2 - 60, WHITE, center=True, font_type=large_font)
        draw_text(f"Score: {score}", WIDTH // 2, HEIGHT // 2, WHITE, center=True)
        draw_text(f"Coins Earned: {coins_earned}", WIDTH // 2, HEIGHT // 2 + 20, GOLD, center=True)
        
        try_again_button.check_hover(mouse_pos)
        home_button.check_hover(mouse_pos)
        try_again_button.draw(screen)
        home_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if try_again_button.is_clicked(mouse_pos, event):
                return "retry"
            if home_button.is_clicked(mouse_pos, event):
                return "home"
        
        screen.fill(background_color)
        for block in blocks:
            screen.blit(block_img, (block[0], block[1]))
        player_size = get_player_size()
        screen.blit(pygame.transform.scale(player_img, (player_size, player_size)), (player_x, player_y))
        draw_text(f"Score: {score}", 10, 40)
        draw_text(f"High Score: {high_score}", 10, 70)
        draw_coin_counter()
        screen.blit(game_over_overlay, (0, 0))
        draw_text("GAME OVER", WIDTH // 2, HEIGHT // 2 - 60, WHITE, center=True, font_type=large_font)
        draw_text(f"Score: {score}", WIDTH // 2, HEIGHT // 2, WHITE, center=True)
        draw_text(f"Coins Earned: {coins_earned}", WIDTH // 2, HEIGHT // 2 + 20, GOLD, center=True)
        try_again_button.check_hover(mouse_pos)
        home_button.check_hover(mouse_pos)
        try_again_button.draw(screen)
        home_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

# Main game loop
def game_loop():
    global player_x, player_y, blocks, score, BLOCK_SPEED, high_score, coins, paused
    
    player_size = get_player_size()
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    blocks = []
    score = 0
    BLOCK_SPEED = get_block_speed()
    player_speed = get_player_speed()
    paused = False
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(background_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = not paused
                    if not paused:
                        show_countdown()

        # Handle player movement based on control scheme
        if not paused:
            if control_scheme == "mouse":
                # Mouse control - player follows mouse X position
                if pygame.mouse.get_focused():  # Only move if mouse is in window
                    mouse_x, _ = pygame.mouse.get_pos()
                    player_x = mouse_x - player_size // 2
                    # Keep player within bounds
                    player_x = max(0, min(WIDTH - player_size, player_x))
            else:
                # Keyboard controls
                keys = pygame.key.get_pressed()
                if control_scheme == "arrows":
                    if keys[pygame.K_LEFT] and player_x > 0:
                        player_x -= player_speed
                    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
                        player_x += player_speed
                elif control_scheme == "wasd":
                    if keys[pygame.K_a] and player_x > 0:
                        player_x -= player_speed
                    if keys[pygame.K_d] and player_x < WIDTH - player_size:
                        player_x += player_speed

        for block in blocks:
            screen.blit(block_img, (block[0], block[1]))
        
        # Draw player with current size
        current_player_img = pygame.transform.scale(player_img, (player_size, player_size))
        screen.blit(current_player_img, (player_x, player_y))
        
        if not paused:
            draw_text("Press Enter to pause", WIDTH // 2, 10, BLACK, center=True, font_type=small_font)

        if paused:
            continue_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Continue")
            home_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "Go Home")
            
            continue_button.check_hover(mouse_pos)
            home_button.check_hover(mouse_pos)
            
            screen.blit(pause_overlay, (0, 0))
            draw_text("PAUSED", WIDTH // 2, HEIGHT // 2 - 60, BLACK, center=True, font_type=large_font)
            continue_button.draw(screen)
            home_button.draw(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if continue_button.is_clicked(mouse_pos, event):
                    paused = False
                    show_countdown()
                if home_button.is_clicked(mouse_pos, event):
                    return True
            
            pygame.display.flip()
            continue

        if random.randint(1, 30) == 1:
            block_x = random.randint(0, WIDTH - BLOCK_SIZE)
            blocks.append([block_x, 0])

        for block in blocks[:]:
            block[1] += BLOCK_SPEED
            
            if (player_x < block[0] + BLOCK_SIZE and
                player_x + player_size > block[0] and
                player_y < block[1] + BLOCK_SIZE and
                player_y + player_size > block[1]):
                action = show_game_over(player_x, player_y, blocks, score, high_score)
                if action == "retry":
                    # Reset game state for new attempt
                    player_size = get_player_size()
                    player_x = WIDTH // 2 - player_size // 2
                    player_y = HEIGHT - player_size - 10
                    blocks = []
                    score = 0
                    BLOCK_SPEED = get_block_speed()
                    player_speed = get_player_speed()
                    paused = False
                    continue
                elif action == "home":
                    return True

        blocks = [block for block in blocks if block[1] < HEIGHT]
        
        score += 1
        if score % SCORE_THRESHOLD == 0:
            BLOCK_SPEED += SPEED_INCREMENT

        draw_text(f"Score: {score}", 10, 40)
        draw_text(f"High Score: {high_score}", 10, 70)
        draw_coin_counter()

        pygame.display.flip()
        clock.tick(60)

# Main game execution
if __name__ == "__main__":
    try:
        running = True
        clock = pygame.time.Clock()

        if home_screen():
            while running:
                should_continue = game_loop()
                if not should_continue:
                    running = False
                else:
                    if score > high_score:
                        save_high_score(score)
                    if not home_screen():
                        running = False

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()