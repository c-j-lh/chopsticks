from tqdm import tqdm

class Node:
    def __init__(self, state, player, pbar=None):
        """State should be a tuple of 2x2=4 ints
        Player 0 and player 1
        """
        self.state = state
        self.player = player
        if pbar is None:
            pbar = tqdm(unit='function call')
        self.pbar = pbar

    def get_actions(self):
        "Returns a list of next nodes"
        return [Node(self.state[:index]+[self.player]+self.state[index+1:], -self.player, self.pbar) for index,val in enumerate(self.state) if val==0]

    def turn(self):
        return sum(cell!=0 for cell in self.state)

    def get_action(self):
        ans = self._get_action()
        self.pbar.close()
        return ans

    def _get_action(self):
        "Returns the (next best Node, reward)"
        #print('get_action({})\n'.format(self))
        self.pbar.update()
        for row in range(3): 
            if sum(self.state[3*row:3*(row+1)]) == 3*self.player: return (self,10)
        for col in range(3): 
            if sum(self.state[3*row+col] for row in range(3)) == 3*self.player: return (self,10)
        if sum(self.state[4*cnt] for cnt in range(3)) == 3*self.player: return (self,10)
        if sum(self.state[2*cnt+2] for cnt in range(3)) == 3*self.player: return (self,10)

        for row in range(3):
            if sum(self.state[3*row:3*(row+1)]) == 3*-self.player: return (self,-10)
        for col in range(3):
            if sum(self.state[3*row+col] for row in range(3)) == 3*-self.player: return (self,-10)
        if sum(self.state[4*cnt] for cnt in range(3)) == 3*-self.player: return (self,-10)
        if sum(self.state[2*cnt+2] for cnt in range(3)) == 3*-self.player: return (self,-10)

        if not sum(cell==0 for cell in self.state):
            return (self, self.turn()) # may change later

        actions = self.get_actions()
        cases = [action._get_action() for action in actions]
        cases = [(action, -case[1]) for case,action in zip(cases,actions)] # invert the rewards
        #print('actions:',actions)
        #print('cases:',cases)
        case = max(cases, key=lambda pair:pair[1]) # max by reward
        return case

        
    def __str__(self):
        "Represents player 1 with X, player -1 with O"
        return '\n' + '\n'.join(''.join(' XO'[self.state[3*i+j]] for j in range(3)) for i in range(3)) + '\n' 

    def __repr__(self):
        "For printing in lists"
        return str(self)

start = Node([0]*9, 1)
print('\n\n',start.get_action())

