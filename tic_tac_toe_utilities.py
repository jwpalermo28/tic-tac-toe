from random import randint
from operator import attrgetter
from copy import deepcopy

# miscellaneous utility functions ----------------------------------------------

# return an empty 3x3 grid, represented by a list of lists with only None values
def init_state():
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]

# pretty-print the state
def print_state(state):
    print
    for i in range(0, 3):
        row_string = str(state[i][0]) + ' | ' + str(state[i][1]) + ' | ' + \
                     str(state[i][2])
        print row_string.replace('None', ' ')

# if turn_of is 'player_1' return 'player_2', and vice versa
def switch_player(turn_of):
    if turn_of == 'player_1':
        return 'player_2'
    else:
        return 'player_1'

# return True if at least one human is set to play
def is_human_playing(player_type):
    return 'human' in player_type.values()

# update the game play record based on the final state of a game
def update_record(final_state, record):
    winner = get_winner(final_state)
    if winner == 'player_1':
        record[0] += 1
    elif winner == 'player_2':
        record[1] += 1
    else:
        record[2] += 1

def print_record(record):
    print
    print "player 1 won " + str(record[0]) + " games"
    print "player 2 won " + str(record[1]) + " games"
    print str(record[2]) + " games were tied"

# given the current state, whose turn it is, and the move taken from the current
# state, return the resulting state
def get_successor_state(state, turn_of, move):
    state = deepcopy(state)
    (x,y) = move
    if turn_of == 'player_1':
        state[x][y] = 'x'
    else:
        state[x][y] = 'o'
    return state

# utility functions to check end-game conditions -------------------------------

# check if any game-ending conditions are satisfied
# the game ends if:
#   - there is a row, column, or diagonal containing 3 of only 1 kind of symbol
#    (i.e. a player has won)
#   - or, symbols have been placed in all 9 positions (i.e. tie game)
def terminal_test(state, printResult=False):
    is_terminal_state = False
    winner = get_winner(state)
    if winner or is_full_state(state):
        is_terminal_state = True
    if is_terminal_state and printResult:
        if winner == 'player_1':
            print '\n' + 'Player 1 is the winner!'
        elif winner == 'player_2':
            print '\n' + 'Player 2 is the winner!'
        else:
            print '\n' + 'The game was a tie.'
    return is_terminal_state

# get the utility of the current state, for the current player
# by convention let player_1 be a maximizer and player_2 be a minimizer
def utility(state, turn_of):
    winner = get_winner(state)
    if winner:
        if winner == 'player_1':
            return 1
        else:
            return -1
    else:
        return 0

# if a player_1 has won the game, return player_1
# if player_2 has won the game, return player_2
# else return None
def get_winner(state):
    winners_symbol = None
    # check the rows
    for i in range(0, len(state)):
        if check_squares_for_win(state[i][0], state[i][1], state[i][2]):
            winners_symbol = state[i][0]
    # check the columns
    for i in range(0, len(state)):
        if check_squares_for_win(state[0][i], state[1][i], state[2][i]):
            winners_symbol = state[0][i]
    # check the diagonals
    # top-left to bottom-right
    if check_squares_for_win(state[0][0], state[1][1], state[2][2]):
        winners_symbol = state[0][0]
    # top-right to bottom-left
    if check_squares_for_win(state[0][2], state[1][1], state[2][0]):
        winners_symbol = state[0][2]
    # if a winner has been found, return the winner's name
    if winners_symbol == 'x':
        return 'player_1'
    elif winners_symbol == 'o':
        return 'player_2'
    else:
        return None

# check to see if a sequence of squares have the same symbol
def check_squares_for_win(x, y, z):
    # make sure at least one value isn't None, and that all values are equal
    if x and x == y and y == z:
        return True
    return False

# check if the state is full with symbols
def is_full_state(state):
    for row in state:
        for square in row:
            if not square:
                return False
    return True

# utility functions to get player moves ----------------------------------------

# get a player's next move as a tuple of integer values
def get_move(turn_of, player_type, state):
    move = None
    # loop until a valid move is selected (i.e. until move is not None)
    if player_type[turn_of] == 'human':
        while not move:
            raw_move_input = raw_input('\n' + turn_of + ', enter your move:')
            move = parse_raw_move_input(raw_move_input)
            if move and not valid_move(move, state):
                move = None
    elif player_type[turn_of] == 'random_ai':
        move = get_random_move(state)
    elif player_type[turn_of] == 'optimal_ai':
        move = get_optimal_move(state, turn_of)
    return move

