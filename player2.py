import socket
from gameboard import BoardClass


def make_connection():
    """Requests host info and establishes a socket connection.

    Asks user for the host and port they would like to bind to
    Returns the socket that is established

    """
    host = str(input('What host name do you want to use?:\n'))
    port = int(input('What port do you want to use?:\n'))
    print(f'Host name: {host}, Port: {port}')
    player2socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player2socket.bind((host, port))
    player2socket.listen(1)
    return player2socket


def run_server():
    """Reads and sends messages to and from the client in order to run the game.

    Includes make_connection function in order to define socket

    """
    player2socket = (make_connection())
    recv_size = 1024
    conn, addr = player2socket.accept()
    player2_user_name = 'player2'
    input_from_client = conn.recv(recv_size).decode()
    print(f'Player 1\'s username: {input_from_client}')
    conn.send(player2_user_name.encode())
    print(f'Waiting for {input_from_client}\'s move...')
    player2board = BoardClass(symbol='O')
    socketclose = False
    while socketclose is False:
        gameover = False
        while gameover is False:
            player2board.setCurrentPlayer(input_from_client)
            player1_move = conn.recv(recv_size).decode()
            player1_move = int(player1_move)
            player2board.updateGameBoard(player1_move, 'X')
            print(f'{input_from_client}\'s move:')
            player2board.drawBoard()
            gameover = player2board.isWinner('player2', 'X')
            if gameover is True:
                break
            gameover = player2board.boardIsFull()
            if gameover is True:
                break
            validmove = False
            while validmove is False:
                player2board.setCurrentPlayer('player2')
                player2_move = input('What move would you like to make? (Please input a number 0-8):\n')
                validmove = player2board.checkValidMove(player2_move)
            player2_move = int(player2_move)
            player2board.updateGameBoard(player2_move, 'O')
            player2board.drawBoard()
            player2_move = str(player2_move)
            conn.send(player2_move.encode())
            gameover = player2board.isWinner('player2', 'O')
            if gameover is True:
                break
            gameover = player2board.boardIsFull()
            if gameover is True:
                break
            player2board.setPastPlayer('player2')
            print(f'Waiting for {input_from_client}\'s move...')
        player2board.updateGamesPlayed()
        playagain_input = conn.recv(recv_size).decode()
        print(playagain_input)
        if playagain_input == 'Play Again':
            print(f'Waiting for {input_from_client}\'s move...')
            player2board.resetGameBoard()
            socketclose = False
        if playagain_input == 'Fun Times':
            player2board.printStats()
            socketclose = True
    conn.close()


if __name__ == "__main__":
    run_server()
