from tqdm import tqdm
from itertools import *

def act(state, parents, debug=0):
    "Returns a tuple: (board, player), reward"
    board, player = state
    if board in dp:
        return dp[board]

    # Avoid cyclic recursion
    if board in parents:
        return 0 # cycling is undesirable?

    # Checks for player death (game end)
    for _player in range(2):
        if sum(board[2*_player : 2*_player+2]) == 0:
            return -50 _player == player else 50 # may change values later

    source = 2*player
    for hand in range(4):
        if hand == source:
            continue
        act = 0

    parents = set.union(parents, {board})
    playerTotal = sum(board[2*player: 2*player+2])
    dp[board] = max(chain(act(
                              (board[:target] + (board[target]+sourceValue if board[target]+sourceValue<limit else 0,) + board[target+1:], parents)
                          ) for source,sourceValue in enumerate(board[2*player: 2*player+2]) for target in range(4) if target != source,
                          act(
                              (board[:2*player] + (value, total-value) + board[2*player+2:], parents)
                          ) for value in range(1,limit) if 1<=total-value and total-value<limit
                    ),
                    key = lambda board,reward:reward)

    return ans


board = (1, 1, 1, 1)
player = 0 # 0 for AI, 1 for human
dp = {}
limit = 5

def print_board(board):
    print('A B')
    print('{} {}'.format(*board[:2]))
    print()
    print('{} {}'.format(*board[2:]))
    print('C D')
    print('\n')

def isValid(state, choice):
    choice = choice.upper()
    board, player = state
    hands = tuple(ord(letter)-order('A') for letter in choice[:2])
    if hands[0]//2 != player:
        if hands[1]//2 != player:
            return False
        hands = hands[1], hands[0]
        # swap so that current player is first

    if len(set(hands))==1: # hands are the same
        return False

    if sum(hands)==2*player and len(choice)==4: # redistributing between own hands
        a,b = map(int, choice[2:])
        if a+b != sum(hands[2*player:2*player+2]):
            return False
        if hands[0] > hands[1]:
            hands = hands[1], hands[0]
            a,b = b,a
        if a,b == board[2*player : 2*player+2]:
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
    

while not finish:
    print_board(board)
    if player: # human
        while not isValid((board, player), choice):
            choice = input('Enter move:')
    else:
        state, _ = act((board, player), set())
    player = 1-player
