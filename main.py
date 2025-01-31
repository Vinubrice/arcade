#!/usr/bin/env python3

import pygame
from menu import game_menu
from tools import load_data, set_current_user, get_current_user, create_user

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
PRUSSIAN_BLUE = (0, 49, 83)
DARK_BLUE = (0, 35, 61)
LIGHT_BLUE = (102, 153, 204)
CONTRAST_BLUE = (0, 68, 102)
BUTTON_BLUE = (51, 102, 153)
BUTTON_RED = (204, 51, 51)
BLACK = (0, 0, 0)

pygame.font.init()
FONT = pygame.font.Font(None, 36)

data = load_data()

button_sound = pygame.mixer.Sound('sounds/button.wav')
game_launch_sound = pygame.mixer.Sound('sounds/launch.wav')
logout_sound = pygame.mixer.Sound('sounds/logout.mp3')

def draw_text(surface, text, x, y, color=BLACK):
    text_surface = FONT.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_rounded_rect(surface, rect, color, border_radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

def draw_rounded_image(surface, image, rect, border_radius=10):
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=border_radius)
    mask.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(mask, rect.topleft)

def login_page(screen):
    global data

    username = ""
    password = ""
    active_field = None
    cursor_visible = True
    cursor_timer = 0
    message = ""

    login_button = pygame.Rect(300, 400, 200, 50)
    create_user_button = pygame.Rect(300, 460, 200, 50)
    username_field = pygame.Rect(300, 200, 300, 40)
    password_field = pygame.Rect(300, 280, 300, 40)

    while True:
        screen.fill(PRUSSIAN_BLUE)
        draw_text(screen, "Welcome! Login or Signup...", 250, 100, LIGHT_BLUE)
        draw_text(screen, "Username:", 150, 205, LIGHT_BLUE)
        draw_text(screen, "Password:", 150, 285, LIGHT_BLUE)

        draw_rounded_rect(screen, username_field, CONTRAST_BLUE, border_radius=15)
        draw_rounded_rect(screen, password_field, CONTRAST_BLUE, border_radius=15)
        draw_rounded_rect(screen, login_button, BUTTON_BLUE, border_radius=15)
        draw_rounded_rect(screen, create_user_button, BUTTON_RED, border_radius=15)

        draw_text(screen, username + ("|" if cursor_visible and active_field == "username" else ""), 310, 210, BLACK)
        draw_text(screen, "*" * len(password) + ("|" if cursor_visible and active_field == "password" else ""), 310, 290, BLACK)
        draw_text(screen, "Login", 360, 410, WHITE)
        draw_text(screen, "Create User", 340, 470, WHITE)

        if message:
            draw_text(screen, message, 300, 370, BUTTON_RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if username_field.collidepoint(event.pos):
                    active_field = "username"
                elif password_field.collidepoint(event.pos):
                    active_field = "password"
                elif login_button.collidepoint(event.pos):
                    button_sound.play()
                    if username in data and data[username] == password:
                        set_current_user(username)
                        return
                    else:
                        message = "Invalid login. Try again."
                elif create_user_button.collidepoint(event.pos):
                    button_sound.play()
                    if username not in data:
                        create_user(username, password)
                        data = load_data()
                        message = "User created successfully!"
                    else:
                        message = "User already exists."
            elif event.type == pygame.KEYDOWN:
                if active_field == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_field = "password"
                    else:
                        username += event.unicode
                elif active_field == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key != pygame.K_RETURN:
                        password += event.unicode
                    if event.key == pygame.K_RETURN:
                        if username in data and data[username] == password:
                            button_sound.play()
                            set_current_user(username)
                            return
                        else:
                            message = "Invalid login. Try again."

        cursor_timer += 1
        if cursor_timer % 200 == 0:
            cursor_visible = not cursor_visible

        pygame.display.flip()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Arcade")

    while True:
        login_page(screen)
        game_menu(screen)
        login_page(screen)

if __name__ == "__main__":
    main()
