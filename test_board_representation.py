from Board import Board, Move

class TestBoardRepresentation:
    # Test that the FEN representation of the starting position is correct
    def test_fen_string_startpos(self):
        board = Board()
        assert board.get_fen() == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    # Test that the FEN representation of the starting position is correct after the move e2e4
    def test_fen_string_startpos_after_one_move(self):
        board = Board()
        board.move(Move.from_uci_str('e2e4'))
        assert board.get_fen() == 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'

    # Test that the FEN representation of the starting position is correct after the move e2e4 e7e5
    def test_fen_string_startpos_after_two_moves(self):
        board = Board()
        board.move(Move.from_uci_str('e2e4'))
        board.move(Move.from_uci_str('c7c5'))
        assert board.get_fen() == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2'

    # Test the board when it's set up from a FEN string
    def test_fen_string_from_given_position(self):
        board = Board('rn1qk2r/pp3ppp/2p1bn2/8/2P5/3B1P2/PP4PP/RN1QK1NR w KQkq - 0 1')
        assert board.get_fen() == 'rn1qk2r/pp3ppp/2p1bn2/8/2P5/3B1P2/PP4PP/RN1QK1NR w KQkq - 0 1'

    # Test the FEN representation of the board when only 5 pieces are left, and neither side can castle
    def test_fen_string_no_castling(self):
        board = Board('r3kr2/7p/2p5/8/8/5P2/6P1/3QK3 w - - 0 1')
        assert board.get_fen() == 'r3kr2/7p/2p5/8/8/5P2/6P1/3QK3 w - - 0 1'

    # Test the FEN representation of the board when only 5 pieces are left, and black can castle quenside
    def test_fen_string_black_queen_castle_available(self):
        board = Board('r3kr2/7p/2p5/8/8/5P2/6P1/3QK3 w q - 0 1')
        assert board.get_fen() == 'r3kr2/7p/2p5/8/8/5P2/6P1/3QK3 w q - 0 1'

    # Tests that a zobrist hash is generated for the starting position
    def test_zobrist_hash_startpos(self):
        board = Board()
        assert type(board.get_zobrist_hash()) is int
    
    # Test that a zobrist hash is generated for the starting position, that it changes when a move is
    # made, and that it changes back to the original hash when the move is undone
    def test_zobrist_hash_matches_previous_hash(self):
        board = Board()
        previous_hash = board.get_zobrist_hash()
        board.move(Move.from_uci_str('e2e4'))
        assert board.get_zobrist_hash() != previous_hash
        board.undo_move()
        assert board.get_zobrist_hash() == previous_hash
    
    def test_zobrist_hash_with_capture(self):
        board = Board()
        board.move(Move.from_uci_str('e2e4'))
        board.move(Move.from_uci_str('d7d5'))
        previous_hash = board.get_zobrist_hash()
        board.move(Move.from_uci_str('e4d5'))
        assert board.get_zobrist_hash() != previous_hash
        board.undo_move()
        assert board.get_zobrist_hash() == previous_hash

    def test_zobrist_hash_with_en_passant(self):
        board = Board()
        board.move(Move.from_uci_str('e2e4'))
        board.move(Move.from_uci_str('a7a5'))
        board.move(Move.from_uci_str('e4e5'))
        board.move(Move.from_uci_str('d7d5'))
        previous_hash = board.get_zobrist_hash()
        board.move(Move.from_uci_str('e5d6'))
        assert board.get_zobrist_hash() != previous_hash
        board.undo_move()
        assert board.get_zobrist_hash() == previous_hash

    def test_zobrist_hash_with_rook_move_white_queenside(self):
        board = Board('r3kbnr/ppp1pppp/8/8/8/8/PPP2PPP/R3KBNR w KQkq - 0 3')
        # Board Setup:
        # r - - - k b n r
        # p p p - p p p p
        # - - - - - - - -
        # - - - - - - - -
        # - - - - - - - -
        # - - - - - - - -
        # P P P - P P P P
        # R - - - K B N R
        previous_hash = board.get_zobrist_hash()
        board.move(Move.from_uci_str('a1d1'))
        assert board.get_zobrist_hash() != previous_hash
        board.undo_move()
        assert board.get_zobrist_hash() == previous_hash

    def test_zobrist_hash_with_rook_move_black_kingside(self):
        board = Board('r3kbnr/ppp1pppp/8/8/8/8/PPP2PPP/R3KBNR b KQkq - 0 3')
        # Board Setup:
        # r - - - k b n r
        # p p p - p p p p
        # - - - - - - - -
        # - - - - - - - -
        # - - - - - - - -
        # - - - - - - - -
        # P P P - P P P P
        # R - - - K B N R
        previous_hash = board.get_zobrist_hash()
        board.move(Move.from_uci_str('a8d8'))
        assert board.get_zobrist_hash() != previous_hash
        board.undo_move()
        assert board.get_zobrist_hash() == previous_hash

    def test_zobrist_hash_with_white_castling(self):
        board = Board('r3kbnr/ppp1pppp/8/8/8/8/PPP2PPP/R3KBNR w KQkq - 0 3')
        # Board Setup:
        # r - - - k b n r
        # p p p - p p p p
        # - - - - - - - -
        # - - - - - - - -
        # - - - - - - - -
        # - - - - - - - -
        # P P P - P P P P
        # R - - - K B N R
        previous_hash = board.get_zobrist_hash()
        board.move(Move.from_uci_str('e1c1'))
        assert board.get_zobrist_hash() != previous_hash
        board.undo_move()
        assert board.get_zobrist_hash() == previous_hash
