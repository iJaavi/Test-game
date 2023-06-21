
import pygame
import random
import time
import heapq

# Initialize Pygame
pygame.init()

# Set the width and height of the window
width = 1280
height = 960

# Initializing surface
screen = pygame.display.set_mode((width, height))
 
# Set the font for the clock display
font = pygame.font.Font(None, 36)

# Initialize the clock
start_time = time.time()

# Load the player and enemy image
player_image = pygame.image.load("player.png")
enemy_image = pygame.image.load("enemy.png")

# Set the colors
background_color = (0, 0, 0)  # Black color
start_color = (0, 0, 255)  # Blue color
end_color = (255, 255, 0)  # Yellow color
path_color = (255, 255, 255)  # White color
player_color = (0, 255, 0)  # Green color
enemy_color = (255, 0, 0)  # Red color

# Set the heart image
heart_image = pygame.image.load("heart.png")
heart_width = 32
heart_height = 32
heart_padding = 10
heart_start_x = 50
heart_y = 50

# Set the invulnerability period
invulnerability_duration = 3 # in seconds
invulnerability_start_time = 0

# Set the player character dimensions
player_width = 20
player_height = 20

# Set up the player's speed
player_speed = 5

# Set the player's health
player_health = 3

# Set the enemy dimensions
enemy_width = 20
enemy_height = 20

# Set up the enemy's speed
enemy_speed = 2

# Create a font for displaying the player's health
font = pygame.font.Font(None, 36)

# Set the maze dimensions
maze_width = width // player_width
maze_height = height // player_height

# Set the start and end points of the maze
start_x = random.randint(0, maze_width - 1) * player_width
start_y = random.randint(0, maze_height - 1) * player_height
end_x = random.randint(0, maze_width - 1) * player_width
end_y = random.randint(0, maze_height - 1) * player_height

# Set the player and enemy initial positions
player_x = start_x
player_y = start_y
enemy_x = random.randint(0, maze_width - 1) * player_width
enemy_y = random.randint(0, maze_height - 1) * player_height

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

    # Function to calculate the Manhattan distance heuristic
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

        # Function to find the shortest path using A* algorithm
def find_path(start, end, maze):
    open_list = []
    closed_list = []
    heapq.heappush(open_list, (0, start))
    path = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == end:
            break

        closed_list.append(current)

        x, y = current
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for neighbor in neighbors:
            nx, ny = neighbor

            if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[ny][nx] == 1:
                new_g_score = g_score[current] + 1

                if neighbor not in g_score or new_g_score < g_score[neighbor]:
                    g_score[neighbor] = new_g_score
                    priority = new_g_score + manhattan_distance(nx, ny, end[0], end[1])
                    heapq.heappush(open_list, (priority, neighbor))
                    path[neighbor] = current

    path_list = []
    while current != start:
        path_list.append(current)
        current = path[current]
    path_list.reverse()

    return path_list


# Start the game loop
running = True
while running:
    current_time = time.time()  # Get the current time
    elapsed_time = current_time - start_time  # Calculate the elapsed time
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y -= player_speed
            elif event.key == pygame.K_DOWN:
                player_y += player_speed
            elif event.key == pygame.K_LEFT:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_x += player_speed

                
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

     # Keep the enemy within the maze boundaries and prevent collision with walls
    if enemy_x > 0 and maze[enemy_y // player_height][(enemy_x - player_width) // player_width] == 1:
        enemy_x -= player_width
    if enemy_x < width - player_width and maze[enemy_y // player_height][(enemy_x + player_width) // player_width] == 1:
        enemy_x += player_width
    if enemy_y > 0 and maze[(enemy_y - player_height) // player_height][enemy_x // player_width] == 1:
        enemy_y -= player_height
    if enemy_y < height - player_height and maze[(enemy_y + player_height) // player_height][enemy_x // player_width] == 1:
        enemy_y += player_height


    # Move the enemy
    if enemy_x < player_x:
        enemy_x += enemy_speed
    elif enemy_x > player_x:
        enemy_x -= enemy_speed

    if enemy_y < player_y:
        enemy_y += enemy_speed
    elif enemy_y > player_y:
        enemy_y -= enemy_speed

    # Check if the player is invulnerable
    invulnerable = current_time - invulnerability_start_time < invulnerability_duration

    # Check for collision between player and enemy
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    if player_rect.colliderect(enemy_rect):
        if current_time - invulnerability_start_time > invulnerability_duration:
            if player_health > 0:
                player_health -= 1
                invulnerability_start_time = current_time
                print("Player was hit! Health:", player_health)
            else:
                print("Player is defeated!")

    # Draw the invulnerability timer
    if current_time - invulnerability_start_time < invulnerability_duration:
        invulnerability_time = invulnerability_duration - (current_time - invulnerability_start_time)
        invulnerability_text = font.render("Invulnerability: " + "{:.1f}".format(invulnerability_time), True, (255, 255, 255))
        screen.blit(invulnerability_text, (10, 50))


    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the player and enemy
    # screen.blit(player_image, (player_x, player_y))
    # screen.blit(enemy_image, (enemy_x, enemy_y))

    # Draw the player character
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # Draw the enemy
    pygame.draw.rect(screen, enemy_color, (enemy_x, enemy_y, enemy_width, enemy_height))


    # Draw the clock display
    clock_text = font.render("Time: {:.2f}".format(elapsed_time), True, (0, 0, 0))
    clock_rect = clock_text.get_rect()
    clock_rect.topright = (130, 20)
    screen.blit(clock_text, clock_rect)

    # Draw the maze
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, path_color, (x * player_width, y * player_height, player_width, player_height))

    # Find the path from enemy to player
    path_to_player = find_path((enemy_x // player_width, enemy_y // player_height),
                               (player_x // player_width, player_y // player_height), maze)
    
    # Update enemy position based on the path
    if path_to_player:
        next_x, next_y = path_to_player[0]
        enemy_x = next_x * player_width
        enemy_y = next_y * player_height


    # Draw the start point
    pygame.draw.rect(screen, start_color, (start_x, start_y, player_width, player_height))

    # Draw the end point
    pygame.draw.rect(screen, end_color, (end_x, end_y, player_width, player_height))


    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()


#This code adds an enemy character to the game that follows the player's movements. The enemy's position is stored in the enemy_x and enemy_y variables, and its speed is stored in the enemy_speed variable. In the game loop, the enemy's position is updated to move towards the player's position. The random module is used to set the enemy's starting position randomly on the screen. Finally, the enemy and player characters are both drawn to the screen using their respective images.