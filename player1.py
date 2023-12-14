import socket
from gameboard import BoardClass


def get_user_input():
    """Receives users intended username.

    Asks user to enter their intended username
    Checks if username is alphanumeric and raises Value Error if not.
    """
    player1_user_name = input('Please enter an alphanumeric username:\n')
    if player1_user_name.isalnum():
        return player1_user_name
    else:
        raise ValueError


def get_valid_input():
    """Asks user if they want to try to make a valid connection and checks if the users input is a valid response.

    Keeps asking user for an input until they enter a valid response
    If they enter 'n' or 'N' for no, it exits the program
    If they enter 'y' or 'Y' for yes, the program continues
    """
    valid_input = False
    while valid_input is False:
        tryagain_input = str(input('Connection could not be made. Would you like to try again? (y or n):\n'))

        if tryagain_input not in ('y', 'Y', 'n', 'N'):
            print('Error: Please enter a valid input (y or n):')
            valid_input = False
            continue

        elif tryagain_input in ('n', 'N'):
            quit()

        elif tryagain_input in ('y', 'Y'):
            valid_input = True
            continue


def make_connection():
    """Requests host info of server to create a connection.

    Asks user for the intended host and port they would like to connect to
    Returns the socket that is established

    """
    connected = False
    while connected is False:
        try:
            host = str(input('What is the host name of player 2?:\n'))
            port = int(input('What is the port of player 2?:\n'))
            print(f'Establishing Connection to server (Host name: {host}, Port: {port})')
            player1socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            player1socket.connect((host, port))
            connected = True
        except Exception:
            get_valid_input()
    return player1socket


def username_exchange():
    """Sends the user's username to server.

    Checks whether the username is valid and raises a Value Error if it is not.
    Returns the user's username
    """
    validname = False
    while not validname:
        try:
            player1_user_name = get_user_input()
            validname = True
        except ValueError:
            print('Error: Please enter a valid alphanumeric user name')
            continue
    return player1_user_name


def run_client():
    """Reads and sends messages to and from the client in order to run the game.

    Includes make_connection() function in order to define socket
    Takes in return value from get_user_input() to initialize player 1's username
    Uses username_exchange to send user's username to server
    BoardClass is used to initialize the current player and past player
    BoardClass is used to update and reset board
    """
    player1socket = make_connection()
    recv_size = 1024
    player1_user_name = username_exchange()
    player1socket.send(player1_user_name.encode())  # use .encode() when sending data
    result_from_server = player1socket.recv(recv_size).decode()  # use .decode() when recieving data
    print(f'Player 2\'s username: {result_from_server}')

    player1board = BoardClass(symbol='X')
    socketclose = False
    player1board.drawBoard()
    while socketclose is False:
        gameover = False
        while gameover is False:
            validmove = False
            while validmove is False:
                player1board.setCurrentPlayer(player1_user_name)
                player1_move = input('What move would you like to make? (Please input a number 0-8):\n')
                validmove = player1board.checkValidMove(player1_move)
            player1_move = int(player1_move)
            player1board.updateGameBoard(player1_move, 'X')
            player1board.drawBoard()
            player1_move = str(player1_move)
            player1socket.send(player1_move.encode())
            gameover = player1board.isWinner(player1_user_name, 'X')
            if gameover is True:
                break
            gameover = player1board.boardIsFull()
            if gameover is True:
                break
            player1board.setPastPlayer(player1_user_name)
            print(f'Waiting for player2\'s move...')
            player1board.setCurrentPlayer('player2')
            player2_move = player1socket.recv(recv_size).decode()
            player2_move = int(player2_move)
            player1board.updateGameBoard(player2_move, 'O')
            print(f'player2\'s move:')
            player1board.drawBoard()
            gameover = player1board.isWinner(player1_user_name, 'O')
            if gameover is True:
                break
            gameover = player1board.boardIsFull()
            if gameover is True:
                break
            player1board.setPastPlayer('player2')
        player1board.updateGamesPlayed()
        playagain_input = input('Would you like to play again? (y or n):\n')
        if playagain_input in ('Y', 'y'):
            player1board.resetGameBoard()
            player1socket.send('Play Again'.encode())
            player1board.drawBoard()
            socketclose = False
        elif playagain_input in ('N', 'n'):
            player1socket.send('Fun Times'.encode())
            player1board.printStats()
            socketclose = True
    player1socket.close()


if __name__ == "__main__":
    run_client()
