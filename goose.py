import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goose Shooting Game")

# Load images
goose_img = pygame.image.load("goose.png")
goose_fall_img = pygame.image.load("goose1.png")
goose_img = pygame.transform.scale(goose_img, (100, 60))
goose_fall_img = pygame.transform.scale(goose_fall_img, (100, 60))

crosshair_img = pygame.image.load("crosshair.png")
crosshair_size = 40
crosshair_img = pygame.transform.scale(crosshair_img, (crosshair_size, crosshair_size))

# Load sounds
gunshot_sound = pygame.mixer.Sound("pistol shot.mp3")
start_cackle_sound = pygame.mixer.Sound("start-cackle.mp3")
reload_sound = pygame.mixer.Sound("reload.mp3")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
speed = 0.5  # Adjusted speed for better difficulty
score = 0
goose_width, goose_height = 100, 60
game_duration = 60
fall_speed = 2
spawn_intervals = [1, 2, 3]
next_spawn_time = time.time() + random.choice(spawn_intervals)

# Multiple geese
goose_list = []
for _ in range(2):
    goose_list.append({
        "x": WIDTH + random.randint(50, 200),
        "y": random.randint(100, HEIGHT - 100),
        "hit": False,
        "falling": False
    })

# Ammo system
ammo = 5
reload_start_time = None

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)

def countdown():
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 100)
        text = font.render(str(i), True, BLACK)
        screen.blit(text, (WIDTH // 2 - 25, HEIGHT // 2 - 50))
        pygame.display.update()
        time.sleep(1)

def game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over!", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 3))
    pygame.display.update()
    time.sleep(2)

def game_loop():
    global score, next_spawn_time, ammo, reload_start_time
    score = 0
    running = True
    pygame.mouse.set_visible(False)
    start_time = time.time()
    
    countdown()

    while running:
        screen.fill(WHITE)
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, game_duration - elapsed_time)
        if remaining_time == 0:
            running = False

        current_time = time.time()
        
        for goose in goose_list:
            if goose["falling"]:
                goose["y"] += fall_speed
                if goose["y"] > HEIGHT:
                    if current_time >= next_spawn_time:
                        goose["x"] = WIDTH + random.randint(50, 200)
                        goose["y"] = random.randint(100, HEIGHT - 100)
                        goose["falling"] = False
                        goose["hit"] = False
                        start_cackle_sound.play()
                        next_spawn_time = current_time + random.choice(spawn_intervals)
            else:
                goose["x"] -= speed
                if goose["x"] < -goose_width:
                    if current_time >= next_spawn_time:
                        goose["x"] = WIDTH + random.randint(50, 200)
                        goose["y"] = random.randint(100, HEIGHT - 100)
                        goose["hit"] = False
                        start_cackle_sound.play()
                        next_spawn_time = current_time + random.choice(spawn_intervals)

        for goose in goose_list:
            if goose["hit"]:
                screen.blit(goose_fall_img, (goose["x"], goose["y"]))
            else:
                screen.blit(goose_img, (goose["x"], goose["y"]))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(crosshair_img, (mouse_x - crosshair_size // 2, mouse_y - crosshair_size // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ammo > 0:
                    gunshot_sound.play()
                    ammo -= 1
                    for goose in goose_list:
                        if goose["x"] < mouse_x < goose["x"] + goose_width and goose["y"] < mouse_y < goose["y"] + goose_height:
                            score += 1
                            goose["hit"] = True
                            goose["falling"] = True
                            print("Goose Hit! Score:", score)
                if ammo == 0 and reload_start_time is None:
                    print("Reloading...")
                    reload_sound.play()
                    reload_start_time = time.time()

        if reload_start_time:
            if time.time() - reload_start_time >= 4:
                ammo = 5
                reload_start_time = None

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
        ammo_text = font.render(f"Ammo: {ammo}/5", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (WIDTH - 150, 10))
        screen.blit(ammo_text, (WIDTH // 2 - 50, 10))

        pygame.display.update()
    
    game_over_screen()

game_loop()
