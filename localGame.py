import Reversi
import myPlayer
import randomPlayer
import myPlayer3
import myPlayer2
import alphaOnePlayer
import time
from io import StringIO
import sys
from multiprocessing import Process, Pool
from threading import Thread

def l():
    b = Reversi.Board(10)

    players = []
    player1 = myPlayer3.myPlayer()
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = myPlayer.myPlayer()
    player2.newGame(b._WHITE)
    players.append(player2)

    totalTime = [0,0] # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK
    nbmoves = 1

    outputs = ["",""]
    sysstdout= sys.stdout
    stringio = StringIO()

    #print(b.legal_moves())
    while not b.is_game_over():
        print("Referee Board:")
        print(b)
        print("Before move", nbmoves)
        print("Legal Moves: ", b.legal_moves())
        nbmoves += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
        
        currentTime = time.time()
        sys.stdout = stringio
        move = players[nextplayer].getPlayerMove()
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        #print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        #print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
        (x,y) = move 
        if not b.is_valid_move(nextplayercolor,x,y):
            #print(otherplayer, nextplayer, nextplayercolor)
            #print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        players[otherplayer].playOpponentMove(x,y)

        nextplayer = otherplayer
        nextplayercolor = othercolor
        #print(b)

    #print("The game is over")
    #print(b)
    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("Time:", totalTime)
    print("Winner: ", end="")
    f = open("result.txt","a+")
    if nbwhites > nbblacks:
        print("WHITE")
        f.write("Winner : White\n")
    elif nbblacks > nbwhites:
        print("BLACK")
        f.write("Winner : Black\n")
    else:
        print("DEUCE")
    f.write("Time :")
    for item in totalTime:
        f.write("%s " % item)
    f.write("\n")
    f.write("Nombre piece joueur Noir : %d\n" %nbblacks)
    f.write("Nombre piece joueur Blanc : %d\n" %nbwhites)
    f.write("\n\n")
    f.close()


workerList=[]
n = 1

for i in range(n):
    workerList.append(Thread(target=l()))

for i in range(n):
    workerList[i].start()

for i in range(n):
    workerList[i].join()
