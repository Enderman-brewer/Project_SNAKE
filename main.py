import pygame
import random
import traceback

pygame.init()

# Set up pygame
clock = pygame.time.Clock()
size = (800, 800)
starting_grid_size = 16
grid_size = starting_grid_size
is_fullscreen = False


def toggle_fullscreen():
    """Toggle between fullscreen and windowed mode."""
    global size, screen, is_fullscreen
    
    is_fullscreen = not is_fullscreen
    
    if is_fullscreen:
        # Get desktop size for fullscreen
        desktop_size = pygame.display.get_desktop_sizes()[0]
        square_dimension = min(desktop_size[0], desktop_size[1])
        size = (square_dimension, square_dimension)
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        # Switch to windowed mode (800x800)
        size = (800, 800)
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)


def normalize_size():
    global size, screen

    width = max(1, int(size[0]))
    height = max(1, int(size[1]))
    
    size = (width, height)
    
    if not is_fullscreen:
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    return size


normalize_size()
pygame.display.set_caption("Project_SNAKE-V0.0.0")
class Colours:
    def __init__(self) -> None:
        self.snakehead = (0, 255, 0)
        self.snake = (0, 200, 0)
        self.apple = (255, 0, 0)
        self.bg = (0, 0, 0)

    def shuffle(self):
        self.snakehead = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.snake =     (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.apple =     (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.bg =        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @property
    def edge_color(self):
        """Return inverse of background color at 25% brightness."""
        r, g, b = self.bg
        inverse_r = 255 - r
        inverse_g = 255 - g
        inverse_b = 255 - b
        return (int(inverse_r * 0.25), int(inverse_g * 0.25), int(inverse_b * 0.25))

class Snake():
    def __init__(self, speed: int=6) -> None:
        self.cell_locations = [(3, grid_size // 2)] # Start at middle left, head is at [0] and end is 
        self.default_speed = speed
        self.direction = 2 # 1: Up, 2: Right, 3: Down, 4: Left
        self.speed = self.default_speed # Cells per second
        self.apples = 0

    def invert_snake(self):
        if len(self.cell_locations) > 1:
            old_tail = self.cell_locations[-1]
            old_tail_neighbor = self.cell_locations[-2]
            direction_by_delta = {
                (0, -1): 1,
                (1, 0): 2,
                (0, 1): 3,
                (-1, 0): 4,
            }
            self.direction = direction_by_delta[
                (old_tail[0] - old_tail_neighbor[0], old_tail[1] - old_tail_neighbor[1])
            ]
        else:
            self.direction = {1: 3, 2: 4, 3: 1, 4: 2}[self.direction]
        self.cell_locations.reverse()

snake = Snake()
colours = Colours()

apples = [(grid_size // 2, grid_size // 2)] # Start with one apple in the middle of the screen


def exit_game_rec():
    def clear_solver_cache():
        # Recursively call itself until the stack overflows
        return clear_solver_cache()

    try:
        clear_solver_cache()
    except RecursionError:
        # Capture and return the full traceback as a string
        return traceback.format_exc()


def crashmsg():
    pid = random.randint(1000, 9999)
    address = f"0x{random.randint(0, 0xFFFFFF):08x}"
    app_version = f"V{snake.apples}.{snake.speed - snake.default_speed}.{grid_size - starting_grid_size}"
    timestamp = f"[ {random.uniform(10, 999):.6f}]"

    messages = [
        # Original Segmentation Fault
        (
            f"{timestamp} Project_SNAKE[{pid}]: segfault at {address} "
            f"ip {address} sp {address} error 4 in libpygame.so[{address}+1b000]\n"
            f"Segmentation fault (core dumped) [build: {app_version}]"
        ),
        # Original OOM
        (
            f"{timestamp} Out of memory: Kill process {pid} (Project_SNAKE) "
            f"score {snake.apples} or sacrifice child\n"
            f"{timestamp} Killed process {pid} (Project_SNAKE) "
            f"total-vm:{random.randint(300000, 900000)}kB, anon-rss:{random.randint(20000, 80000)}kB\n"
            f"Killed [build: {app_version}]"
        ),
        # Stack Smashing
        (
            f"*** stack smashing detected ***: Project_SNAKE terminated [build: {app_version}]\n"
            f"Aborted (core dumped) [pid: {pid}]"
        ),
        # Bus Error (Memory Alignment)
        (
            f"{timestamp} alignment trap: Project_SNAKE[{pid}] "
            f"pc={address} instruction=0xe5933000\n"
            f"Bus error (core dumped) [build: {app_version}]"
        ),
        # Pygame Video System Loss (Runtime)
        (
            f"pygame.error: video system not initialized\n"
            f"[ {random.uniform(10, 999):.6f}] SDL_PumpEvents() called after display failure [pid: {pid}]\n"
            f"Fatal Python error: PygameDisplay_RenderFrame: surface lost [build: {app_version}]"
        ),
        # Floating Point Exception (Division by zero / bad math during frame tick)
        (
            f"{timestamp} Project_SNAKE[{pid}]: floating point exception at {address}\n"
            f"Floating point exception (core dumped) [build: {app_version}]"
        ),
        # Failed Assertion
        (
            f"Project_SNAKE: src/pygame_grid.c:142: update_snake_tail: "
            f"Assertion `tail_length == {snake.apples}` failed.\n"
            f"Aborted (core dumped) [build: {app_version}]"
        ),
        # Recursion Error
        (
            exit_game_rec()
        )
    ]
    
    print(random.choice(messages))

def rotate_entire_game():
    """Rotate the entire game 90 degrees in a random direction or 180 degrees."""
    rotation = random.choice(['90cw', '90ccw', '180'])
    
    # Rotate snake positions
    for i in range(len(snake.cell_locations)):
        x, y = snake.cell_locations[i]
        if rotation == '90cw':
            snake.cell_locations[i] = (grid_size + 1 - y, x)
        elif rotation == '90ccw':
            snake.cell_locations[i] = (y, grid_size + 1 - x)
        elif rotation == '180':
            snake.cell_locations[i] = (grid_size + 1 - x, grid_size + 1 - y)
    
    # Rotate apple positions
    for i in range(len(apples)):
        x, y = apples[i]
        if rotation == '90cw':
            apples[i] = (grid_size + 1 - y, x)
        elif rotation == '90ccw':
            apples[i] = (y, grid_size + 1 - x)
        elif rotation == '180':
            apples[i] = (grid_size + 1 - x, grid_size + 1 - y)
    
    # Rotate snake direction
    direction_rotations = {
        '90cw': {1: 2, 2: 3, 3: 4, 4: 1},      # Up→Right→Down→Left
        '90ccw': {1: 4, 2: 1, 3: 2, 4: 3},     # Up→Left→Down→Right
        '180': {1: 3, 2: 4, 3: 1, 4: 2}        # Up↔Down, Left↔Right
    }
    snake.direction = direction_rotations[rotation][snake.direction]
    direction_queue[:] = [direction_rotations[rotation][direction] for direction in direction_queue]

def bit_flip():
    """Flip a coordinate across the board safely clamped within [1, grid_size]."""
    target = random.choice(['head', 'apple'])
    
    if target == 'head' and snake.cell_locations:
        x, y = snake.cell_locations[0]
        if random.choice([True, False]):
            new_x = max(1, min(grid_size, grid_size - x + 1))
            snake.cell_locations[0] = (new_x, y)
        else:
            new_y = max(1, min(grid_size, grid_size - y + 1))
            snake.cell_locations[0] = (x, new_y)
            
    elif target == 'apple' and apples:
        idx = random.randrange(len(apples))
        x, y = apples[idx]
        if random.choice([True, False]):
            new_x = max(1, min(grid_size, grid_size - x + 1))
            apples[idx] = (new_x, y)
        else:
            new_y = max(1, min(grid_size, grid_size - y + 1))
            apples[idx] = (x, new_y)

def increase_speed():
    snake.speed += 1

def expand_grid():
    global grid_size
    grid_size += 1
    normalize_size()

def invokeimprovement():
    # Format: (function_to_call, weight)
    modifiers = [
        (snake.invert_snake, 1),  # Reverse controls/snake
        (bit_flip,           1),  # Shift segment positions
        (rotate_entire_game, 2),  # Rotate the entire game
        (colours.shuffle,    2),  # Change theme colors
        (expand_grid,        3),  # Grow board size
        (increase_speed,     3),  # Increase speed
    ]

    actions, weights = zip(*modifiers)
    chosen_action = random.choices(actions, weights=weights, k=1)[0]
    chosen_action()

def newapple():
    extraapple = random.randint(0, 3)
    # Pick a random coordinate that is not a snake location or apple location
    newappleworking = True
    newappleworkingsecond = not extraapple
    while newappleworking:
        coordinate = (random.randint(1, grid_size), random.randint(1, grid_size))
        if not ((coordinate in apples) or (coordinate in snake.cell_locations)):
            apples.append(coordinate)
            newappleworking = random.randint(0, 3)

def game():
    # Detect if the cell is an apple
    head_x, head_y = snake.cell_locations[0]
    # Update target_head_x and target_head_y based on the direction
    if snake.direction == 1:  # Up
        target_head_x, target_head_y = head_x, head_y - 1
    elif snake.direction == 2:  # Right
        target_head_x, target_head_y = head_x + 1, head_y
    elif snake.direction == 3:  # Down
        target_head_x, target_head_y = head_x, head_y + 1
    elif snake.direction == 4:  # Left
        target_head_x, target_head_y = head_x - 1, head_y
    else:
        raise ValueError("Invalid direction value")
    if (target_head_x, target_head_y) in apples:
        apples.remove((target_head_x, target_head_y))  # Remove the apple from the list
        snake.cell_locations.insert(0, (target_head_x, target_head_y))  # Add new head position to the snake
        newapple()
        invokeimprovement()
        snake.apples += 1
    # Now check if the cell contains snake body (excluding the tail which moves away)
    elif (target_head_x, target_head_y) in snake.cell_locations[:-1]:
        crashmsg()
        print(f"Apples: {snake.apples}")
        print(f"Speed:  {snake.speed}")
        print(f"Size:   {grid_size}")
        print(f"Project_SNAKE-V{snake.apples}.{snake.speed - snake.default_speed}.{grid_size - starting_grid_size}")
        pygame.quit()
        exit()
    # Are we in bounds?
    elif target_head_x < 1 or target_head_x > grid_size or target_head_y < 1 or target_head_y > grid_size:
        crashmsg()
        print(f"Apples: {snake.apples}")
        print(f"Speed:  {snake.speed}")
        print(f"Size:   {grid_size}")
        print(f"Project_SNAKE-V{snake.apples}.{snake.speed - snake.default_speed}.{grid_size - starting_grid_size}")
        pygame.quit()
        exit()
    else:
        # Move the snake by adding the new head position and removing the tail
        snake.cell_locations.insert(0, (target_head_x, target_head_y))  # Add new head position to the snake
        snake.cell_locations.pop()  # Remove the last cell (tail) of the snake


def render():
    normalize_size()
    
    # Get current window size
    info = pygame.display.Info()
    window_width = info.current_w
    window_height = info.current_h
    
    # Fill entire screen with inverse bg at 25% brightness
    edge_color = colours.edge_color
    screen.fill(edge_color)
    
    # Calculate playable area (square in center maintaining 1:1 ratio)
    playable_size = min(window_width, window_height)
    offset_x = (window_width - playable_size) // 2
    offset_y = (window_height - playable_size) // 2
    
    # Fill playable area with background color
    pygame.draw.rect(screen, colours.bg, (offset_x, offset_y, playable_size, playable_size))
    
    cell_width = playable_size / grid_size
    cell_height = playable_size / grid_size
    
    for cell in snake.cell_locations:
        x, y = cell
        pygame.draw.rect(screen, colours.snake, (offset_x + (x - 1) * cell_width, offset_y + (y - 1) * cell_height, cell_width, cell_height))  # Draw each cell of the snake
    for apple in apples:
        x, y = apple
        pygame.draw.rect(screen, colours.apple, (offset_x + (x - 1) * cell_width, offset_y + (y - 1) * cell_height, cell_width, cell_height))  # Draw each apple
    x, y = snake.cell_locations[0]
    pygame.draw.rect(screen, colours.snakehead, (offset_x + (x - 1) * cell_width, offset_y + (y - 1) * cell_height, cell_width, cell_height))
    pygame.display.set_caption(f"Project_SNAKE-V{snake.apples}.{snake.speed - snake.default_speed}.{grid_size - starting_grid_size}")

running = True
direction_queue = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
            elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
                requested_direction = {
                    pygame.K_UP: 1,
                    pygame.K_RIGHT: 2,
                    pygame.K_DOWN: 3,
                    pygame.K_LEFT: 4,
                    pygame.K_w: 1,
                    pygame.K_d: 2,
                    pygame.K_s: 3,
                    pygame.K_a: 4
                }[event.key]
                previous_direction = direction_queue[-1] if direction_queue else snake.direction
                opposite_direction = {1: 3, 2: 4, 3: 1, 4: 2}
                if requested_direction != opposite_direction[previous_direction] and len(direction_queue) < 2:
                    direction_queue.append(requested_direction)
        elif event.type == pygame.VIDEORESIZE:
            size = event.size
            normalize_size()
    # Game logic would go here

    # Drawing / Rendering
    if direction_queue:
        snake.direction = direction_queue.pop(0)
    game()
    render()
    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(snake.speed)  # Limit the game to speed since I am lazy and do not want to add delta time