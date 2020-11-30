from itertools import *
from sys import setrecursionlimit

from tqdm import tqdm



def get_actions(state):
    board, player = state
    actions = set()

    # taps
    for source, sourceValue in enumerate(board[2*player : 2*player+2]):
        if sourceValue:
            source += 2 * player
            for target in range(4):
                if target==source or board[target]==0:
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
    return list(actions)


#setrecursionlimit(1000)
dp = {}
limit = 5
cnt = 0
def recurse(board, player, level=0):
    #print('  '*level, board, player)
    if (board, player) in dp:
        if dp[(board, player)][1] != None:
            return dp[(board, player)]
        else:  # cycle
            return dp[(board, player)][0], None
    dp[(board, player)] = 'undef state', None 

    if (0,0) == board[0:2]:
        dp[board, player] = (board, 10000-level); return dp[board, player]
    if (0,0) == board[2:4]:
        dp[board, player] = (board, 0+level); return dp[board, player]
    branches = []
    actions_ = get_actions((board, player))
    assert actions_, f'actions_ = {actions_} is empty'
    #print('  '*level, 'actions:', *actions_)
    for action in actions_:
        #print('debug DEBUG', action, 1-player, level+1)
        branches.append(recurse(action, 1-player, level+1))

    ##print('branches:', branches) 
    if player==0:
        index = min(range(len(branches)),
            key=lambda x:branches[x][1] if branches[x][1]!=None else float('inf'))
        ans = actions_[index], branches[index][1]
        if ans[1] == float('inf'): ans = 'undef state', None
        dp[(board, player)] = ans
        return ans

    if player==1:
        index = max(range(len(branches)),
            key=lambda x:branches[x][1] if branches[x][1]!=None else -float('inf'))
        ans = actions_[index], branches[index][1]
        if ans[1] == -float('inf'): ans = 'undef state', None
        dp[(board, player)] = ans
        return ans


dp = {}
state = board, player = (1,1,1,1), 1
print(board, f'player {1}')
#boards = actions(state)
states = set()
while (0,0) not in (board[0:2], board[2:4]) and (board, player) not in states:
    states.add((board, player))
    board, score = recurse(board, player)
    print(board, score, f'player {1-player}')
    player = 1-player
    #break
#print('next state:', a)



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
