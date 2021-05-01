# Author: Alyssa Comstock
# Date: 11/24/2020
# Description:  Portfolio Project.  Contains the focus / domination game.  This game is contained within
# a 6x6 board (in this case) in which players can capture or reserve pieces.  The player that gets 6
# captures first wins.


class FocusGame:
    """
    Class that defines the Focus game, which is an abstract board game
    called Focus/Domination.  Board contains
    """

    def __init__(self, play_a, play_b):
        """
        Initializes the game board with the pieces.
        Storing the board as a list of lists of lists in which when a piece is put on the location it
        will be stored in the list, and can be removed.

        The board itself is a 6x6 board.  The first row starts with 2 red pieces, followed by 2 green
        pieces followed by 2 red pieces again.  The 2nd row starts with 2 green pieces, and the colors
        continue to alternate as such.

        For example, if a Green piece were to go above the (0,0) location, then to index to it
        we would have to do self._board[0][0][1], where self._board[0][0][0] is the bottom piece and
        self._board[0][0][1] is the top of the stack.  Since lists can be displayed in reverse order easily
        if this is a problem later on then I might need to make it so that the new item is put in the first
        index and the rest of the list follows.

        As specified, (0,0) is the top left corner, and (5,5) is the bottom right corner.
        """

        self._players = {play_a[0]:play_a[1], play_b[0]:play_b[1]}    # Contains the player's information
        self._player_reserves = {play_a[0]:0, play_b[0]:0}  # Dictionary that stores the player reserves
        self._player_captures  ={play_a[0]:0, play_b[0]:0}  # Dictionary that contains player captures
        self._current_turn = play_a[0]    # Starts with the first player's name
        self._winner = None

        self._board = [
                        [
                            [play_a[1]],[play_a[1]],[play_b[1]],[play_b[1]],[play_a[1]],[play_a[1]]
                        ],
                       [
                           [play_b[1]],[play_b[1]],[play_a[1]],[play_a[1]],[play_b[1]],[play_b[1]]
                       ],
                       [
                           [play_a[1]],[play_a[1]],[play_b[1]],[play_b[1]],[play_a[1]],[play_a[1]]
                       ],
                       [
                           [play_b[1]],[play_b[1]],[play_a[1]],[play_a[1]],[play_b[1]],[play_b[1]]
                       ],
                       [
                           [play_a[1]],[play_a[1]],[play_b[1]],[play_b[1]],[play_a[1]],[play_a[1]]
                       ],
                       [
                           [play_b[1]],[play_b[1]],[play_a[1]],[play_a[1]],[play_b[1]],[play_b[1]]
                       ]
                    ]


    def get_current_turn(self):
        """
        Function that returns who's turn it is to make a move.
        :return: Player name
        """

        return self._current_turn


    def move_piece(self, player_name, start_loc, end_loc, num_pieces):
        """
        Function that moves a piece for a player that is passed in.  Has to check to see if
        it is the players turn, if the locations are valid, or if the number of pieces are
        valid and returns proper messages to inform the user.
        :param player_name: Name of the player who wishes to make the move.
        :param start_loc: Starting location of the piece to move.
        :param end_loc: Ending location of the piece to move.  Where to move it to
        :param num_pieces: Number of pieces to move.
        :return:
        """

        self.check_if_win()
        if(self._winner != None):
            print(self._winner,"won")
            return

        # Check to see if the user input a valid move.
        result = self.check_if_valid_move(player_name, start_loc, end_loc, num_pieces)

        if(result == True):

            # Move the piece
            self.make_move(start_loc, end_loc, num_pieces)
            # Passes all the checks to be a valid move.
            end_stack_size = len(self._board[end_loc[0]][end_loc[1]])

            if(end_stack_size >= 5):
                for i in range(0,end_stack_size - 5):
                    # Loop that gets the bottom pieces from the stack so that the stack still has 5 pieces.

                    self.set_reserve_or_capture(end_loc, player_name)

            # Change turn to other player
            self.swap_player_turn(player_name)

            return "successfully moved"

        else:
            # There was an error, don't move the piece, return the error.
            return result


    def check_if_win(self):
        """
        Function that checks to see if a player has 6 captures.
        :return:
        """

        for player in self._players:
            # Check both players

            if(self._player_captures[player] >= 6 ):
                self._winner = player
                return
        return


    def set_reserve_or_capture(self, loc, player_name):
        """
        Function that puts the piece from the bottom of the stack and determines if it needs
        to be added to captures or reserves and add it if so.  Then the piece if popped off the stack.
        :param loc: Location on the board of the stack
        :param player_name: Player name, to determine if it is their piece.
        :return:
        """

        if (self._board[loc[0]][loc[1]][-1] == self._players[player_name]):
            # player's piece, add to reserve.

            self._board[loc[0]][loc[1]].pop()
            self._player_reserves[player_name] += 1
            return
        else:
            # Not player's piece, add to captures.

            self._board[loc[0]][loc[1]].pop()
            self._player_captures[player_name] += 1
            return


    def swap_player_turn(self, player_name):
        """
        Function that changes the player turn to the other player's
        :param player_name: Current player
        :return:
        """

        for items in self._players:
            # For each player in the list of players

            if items != player_name:
                # if the player is not the current player then set the current turn to the player.

                self._current_turn = items


    def get_stack_size(self, location_to_get):
        """
        Function that returns the stack size for the location.
        :param location_to_get: Location of the stack to get the size of
        :return: Size of the stack.
        """

        return len(self._board[location_to_get[0]][location_to_get[1]])


    def make_move(self, start_loc, end_loc, num_pieces):
        """
        Function that moves the pieces to their location.  In this function, it will
        put the new pieces in the start of the list and append the old items to it.
        :param start_loc: Starting location, the pieces to put on top
        :param end_loc: Ending location, the pieces on the bottom.
        :return:
        """

        # Top the stack is the current control, index 0

        temp = []

        if(num_pieces == 1):
            # If we have to move 1 piece then we don't need to
            # copy the entire list

            temp.append(self._board[start_loc[0]][start_loc[1]][0])
            self._board[start_loc[0]][start_loc[1]].pop(0)
        elif(num_pieces == len(self._board[start_loc[0]][start_loc[1]])):
            # If the number of pieces to move is the same as the stack size,
            # we just copy the entire list.

            temp = self._board[start_loc[0]][start_loc[1]].copy()
            self._board[start_loc[0]][start_loc[1]] = []
        else:
            # For the number of pieces we need to move, we remove the top 1 (the first index)

            for i in range (0,num_pieces):
                temp.append(self._board[start_loc[0]][start_loc[1]][0])
                self._board[start_loc[0]][start_loc[1]].pop(0)

        for i in self._board[end_loc[0]][end_loc[1]]:
            # for each item in the stack at that location we append that to the end of temp.

            temp.append(i)

        self._board[end_loc[0]][end_loc[1]] = temp

        return


    def check_if_valid_move(self, player_name, start_loc, end_loc, num_pieces):
        """
        Function that is used with the move_piece function that returns true if the player is trying to
        make a valid move.  This function will check if it is the player's turn, if the start location is
        valid (there is a piece to move, or the move is on the board), or if the ending location is valid
        (if the move is on the board.)
        :param player_name: name of the player attempting to make the move
        :param start_loc: Location of the piece to move
        :param end_loc: Location to move the piece to
        :param num_pieces: Number of pieces to move.
        :return:
        """

        if (self._current_turn != player_name):
            # Checking to see if the player_name matches the current turn.

            return False
        elif(not self.check_if_valid_range(start_loc, end_loc, num_pieces)):
            # Check if its within the correct range or if it is on a diagonal.

            return False
        elif(not self.check_if_valid_location(start_loc) or not self.check_if_valid_location(end_loc)):
            # Getting return from check_if_valid_location function which returns true or false
            # if location is on the board.

            return False
        elif(self._board[start_loc[0]][start_loc[1]][0] != self._players[player_name]):
            # Checks the first piece on the stack to see if it is the current player's turn

            return False
        elif(len(self._board[start_loc[0]][start_loc[1]]) < num_pieces):
            # Checks to see if there are enough pieces to move.

            return False
        else:
            return True


    def check_if_valid_location(self, loc):
        """
        Function that checks if the location is on the playing board.  Returns true if so, false if not.
        :param loc: Location to check
        :return: True if it is; False if not.
        """

        if(0>loc[0]>5 or 0>loc[1]>5):
            return False
        else:
            # Location is on the 6x6 board.
            return True


    def check_if_valid_range(self, start_loc, end_loc, num_pieces):
        """
        Function that checks if the end location to move to is within the range of num_pieces.
        Also checks if its on a diagonal or not.
        :param start_loc: Starting location
        :param end_loc: Location to move to
        :param num_pieces: How many slots to move
        :return:
        """

        x_axis = end_loc[0] - start_loc[0]
        y_axis = end_loc[1] - start_loc[1]

        if(x_axis <= num_pieces and y_axis <= num_pieces):
            if((end_loc[0] == start_loc[0]) and (end_loc[1] != start_loc[1])):
                # Check if diagonal in 1 direction

                return True
            elif((end_loc[1] == start_loc[1]) and (end_loc[0] != start_loc[0])):
                # Check if diagonal in the other direction

                return True
            else:
                # Trying to place on diagonal

                return False
        else:
            # Trying to place out of range

            return False


    def show_pieces(self, pos):
        """
        Function that takes a position and returns the pieces in that position
        :param pos: Position on the board.
        :return: Pieces in that position.
        """

        if(self.check_if_valid_location(pos)):
            temp = self._board[pos[0]][pos[1]].copy()
            return temp[::-1]
        else:
            return "not a valid position"


    def show_reserve(self, player):
        """
        Function that returns the reserves for each player.
        :param player: Player name
        :return: the player's reserves
        """

        # Need to check to see if the player name is valid before returning.

        return self._player_reserves[player]


    def show_captured(self, player):
        """
        Function that returns the player's captures.
        :param player:
        :return: 0 if they don't have any reserves, or the number of reserves they have.
        """

        # Need to check if the player name is valid before returning.

        return self._player_captures[player]


    def reserved_move(self, player, location):
        """
        Function that takes the player name and location and places a piece in that location
        only if the user has pieces in reserve.  Otherwise will display an error message.
        :param player: Player name to take from the reserve of.
        :param location: Location to place the reserved piece
        :return:
        """

        if(self._player_reserves[player] >= 1):
            self._player_reserves[player] -= 1
            temp = []
            temp.append(self._players[player])
            for item in self._board[location[0]][location[1]]:
                temp.append(item)

            # Move piece
            self._board[location[0]][location[1]] = temp

            # Check if stack is > 5
            self.set_reserve_or_capture(location, player)

            # Change turn to other player
            self.swap_player_turn(player)

        else:
            return False


def main():
    game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
    game.move_piece('PlayerA', (0, 1), (0, 2), 1)  # Returns message "successfully moved"
    print('\n')
    print(game.show_pieces((0, 2)))  # Returns ['R','R']
    game.show_captured('PlayerA')  # Returns 0
    game.reserved_move('PlayerA', (0, 0))  # Returns message "No pieces in reserve"
    game.show_reserve('PlayerA')  # Returns 0


if __name__ == '__main__':
    main()


