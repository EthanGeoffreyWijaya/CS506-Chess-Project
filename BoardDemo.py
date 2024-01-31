from Board import Board, Move

# Author: Alex Arovas

# Method to run the board class in the console
def main():
    # Get the starting board as a FEN string (or None for default board)
    fen_str = input("Enter starting board FEN string (empty for default board): ")
    fen_str = fen_str.strip()
    fen_str = None if fen_str == "" else fen_str

    # FEN for evaluation: 
    # rnbqk2r/pp3ppp/2p5/4p3/2P1B3/2N2N2/PP1Q1PPP/R3K2R b KQkq - 0 1 (2.0 on chess.com)
    # r3k1nr/ppp1qppp/8/8/1nB1N3/5P2/PPP1Q1PP/R3K2R b KQkq - 0 1 (0.0 on chess.com)
    # r3k1nr/pp2qppp/1p6/8/4n3/8/PPP1Q1PP/R3K2R w KQkq - 0 1 (-6.0 on chess.com)
    # r3k2r/pp3ppp/1p6/8/1n2N3/2P5/PP4PP/3RK2R b Kkq - 0 1 (-0.1 on chess.com)


    board = Board(fen_str)
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