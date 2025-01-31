import pygame
import random
import time
from tools import load_data, save_data, get_current_user

def flappy():
    pygame.init()

    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    PIPE_WIDTH = 60
    PIPE_GAP = 200
    PIPE_SPEED = 3
    HORIZONTAL_GAP = 400

    PRUSSIAN_BLUE = (0, 49, 83)
    LIGHT_BLUE = (173, 216, 230)
    YELLOW_ACCENT = (255, 223, 0)
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    background_image = pygame.image.load('assets/flappy_bg.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    cross_pipe_sound = pygame.mixer.Sound('sounds/complete.wav')
    game_over_sound = pygame.mixer.Sound('sounds/lose.wav')

    class Bird:
        def __init__(self):
            self.x = 200
            self.y = 300
            self.width = 40
            self.height = 40
            self.velocity = 0
            self.bird_image = pygame.image.load('resources/bird_up.png')
            self.bird_image = pygame.transform.scale(self.bird_image, (self.width, self.height))

        def move(self):
            self.velocity += 0.2
            self.y += self.velocity
            if self.y < 0:
                self.y = 0
                self.velocity = 0
            if self.y > 600 - self.height:
                self.y = 600 - self.height
                self.velocity = 0

        def jump(self):
            self.velocity = -6

        def draw(self, draw_sc):
            draw_sc.blit(self.bird_image, (self.x, self.y))

    class Pipe:
        def __init__(self):
            self.x = WIDTH
            self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
            self.width = PIPE_WIDTH
            self.top_rect = pygame.Rect(self.x, 0, self.width, self.height)
            self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, self.width, HEIGHT - self.height - PIPE_GAP)

        def move(self):
            self.x -= PIPE_SPEED
            self.top_rect.x = self.x
            self.bottom_rect.x = self.x

        def draw(self):
            pygame.draw.rect(screen, LIGHT_BLUE, self.top_rect)
            pygame.draw.rect(screen, LIGHT_BLUE, self.bottom_rect)

        def off_screen(self):
            return self.x + self.width < 0

        def collide(self, bird):
            return self.top_rect.colliderect(pygame.Rect(bird.x, bird.y, bird.width, bird.height)) or \
                   self.bottom_rect.colliderect(pygame.Rect(bird.x, bird.y, bird.width, bird.height))

    def game():
        bird = Bird()
        pipes = []
        clock = pygame.time.Clock()
        score = 0
        running = True
        start_time = time.time()

        data = load_data()
        current_user = get_current_user()
        high_score_key = f"{current_user}_flappy"
        high_score = data.get(high_score_key, 0)

        while running:
            clock.tick(FPS)
            screen.blit(background_image, (0, 0))  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        bird.jump()

            bird.move()
            bird.draw(screen)

            if time.time() - start_time > 5:
                if len(pipes) == 0 or pipes[-1].x < WIDTH - HORIZONTAL_GAP:
                    pipes.append(Pipe())

            for pipe in pipes:
                pipe.move()
                pipe.draw()
                if pipe.off_screen():
                    pipes.remove(pipe)
                    score += 1
                    cross_pipe_sound.play()  

                if pipe.collide(bird):
                    running = False

            if bird.y > HEIGHT - bird.height or bird.y < 0:
                running = False

            font = pygame.font.SysFont('Arial', 30)
            score_text = font.render(f"Score: {score}", True, YELLOW_ACCENT)
            screen.blit(score_text, (10, 10))

            high_score_text = font.render(f"High Score: {high_score}", True, YELLOW_ACCENT)
            screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

            pygame.display.update()

        if score > high_score:
            data[high_score_key] = score
            save_data(data)

        screen.fill(PRUSSIAN_BLUE)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        game_over_sound.play() 
        time.sleep(4)
        return_to_menu(screen)

        pygame.quit()

    def return_to_menu(screen):
        import menu
        menu.game_menu(screen)

    game()
