def main(filename):

    file  = open(filename, 'r').read()
    nbWinWhite = file.count("Winner : White")
    nbWinBlack = file.count("Winner : Black")
    nbEquals = file.count("Nombre piece joueur Noir : 50\nNombre piece joueur Blanc : 50")

    nbTotal = nbWinBlack + nbWinWhite
    winrateWhite = nbWinWhite / nbTotal
    winrateBlack = nbWinBlack / nbTotal
    #winRateNull = nbEquals / nbTotal
    print("Ratio de victoires du joueur blanc :")
    print(winrateWhite)

    print("Ratio de victoires du joueur noir :")
    print(winrateBlack)

    print(nbTotal)
    #print("50/50 :")
    #print(winRateNull)
main('result.txt')