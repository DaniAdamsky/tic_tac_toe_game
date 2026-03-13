import pygame
import random
import sys

# -------------------- COLORS & SETTINGS --------------------
WIDTH, HEIGHT = 600, 800
BG_COLOR = (15, 15, 25)
LINE_COLOR = (60, 60, 90)
X_COLOR = (255, 80, 80)
O_COLOR = (80, 180, 255)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (40, 40, 60)
BUTTON_HOVER = (60, 60, 90)
WIN_LINE_COLOR = (255, 215, 0)
RESTART_COLOR = (255, 140, 0)
RESTART_HOVER = (255, 180, 60)

CELL_SIZE = WIDTH // 3
FONT_SIZE = 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font_large = pygame.font.SysFont("segoeui", FONT_SIZE, bold=True)
font_medium = pygame.font.SysFont("segoeui", 36, bold=True)
font_small = pygame.font.SysFont("segoeui", 24)
font_tiny = pygame.font.SysFont("segoeui", 18)

# -------------------- ORIGINAL TERMINAL --------------------

def create_board():
    return [str(i + 1) for i in range(9)]

def make_move(board, position, symbol):
    board[int(position) - 1] = symbol

def check_winner(board, symbol):
    combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in combos:
        if all(board[i] == symbol for i in combo):
            return combo
    return None

def is_tie(board):
    for square in board:
        if square != 'X' and square != 'O':
            return False
    return True

def switch_player(current):
    if current == 'X':
        return 'O'
    else:
        return 'X'

def cpu_move(board):
    available = [square for square in board if square not in ['X', 'O']]
    return random.choice(available)

def score_board(current_player, is_tie_result, ties, x_score, o_score):
    if is_tie_result:
        ties += 1
    elif current_player == 'X':
        x_score += 1
    elif current_player == 'O':
        o_score += 1
    return ties, x_score, o_score

# -------------------- DRAW FUNCTIONS --------------------

def draw_board(board, winning_combo=None):
    screen.fill(BG_COLOR)

    # draw grid lines
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), 4)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 4)

    # draw X and O
    for i, cell in enumerate(board):
        row = i // 3
        col = i % 3
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2

        if cell == 'X':
            color = X_COLOR if not winning_combo or i not in winning_combo else WIN_LINE_COLOR
            text = font_large.render("X", True, color)
            screen.blit(text, text.get_rect(center=(cx, cy)))
        elif cell == 'O':
            color = O_COLOR if not winning_combo or i not in winning_combo else WIN_LINE_COLOR
            text = font_large.render("O", True, color)
            screen.blit(text, text.get_rect(center=(cx, cy)))

def draw_status(message, color=TEXT_COLOR):
    pygame.draw.rect(screen, (25, 25, 40), (0, WIDTH, WIDTH, 55))
    text = font_medium.render(message, True, color)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, WIDTH + 27)))

def draw_scores(x_score, o_score, ties):
    pygame.draw.rect(screen, (20, 20, 35), (0, WIDTH + 55, WIDTH, 30))
    score_text = f"X: {x_score}   O: {o_score}   Ties: {ties}"
    text = font_small.render(score_text, True, (150, 150, 180))
    screen.blit(text, text.get_rect(center=(WIDTH // 2, WIDTH + 70)))

def draw_button(label, rect, hovered, override_color=None, override_hover=None):
    bc = override_color if override_color else BUTTON_COLOR
    bh = override_hover if override_hover else BUTTON_HOVER
    color = bh if hovered else bc
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, LINE_COLOR, rect, 2, border_radius=8)
    text = font_small.render(label, True, TEXT_COLOR)
    screen.blit(text, text.get_rect(center=rect.center))

def draw_restart_hint():
    """shows the mid-game restart hint"""
    pygame.draw.rect(screen, (20, 20, 35), (0, WIDTH + 85, WIDTH, 25))
    hint = font_tiny.render("Press  [R]  to restart mid-game", True, (100, 100, 130))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, WIDTH + 97)))

