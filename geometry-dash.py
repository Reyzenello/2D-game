import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_LIGHT = (200, 200, 200)
GRAY_MEDIUM = (150, 150, 150)
GRAY_DARK = (100, 100, 100)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash 2D")
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 48)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 80
        self.vel_y = 0
        self.on_ground = True
        self.lives = 3

    def update(self):
        self.vel_y += 0.8  # Gravity
        self.rect.y += self.vel_y
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = -15
            self.on_ground = False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.create_shaded_triangle()

    def create_shaded_triangle(self):
        # Draw darker triangle for shading
        pygame.draw.polygon(self.image, GRAY_DARK, [(0, 30), (15, 0), (30, 30)])
        # Draw medium triangle slightly smaller
        pygame.draw.polygon(self.image, GRAY_MEDIUM, [(5, 25), (15, 5), (25, 25)])
        # Draw light triangle even smaller
        pygame.draw.polygon(self.image, GRAY_LIGHT, [(10, 20), (15, 10), (20, 20)])

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

def show_instructions():
    screen.fill(BLACK)
    instructions = [
        "Geometry Dash 2D",
        "",
        "Instructions:",
        "- Press SPACE to jump",
        "- Avoid obstacles",
        "- Collect coins",
        "- Don't fall off platforms",
        "- You have 3 lives",
        "",
        "Press any key to start"
    ]
    for i, line in enumerate(instructions):
        text = font_small.render(line, True, WHITE)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + i * 30))
        screen.blit(text, rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def game_loop():
    player = Player()
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    all_sprites.add(player)

    score = 0
    obstacle_timer = 0
    coin_timer = 0
    platform_timer = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Spawn obstacles
        obstacle_timer += 1
        if obstacle_timer > 60:
            obstacle = Obstacle(WIDTH, HEIGHT - 80)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            obstacle_timer = 0

        # Spawn coins
        coin_timer += 1
        if coin_timer > 90:
            coin = Coin(WIDTH, random.randint(HEIGHT - 200, HEIGHT - 100))
            all_sprites.add(coin)
            coins.add(coin)
            coin_timer = 0

        # Spawn platforms
        platform_timer += 1
        if platform_timer > 200:
            platform_width = random.randint(100, 200)
            platform = Platform(WIDTH, HEIGHT - random.randint(100, 150), platform_width)
            all_sprites.add(platform)
            platforms.add(platform)
            platform_timer = 0

        all_sprites.update()

        # Check for collisions
        if pygame.sprite.spritecollide(player, obstacles, True):
            player.lives -= 1
            if player.lives <= 0:
                running = False

        coins_collected = pygame.sprite.spritecollide(player, coins, True)
        score += len(coins_collected)

        # Check if player is on a platform
        if not player.on_ground:
            hits = pygame.sprite.spritecollide(player, platforms, False)
            if hits:
                player.rect.bottom = hits[0].rect.top
                player.vel_y = 0
                player.on_ground = True

        # Check if player has fallen
        if player.rect.top > HEIGHT:
            running = False

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))

        # Draw score and lives
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        lives_text = font_small.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()

    return score

def show_game_over(score):
    screen.fill(BLACK)
    game_over_text = font_large.render("Game Over", True, WHITE)
    score_text = font_small.render(f"Final Score: {score}", True, WHITE)
    restart_text = font_small.render("Press any key to restart", True, WHITE)

    screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    while True:
        show_instructions()
        score = game_loop()
        show_game_over(score)

if __name__ == "__main__":
    main()
