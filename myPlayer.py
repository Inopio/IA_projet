# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    nbnodes = 0
    tab = [0,0]

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Mikoyan-Gourevitch Ye-2A"

    def getMyColor(self):
        return self._mycolor

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == self.winner():
            print("I won!!!")
        else:
            print("I lost :(!!")

    def winner(self):
        self.tab = self._board.get_nb_pieces()
        if(self.tab[0] > self.tab[1]):
            return 2 
        else:
            return 1
    
    def _max_min(self):
        global nbnodes
        self.nbnodes += 1
        if self._board.is_game_over():
           return self.winner()
        best = -100000000
        for move in self._board.legal_moves():
            self._board.push(move)
            v = self._min_max()
            if v > best:
                best = v
            self._board.pop()
        return best


    def _min_max(self):
        global nbnodes
        self.nbnodes += 1
        if self._board.is_game_over():
           return self.winner()
        worst = 100000000
        for move in self._board.legal_moves():
            self._board.push(move)
            v = self._max_min()
            if v < worst:
                worst = v
            self._board.pop()
        return worst

    
    # take in count the best shot
    def _ia_min_max(self):
        
        self.nbnodes += 1
        best = -100000000
        best_shot = None
        list_of_equal_moves = []
        for move in self._board.legal_moves():
            self._board.push(move)
            v = self._min_max()
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
        move =  self._ia_min_max()
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 
