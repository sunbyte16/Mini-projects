import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (100, 100, 100)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Start with a snake of length 3 in the middle of the screen
        self.length = 3
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # Get current head position
        current = self.get_head_position()
        x, y = self.direction
        new = (current[0] + x, current[1] + y)
        
        # Check if snake hits the wall
        if new[0] < 0 or new[0] >= GRID_WIDTH or new[1] < 0 or new[1] >= GRID_HEIGHT:
            return True  # Wall collision detected
        
        # Check if snake collides with itself
        if new in self.positions[3:]:
            return True  # Self collision detected
        
        # Update positions
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return False  # No collision
    
    def render(self, surface):
        # Draw snake body
        for i, p in enumerate(self.positions):
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)
            # Draw a darker outline for each segment
            pygame.draw.rect(surface, DARK_GREEN, rect, 1)

    def handle_keys(self, keys):
        # Prevent reversing into itself
        if keys[pygame.K_UP] and self.direction != DOWN:
            self.direction = UP
        elif keys[pygame.K_DOWN] and self.direction != UP:
            self.direction = DOWN
        elif keys[pygame.K_LEFT] and self.direction != RIGHT:
            self.direction = LEFT
        elif keys[pygame.K_RIGHT] and self.direction != LEFT:
            self.direction = RIGHT

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])
        
    def randomize_position(self, snake_positions):
        # Generate a random position that's not occupied by the snake
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        while self.position in snake_positions:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        # Draw a white outline for the food
        pygame.draw.rect(surface, WHITE, rect, 1)

def draw_grid(surface):
    # Draw the grid lines
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WINDOW_WIDTH, y))
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, WINDOW_HEIGHT))

def main():
    # Setup
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    font = pygame.font.SysFont('arial', 25)
    game_over_font = pygame.font.SysFont('arial', 50)
    
    # Game objects
    snake = Snake()
    food = Food()
    
    # Game state
    game_over = False
    running = True
    
    # Main game loop
    while running:
        clock.tick(10)  # 10 FPS - controls game speed
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:  # Restart game
                        snake.reset()
                        food.randomize_position(snake.positions)
                        game_over = False
                    elif event.key == pygame.K_q:  # Quit game
                        running = False
        
        # Get key states for continuous movement
        keys = pygame.key.get_pressed()
        
        if not game_over:
            # Update snake direction based on keys
            snake.handle_keys(keys)
            
            # Update snake position and check for collisions
            collision = snake.update()
            
            # Set game over if collision detected
            if collision:
                game_over = True
            
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position(snake.positions)
        
        # Drawing
        screen.fill(BLACK)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        
        # Display score
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        screen.blit(score_text, (5, 5))
        
        # Display game over message
        if game_over:
            game_over_text = game_over_font.render('GAME OVER', True, WHITE)
            restart_text = font.render('Press R to Restart or Q to Quit', True, WHITE)
            screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                                        WINDOW_HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                                      WINDOW_HEIGHT // 2 + game_over_text.get_height()))
        
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()