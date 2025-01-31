import pygame
import random
import time

def ping_pong():
    FONT = pygame.font.Font(None, 36)
    BLACK = (0, 0, 0)

    def draw_result(surface, text, x, y, color=BLACK):
        text_surface = FONT.render(text, True, color)
        surface.blit(text_surface, (x, y))

    pygame.init()

    WIDTH, HEIGHT = 800, 600
    FPS = 60

    PRUSSIAN_BLUE = (0, 49, 83)
    LIGHT_PRUSSIAN_BLUE = (89, 128, 163)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (211, 211, 211)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pong Game')

    background_image = pygame.image.load('assets/pong_bg.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
    PADDLE_SPEED = 10
    BALL_RADIUS = 10
    BALL_SPEED = 5

    player1_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    player2_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    ball_velocity = [random.choice([1, -1]) * BALL_SPEED, random.choice([1, -1]) * BALL_SPEED]

    score_player1 = 0
    score_player2 = 0

    font = pygame.font.SysFont('Arial', 30)

    knock_sound = pygame.mixer.Sound('sounds/knock.mp3')
    miss_sound = pygame.mixer.Sound('sounds/eat.wav')
    game_over_sound = pygame.mixer.Sound('sounds/lose.wav')

    def reset_ball():
        ball_velocity[0] = random.choice([1, -1]) * BALL_SPEED
        ball_velocity[1] = random.choice([1, -1]) * BALL_SPEED
        ball.x = WIDTH // 2 - BALL_RADIUS
        ball.y = HEIGHT // 2 - BALL_RADIUS

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and player1_paddle.top > 0:
            player1_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
            player1_paddle.y += PADDLE_SPEED

        if keys[pygame.K_UP] and player2_paddle.top > 0:
            player2_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player2_paddle.bottom < HEIGHT:
            player2_paddle.y += PADDLE_SPEED

        ball.x += ball_velocity[0]
        ball.y += ball_velocity[1]

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_velocity[1] *= -1

        if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
            ball_velocity[0] *= -1
            knock_sound.play()  

        if ball.left <= 0:
            score_player2 += 1
            miss_sound.play() 
            reset_ball()
        if ball.right >= WIDTH:
            score_player1 += 1
            miss_sound.play()
            reset_ball()

        screen.blit(background_image, (0, 0)) 

        pygame.draw.rect(screen, LIGHT_PRUSSIAN_BLUE, player1_paddle)
        pygame.draw.rect(screen, LIGHT_PRUSSIAN_BLUE, player2_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        score_text = font.render(f'{score_player1}  -  {score_player2}', True, LIGHT_GRAY)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()

        if (score_player1 - score_player2) >= 10:
            draw_result(screen, f"Player 1 wins!", 300, 300, color=WHITE)
            pygame.display.update()
            game_over_sound.play()  
            time.sleep(4)
            running = False
        elif (score_player2 - score_player1) >= 10:
            draw_result(screen, f"Player 2 wins!", 300, 300, color=WHITE)
            pygame.display.update()
            game_over_sound.play()  
            time.sleep(4)
            running = False

    screen.fill(PRUSSIAN_BLUE)
    game_over_text = FONT.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    game_over_sound.play() 
    time.sleep(4)
    return_to_menu(screen)

    pygame.quit()

def return_to_menu(screen):
    import menu
    menu.game_menu(screen)
