# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint, choice
from playerInterface import *
from multiprocessing.pool import ThreadPool

class myPlayer(PlayerInterface):

    pool = ThreadPool(processes=4)  #pour les threads

    nbnodes = 0
    tab = [0,0]
    EC = 500
    MC = 0
    SC = 0
    
    #tableau pour donner un poids à chaque case, utilisé par certaines fonction d'évaluation
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
        #print("Opponent played ", (x,y))
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

    def discCount(self):
        tabDiscs =  self._board.get_nb_pieces()
        return  tabDiscs[0] + tabDiscs[1]

    #pour set des constantes, et donner un poids différents aux heuristiques
    def setMcSc(self):
        discs  = self.discCount()
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

    #donne le nombre de coups valides, utilisé par la fonction de mobilité
    def num_valid_moves(self, player):
        count = 0
        for i in range (0,10):
            for j in range (0,10):
                if(self._board.is_valid_move(player, i, j)):
                    count+=1
        return count

    #evaluation de la mobilité
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
        
    #permet de se focus sur les coins, car emplacement stratégique
    def CornesEval(self):
        v = 0
        i = 0
        
        #cases coin
        if(self._board._board[0][0] == self._mycolor):
                v = v + self.tab_weight[0][0]
                
        if(self._board._board[0][9] == self._mycolor):
                v = v + self.tab_weight[0][9]

        if(self._board._board[9][0] == self._mycolor):
                v = v + self.tab_weight[9][0]
                
        if(self._board._board[9][9] == self._mycolor):
                v = v + self.tab_weight[9][9]

        #cases qui pourraient donner un coin à l'adversaire
        if(self._board._board[1][0] == self._mycolor):
            v = v + self.tab_weight[1][0]
            
        if(self._board._board[1][1] == self._mycolor):
            v = v + self.tab_weight[1][1]
            
        if(self._board._board[0][1] == self._mycolor):
            v = v + self.tab_weight[ 0][1]

        if(self._board._board[8][0] == self._mycolor):
            v = v + self.tab_weight[8][0]
            
        if(self._board._board[8][1] == self._mycolor):
            v = v + self.tab_weight[8][1]
            
        if(self._board._board[9][1] == self._mycolor):
            v = v + self.tab_weight[9][1]
            
        if(self._board._board[0][8] == self._mycolor):
            v = v + self.tab_weight[0][8]

        if(self._board._board[1][8] == self._mycolor):
            v = v + self.tab_weight[1][8]
            
        if(self._board._board[1][9] == self._mycolor):
            v = v + self.tab_weight[1][9]
            
        if(self._board._board[8][8] == self._mycolor):
            v = v + self.tab_weight[8][8]
            
        if(self._board._board[9][8] == self._mycolor):
            v = v + self.tab_weight[9][8]
            
        if(self._board._board[8][9] == self._mycolor):
            v = v + self.tab_weight[8][9]
        return v


    #permet de se focus sur les cases des bords du jeu
    def evalEdgeOccupation(self):
        v = 0
        for i in range (0,10) :
            if(self._board._board[0][i] == self._mycolor):
                v+=1
            if(self._board._board[9][i] == self._mycolor):
                v+=1
        for j in range (1,9):
            if(self._board._board[i][9] == self._mycolor):
                v+=1
            if(self._board._board[i][0] == self._mycolor):
                v+=1
        return v

    #heuristique finale
    def eval(self):
        
        #mobilite
        m = self.mobilityEval()
        
        #Corners occupation
        c = self.CornesEval()

        #Edge occupation
        e = self.evalEdgeOccupation()

        #nombre de pièces
        p = self._board.heuristique()

        #self.setMcSc()
        return   2*m + 5*c +  2*e + 0.5*p
    

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

    # _ia_min_max prend en compte le meilleur coup
    def _ia_min_max(self,profmax):
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
            #print("Referee told me to play but the game is over!")
            return (-1,-1)
        move =  self._ia_min_max(profmax=2)
        self._board.push(move)
        #print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        #print("My current board :")
        #print(self._board)
        return (x,y) 