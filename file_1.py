import pygame
import random

pygame.init()

window_width = 800
window_height = 600

# Velocity of moving the player
Velocity = 1

# Clock and FPS frames per second for the speed of movement
fps = 100
clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Monsters MAZE!")

# Coloring our game with RGB!
Black = (0, 0, 0)
White = (255, 255, 255)
Mint = (95, 180, 130)
DarkGreen = (10, 50, 10)

# Adding image at the top
cupcake_image = pygame.image.load("dragon.png")
cupcake_image_rect = cupcake_image.get_rect()
cupcake_image_rect.topright = (window_width, 0)

# Maze dimensions
maze_width = 47
maze_height = 33
cell_size = 17

# Player adjustments
player_image = pygame.image.load("monster (4).png")
player_image_rect = player_image.get_rect()
player_image_rect.topleft = (cell_size, cell_size + 40)  # Start position within the maze

# Define Font
custom_font = pygame.font.Font('CrotahFreeVersionItalic-z8Ev3.ttf', 28)

custom_text = custom_font.render("Welcome to Monsters Maze", True, White)
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (window_width // 2, 20)

end_font = pygame.font.Font('CrotahFreeVersionItalic-z8Ev3.ttf', 10)
end_text = end_font.render("END", True, White)
end_text_rect = end_text.get_rect()
end_text_rect.bottomright = (window_width - 19, window_height - 19)

# Maze generation using recursive backtracking
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]  # Creates a 2D list (grid) filled with 1s, representing walls. The maze is initially filled with walls.
    stack = [(1, 1)]  # Starts with the initial cell (1, 1).
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]  # Possible movements (right, left, down, up) in steps of 2 cells to ensure walls remain between paths.

    while stack:
        x, y = stack[-1]  # Current cell coordinates.
        maze[y][x] = 0  # Marks the current cell as part of the maze (path).
        neighbors = []  # List to store valid neighboring cells.

        for dx, dy in directions:  # Iterates through possible directions.
            nx, ny = x + dx, y + dy  # Coordinates of the neighboring cell.
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1:  # Checks if the neighboring cell is within bounds and is a wall
                neighbors.append((nx, ny))  # Adds valid neighbors to the neighbors list.

        if neighbors:
            nx, ny = random.choice(neighbors)  # If there are valid neighbors: Chooses a random neighbor.
            stack.append((nx, ny))  # Adds the neighbor to the stack.
            maze[(y + ny) // 2][(x + nx) // 2] = 0  # Removes the wall between the current cell and the chosen neighbor
        else:
            stack.pop()  # If no valid neighbors: Backtracks by popping the stack.

    return maze  # Returns the generated maze grid.

maze = generate_maze(maze_width, maze_height)

def draw_maze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(display_surface, (26, 106, 109), (x * cell_size, y * cell_size + 40, cell_size, cell_size))

def can_move_to(x, y):
    maze_x = x // cell_size
    maze_y = (y - 40) // cell_size
    if 0 <= maze_x < maze_width and 0 <= maze_y < maze_height:
        return maze[maze_y][maze_x] == 0
    return False

# Function to display text
def display_message(text):
    message = custom_font.render(text, True, White)
    display_surface.blit(message, [window_width // 4, window_height // 2])
    pygame.display.flip()
    pygame.time.wait(4000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player continuously
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_image_rect.left > 0:
        if can_move_to(player_image_rect.left - Velocity, player_image_rect.top):
            player_image_rect.x -= Velocity
    if keys[pygame.K_RIGHT] and player_image_rect.right < window_width:
        if can_move_to(player_image_rect.right + Velocity, player_image_rect.top):
            player_image_rect.x += Velocity
    if keys[pygame.K_UP] and player_image_rect.top > 40:
        if can_move_to(player_image_rect.left, player_image_rect.top - Velocity):
            player_image_rect.y -= Velocity
    if keys[pygame.K_DOWN] and player_image_rect.bottom < window_height:
        if can_move_to(player_image_rect.left, player_image_rect.bottom + Velocity):
            player_image_rect.y += Velocity

    # Check if player reaches the end
    if (player_image_rect.x < end_text_rect.x + end_text_rect.width and
        player_image_rect.x + player_image_rect.width > end_text_rect.x and
        player_image_rect.y < end_text_rect.y + end_text_rect.height and
        player_image_rect.y + player_image_rect.height > end_text_rect.y):
        display_message("Congratulations! You Win")
        running = False  # Stop the game loop

    # Fill the display surface to cover the old images of the player
    display_surface.fill(Black)
            
    # Draw the maze
    draw_maze(maze)
    
    # The header on the top
    display_surface.blit(cupcake_image, cupcake_image_rect)
    pygame.draw.line(display_surface, White, (0, 40), (window_width, 40), 3)
    
    display_surface.blit(custom_text, custom_text_rect)
    
    display_surface.blit(player_image, player_image_rect)
    
    display_surface.blit(end_text, end_text_rect)
    
    # Update the display
    pygame.display.update()
    
    # Clock
    clock.tick(fps)
            
pygame.quit()
