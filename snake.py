import pygame
import time
import random
import os

# Initialize the pygame
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
border_color = (200, 200, 200)

# Get screen dimensions
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set display size to half the screen size
dis_width = screen_width // 2
dis_height = screen_height // 2

# Center the window on the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(screen_width - dis_width) // 2},{(screen_height - dis_height) // 2}"
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by ChatGPT')

# Load background image and scale to fit display size
background_img = pygame.image.load('background.jpg')
background_img = pygame.transform.scale(background_img, (dis_width, dis_height))
background_img = background_img.convert()

# Dim the background image
background_img_dim = background_img.copy()
dim_surface = pygame.Surface(background_img.get_size()).convert_alpha()
dim_surface.fill((0, 0, 0, 128))  # Half transparent black overlay
background_img_dim.blit(dim_surface, (0, 0))

# Clock and speed settings
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# Font settings
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [10, 10])

def our_snake(snake_block, snake_list):
    for i, x in enumerate(reversed(snake_list)):
        # Calculate transparency level based on position in snake
        alpha = int(255 - i * (255 / len(snake_list)))
        snake_segment = pygame.Surface((snake_block, snake_block), pygame.SRCALPHA)
        snake_segment.fill((255, 255, 255, alpha))  # White with variable alpha
        dis.blit(snake_segment, (x[0], x[1]))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2))
    dis.blit(mesg, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block, snake_block))
    foody = round(random.randrange(0, dis_height - snake_block, snake_block))

    while not game_over:

        while game_close:
            dis.blit(background_img_dim, (0, 0))
            message("You Lost! Press Q-Quit or C-Play Again", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width - snake_block or x1 < 0 or y1 >= dis_height - snake_block or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Check if snake touches the borders drawn on the screen
        if x1 >= dis_width - snake_block:
            x1 = dis_width - snake_block - 1
            game_close = True
        elif x1 < 0:
            x1 = 0
            game_close = True
        elif y1 >= dis_height - snake_block:
            y1 = dis_height - snake_block - 1
            game_close = True
        elif y1 < 0:
            y1 = 0
            game_close = True
        
        # Round snake position to nearest snake_block
        x1 = round(x1 / snake_block) * snake_block
        y1 = round(y1 / snake_block) * snake_block
        
        # Clear the screen with a semi-transparent surface
        dis.fill((0, 0, 0, 10))  # Adjust alpha as needed for fading effect
        
        dis.blit(background_img_dim, (0, 0))
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake segments in reverse order to create the trailing effect
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        # Draw borders
        pygame.draw.rect(dis, border_color, [0, 0, dis_width, 10])
        pygame.draw.rect(dis, border_color, [0, dis_height - 10, dis_width, 10])
        pygame.draw.rect(dis, border_color, [0, 0, 10, dis_height])
        pygame.draw.rect(dis, border_color, [dis_width - 10, 0, 10, dis_height])

        pygame.display.update()

        # Check if snake has eaten the food
        if x1 >= foodx and x1 < foodx + snake_block and y1 >= foody and y1 < foody + snake_block:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
