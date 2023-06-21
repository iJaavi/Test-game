import pygame
import random

# Initialize Pygame
pygame.init()

# Set the width and height of the window
width = 1280
height = 960

# Create the game window
window = pygame.display.set_mode((width, height))

# Set the colors
background_color = (0, 0, 0)  # Black color
player_color = (255, 0, 0)  # Red color
enemy_color = (0, 255, 0)  # Green color
path_color = (255, 255, 255)  # White color

# Set the player character dimensions
player_width = 20
player_height = 20

# Set the enemy dimensions
enemy_width = 20
enemy_height = 20

# Set the maze dimensions
maze_width = width // player_width
maze_height = height // player_height

# Set the player and enemy initial positions
player_x = random.randint(0, maze_width - 1) * player_width
player_y = random.randint(0, maze_height - 1) * player_height
enemy_x = random.randint(0, maze_width - 1) * player_width
enemy_y = random.randint(0, maze_height - 1) * player_height

# Set the start and end points of the maze
start_x = random.randint(0, maze_width - 1) * player_width
start_y = random.randint(0, maze_height - 1) * player_height
end_x = random.randint(0, maze_width - 1) * player_width
end_y = random.randint(0, maze_height - 1) * player_height

# Generate the maze using depth-first search algorithm
maze = [[0] * maze_width for _ in range(maze_height)]
stack = [(start_x // player_width, start_y // player_height)]
maze[start_y // player_height][start_x // player_width] = 1
while stack:
    x, y = stack[-1]
    neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
    random.shuffle(neighbors)
    found = False
    for nx, ny in neighbors:
        if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[ny][nx] == 0:
            maze[ny][nx] = 1
            maze[(y + ny) // 2][(x + nx) // 2] = 1
            stack.append((nx, ny))
            found = True
            break
    if not found:
        stack.pop()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill(background_color)

    # Draw the maze
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                pygame.draw.rect(window, path_color, (x * player_width, y * player_height, player_width, player_height))

    # Draw the player character
    pygame.draw.rect(window, player_color, (player_x, player_y, player_width, player_height))

    # Draw the enemy
    pygame.draw.rect(window, enemy_color, (enemy_x, enemy_y, enemy_width, enemy_height))

    # Get the state of the keyboard
    keys = pygame.key.get_pressed()

    # Update player position based on keyboard input
    if keys[pygame.K_LEFT]:
        if player_x > 0 and maze[player_y // player_height][(player_x - player_width) // player_width] == 1:
            player_x -= player_width
    if keys[pygame.K_RIGHT]:
        if player_x < width - player_width and maze[player_y // player_height][(player_x + player_width) // player_width] == 1:
            player_x += player_width
    if keys[pygame.K_UP]:
        if player_y > 0 and maze[(player_y - player_height) // player_height][player_x // player_width] == 1:
            player_y -= player_height
    if keys[pygame.K_DOWN]:
        if player_y < height - player_height and maze[(player_y + player_height) // player_height][player_x // player_width] == 1:
            player_y += player_height

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()