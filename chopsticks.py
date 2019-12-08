from itertools import *
from sys import setrecursionlimit

from tqdm import tqdm

setrecursionlimit(2000)
dp = {}
limit = 5
cnt = 0


def get_actions(state):
    board, player = state
    actions = set()

    # taps
    for source, sourceValue in enumerate(board[2*player : 2*player+2]):
        source += 2 * player
        for target in range(4):
            if target == source:
                continue
            actions.add(board[:target]
                        + (board[target] + sourceValue
                           if board[target] + sourceValue < limit else 0,)
                        + board[target+1: ])

    if cnt==1: print('taps: ', actions)
    # redistributions
    total = sum(board[2*player : 2*player+2])
    for value in range(1, limit):
        if 1 <= total-value and total-value < limit \
            and value not in board[2*player : 2*player+2]: 
            actions.add(board[: 2*player]
                        + (value, total-value)
                        + board[2*player+2: ])
    if cnt==1: print('all actions:', actions)
    return actions
    

def act(state, parents, debug=0):
    """Returns a tuple: (board, player), reward"""
    global cnt; cnt+=1
    board, player = state
    if board in dp:
        return dp[board]

    # Avoid cyclic recursion
    if board in parents:
        return (board, 1-player), 0

    # Checks for player death (game end)
    for _player in range(2):
        if sum(board[2*_player : 2*_player+2]) == 0:
            # May change values later
            return (board, 1-player), (-50 if _player == player else 50)

    actions = get_actions(state)
    if cnt==1: print(actions)
    parents = set.union(parents, {board})
    playerTotal = sum(board[2*player : 2*player+2])
    action = max(range(len(actions)),
                 key=lambda action: -act((action, 1-player), parents)[1])
    dp[board] = action

    return action
