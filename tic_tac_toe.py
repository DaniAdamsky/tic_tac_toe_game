import random

def create_board():
    """returns a clear board list
    with 1-9"""
    return ['1','2','3','4','5','6','7','8','9']

def print_board(board):
    """prints out each row and column, and also adds a divider between each row (except for last)"""
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("➖➕➖➕➖")

def get_move(player, board):
    """user inputs his move with a 1-9 number
    function checks whether the move is valid"""
    while True:
        player_move = input(f"Player {player}, Please enter your move: ")
        if player_move == "-999":
            print("restarting game...")
            play_game()
            break
        elif not player_move.isdigit():
            print("Please enter a valid move")
        elif int(player_move) not in range(1, 10):
            print("Please enter a valid move")
        elif board[int(player_move) - 1] in ['✖️', '⭕']:
            print("Spot is already taken, please enter a different move")
        #Easy bonus: add a restart option mid-game
        else:
            return int(player_move)


def make_move(board, position, symbol):
    """makes a move on the board for the chosen player"""
    board[int(position) - 1] = symbol


def check_winner(board, symbol):
    """returns True if a player won the game (3 in a row/column/diagonal line)"""
    combos = [
        [0,1,2] , [3,4,5] , [6,7,8] ,
        [0,3,6] , [1,4,7] , [2,5,8] ,
        [0,4,8] , [2,4,6]
    ]
    for combo in combos:
        if all(board[i] == symbol for i in combo):
            return True
    return False


def is_tie(board):
    """return true if there are no more valid moves"""
    for square in board:
        if square != '✖️' and square != '⭕':
            return False
    return True

def switch_player(current):
    """switches the current player from one to the other"""
    if current == '✖️':
        return '⭕'
    else:
        return '✖️'

#bonus function

def score_board(board, player, ties, player_x_score, player_o_score):
    if is_tie(board):
        ties += 1
    if check_winner(board, player):
        if player == '✖️':
            player_x_score += 1
        elif player == '⭕':
            player_o_score += 1
    return f"player ✖️ score is: {player_x_score}\nplayer ⭕ score is:{player_o_score}\ntotal ties are: {ties}"

def play_game():
    """plays through the game board"""
    player_x_score = 0
    player_o_score = 0
    ties = 0
    board = create_board()
    current_player = random.choice(['✖️', '⭕'])
    print(f"Welcome to Tic Tac Toe! ⭕✖️\n(to restart mid-game, input -999 as a move)\n")
    while True:
        print_board(board)
        print(f"Current player is - player {current_player}")
        make_move(board, get_move(current_player, board), current_player)
        if check_winner(board, current_player):
            print_board(board)
            print (f"player {current_player} wins!")
            break
        elif is_tie(board):
            print_board(board)
            print("Tie")
            break
        else:
            current_player = switch_player(current_player)
    result = score_board(board, current_player, ties, player_x_score, player_o_score)
    print (result)
    play_again = input("Do you want to play again? (Y/N): ")
    if play_again == 'Y':
        print("restarting game...")
        play_game()

play_game()




