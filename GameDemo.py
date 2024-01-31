from Board import Board, TeamColor, Move
from MiniMax import MiniMax
from generateTree import Node
from random import randrange

# Author: Alex Arovas

# Globals
best_score: int = 0
best_move: Move

# Callback fucntion for minimax
def minimax_callback(stopped, best_child: Node, depth_to_mate: int):
    global best_score
    global best_move
    best_score = best_child.score
    best_move = best_child.previous_move

# Method to run the board class in the console
def main():
    global best_score
    global best_move
    # Get the starting board as a FEN string (or None for default board)
    fen_str = input("Enter starting board FEN string (empty for default board): ")
    fen_str = fen_str.strip()
    fen_str = None if fen_str == "" else fen_str

    board = Board(fen_str)

    # Get what team the user will be
    user_team = None
    while (user_team not in ["w", "b", ""]):
        user_team = input("What team do you want to be (w or b - empty for random): ").strip()
    
    if (user_team == ""):
        user_team = TeamColor.WHITE if randrange(2) == 0 else TeamColor.BLACK
    else:
        user_team = TeamColor.WHITE if user_team == "w" else TeamColor.BLACK

    print("\nUser Team: " + user_team.name)

    # print("Board: ")
    board.print_board()
    valid_moves = board.get_all_legal_moves()
    print("Valid moves: " + str(valid_moves))
    print("Evaluation: " + str(board.evaluate()))
    print("Material: " + str(board._count_material()))
    print("Pawn Structure: " + str(board._pawn_structure()))
    print("Attack Protection: " + str(board._get_attack_protection()))
    print("Piece Count: " + str(board.get_piece_count()))

    move = ""

    while move != "q":

        if (board.get_turn_color() != user_team):
            # Bot turn
            # IF undo - undo until user turn
            if (move != "u"): 
                # Generate the minimax tree
                minimax = MiniMax(board, 3)
                event = minimax.run(minimax_callback)
                # Wait for the tree to finish generating
                event.wait()
                # Make the best move
                valid_move = board.move(best_move)
                # Print the best move and score
                print()
                print("Bot Move: " + str(best_move))
                print("Bot Score for Move: " + str(best_score))
                print()
            else:
                # Undo bot turn so it gets back to user turn
                valid_move = board.undo_move()
        else:
            # User Turn
            # Get the move from the user
            move = input("Enter move (q to quit, u to undo, p to print attacking board, f to print FEN string): ")
            move = move.strip()

            # If the user wants to quit, break out of the loop
            if move == "q":
                break
            # If the user wants to undo, undo the last move
            elif move == "u":
                valid_move = board.undo_move()
            # If the user wants to print the attacking board, print it
            elif move == "p":
                board._print_attack_arr()
                continue
            # If the user wants to print the FEN string, print it
            elif move == "f":
                print(board.get_fen())
                continue
            # Otherwise, attempt to move the piece
            else:
                valid_move = board.move(Move.from_uci_str(move))

        # If the move was invalid, print an error message
        if not valid_move:
            print("Invalid move, try again.")
        else:
            # print("Board: ")
            # print("\n\n\n\n\n\n\n\n\n\n\n")
            board.print_board()
            valid_moves = board.get_all_legal_moves()
            print("Valid moves: " + str(valid_moves))
            print("Evaluation: " + str(board.evaluate()))
            print("Material: " + str(board._count_material()))
            print("Pawn Structure: " + str(board._pawn_structure()))
            print("Attack Protection: " + str(board._get_attack_protection()))
            print("Piece Count: " + str(board.get_piece_count()))

if __name__ == "__main__":
    main()