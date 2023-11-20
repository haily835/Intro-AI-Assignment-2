import numpy as np
from enum import Enum

class Player(Enum):
    MIN = 'MIN'
    MAX = 'MAX'

class State:
    def __init__(self, label:str, util = None, player=Player.MAX, children=None):
        self.player = player # Min or Max
        self.children = children # None by default for terminal state
        self.util = util # None for internal nodes.
        self.label = label

    def __str__(self): return self.label

class Game():
    def to_move(self, state: State):
        return state.player
    
    def actions(self, state: State):
        return state.children.keys()

    def result(self, state: State, action: str):
        return state.children[action]

    def utility(self, state: State, player: Player):
        if player == Player.MAX:
            return state.util
        else:
            return -state.util

    def is_terminal(self, state: State):
        return state.children == None

    


# MiniMax Search
"""Follow the psuedo code in AIMA book"""
def minimax_search(game: Game, state: State):
    player = game.to_move(state)
    def max_value(game: Game, state: State):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v = -np.inf

        for a in game.actions(state):
            v2, _ = min_value(game, game.result(state, a))
            if v2 > v: v, move = v2, a  
        return v, move

    def min_value(game: Game, state: State):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v = np.inf
        
        for a in game.actions(state):
            v2, a2 = max_value(game, game.result(state, a))
            if v2 < v: v, move = v2, a  
        return v, move

    return max_value(game,state)

def alphabeta_search(game: Game, state: State):
    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        
        v, move = -np.inf, None

        for a in game.actions(state):
            v2, a2 = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = np.inf, None
        for a in game.actions(state):
            v2, a2 = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -np.inf, np.inf)

