# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint, choice
from playerInterface import *

class myPlayer(PlayerInterface):

    nbnodes = 0
    tab = [0,0]
    EC = 500
    MC = 0
    SC = 0
    #tableau pour donner un poids à chaque case, utilisé pour l'heuristique
    tab_weight = [[ 100, -20, 20, -5, 10, 10, -5, 20, -20, 100] ,
                  [-20, -40, -5, -5, -3, -3, -5, -5, -40, -20 ],
                  [20, -5, 15, -4, 5, 5, -4, 15, -5, 20],
                  [-5,-5, -4, -4, 3, 3, -4, -4, -5, -5],
                  [10, -3, 5, 3, 2, 2, 3, 5, -3, 10],
                  [10, -3, 5, 3, 2, 2, 3, 5, -3, 10],
                  [-5,-5, -4, -4, 3, 3, -4, -4, -5, -5],
                  [20, -5, 15, -4, 5, 5, -4, 15, -5, 20],
                  [-20, -40, -5, -5, -3, -3, -5, -5, -40, -20 ],
                  [ 100, -20, 20, -5, 10, 10, -5, 20, -20, 100]]
    
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
        
    def isColorWhite(self):
        if(self.getMyColor() == 2):
            return True
        return False

    def setMcSc(self):
        tabDiscs =  self._board.get_nb_pieces()
        discs = tabDiscs[0] + tabDiscs[1]
        self.MC = 350 - 2 * discs
        if( discs < 10):
            self.SC = 200 - discs
        elif( discs < 20):
            self.SC = 190 - 2 * (discs - 10)
        elif( discs < 40):
           self. SC = 170 - 5 * (discs - 20)
        elif( discs < 50):
           self.SC = 70 - 7 * (discs - 40)
        else:
           self.SC = 0


    def num_valid_moves(self, player):
        count = 0
        for i in range (0,10):
            for j in range (0,10):
                if(self._board.is_valid_move(player, i, j)):
                    count+=1
        return count

    def mobilityEval(self):
        if(self._mycolor ==1):
            opponent = 2
        else:
            opponent = 1
        minMoves = min (self.num_valid_moves(self._mycolor),self.num_valid_moves(opponent))
        maxMoves = max(self.num_valid_moves(self._mycolor),self.num_valid_moves(opponent))
        if(minMoves + maxMoves != 0):
            return 100 * (maxMoves - minMoves) / (maxMoves + minMoves )
        else :
            return 0
        

    def eval(self):
        h = self._board.heuristique(player=None)
        #mobilite
        m = self.mobilityEval()
        return  self.MC * m + self.SC + h
    
    #poids des stratégies :
    #10 pour la parité des pièces
    # 900 pour le poids des cases occupées
    
        
    def _max_min(self,profmax=4):
        playerColor = self.isColorWhite()
        global nbnodes
        self.nbnodes += 1
        if self._board.is_game_over():
           return self.winner()
        if profmax == 0:
            eval = self.eval()
            return eval if playerColor else -eval
        best = -100
        for move in self._board.legal_moves():
            self._board.push(move)
            v = self._min_max(profmax-1)
            if v > best:
                best = v
            self._board.pop()
        return best

    def _min_max(self,profmax=4):
        playerColor = self.isColorWhite()
        global nbnodes
        self.nbnodes += 1
        if self._board.is_game_over():
           return self.winner()
        if profmax == 0:
            eval = self.eval()
            return eval if playerColor else -eval
        worst = 100
        for move in self._board.legal_moves():
            self._board.push(move)
            v = self._max_min(profmax-1)
            if v < worst:
                worst = v
            self._board.pop()
        return worst

    # take in count the best shot
    def _ia_min_max(self,profmax=4):
        self.nbnodes += 1
        best = -100
        best_shot = None
        list_of_equal_moves = []
        for move in self._board.legal_moves():
            self._board.push(move)
            v = self._min_max(profmax-1)
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
        move =  self._ia_min_max(4)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 
