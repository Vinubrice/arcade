import pygame
from snake import snake
from tetris import tetris
from flappy import flappy
from ping_pong import ping_pong
from tic_tac_toe import tic_tac_toe
from tools import get_current_user, set_current_user

pygame.init()
pygame.mixer.init()  
pygame.font.init()
FONT = pygame.font.Font(None, 36)

button_sound = pygame.mixer.Sound('sounds/button.wav')
game_launch_sound = pygame.mixer.Sound('sounds/launch.wav')
logout_sound = pygame.mixer.Sound('sounds/logout.mp3')

def draw_text(surface, text, x, y, color=(0, 0, 0)):
    text_surface = FONT.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_rounded_rect(surface, rect, color, border_radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

def draw_rounded_image(surface, image, rect, border_radius=10):
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=border_radius)
    mask.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(mask, rect.topleft)

def game_menu(screen):

    game_names = ["Snake", "Tetris", "Flappy Bird", "Ping Pong", "Tic Tac Toe"]
    game_functions = [snake, tetris, flappy, ping_pong, tic_tac_toe]
    game_thumbnails = ["resources/snake_thumb.png", "resources/tetris_thumb.png", "resources/flappy_thumb.png", "resources/ping_pong_thumb.png", "resources/tic_tac_toe_thumb.png"]

    button_width = 220
    button_height = 150
    grid_width = 3
    grid_height = 2
    padding = 20

    total_width = button_width * grid_width + padding * (grid_width - 1)
    total_height = button_height * grid_height + padding * (grid_height - 1)

    start_x = (800 - total_width) // 2
    start_y = (600 - total_height) // 2

    buttons = [pygame.Rect(start_x + (i % grid_width) * (button_width + padding), start_y + (i // grid_width) * (button_height + padding), button_width, button_height) for i in range(len(game_names))]
    top_bar = pygame.Rect(0, 0, 800, 50)
    logout_button = pygame.Rect(650, 10, 120, 35)

    while True:
        screen.fill((0, 49, 83))
        draw_rounded_rect(screen, top_bar, (0, 35, 61), border_radius=0)
        draw_text(screen, f"Welcome {get_current_user()}!", 20, 15, (255, 255, 255))
        draw_text(screen, "Game Menu", 320, 70, (102, 153, 204))

        for i, button in enumerate(buttons):
            thumbnail = pygame.image.load(game_thumbnails[i])
            thumbnail = pygame.transform.scale(thumbnail, (button.width, button.height))
            draw_rounded_image(screen, thumbnail, button, border_radius=15)
            draw_text(screen, game_names[i], button.x + 20, button.y + 110, (255, 255, 255))

        draw_rounded_rect(screen, logout_button, (204, 51, 51), border_radius=10)
        draw_text(screen, "Logout", logout_button.x + 20, logout_button.y + 5, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if logout_button.collidepoint(event.pos):
                    logout_sound.play() 
                    set_current_user(None)
                    return
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        game_launch_sound.play() 
                        game_functions[i]()
                        return  

        pygame.display.flip()