# if raw_move_input represents a valid move, then return a parsed representation
# of it as a tuple of integer values; otherwise, return None
def parse_raw_move_input(raw_move_input):
    move = None
    # check that a comma was supplied to separate values
    if ',' in raw_move_input:
        raw_move_components = raw_move_input.split(',')
        # check that the raw input can be converted into a pair of integers
        if raw_move_components[0].isdigit() and \
           raw_move_components[1].isdigit():
            # convert the components to integers
            move_components = [int(raw_move_components[0]),
                               int(raw_move_components[1])]
            # check that the integer inputs are bounded by 0 and 2
            if (0 <= move_components[0] and move_components[0] <= 2) and \
               (0 <= move_components[1] and move_components[1] <= 2):
               move = (move_components[0], move_components[1])
            else:
                print '\n' + 'Invalid input. The components are not in range'
        else:
            print '\n' + 'Invalid input. Remember to supply 2 integer values'
    else:
        print '\n' + 'Invalid input. Remember to separate values by a comma'
    return move

# validate a move against the current state
def valid_move(move, state):
    (x, y) = move
    is_valid_move = not state[x][y]
    if not is_valid_move:
        print "Invalid input. You can only place a symbol on an empty square"
    return is_valid_move

# get a list of valid moves
def get_valid_moves(state):
    all_positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    return [(x,y) for (x,y) in all_positions if not state[x][y]]

# get a random valid move
def get_random_move(state):
    valid_moves = get_valid_moves(state)
    move_index = randint(0,len(valid_moves)-1)
    return valid_moves[move_index]

# generate the rest of the game tree from the current state
def get_optimal_move(state, turn_of):
    game_node = GameNode(state, turn_of)
    game_node.generate_game_tree()
    return game_node.optimal_move

# A class whose objects represent nodes in a game tree
class GameNode:

    def __init__(self, state, turn_of, move_from_parent=None):
        self.state = state
        self.turn_of = turn_of
        self.move_from_parent = move_from_parent
        # set starting utility to a value that would never be chosen if there
        # was any other alternative
        if self.turn_of == 'player_1':
            self.utility = float("inf")
        else:
            self.utility = - float("inf")
        self.successors = None
        self.optimal_move = None

    def print_properties(self):
        print_state(self.state)
        print "\n turn of:" + self.turn_of
        print "\n move from parent: " + str(self.move_from_parent)
        print "\n utility:" + str(self.utility)
        print "\n optimal_move:" + str(self.optimal_move)

    # generate the rest of the game tree by depth-first search
    def generate_game_tree(self, alpha = -float("inf"), beta = float("inf")):
        self.alpha = alpha
        self.beta = beta
        if terminal_test(self.state):
            self.utility = utility(self.state, self.turn_of)
            # inform the parent node if it should kill its successor search
            return self.kill_test()
        else:
            self.successors = self.generate_successors()
            for succ in self.successors:
                kill = succ.generate_game_tree(alpha, beta)
                if kill:
                    # the parent of a node killing its successor search will
                    # never also have to kill its successor search
                    assert not self.kill_test()
                    return False
                # if necessary update alpha and beta for successors
                if self.turn_of == 'player_1' and succ.utility > alpha:
                    alpha = succ.utility
                elif self.turn_of == 'player_2' and succ.utility < beta:
                    beta = succ.utility
            # at this point all successor nodes have utility values
            if self.turn_of == 'player_1':
                minimax_node = max(self.successors, key = attrgetter('utility'))
            elif self.turn_of == 'player_2':
                minimax_node = min(self.successors, key = attrgetter('utility'))
            self.utility = minimax_node.utility
            self.optimal_move = minimax_node.move_from_parent
            # inform the parent node if it should kill its successor search
            return self.kill_test()

    # generate all successors of the current node
    def generate_successors(self):
        successors = []
        moves = get_valid_moves(self.state)
        for move in moves:
            successor_state = get_successor_state(self.state, self.turn_of, move)
            node = GameNode(successor_state, switch_player(self.turn_of), move)
            successors.append(node)
        return successors

    # test whether the parent node should kill its search through successors
    def kill_test(self):
        return (self.turn_of == 'player_1' and self.utility <= self.alpha) or \
               (self.turn_of == 'player_2' and self.utility >= self.beta)
