# -*- coding: utf-8 -*-

import time
import Reversi
import math
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

    def stability(self):
        if(self._mycolor == 1):
            opponent = 2
        else:
            opponent = 1
        for move in self._board.legal_moves():
            x = move[1]
            y = move[2]
            weight_move = self.tab_weight[x][y]

            if(x < 9 and x > 1):
                if(self._board._board[x-1][y] == opponent):
                    if(self._board._board[x+1][y] == 0):
                        return weight_move

                if(self._board._board[x+1][y] == opponent):
                    if(self._board._board[x-1][y] == 0):
                        return weight_move
                    
                if(y < 9 and y > 1):
                    if(self._board._board[x-1][y-1] == opponent):
                        if(self._board._board[x+1][y+1] == 0):
                            return weight_move

                    if(self._board._board[x-1][y+1] == opponent):
                        if(self._board._board[x+1][y-1] == 0):
                            return weight_move
                        
                    if(self._board._board[x+1][y-1] == opponent):
                        if(self._board._board[x-1][y+1] == 0):
                            return weight_move
                    
                    if(self._board._board[x+1][y+1] == opponent):
                        if(self._board._board[x-1][y-1] == 0):
                            return weight_move
                
            if(y < 9 and y > 1):
                if(self._board._board[x][y-1] == opponent):
                    if(self._board._board[x][y+1] == 0):
                        return weight_move
                
                if(self._board._board[x][y+1] == opponent):
                    if(self._board._board[x][y-1] == 0):
                        return weight_move
                
        return 0
    
    def opponent_stopping_move(self):
        if(self._mycolor == 1):
            opponent = 2
        else:
            opponent = 1
        if(self.num_valid_moves(opponent)==0):
            return 100
        else:
            return 0
        
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
            v = v + self.tab_weight[0][1]

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

    def edge_eval(self):

        corners = [[1,1],[1,10], [10,1], [10,10]]
        score = 0
        
        for i in range(self._board._boardsize):
            for j in range(self._board._boardsize):
                delta = 1
                if i == 0 or i == 9:
                    delta += 5
                if j == 0 or j == 9:
                    delta += 5

                if i == 1 or i == 8:
                    delta -= 5
                if j == 1 or j == 8:
                    delta -= 5

                for corner in corners:
                    distX = abs(corner[0] - i)
                    distY = abs(corner[1] - j)
                    dist  = math.sqrt(distX*distX + distY*distY)
                    if dist < 4:
                        delta += 3

                
                if self._board._board[i][j] == self._mycolor:
                    score += delta
                elif self._board._board[i][j] == self._opponent:
                    score -= delta

        for l in range(self._board._boardsize):
            
            for c in range(l):
                delta = 1
                if l == 0 or l == 9:
                    delta += 5
                if c == 0 or c == 9:
                    delta += 5

                if l == 1 or l == 8:
                    delta -= 5
                if c == 1 or c == 8:
                    delta -= 5

                for corner in corners:
                    distX = abs(corner[0] - l)
                    distY = abs(corner[1] - c)
                    dist  = math.sqrt(distX*distX + distY*distY)
                    if dist < 4:
                        delta += 3

                if c == self._mycolor:
                    score += delta
                elif c == self._opponent:
                    score -= delta
                    
        return score

    #permet de se focus sur les cases des bords du jeu
    def evalEdgeOccupation(self):
        v = 0
        for i in range (1,9) :
            if(self._board._board[0][i] == self._mycolor):
                v = v + self.tab_weight[0][i]
            if(self._board._board[9][i] == self._mycolor):
                v = v + self.tab_weight[9][i]
        for j in range (1,9):
            if(self._board._board[i][9] == self._mycolor):
                v = v + self.tab_weight[i][9]
            if(self._board._board[i][0] == self._mycolor):
                v = v + self.tab_weight[i][0]
        return v

    def minimization(self):
        tabDisc =  self._board.get_nb_pieces()
        if self._mycolor == 2:
            return tabDisc[1] - tabDisc[0]
        else :
            return tabDisc[0] - tabDisc[1]
        
    #heuristique finale
    def eval(self):

        #mobilite
        m = self.mobilityEval()
        
        #Corners occupation
        c = self.CornesEval()

        #Edge occupation
        #e = self.evalEdgeOccupation()
        e = self.evalEdgeOccupation()
        e2 = self.edge_eval()

        #nombre de pièces
        p = self._board.heuristique()

        #minimisation du nombre de pièces
        mini = self.minimization()

        #empêcher l'adversaire de jouer
        o = self.opponent_stopping_move()

        #disque stable
        s = self.stability()

        #self.setMcSc()
        current_board = self._board.get_nb_pieces()
        # bonne pour white, return 2*m + 15*c + 4*e + 0.5*mini
        if(self._mycolor == 2):
            return 2*m + 10*c + 6*e + 0.5*p + 2*o + 2*s + e2
        else:
            return 2*m + 10*c + 6*e + 0.5*p + 2*o + 2*s

    
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
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        #move = self._ia_min_max(profmax=2)
        if(self.discCount() < 20):
            move = self._ia_min_max(profmax=2)
        elif(self.discCount() >=20 and self.discCount() <= 80):
            move = self._ia_min_max(profmax=3)
        elif(self.discCount() > 80):
            move = self._ia_min_max(profmax=6)
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 
