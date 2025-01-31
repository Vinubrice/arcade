import pygame
import random
import time
from tools import load_data, save_data, get_current_user

def tetris():
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    TETRIS_WIDTH, TETRIS_HEIGHT = 300, 600
    GRID_SIZE = 30
    COLUMNS = TETRIS_WIDTH // GRID_SIZE
    ROWS = TETRIS_HEIGHT // GRID_SIZE

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    COLORS = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), 
        (255, 255, 0), (0, 255, 255), (255, 0, 255), 
        (255, 165, 0)
    ]

    SHAPES = [
        [[[1, 1, 1], [0, 1, 0]], 
         [[0, 1], [1, 1], [0, 1]],
         [[0, 1, 0], [1, 1, 1]],
         [[1, 0], [1, 1], [1, 0]]],

        [[[1, 1], [1, 1]]], 

        [[[1, 1, 1, 1]], 
         [[1], [1], [1], [1]]],

        [[[0, 1, 1], [1, 1, 0]], 
         [[1, 0], [1, 1], [0, 1]]],

        [[[1, 1, 0], [0, 1, 1]], 
         [[0, 1], [1, 1], [1, 0]]],

        [[[1, 1, 1], [1, 0, 0]], 
         [[1, 1], [0, 1], [0, 1]],
         [[0, 0, 1], [1, 1, 1]],
         [[1, 0], [1, 0], [1, 1]]],

        [[[1, 1, 1], [0, 0, 1]], 
         [[0, 1], [0, 1], [1, 1]],
         [[1, 0, 0], [1, 1, 1]],
         [[1, 1], [1, 0], [1, 0]]]
    ]

    data = load_data()
    current_user = get_current_user()
    high_score_key = f"{current_user}_tetris"
    high_score = data.get(high_score_key, 0)

    clear_row_sound = pygame.mixer.Sound('sounds/button.wav')
    game_over_sound = pygame.mixer.Sound('sounds/lose.wav')

    def create_grid(locked_positions):
        grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
        for (row, col), color in locked_positions.items():
            grid[row][col] = color
        return grid

    def convert_shape_format(shape):
        positions = []
        shape_format = shape['shape'][shape['rotation']]
        for i, line in enumerate(shape_format):
            for j, column in enumerate(line):
                if column == 1:
                    positions.append((shape['y'] + i, shape['x'] + j))
        return positions

    def valid_space(shape, grid):
        accepted_positions = [[(row, col) for col in range(COLUMNS) if grid[row][col] == BLACK] for row in range(ROWS)]
        accepted_positions = [pos for sublist in accepted_positions for pos in sublist]
        formatted = convert_shape_format(shape)
        for pos in formatted:
            if pos not in accepted_positions and pos[0] >= 0:
                return False
        return True

    def check_lost(positions):
        return any(row < 1 for row, col in positions)

    def get_shape():
        return {
            'shape': random.choice(SHAPES),
            'color': random.choice(COLORS),
            'x': COLUMNS // 2 - 2,
            'y': 0,
            'rotation': 0
        }

    def draw_grid(surface):
        for row in range(ROWS):
            pygame.draw.line(surface, WHITE, (0, row * GRID_SIZE), (TETRIS_WIDTH, row * GRID_SIZE))
        for col in range(COLUMNS):
            pygame.draw.line(surface, WHITE, (col * GRID_SIZE, 0), (col * GRID_SIZE, TETRIS_HEIGHT))

    def draw_window(surface, grid, current_piece, next_piece, score):
        surface.fill(BLACK)
        tetris_surface = pygame.Surface((TETRIS_WIDTH, TETRIS_HEIGHT))
        tetris_surface.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLUMNS):
                pygame.draw.rect(tetris_surface, grid[row][col], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        formatted = convert_shape_format(current_piece)
        for pos in formatted:
            x, y = pos[1], pos[0]
            if y >= 0:
                pygame.draw.rect(tetris_surface, current_piece['color'],
                                 (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        draw_grid(tetris_surface)
        surface.blit(tetris_surface, ((SCREEN_WIDTH - TETRIS_WIDTH) // 2, 0))
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Piece', True, WHITE)
        surface.blit(label, (SCREEN_WIDTH - 200, 50))
        next_format = next_piece['shape'][0]
        for i, line in enumerate(next_format):
            for j, column in enumerate(line):
                if column == 1:
                    pygame.draw.rect(surface, next_piece['color'],
                                     (SCREEN_WIDTH - 200 + j * GRID_SIZE, 100 + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        score_label = font.render(f'Score: {score}', True, WHITE)
        surface.blit(score_label, (50, 50))

        high_score_label = font.render(f'High Score: {high_score}', True, WHITE)
        surface.blit(high_score_label, (SCREEN_WIDTH - high_score_label.get_width() - 10, 10))

    def clear_rows(grid, locked):
        cleared = 0
        for i in range(len(grid) - 1, -1, -1):
            if BLACK not in grid[i]:
                cleared += 1
                del grid[i]
                grid.insert(0, [BLACK for _ in range(COLUMNS)])
                for key in sorted(list(locked.keys()), key=lambda x: x[0], reverse=True):
                    if key[0] == i:
                        del locked[key]
                    elif key[0] < i:
                        locked[(key[0] + 1, key[1])] = locked.pop(key)
        if cleared > 0:
            clear_row_sound.play()
        return cleared

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()
    locked_positions = {}
    grid = create_grid(locked_positions)

    current_piece = get_shape()
    next_piece = get_shape()
    score = 0
    run = True
    fall_time = 0
    fall_speed = 0.5

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece['y'] += 1
            if not valid_space(current_piece, grid):
                current_piece['y'] -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[(pos[0], pos[1])] = current_piece['color']
                current_piece = next_piece
                next_piece = get_shape()
                score += clear_rows(grid, locked_positions) * 10
                if check_lost(locked_positions):
                    run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece['x'] -= 1
                    if not valid_space(current_piece, grid):
                        current_piece['x'] += 1
                if event.key == pygame.K_RIGHT:
                    current_piece['x'] += 1
                    if not valid_space(current_piece, grid):
                        current_piece['x'] -= 1
                if event.key == pygame.K_DOWN:
                    current_piece['y'] += 1
                    if not valid_space(current_piece, grid):
                        current_piece['y'] -= 1
                if event.key == pygame.K_UP:
                    current_piece['rotation'] = (current_piece['rotation'] + 1) % len(current_piece['shape'])
                    if not valid_space(current_piece, grid):
                        current_piece['rotation'] = (current_piece['rotation'] - 1) % len(current_piece['shape'])
        draw_window(screen, grid, current_piece, next_piece, score)
        pygame.display.update()

    if score > high_score:
        data[high_score_key] = score
        save_data(data)

    screen.fill(BLACK)
    font = pygame.font.SysFont('Arial', 50)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()
    game_over_sound.play()
    time.sleep(4)
    return_to_menu(screen)
    pygame.quit()

def return_to_menu(screen):
    import menu
    menu.game_menu(screen)
