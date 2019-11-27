# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint, choice
from playerInterface import *

class alphaOnePlayer(PlayerInterface):
    nbnodes = 0
    tab = [0,0]

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def max_score_alpha_beta(self, ply, alpha, beta):
        if ply == 0 or self._board.is_game_over() == True:
            return self._board.heuristique()
        bestscore = -10000
        for move in self._board.legal_moves():
            score = self.min_score_alpha_beta(ply-1, alpha, beta)
            if score > bestscore:
                bestscore = score
            if bestscore >= beta:
                return bestscore
            alpha = max (alpha,bestscore)
        return bestscore

    def min_score_alpha_beta(self, ply, alpha, beta):
        if ply == 0 or self._board.is_game_over() == True:
             return self._board.heuristique()
        bestscore = 10000
        for move in self._board.legal_moves():
            score = self.max_score_alpha_beta(ply-1, alpha, beta)
            if score < bestscore:
                bestscore = score
            if bestscore <= alpha:
                return bestscore
            beta = min(beta,bestscore)
        return bestscore

    # take in count the best shot
    def _ia_min_max(self,profmax=7):
        self.nbnodes += 1
        best = -100
        best_shot = None
        list_of_equal_moves = []
        for move in self._board.legal_moves():
            self._board.push(move)
            v = self.min_score_alpha_beta(profmax,-10000, 10000)
            if v > best or best_shot == None:
                best = v
                best_shot = move
                list_of_equal_moves = [move]
            elif v == best:
                list_of_equal_moves.append(move)
            self._board.pop()
        return choice(list_of_equal_moves)
        
    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        move =  self._ia_min_max(profmax=3)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


