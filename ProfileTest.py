from Board import *
from MiniMax import MiniMax
from generateTree import Tree, Node
import time

# Fen strings
#   Only kings: 8/8/4k3/8/8/4K3/8/8 w - - 0 1
#   King and one pawn: 3k3q/8/8/6N1/8/8/8/1K6 w - - 0 1
#   Only knights: 3k4/1n6/8/8/8/8/5N2/3K4 w - - 0 1
#   Easy capture: k7/8/4n3/3P4/8/8/8/K7 w - - 0 1
#   Fork: 3k4/q7/6b1/4N3/8/P7/1PP5/1K6 w - - 0 1
#   Pin: k7/8/8/3r4/8/8/4B3/2K5 w - - 0 1
#   Sacrifice: 1Q2qk2/4pp2/8/8/8/8/8/K5R1 w - - 0 1
#   Capture Decision: 8/1k6/2n1n3/3K4/8/8/8/8 w - - 0 1q
#   Capture Decision (different best move with early stop): 8/5k2/2n1n3/3K4/8/8/8/8 w - - 0 1
#   Capture Decision - Black Turn: 8/8/8/8/3k4/2N1N3/1K6/8 b - - 0 1
#   Capture Decision different best move with early stop) - Black Turn: 8/8/8/8/3k4/2N1N3/5K2/8 b - - 0 1
def main():
    max_depth = 5
    board = Board("rn1qkb1r/4pppp/p5b1/1p2N3/5N2/3B4/PP1Q1PPP/R3K2R b KQkq - 0 16")
    minimax = MiniMax(board, max_depth)
    
    start_time = time.time()
    # Print to show that the tree is generating
    print("Generating tree...")
    
    minimax.run().wait()

    # Print to show that the tree is done generating
    print("Done generating tree")
    print("Tree generated in " + str(time.time() - start_time) + " seconds")
    # event.wait()
    

if __name__ == "__main__":
    main()