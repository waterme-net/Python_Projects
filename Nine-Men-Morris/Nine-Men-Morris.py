import sys
import NMM  # This is necessary for the project

BANNER = """
    __      _(_)_ __  _ __   ___ _ __| | |
    \ \ /\ / / | '_ \| '_ \ / _ \ '__| | |
     \ V  V /| | | | | | | |  __/ |  |_|_|
      \_/\_/ |_|_| |_|_| |_|\___|_|  (_|_)
"""

RULES = """                                                                                       
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    The game is ends when a player (the loser) has less than three 
    pieces on the board.
"""

MENU = """
    Game commands (first character is a letter, second is a digit):
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game

"""


# Uncomment the following lines when you are ready to do input/output tests!
# Make sure to uncomment when submitting to Codio.
def input(prompt=None):
    if prompt != None:
        print(prompt, end="")
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip("\n")
    print(aaa_str)
    return aaa_str


def count_mills(board, player):
    """
    Arguments: board, player
    makes an variable count that has a value of zero
    loops through the mill list
      checks if all the points are occupied by the player
        if they are occupied then it will increase the count by one

    returns: count
    """
    count = 0
    for mill in board.MILLS:                                          #iterates through the list of mills
        if all([board.points[point] == player for point in mill]):
            count += 1
    return count


def place_piece_and_remove_opponents(board, player, destination):
    """
    Arguments: board, player, destination
    checks if the destination is not in board
        if it is not then it will give a run time error and prompt an error message
    checks if the point player wants to move is empty or not
        if it is not then it will give a run time error and prompt an error message

    makes a variable that is the number of mills
    allows the player to place a piece
    checks if the count of mills has increased since before
        if it has then it will prompt a message
        it will print the board
        and remove a piece of the opponent

    """
    # Check if the destination is valid
    if destination not in board.points:                                             #checks if the destination is on the board on not
        raise RuntimeError("Invalid command: Not a valid point")
    if board.points[destination] != " ":                                            #checks if the destination is open or not
        raise RuntimeError("Invalid command: Destination point already taken")

    # Check the number of mills before placing a piece
    prev_mill_count = count_mills(board, player)

    board.assign_piece(player, destination)
    # If we made a mill, remove a piece
    if count_mills(board, player) > prev_mill_count:                                #checks if the number of mills created has increased or not
        print("A mill was formed!")
        print(board)
        remove_piece(board, get_other_player(player))


def move_piece(board, player, origin, destination):
    """
    Arguments: board, player, origin, destination
    checks if the entered place is on board or not while also checking if the place to move is on the board or not
        it will raise a run time error and show an error message
    checks if the point belongs to the player or not
        if it doesnt then it will raise a run time error along with an error message
    checks if the point is empty or not
        if it is not then it will raise a run time error along with an error message
    checks if the point to move is adjacent to the initial point
        if it is not then it will raise a run time error along with an error message
    """
    if origin not in board.points or destination not in board.points:                   #checks for points on board
        raise RuntimeError("Invalid command: Not a valid point")
    if board.points[origin] != player:                                                  #checks if the point is the players or not
        raise RuntimeError("Invalid command: Origin point does not belong to player")
    if board.points[destination] != " ":                                                #checks if the point is empty
        raise RuntimeError("Invalid command: Destination point already taken")
    if destination not in board.ADJACENCY[origin] and len(placed(board, player)) > 3:   #checks if the destination point is adjacent to the initial point or not
        raise RuntimeError("Invalid command: Destination not adjacent")
    board.clear_place(origin)
    place_piece_and_remove_opponents(board, player, destination)


def points_not_in_mills(board, player):
    """
    Arguments: board, player
    makes a variable that is the number of points place by the player
    makes an empty set
    runs a loop through the entire placed_point variable
        makes a variable and flags it to false
            runs a loop through the list of mills
                checks if points belong to the list of mills
                    if they do then changes the flag of the variable to True
                    breaks the loop
            if the varible is still false
                it will add the point to the set
    Returns a set of points not in mills for a player
    """
    placed_points = placed(board, player)
    points = set()                                                                      #empty set
    for point in placed_points:                                                         #iterates through the points placed by the player
        in_mill = False
        for mill in board.MILLS:                                                        #iterates through the list of mills
            if all([board.points[np] == player for np in mill]) and point in mill:      #checks if the point is in the list of mills or not
                in_mill = True
                break
        if not in_mill:                                                                 #if the variable is still flagged as false then it will add the point to the empty set
            points.add(point)
    return list(points)


