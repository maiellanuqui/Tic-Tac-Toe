import socket


class BoardClass:
    '''
    attributes:
        players username
        username of the last player to have a turn
        number of wins
        number of ties
        number of losses
    '''

    def __init__(self, currentplayer: str = "", pastplayer: str = "", numwins: int = 0, numties: int = 0, numlosses: int = 0, symbol: str = '') -> None:
        """Make a BoardClass

        Args:
            currentplayer: the player that is making the move
            pastplayer: the player that made the last move
            numwins: initializes the number of wins
            numties: initializes the number of ties
            numlosses: initializes the number of losses
            symbol: initializes the player's symbol

        """
        self._currentplayer = currentplayer
        self._pastplayer = pastplayer
        self._numwins = numwins
        self._numties = numties
        self._numlosses = numlosses

        self._symbol = symbol
        self._board = [0, 1, 2,
                    3, 4, 5,
                    6, 7, 8]
        self._win_conditions = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8))
        self._gamesplayed = 0

    def setCurrentPlayer(self, currentplayer: str) -> None:
        """Set the current player of BoardClass.

        Args:
            currentplayer: current player of the BoardClass.
        """
        self._currentplayer = currentplayer


    def setPastPlayer(self, pastplayer: str) -> None:
        """Set the pass player of BoardClass.

        Args:
            pastplayer: current player of the BoardClass.
        """
        self._pastplayer = pastplayer


    def updateGamesPlayed(self):
        """Keeps track of how many games have started.

        Adds to the count of games played.
        """
        self._gamesplayed += 1


    def resetGameBoard(self):
        """Clears all the moves from game board.

        Resets the board to its original form and removes all symbols.
        """
        self._board = [0, 1, 2,
                       3, 4, 5,
                       6, 7, 8]



    def drawBoard(self):
        """Prints the board formatted tic-tac-toe board.

        Returns the formatted board.
        """
        print('|', self._board[0], '|', self._board[1], '|', self._board[2], '|')
        print('-------------')
        print('|', self._board[3], '|', self._board[4], '|', self._board[5], '|')
        print('-------------')
        print('|', self._board[6], '|', self._board[7], '|', self._board[8], '|')
        return


    def updateGameBoard(self, move:int, symbol:str):
        """Updates the game board with the player's move.

        Replaces the number on the board to the player's symbol
        Args:
            move: integer in relation to the board
            symbol: the player's designated symbol
        """
        self._board[move] = symbol


    def checkValidMove(self, move):
        """Checks if the move made by the player is an integer and if the position is free to take.

        Returns boolean expression in order to evaluate whether the move given is not a
        position that is already taken. Checks if the move is within the range 0-9 and
        is an integer.

        """
        try:
            move = int(move)
            if self._board[move] in ('X','O'):
                print('Move cannot be made, position already taken. Please enter another input.\n')
                return False
            if self._board[move] not in range(0,9):
                print('Move cannot be made, position not in range. Please enter another input.\n')
                return False
            else:
                return True
        except ValueError:
            print('Please enter a valid move (Input a number 0-8):\n')
            return False


    def isWinner(self, user_name, symbol:str):
        """Checks if the latest move resulted in a win and updates the wins and losses count.

        Returns boolean expression in order to evaluate whether positions that equate to a
        win on the board are taken to establish that the game is over or not
        Args:
            user_name: name of the user
            symbol: the player's designated symbol
        """
        for i in self._win_conditions:
            if self._board[i[0]] == self._board[i[1]] == self._board[i[2]] == symbol:
                print(f'{self._currentplayer} WINS')
                if user_name == self._currentplayer:
                    self._numwins += 1
                else:
                    self._numlosses += 1
                return True
        return False


    def boardIsFull(self):
        """Checks if the board is full and updates the ties count.

        Returns boolean expression in order to evaluate whether all positions on the
        board are taken to establish that the game is over or not
        """
        for i in self._board:
            if i not in ('X', 'O'):
                return False
        print('Game is a TIE')
        self._numties += 1
        return True


    def printStats(self):
        """Prints the stats of each player including current and past player usernames and win, loss, tie counts.

        prints the players username
        prints the username of the last person to make a move
        prints the number of games
        prints the number of wins
        prints the number of losses
        prints the number of ties
        """
        print('\nYour Stats:')
        print(f'Current players username: {self._currentplayer}')
        print(f'Past players username: {self._pastplayer}')
        print(f'Number of games: {self._gamesplayed}')
        print(f'Number of wins: {self._numwins}')
        print(f'Number of losses: {self._numlosses}')
        print(f'Number of ties: {self._numties}')

