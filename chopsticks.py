from tqdm import tqdm
from itertools import *

dp = {}
limit = 5
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
            return ()-50 if _player == player else 50 # may change values later

    source = 2*player
    for hand in range(4):
        if hand == source:
            continue
        #act = 0

    parents = set.union(parents, {board})
    playerTotal = sum(board[2*player: 2*player+2])
    dp[board] = max(chain((act(
                              (board[:target] + (board[target]+sourceValue if board[target]+sourceValue<limit else 0,) + board[target+1:], 1-player), parents
                          ) for source,sourceValue in enumerate(board[2*player: 2*player+2]) for target in range(4) if target != source),
                          (act(
                              (board[:2*player] + (value, total-value) + board[2*player+2:], 1-player), parents
                          ) for value in range(1,limit) if 1<=total-value and total-value<limit)
                    ),
                    key = lambda tpl:tpl[1]) # action that returns max reward

    return dp[board]