def draw_menu(hovered):
    screen.fill(BG_COLOR)

    title = font_large.render("TIC TAC TOE", True, TEXT_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

    subtitle = font_small.render("Choose game mode", True, (120, 120, 150))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 260)))

    btn1 = pygame.Rect(WIDTH // 2 - 150, 310, 300, 60)
    btn2 = pygame.Rect(WIDTH // 2 - 150, 400, 300, 60)

    draw_button("vs CPU", btn1, hovered == 1)
    draw_button("2 Players", btn2, hovered == 2)

    return btn1, btn2

# -------------------- GAME STATE --------------------

def run_game(menu_choice, x_score=0, o_score=0, ties=0):
    board = create_board()

    # mirrors original: randomly assign which player goes first
    current_player = random.choice(['X', 'O'])
    winning_combo = None
    game_over = False
    status = f"Player {current_player}'s turn"

    # buttons shown after game ends
    rematch_btn = pygame.Rect(WIDTH // 2 - 160, WIDTH + 110, 150, 45)
    menu_btn = pygame.Rect(WIDTH // 2 + 10, WIDTH + 110, 150, 45)

    clock = pygame.time.Clock()

    while True:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # mid-game restart: mirrors terminal's -999 input
                if event.key == pygame.K_r and not game_over:
                    print("restarting game...")
                    return run_game(menu_choice, x_score, o_score, ties)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # rematch: same as "Y" in terminal play_again
                    if rematch_btn.collidepoint(mx, my):
                        print("restarting game...")
                        return run_game(menu_choice, x_score, o_score, ties)
                    # back to menu
                    if menu_btn.collidepoint(mx, my):
                        return main_menu_screen(x_score, o_score, ties)
                else:
                    # handle click on board
                    if my < WIDTH:
                        col = mx // CELL_SIZE
                        row = my // CELL_SIZE
                        position = row * 3 + col + 1
                        if board[position - 1] not in ['X', 'O']:
                            # 2 player: both click | vs CPU: only X clicks
                            if menu_choice == 2 or current_player == 'X':
                                make_move(board, position, current_player)
                                winning_combo = check_winner(board, current_player)
                                if winning_combo:
                                    ties, x_score, o_score = score_board(current_player, False, ties, x_score, o_score)
                                    status = f"Player {current_player} wins! 🎉"
                                    game_over = True
                                elif is_tie(board):
                                    ties, x_score, o_score = score_board(current_player, True, ties, x_score, o_score)
                                    status = "It's a tie!"
                                    game_over = True
                                else:
                                    current_player = switch_player(current_player)
                                    status = f"Player {current_player}'s turn"

        # CPU move (mirrors original: CPU plays as O in vs CPU mode)
        if not game_over and menu_choice == 1 and current_player == 'O':
            pygame.time.wait(400)
            move = cpu_move(board)
            make_move(board, move, 'O')
            winning_combo = check_winner(board, 'O')
            if winning_combo:
                ties, x_score, o_score = score_board('O', False, ties, x_score, o_score)
                status = "CPU wins! 🤖"
                game_over = True
            elif is_tie(board):
                ties, x_score, o_score = score_board('O', True, ties, x_score, o_score)
                status = "It's a tie!"
                game_over = True
            else:
                current_player = switch_player(current_player)
                status = f"Player {current_player}'s turn"

        # draw everything
        draw_board(board, winning_combo)
        draw_status(status)
        draw_scores(x_score, o_score, ties)

        if game_over:
            draw_button("Rematch", rematch_btn, rematch_btn.collidepoint(mx, my))
            draw_button("Main Menu", menu_btn, menu_btn.collidepoint(mx, my))
        else:
            draw_restart_hint()

        pygame.display.flip()
        clock.tick(60)


def main_menu_screen(x_score=0, o_score=0, ties=0):
    clock = pygame.time.Clock()
    while True:
        mx, my = pygame.mouse.get_pos()
        hovered = 0

        if True:
            btn1, btn2 = draw_menu(hovered)
            if btn1.collidepoint(mx, my):
                hovered = 1
            elif btn2.collidepoint(mx, my):
                hovered = 2
            btn1, btn2 = draw_menu(hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.collidepoint(mx, my):
                    return run_game(1, x_score, o_score, ties)
                if btn2.collidepoint(mx, my):
                    return run_game(2, x_score, o_score, ties)

        pygame.display.flip()
        clock.tick(60)


main_menu_screen()