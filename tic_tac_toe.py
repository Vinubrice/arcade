import pygame
import sys
import time
from tools import load_data, save_data, get_current_user

def tic_tac_toe():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    GRID_SIZE = 400
    GRID_TOPLEFT_X = (WIDTH - GRID_SIZE) // 2
    GRID_TOPLEFT_Y = (HEIGHT - GRID_SIZE) // 2
    SQUARE_SIZE = GRID_SIZE // 3
    LINE_WIDTH = 10

    CIRCLE_RADIUS = SQUARE_SIZE // 3
    CIRCLE_WIDTH = 15
    CROSS_WIDTH = 25
    SPACE = SQUARE_SIZE // 4

    BG_COLOR = (25, 49, 83)
    LINE_COLOR = (255, 255, 255)
    CIRCLE_COLOR = (0, 35, 61)
    CROSS_COLOR = (255, 69, 0)
    TEXT_COLOR = (0, 0, 0)
    BORDER_COLOR = (255, 255, 255)

    FONT = pygame.font.Font(None, 40)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")

    background_image = pygame.image.load('assets/tic_tac_bg.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    place_sound = pygame.mixer.Sound('sounds/complete.wav')
    point_sound = pygame.mixer.Sound('sounds/eat.wav')
    win_sound = pygame.mixer.Sound('sounds/win.wav')
    game_over_sound = pygame.mixer.Sound('sounds/lose.wav')

    board = [[None for _ in range(3)] for _ in range(3)]
    player = "O"
    wins = {"O": 0, "X": 0, "Draws": 0}
    rounds = 0

    data = load_data()
    current_user = get_current_user()
    user_wins_key = f"{current_user}_xo"
    user_wins = data.get(user_wins_key, 0)

    def draw_lines():
        pygame.draw.rect(screen, BORDER_COLOR,
                         (GRID_TOPLEFT_X - 5, GRID_TOPLEFT_Y - 5, GRID_SIZE + 10, GRID_SIZE + 10), 5)
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR,
                             (GRID_TOPLEFT_X, GRID_TOPLEFT_Y + i * SQUARE_SIZE),
                             (GRID_TOPLEFT_X + GRID_SIZE, GRID_TOPLEFT_Y + i * SQUARE_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR,
                             (GRID_TOPLEFT_X + i * SQUARE_SIZE, GRID_TOPLEFT_Y),
                             (GRID_TOPLEFT_X + i * SQUARE_SIZE, GRID_TOPLEFT_Y + GRID_SIZE), LINE_WIDTH)

    def draw_figures():
        for row in range(3):
            for col in range(3):
                center = (GRID_TOPLEFT_X + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                          GRID_TOPLEFT_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2)
                if board[row][col] == "O":
                    pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif board[row][col] == "X":
                    pygame.draw.line(screen, CROSS_COLOR,
                                     (center[0] - SPACE, center[1] - SPACE),
                                     (center[0] + SPACE, center[1] + SPACE), CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR,
                                     (center[0] - SPACE, center[1] + SPACE),
                                     (center[0] + SPACE, center[1] - SPACE), CROSS_WIDTH)

    def check_winner():
        for row in board:
            if row.count(row[0]) == 3 and row[0] is not None:
                return row[0]
        for col in range(3):
            column = [board[row][col] for row in range(3)]
            if column.count(column[0]) == 3 and column[0] is not None:
                return column[0]
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2]
        return None

    def is_draw():
        return all(all(cell is not None for cell in row) for row in board)

    def restart_game():
        nonlocal board, player
        board = [[None for _ in range(3)] for _ in range(3)]
        player = "O"
        screen.blit(background_image, (0, 0))
        draw_lines()
        display_scores()
        display_turn()
        display_user_wins()

    def display_scores():
        scores_text = FONT.render(f"O Wins: {wins['O']}  X Wins: {wins['X']}  Draws: {wins['Draws']}", True, TEXT_COLOR)
        screen.blit(scores_text, (20, 20))

    def display_turn():
        pygame.draw.rect(screen, BORDER_COLOR, (WIDTH - 220, 20, 200, 40))
        turn_text = FONT.render(f"Turn: {player}", True, TEXT_COLOR)
        screen.blit(turn_text, (WIDTH - 220, 20))

    def display_user_wins():
        user_wins_text = FONT.render(f"No. of Wins: {user_wins}", True, TEXT_COLOR)
        screen.blit(user_wins_text, (GRID_TOPLEFT_X - 200, GRID_TOPLEFT_Y + GRID_SIZE // 2 - 20))

    def display_result(result):
        result_text = FONT.render(result, True, TEXT_COLOR)
        screen.fill(BG_COLOR)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - result_text.get_height() // 2))
        pygame.display.update()
        game_over_sound.play()
        time.sleep(4)
        return_to_menu(screen)

    def return_to_menu(screen):
        import menu
        menu.game_menu(screen)

    screen.blit(background_image, (0, 0))
    draw_lines()
    display_scores()
    display_turn()
    display_user_wins()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_result("Game Over")
                return_to_menu(screen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_col = (mouseX - GRID_TOPLEFT_X) // SQUARE_SIZE
                clicked_row = (mouseY - GRID_TOPLEFT_Y) // SQUARE_SIZE

                if 0 <= clicked_row < 3 and 0 <= clicked_col < 3 and board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    draw_figures()
                    place_sound.play()

                    winner = check_winner()
                    if winner:
                        wins[winner] += 1
                        display_scores()
                        point_sound.play()
                        rounds += 1
                        if rounds >= 5:
                            if wins["O"] > wins["X"]:
                                display_result("O Wins!")
                                win_sound.play()
                            elif wins["X"] > wins["O"]:
                                user_wins += 1
                                data[user_wins_key] = user_wins
                                save_data(data)
                                display_result("X Wins!")
                                win_sound.play()
                            else:
                                display_result("It's a Draw!")
                        else:
                            restart_game()
                    elif is_draw():
                        wins["Draws"] += 1
                        display_scores()
                        rounds += 1
                        if rounds >= 5:
                            if wins["O"] > wins["X"]:
                                display_result("O Wins!")
                                win_sound.play()
                            elif wins["X"] > wins["O"]:
                                user_wins += 1
                                data[user_wins_key] = user_wins
                                save_data(data)
                                display_result("X Wins!")
                                win_sound.play()
                            else:
                                display_result("It's a Draw!")
                        else:
                            restart_game()
                    else:
                        player = "X" if player == "O" else "O"
                        display_turn()

        pygame.display.update()
