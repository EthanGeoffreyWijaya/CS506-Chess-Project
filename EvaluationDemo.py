from Board import Board

def main():
    fen_str = ""
    fen_str = input("Enter starting board FEN string (empty for default board, q to quit): ")
    fen_str = fen_str.strip()
    fen_str = None if fen_str == "" else fen_str

    while fen_str != "q":
        board = Board(fen_str)
        print('Material score: '+ str(board._count_material()))
        print('Pawn Structure score: '+ str(board._pawn_structure()))
        print('Score: '+ str(board.score()))
        # Get the starting board as a FEN string (or None for default board)
        fen_str = input("Enter starting board FEN string (empty for default board, q to quit): ")
        fen_str = fen_str.strip()
        fen_str = None if fen_str == "" else fen_str

        # FEN for evaluation: 
        # rnbqk2r/pp3ppp/2p5/4p3/2P1B3/2N2N2/PP1Q1PPP/R3K2R b KQkq - 0 1 (2.0 on chess.com)
        # r3k1nr/ppp1qppp/8/8/1nB1N3/5P2/PPP1Q1PP/R3K2R b KQkq - 0 1 (0.0 on chess.com)
        # r3k1nr/pp2qppp/1p6/8/4n3/8/PPP1Q1PP/R3K2R w KQkq - 0 1 (-6.0 on chess.com)
        # r3k2r/pp3ppp/1p6/8/1n2N3/2P5/PP4PP/3RK2R b Kkq - 0 1 (0.0 on chess.com)
        # 4k3/pp3ppp/1p6/8/8/2P5/PP4PP/4K3 b - - 0 1 (-0.8 on chess.com)


        

if __name__ == "__main__":
    main()