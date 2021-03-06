from chopsticks import act

def print_board(board):
    """Prints the board. e.g.
    A B
    3 4

    4 2
    C D
    """
    print('A B')
    print('{} {}'.format(*board[:2]))
    print()
    print('{} {}'.format(*board[2:]))
    print('C D')
    print('\n')

def isValid(state, choice):
    """Checks whether choice is valid.
    If choice is valid, return the state of the board;
    else, return False
    """
    choice = choice.upper()
    board, player = state
    hands = tuple(ord(letter)-ord('A') for letter in choice[:2])
    if hands[0]//2 != player:
        if hands[1]//2 != player:
            return False
        hands = hands[1], hands[0] # swap so that current player is first
        

    # hands are the same
    if len(set(hands))==1:
        return False

    # redistributing between own hands
    if sum(hands)==2*player and len(choice)==4: 
        a,b = map(int, choice[2:])
        if a+b != sum(hands[2*player:2*player+2]):
            return False
        if hands[0] > hands[1]:
            hands = hands[1], hands[0]
            a,b = b,a
        if (a,b) == board[2*player : 2*player+2]:
            return False # needs to change
        if a <= 0 or a >= limit:
            return False
        if b <= 0 or b >= limit:
            return False
        return board[:2*player] + (a,b) + board[2*player+2:]

    if len(choice)!=2:
        return False

    # tapping
    source,target = hands[0],hands[1]
    if board[source] == 0: # source is dead
        return False
    if board[target] == 0: # target is dead
        return False
    return board[:target] + (board[target]+board[source] if board[target]+board[source]<limit else 0) + board[target+1:]

    
board = (1, 1, 1, 1)
player = 0 # 0 for AI, 1 for human
winner = -1 # no winner yet

while winner == -1:
    print_board(board)
    if player: # human
        choice = 'rubbish'
        while not isValid((board, player), choice):
            choice = input('Enter move:')
    else:
        (board, _), _ = act((board, player), set())
    for _player in range(2):
        if not sum(hand != 0 for hand in board[2*_player : 2*_player+2]):
            winner = 1 - _player
    print(board, winner)
    player = 1-player
