
from mancala import Match, HumanPlayer, Player

def main():
    print "Welcome to Mancala!"
    match = Match(player1_type=HumanPlayer, player2_type=HumanPlayer)
    match.handle_next_move()

if __name__ == '__main__':
    main()