from mancala import Match, HumanPlayer, ComputerRandomPlayer

def main():
    print("Welcome to Mancala!")
    match = Match(player1_type=HumanPlayer, player2_type=ComputerRandomPlayer)
    match.checkMove()

if __name__ == '__main__':
    main()