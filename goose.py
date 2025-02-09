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
goose_img = pygame.image.load("goose.png")  # Main goose image
goose_fall_img = pygame.image.load("goose1.png")  # Falling goose image
goose_img = pygame.transform.scale(goose_img, (100, 60))
goose_fall_img = pygame.transform.scale(goose_fall_img, (100, 60))

crosshair_img = pygame.image.load("crosshair.png")  # Load crosshair image
crosshair_size = 40
crosshair_img = pygame.transform.scale(crosshair_img, (crosshair_size, crosshair_size))

# Load sound
gunshot_sound = pygame.mixer.Sound("pistol shot.mp3")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
goose_x = WIDTH
goose_y = random.randint(100, HEIGHT - 100)
speed = 0.5
score = 0
goose_width, goose_height = 100, 60
game_duration = 60
falling = False  # New variable for fall animation
fall_speed = 1  # Speed at which the goose falls

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

def game_loop():
    global goose_x, goose_y, score, falling
    score = 0  # Reset score when the game starts
    running = True
    goose_hit = False
    falling = False  # Reset falling state
    pygame.mouse.set_visible(False)
    start_time = time.time()
    
    countdown()  # Start countdown before the game begins

    while running:
        screen.fill(WHITE)
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, game_duration - elapsed_time)
        if remaining_time == 0:
            running = False

        # Goose movement logic
        if falling:
            goose_y += fall_speed  # Make goose fall downward
            if goose_y > HEIGHT:  # Reset when it reaches the bottom
                goose_x = WIDTH + random.randint(50, 200)
                goose_y = random.randint(100, HEIGHT - 100)
                falling = False  # Reset falling state
                goose_hit = False
        else:
            goose_x -= speed
            if goose_x < -goose_width:
                goose_x = WIDTH + random.randint(50, 200)  # Random respawn
                goose_y = random.randint(100, HEIGHT - 100)
                goose_hit = False

        # Draw the goose
        if goose_hit:
            screen.blit(goose_fall_img, (goose_x, goose_y))  # Show falling goose
        else:
            screen.blit(goose_img, (goose_x, goose_y))  # Show normal goose

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Draw crosshair at mouse position
        screen.blit(crosshair_img, (mouse_x - crosshair_size // 2, mouse_y - crosshair_size // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                gunshot_sound.play()  # Play gunshot sound
                if goose_x < mouse_x < goose_x + goose_width and goose_y < mouse_y < goose_y + goose_height:
                    score += 1
                    goose_hit = True  # Change goose image to fallen state
                    falling = True  # Start the falling animation
                    print("Goose Hit! Score:", score)

        # Display Score and Time
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (WIDTH - 150, 10))

        pygame.display.update()
    
    game_over_screen()

def game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("Game Over!", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 3))
    
    pygame.mouse.set_visible(True)  # Show mouse cursor
    
    try_again_button = draw_button("Try Again", WIDTH // 3, HEIGHT // 2, 150, 50, BLACK, WHITE)
    quit_button = draw_button("Quit", WIDTH // 2 + 50, HEIGHT // 2, 150, 50, BLACK, WHITE)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if try_again_button.collidepoint(mouse_x, mouse_y):
                    game_loop()
                if quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    return

game_loop()
