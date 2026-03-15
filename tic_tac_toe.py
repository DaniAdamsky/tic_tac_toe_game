import random

player1 = random.choice(['✖️', '⭕'])
player2 = '✖️' if player1 == '⭕' else '⭕'


def main_menu() -> int:
    """menu choice for who to play against
    1 == against cpu
    2 == 2 player"""
    # Medium bonus: player menu
    print(f"Welcome to Tic Tac Toe! ⭕✖️\nplease choose menu option:\n\n1 -- play against cpu\n2 -- 2 players\n")
    menu_choice = input("please input menu choice: ")
    if menu_choice == "1":
        return int(menu_choice)
    elif menu_choice == "2":
        return int(menu_choice)
    elif not menu_choice.isdigit():
        print("Please enter a valid menu choice")
        return main_menu()
    else:
        print("invalid choice, please try again")
        return main_menu()


menu_choice = main_menu()


def create_board() -> list:
    """returns a clear board list
    with 1-9"""
    return [str(i + 1) for i in range(9)]


def print_board(board):
    """prints out each row and column, and also adds a divider between each row (except for last)"""
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i + 1]} | {board[i + 2]}")
        if i < 6:
            print("➖➕➖➕➖")


def get_move(current_player, board):
    """user inputs his move with a 1-9 number
    function checks whether the move is valid"""
    while True:
        if menu_choice == 1 and player2 == current_player:
            """checks if menu choice was play against cpu and also if it is the cpu's turn, if true - cpu makes the move"""
            # cpu move
            player_move = cpu_move(board)
        else:
            # player move
            player_move = input(
                f"Player {current_player}, Please enter your move:\n(to restart mid-game, input -999 as a move)\n")
        if player_move == "-999":
            # Easy bonus: add a restart option mid-game
            print("restarting game...")
            return play_game()
        elif not player_move.isdigit():
            print("Please enter a valid move")
        elif int(player_move) not in range(1, 10):
            print("Please enter a valid move")
        elif board[int(player_move) - 1] in ['✖️', '⭕']:
            print("Spot is already taken, please enter a different move")
        else:
            return int(player_move)


def make_move(board, position, symbol):
    """makes a move on the board for the current player"""
    board[position - 1] = symbol


def check_winner(board, symbol) -> bool:
    """returns True if a player won the game (3 in a row/column/diagonal line)"""
    winning_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combos:
        # check all possible combos for win
        if all(board[i] == symbol for i in combo):
            return True
    return False


def is_tie(board) -> bool:
    """check all squares and return true if there are no more valid moves"""
    for square in board:
        # checks if board is full
        if square != '✖️' and square != '⭕':
            return False
    return True


def switch_player(current) -> str:
    """switches the current player from one to the other"""
    if current == '✖️':
        return '⭕'
    else:
        return '✖️'


# bonus function
def score_board(board, player, ties, player_x_score, player_o_score) -> tuple:
    """score board indexer and announcer"""
    if is_tie(board):
        ties += 1
    if check_winner(board, player):
        if player == '✖️':
            player_x_score += 1
        elif player == '⭕':
            player_o_score += 1
    print(f"player ✖️ score is: {player_x_score}\nplayer ⭕ score is:{player_o_score}\ntotal ties are: {ties}")
    return ties, player_x_score, player_o_score


# Bonus function - computer player
def cpu_move(board) -> str:
    """Cpu player moves"""
    return str(random.randint(1, 9))


def play_game(tie_amount=0, x_score=0, o_score=0):
    """plays through the game board"""
    board = create_board()
    current_player = random.choice(['✖️', '⭕'])
    while True:
        print_board(board)
        print(f"Current player is - player {current_player}")
        make_move(board, get_move(current_player, board), current_player)
        if check_winner(board, current_player):
            print_board(board)
            print(f"player {current_player} wins!")
            break
        elif is_tie(board):
            print_board(board)
            print("Tie")
            break
        else:
            current_player = switch_player(current_player)
    tie_amount, x_score, o_score = score_board(board, current_player, tie_amount, x_score, o_score)
    play_again = input("Do you want to play again? (y/n): ")
    if play_again == 'y':
        print("restarting game...")
        play_game(tie_amount, x_score, o_score)
    else:
        print("goodbye! thanks for playing")


play_game()
