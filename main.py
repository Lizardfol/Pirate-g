import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pirate Ship Adventure")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load assets
ship_img = pygame.image.load("ship.png")
ship_img = pygame.transform.scale(ship_img, (50, 50))

# Game variables
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5
resources = 100
territories = 0
player_health = 100

# Map dimensions
MAP_WIDTH = 2000
MAP_HEIGHT = 2000
map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
map_surface.fill(BLUE)

# Enemy ships
enemy_ships = []
for _ in range(10):
    enemy_ships.append({
        "pos": [random.randint(0, MAP_WIDTH - 50), random.randint(0, MAP_HEIGHT - 50)],
        "health": 50,
    })

# Resources on the map
resources_locations = []
for _ in range(20):
    resources_locations.append([random.randint(0, MAP_WIDTH - 20), random.randint(0, MAP_HEIGHT - 20)])

def draw_map():
    screen.fill(BLUE)
    # Draw territories
    for i in range(territories):
        pygame.draw.rect(map_surface, BROWN, (i * 100, i * 100, 100, 100))

    # Draw resources
    for resource in resources_locations:
        pygame.draw.circle(map_surface, WHITE, resource, 10)

    # Draw enemy ships
    for enemy in enemy_ships:
        pygame.draw.rect(map_surface, RED, (*enemy["pos"], 50, 50))

    # Draw player ship
    map_surface.blit(ship_img, player_pos)

    # Blit the map on the screen
    screen.blit(map_surface, (-player_pos[0] + SCREEN_WIDTH // 2, -player_pos[1] + SCREEN_HEIGHT // 2))

def move_player(keys):
    global player_pos
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed

def check_collisions():
    global resources, territories, player_health

    # Check resource collection
    for resource in resources_locations[:]:
        if pygame.Rect(*resource, 20, 20).colliderect(pygame.Rect(*player_pos, 50, 50)):
            resources += 10
            resources_locations.remove(resource)

    # Check enemy ship battles
    for enemy in enemy_ships[:]:
        if pygame.Rect(*enemy["pos"], 50, 50).colliderect(pygame.Rect(*player_pos, 50, 50)):
            player_health -= 10
            enemy["health"] -= 10
            if enemy["health"] <= 0:
                enemy_ships.remove(enemy)

    # Check for territory acquisition
    if resources >= 50:
        resources -= 50
        territories += 1

def draw_ui():
    font = pygame.font.Font(None, 36)
    resources_text = font.render(f"Resources: {resources}", True, WHITE)
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    territories_text = font.render(f"Territories: {territories}", True, WHITE)
    screen.blit(resources_text, (10, 10))
    screen.blit(health_text, (10, 50))
    screen.blit(territories_text, (10, 90))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move_player(keys)
    check_collisions()

    draw_map()
    draw_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
