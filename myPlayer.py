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
        

    def OccupiedCornesEval(self):
        v = 0
        i = 0
        if(self._board._board[0][0] == self._mycolor):
                v = v + self.tab_weight[0][0]
                
        if(self._board._board[0][9] == self._mycolor):
                v = v + self.tab_weight[0][9]

        if(self._board._board[9][0] == self._mycolor):
                v = v + self.tab_weight[9][0]
                
        if(self._board._board[9][9] == self._mycolor):
                v = v + self.tab_weight[9][9]
        return v

    def evalBoardExceptCorners(self):
        v = 0
        for x in range (0,10):
            for y in range (0,10):
                if(self._board._board[x][y] == self._mycolor):
                    v = v + self.tab_weight[x][y]
        return v
    
    def eval(self):
        #mobilite
        m = self.mobilityEval()
        #Corners occupation
        v = self.OccupiedCornesEval()
        #eval rest of the board
        #b = self.evalBoardExceptCorners()
        return  self.MC * m + self.SC * v
    
        
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


    def alphaBeta(self,depth, a, B, maximizingPlayer):
        if depth == 0:
            return self.eval
        
        if maximizingPlayer== True:
            value = -10000
            for move in self._board.legal_moves():
                tmp = self.alphaBeta(depth - 1, a, B, False)
                value = max(value, tmp)
                a = max(a, value)
                if a >= B:
                    return a
            return B
        else:
            value = 10000
            for move in self._board.legal_moves():
                tmp = self.alphaBeta(depth -1, a, B, True)
                value = min(value, tmp)
                B = min(B, value)
                if a >= B:
                    return a
            return B

    def MaxValue(self,depth,a, B):
        if depth == 0 or self._board.is_game_over() == True:
            return self.eval
        for move in self._board.legal_moves():
            a = max(a,self.MinValue(depth-1,a,B))
            if a >= B:
                return B
        return a


    def MinValue(self, depth,a, B):
        if depth == 0 or self._board.is_game_over() == True:
            return self.eval
        for move in self._board.legal_moves():
            B = min(self.MaxValue(depth -1,a,B))
            if a >= B:
                return a
        return B

    def max_score_alpha_beta(self, ply, alpha, beta):
        if ply == 0 or self._board.is_game_over() == True:
            return self.eval()
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
             return self.eval()
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
    def _ia_min_max(self,profmax=5):
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
        move =  self._ia_min_max(profmax=5)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 