def placed(board, player):
    """
    Arguments: board, player
    runs a loop through the board points list
        checks of the point is the player
            if it is then it will add it to the list
    Returns a list of points that a player has placed pieces on
    """
    return [point for point in board.points if board.points[point] == player]


def remove_piece(board, player):
    """
    Arguments: board, player
    makes a variable that will the points that are not in a mill
    makes a varible that will be the points placed in the mill
    makes a while loop
        tries
            asks for input to remove a piece
            checks if the point is on the board
                if it is not then it will give a run time error along with an error message
            checks if the point belongs to the player or not
                if it does not then it will raise a run time error and will print an error message
            checks if the zero points are in mill
                it will then clear the point
                breaks the loops
            checks if the point is not in a mill
                it will then clear the point
                breaks the loops
            else
                it will raise a run time error and prompt an error message

        except
            prints error message along with try again

    """
    not_in_mill = points_not_in_mills(board, player)
    placed_points = placed(board, player)
    while True:
        try:
            point = input("Remove a piece at :> ").strip().lower()
            if point not in board.points:                                                   #checks if the point is on board on not
                raise RuntimeError("Invalid command: Not a valid point")
            elif point not in placed_points:                                                #checks if the point belongs to the player
                raise RuntimeError("Invalid command: Point does not belong to player")

            if len(not_in_mill) == 0:                                                       #checks if the number of points not in mill are zero
                board.clear_place(point)
                break
            if point in not_in_mill:                                                        #checks if the point is not in a mill
                board.clear_place(point)
                break
            else:
                raise RuntimeError("Invalid command: Point is in a mill")

        except RuntimeError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))


def is_winner(board, player):
    """
    Arguments: board, player
    Check if a player has won the game
    """
    return len(placed(board, get_other_player(player))) < 3


def get_other_player(player):
    """
    Get the other player.
    """
    return "X" if player == "O" else "O"




def main():
    """
    starts a loop
        prints the rules
        prints the menu
        prints board
        makes a variable and flags it to false
        makes a variable player and makes it as X
        makes an variable initiaziled to zero
        prints the player turn
        asks for an input to where to put the piece
        prints an empty lines
        starts a loop for when the players do not want to quit or when the placed pieces are less than 18
            tries
                if the command is h
                    it prints the menu
                if the command is r
                    it will break
                else
                    it will place the piece
                    switch to the other player
                    increase the placed piece count by one

            except
                prints an error message

            checks if the command is not h
                if it is then it will print the board
                it will say the other players turn
            checks if the pieces played are less than 18
                if they are less than 18 then it will place a piece
            else
                it will print the phase 2
                makes a variable that asks for input to move the pieces

        starts another loop for when the command is not q
            tries
                if the length of command is not two
                    it will raise a run time error and prompt an error message
                moves a piece

            except
                prints and error message

            prints the board
            prints the other players turn
            takes input for a variable for player to move a piece

        if the winner flag is true:
            prints the banner

        it the command is q
            prints an empty line
    """
    # Loop so that we can start over on reset
    while True:
        # Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        winner  =False
        player = "X"
        placed_count = 0  # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent

        # PHASE 1
        print(player + "'s turn!")
        # placed = 0
        command = input("Place a piece at :> ").strip().lower()
        print()
        # Until someone quits or we place all 18 pieces...
        while command != 'q' and placed_count != 18:
            try:
                if command == 'h':
                    #print()
                    print(MENU)

                elif command == 'r':
                    #print()
                    break
                else:
                    place_piece_and_remove_opponents(board, player, command)
                    player = get_other_player(player)
                    placed_count += 1

            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))

            # Prompt again
            if command != 'h':
                print(board)
                print(player + "'s turn!")
            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()
            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        # Go back to top if reset
        if command == 'r':
            continue
        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            command = command.split()
            # print(command) # DEBUG LINE
            try:
                if len(command) != 2:
                    raise RuntimeError("Invalid number of points")
                move_piece(board, player, command[0], command[1])
                if is_winner(board, player):
                    winner = True
                    break

                player = get_other_player(player)

            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
                # Display and reprompt
            print(board)
            # display_board(board)
            print(player + "'s turn!")
            command = input("Move a piece (source,destination) :> ").strip().lower()
            print()

        if winner:
            print(BANNER)
            return

        # If we ever quit we need to return
        if command == 'q':
            print()
            return


if __name__ == "__main__":
    main()

