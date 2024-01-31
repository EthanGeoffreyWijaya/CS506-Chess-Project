from Board import *
from MiniMax import MiniMax

options = ['q', 'g', 's', 'p', 'b', 'r', 'n', 'd', 't', 'i', 'pnr', 'phit']

def get_board():
    fen_str = input("Enter board starting position as a fen string: ").strip()
    fen_str = None if fen_str == "" else fen_str
    return Board(fen_str)

def get_max_depth():
    max_depth = ''
    
    while (not max_depth.isdigit()):
        max_depth = input("Enter the maximum depth of the minimax tree: ").strip()
    
    return int(max_depth)

def get_time_limit():
    time_limit = 'placeholder'

    while (not time_limit == "" and not time_limit.isdigit()):
        time_limit = input("Enter the time limit in seconds. For no time limit, enter nothing: ").strip()

    return None if time_limit == "" else int(time_limit)

# Fen strings
#   Only kings: 8/8/4k3/8/8/4K3/8/8 w - - 0 1
#   King and one pawn: 3k3q/8/8/6N1/8/8/8/1K6 w - - 0 1
#   Only knights: 3k4/1n6/8/8/8/8/5N2/3K4 w - - 0 1
#   Easy capture: k7/8/4n3/3P4/8/8/8/K7 w - - 0 1
#   Fork: 3k4/q7/6b1/4N3/8/P7/1PP5/1K6 w - - 0 1
#   Pin: k7/8/8/3r4/8/8/4B3/2K5 w - - 0 1
#   Sacrifice: 1Q2qk2/4pp2/8/8/8/8/8/K5R1 w - - 0 1
#   Sacrifice with Promotion: 2r5/pp4P1/5R2/8/4k3/8/7P/4K3 w - - 0 1
#   Capture Decision: 8/1k6/2n1n3/3K4/8/8/8/8 w - - 0 1q
#   Capture Decision (different best move with early stop): 8/5k2/2n1n3/3K4/8/8/8/8 w - - 0 1
#   Capture Decision - Black Turn: 8/8/8/8/3k4/2N1N3/1K6/8 b - - 0 1
#   Capture Decision different best move with early stop) - Black Turn: 8/8/8/8/3k4/2N1N3/5K2/8 b - - 0 1
#
# Quiescence Tests:
#   Avoid fork(Depth 3): k7/5p2/8/8/2n5/8/8/1bK2R2 w - - 0 1
#   Fork w/ many captures: 3k3r/q7/6b1/4N1p1/7P/P5P1/1PP5/1K6 w - - 0 1
#   Long trade sequence: 1k1q2b1/1pp1r3/p4r2/3n4/5N2/P7/BPPQ4/1KR5 w - - 0 1
# Tablebase integration tests:
#   Avoid known draw: 1b6/1k6/7p/5KP1/8/8/1N6/8 w - - 0 1
#   Poor trade but known win: 8/2k5/8/8/6BN/8/2n2Q2/4rK2 w - - 0 1
#   Promotion to win endgame: 8/8/5k2/8/8/5K2/p7/8 b - - 0 1
#   

def main():
    board = get_board()
    max_depth = get_max_depth()
    time_limit = get_time_limit()
    minimax = None

    option = ''

    while (option != 'q'):
        while (option not in options):
            option = input("\nWhat do you want to do?\nCommand list:\n" 
                           + "g - generate minimax tree\n" 
                           + "i - generate minimax tree infinitely (until s or q are pressed)\n"
                           + "pnr - generate minimax tree in ponder mode\n"
                           + "phit - call ponderhit on the tree if generated in ponder mode\n"
                           + "s - stop tree generation/score the tree\n"
                           + "t - set time limit for move search\n"
                           + "p - print an existing tree\n"
                           + "b - print the board\n"
                           + "r - generate, stop / score, and print the tree\n"
                           + "n - input a new board (if generating no need to regenerate)\n"
                           + "d - input a new depth (if generating no need to regenerate)\n"
                           + "q - quit\n").strip().lower()
            print()
        
        match(option):
            case 'g':
                minimax = generate(board, max_depth, time_limit) # Generates or Regenerates tree
            case 'i':
                minimax = generate_infinite(board)
            case 'pnr':
                minimax = ponder(board, max_depth, time_limit)
            case 's':
                stop_and_score(minimax)
            case 'phit':
                ponderhit(minimax)
            case 'p':
                print_tree(minimax, max_depth)
            case 'b':
                board.print_board()
            case 'r': 
                minimax = generate(board, max_depth) # Generates or Regenerates tree
                stop_and_score(minimax)
                print_tree(minimax, max_depth)
            case 'n':
                board = get_board()
                if minimax != None:
                    minimax.change_board_or_max_depth(board, max_depth)
            case 'd':
                max_depth = get_max_depth()
                if minimax != None:
                    minimax.change_board_or_max_depth(board, max_depth)
            case 't':
                time_limit = get_time_limit()
                if minimax != None:
                    minimax.set_time_limit(time_limit)
            case 'q':
                if minimax != None:
                    minimax.stop()
                return
        
        # Reset option
        option = ''


def generate(board: Board, max_depth: int, time_limit: int = None) -> MiniMax:
    minimax = MiniMax(board, max_depth, movetime=time_limit)
    minimax.run()
    return minimax

def generate_infinite(board: Board) -> MiniMax:
    minimax = MiniMax(board, 3)
    minimax.run_infinite()
    return minimax

def ponder(board: Board, max_depth: int, time_limit: int = None) -> MiniMax:
    minimax = MiniMax(board, max_depth, movetime=time_limit)
    minimax.ponder()
    return minimax

def stop_and_score(minimax: MiniMax):
    if (minimax == None):
        print("You need to generate a tree first")
        return
    best_move = minimax.stop()
    print("Best move: " + str(best_move))
    print()

def ponderhit(minimax: MiniMax):
    if (minimax == None):
        print("You need to generate in ponder mode first")
        return
    minimax.ponderhit()

def print_tree(minimax: MiniMax, max_depth: int):
    if (minimax == None):
        print("You need to generate a tree first")
        return
    minimax.print_tree()
    print()
    minimax.print_best_line()
    

if __name__ == "__main__":
    main()