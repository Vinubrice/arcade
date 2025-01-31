import time
import pygame
import random
from tools import load_data, save_data, get_current_user

def snake():
    pygame.init()

    WIDTH, HEIGHT = 800, 600

    PRUSSIAN_BLUE = (0, 49, 83)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    ACCENT_GREEN = (0, 255, 123)
    ACCENT_YELLOW = (255, 223, 0)

    BLOCK_SIZE = 20
    SNAKE_SPEED = 7

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

    data = load_data()
    current_user = get_current_user()
    high_score_key = f"{current_user}_snake"
    high_score = data.get(high_score_key, 0)

    # Load sounds
    eat_sound = pygame.mixer.Sound('sounds/eat.wav')
    game_over_sound = pygame.mixer.Sound('sounds/lose.wav')

    def your_score(score):
        value = score_font.render(f"Your Score: {score}", True, ACCENT_YELLOW)
        screen.blit(value, [0, 0])

    def high_score_display(score):
        value = score_font.render(f"High Score: {score}", True, ACCENT_YELLOW)
        screen.blit(value, [WIDTH - value.get_width() - 10, 10])

    def our_snake(block_size, snake_list):
        for i, x in enumerate(snake_list):
            color = ACCENT_GREEN if i % 2 == 0 else ACCENT_YELLOW
            if i == len(snake_list) - 1:
                pygame.draw.ellipse(screen, ACCENT_YELLOW, [x[0], x[1], block_size, block_size])
                eye_x = x[0] + block_size // 4
                eye_y = x[1] + block_size // 4
                pygame.draw.circle(screen, BLACK, (eye_x, eye_y), block_size // 8)
            else:
                pygame.draw.rect(screen, color, [x[0], x[1], block_size, block_size], border_radius=8)

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

    def gameLoop():
        game_over = False
        game_close = False

        x1 = WIDTH / 2
        y1 = HEIGHT / 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
        foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0

        while not game_over:

            while game_close:
                screen.fill(PRUSSIAN_BLUE)
                message("You Lost! Press Q-Quit or C-Play Again", RED)
                your_score(length_of_snake - 1)
                high_score_display(high_score)
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
                    if event.key == pygame.K_LEFT:
                        if x1_change == 0:
                            x1_change = -BLOCK_SIZE
                            y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        if x1_change == 0:
                            x1_change = BLOCK_SIZE
                            y1_change = 0
                    elif event.key == pygame.K_UP:
                        if y1_change == 0:
                            y1_change = -BLOCK_SIZE
                            x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        if y1_change == 0:
                            y1_change = BLOCK_SIZE
                            x1_change = 0

            x1 = (x1 + x1_change) % WIDTH
            y1 = (y1 + y1_change) % HEIGHT

            screen.fill(PRUSSIAN_BLUE)
            pygame.draw.rect(screen, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True

            our_snake(BLOCK_SIZE, snake_list)
            your_score(length_of_snake - 1)
            high_score_display(high_score)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                eat_sound.play()  # Play sound when snake eats food
                foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
                foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
                length_of_snake += 1

            clock.tick(SNAKE_SPEED)

        if length_of_snake - 1 > high_score:
            data[high_score_key] = length_of_snake - 1
            save_data(data)

        screen.fill(PRUSSIAN_BLUE)
        game_over_text = font_style.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        game_over_sound.play() 
        time.sleep(4)
        return_to_menu(screen)

        pygame.quit()

    def return_to_menu(screen):
        import menu
        menu.game_menu(screen)

    gameLoop()
