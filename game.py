import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Stars!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Level settings
current_level = 1
stars_to_complete_level = 10  # First level needs 10 stars
time_limit = 20  # First level has 20 seconds

# Game variables
score = 0
game_over = False
level_complete = False
clock = pygame.time.Clock()
start_time = time.time()

class MovingObstacle:
    def __init__(self, x, y, size, movement_type, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.movement_type = movement_type
        self.speed = speed
        self.original_x = x
        self.original_y = y
        self.angle = random.uniform(0, 2 * math.pi)  # For circular movement
        self.direction = 1  # For horizontal/vertical movement
        
    def move(self):
        if self.movement_type == "horizontal":
            self.rect.x += self.speed * self.direction
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.direction *= -1
                
        elif self.movement_type == "vertical":
            self.rect.y += self.speed * self.direction
            if self.rect.bottom > HEIGHT or self.rect.top < 0:
                self.direction *= -1
                
        elif self.movement_type == "circular":
            self.angle += self.speed * 0.05
            radius = 100
            self.rect.x = self.original_x + math.cos(self.angle) * radius
            self.rect.y = self.original_y + math.sin(self.angle) * radius
            
        elif self.movement_type == "chase":
            # Move towards player
            dx = player_x - self.rect.x
            dy = player_y - self.rect.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist != 0:
                self.rect.x += (dx / dist) * self.speed
                self.rect.y += (dy / dist) * self.speed

def reset_level(level):
    global player_x, player_y, stars, obstacles, start_time, stars_to_complete_level, time_limit, player_speed, score
    
    # Reset player position
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    
    # Reset score at the start of each level
    if level > 1:
        score = 0
    
    # Adjust player speed based on level
    player_speed = 5 + (level - 1)
    
    # Clear and create new stars
    stars.clear()
    num_stars = min(3 + level, 8)  # More stars in higher levels, max 8
    for _ in range(num_stars):
        star = pygame.Rect(
            random.randint(0, WIDTH - star_size),
            random.randint(0, HEIGHT - star_size),
            star_size,
            star_size
        )
        stars.append(star)
    
    # Clear and create new obstacles
    obstacles.clear()
    base_speed = 2 + level  # Speed increases with level
    
    # Add different types of obstacles based on level
    if level >= 1:
        # Horizontal moving obstacles
        for _ in range(level):
            obstacles.append(MovingObstacle(
                random.randint(0, WIDTH - obstacle_size),
                random.randint(0, HEIGHT//3),
                obstacle_size,
                "horizontal",
                base_speed
            ))
    
    if level >= 2:
        # Vertical moving obstacles
        for _ in range(level-1):
            obstacles.append(MovingObstacle(
                random.randint(0, WIDTH - obstacle_size),
                random.randint(0, HEIGHT//3),
                obstacle_size,
                "vertical",
                base_speed
            ))
    
    if level >= 3:
        # Circular moving obstacles
        for _ in range(level-2):
            obstacles.append(MovingObstacle(
                random.randint(0, WIDTH - obstacle_size),
                random.randint(0, HEIGHT//3),
                obstacle_size,
                "circular",
                base_speed
            ))
    
    if level >= 4:
        # Chasing obstacles
        for _ in range(level-3):
            obstacles.append(MovingObstacle(
                random.randint(0, WIDTH - obstacle_size),
                random.randint(0, HEIGHT//3),
                obstacle_size,
                "chase",
                base_speed * 0.5  # Slower speed for chasing obstacles
            ))
    
    # Update level requirements
    if level == 1:
        stars_to_complete_level = 10  # First level needs 10 stars
        time_limit = 20  # First level has 20 seconds
    else:
        stars_to_complete_level = 5 * level  # Level 2: 10 stars, Level 3: 15 stars, etc.
        time_limit = 25  # Other levels have 25 seconds
    
    # Reset timer
    start_time = time.time()

# Star settings
star_size = 30
stars = []

# Obstacle settings
obstacle_size = 40
obstacles = []

# Initialize first level
reset_level(current_level)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or level_complete):
                # Reset game
                score = 0
                current_level = 1
                game_over = False
                level_complete = False
                reset_level(current_level)

    if not game_over and not level_complete:
        # Timer calculation
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)
        
        if remaining_time == 0:
            game_over = True
        
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
            player_y += player_speed

        # Move obstacles
        for obstacle in obstacles:
            obstacle.move()

        # Collision detection with stars
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for star in stars[:]:
            if player_rect.colliderect(star):
                stars.remove(star)
                score += 1
                if score >= stars_to_complete_level:
                    level_complete = True
                    break
                # Add new star
                new_star = pygame.Rect(
                    random.randint(0, WIDTH - star_size),
                    random.randint(0, HEIGHT - star_size),
                    star_size,
                    star_size
                )
                stars.append(new_star)

        # Collision detection with obstacles
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.rect):
                game_over = True

    # Drawing
    window.fill(BLACK)
    
    # Draw player
    pygame.draw.rect(window, BLUE, (player_x, player_y, player_size, player_size))
    
    # Draw stars
    for star in stars:
        pygame.draw.rect(window, YELLOW, star)
    
    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(window, RED, obstacle.rect)

    # Draw HUD
    font = pygame.font.Font(None, 36)
    # Score and level
    score_text = font.render(f'Score: {score}/{stars_to_complete_level}  Level: {current_level}', True, WHITE)
    window.blit(score_text, (10, 10))
    
    # Timer
    if not game_over and not level_complete:
        timer_text = font.render(f'Time: {int(remaining_time)}s', True, WHITE)
        window.blit(timer_text, (10, 50))

    # Game over screen
    if game_over:
        game_over_text = font.render('Game Over! Press R to restart', True, WHITE)
        window.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
    
    # Level complete screen
    if level_complete:
        if current_level < 5:  # Max 5 levels
            level_complete_text = font.render('Level Complete! Press SPACE to continue', True, GREEN)
            window.blit(level_complete_text, (WIDTH//2 - 200, HEIGHT//2))
            
            # Check for space key to start next level
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                current_level += 1
                level_complete = False
                reset_level(current_level)
        else:
            victory_text = font.render('Congratulations! You Won! Press R to play again', True, GREEN)
            window.blit(victory_text, (WIDTH//2 - 250, HEIGHT//2))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
