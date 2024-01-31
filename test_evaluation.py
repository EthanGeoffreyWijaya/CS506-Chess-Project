from Board import Board

'''
This class is used to test the evaluation methods in the Board class. It tests the following methods:
    - evaluate
    - _count_material
    - _pawn_structure
    - _get_mobility
'''
class TestEvaluation:
    # Evaluate the board from the starting position
    def test_evaluate_startpos(self):
        board = Board()
        assert board.evaluate() == 0

    # Test the material score after black has captured one of white's pieces
    def test_count_material_black_up_1(self):
        # Board setup (lowercase are black, uppercase are white): 
        # rook  knight  bishop  queen   king    bishop  knight  rook
        # pawn  pawn    pawn    pawn     -      pawn    pawn    pawn
        #  -     -       -       -       -        -       -       -
        #  -     -       -       -       -        -       -       -
        #  -     -       -      pawn    PAWN      -       -       -
        #  -     -       -       -       -        -       -       -
        # PAWN  PAWN    PAWN     -       -   PAWN    PAWN    PAWN
        # ROOK  KNIGHT  BISHOP  QUEEN   KING    BISHOP  KNIGHT  ROOK
        board = Board('rnbqkbnr/pppp1ppp/8/8/3pP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 1')
        assert board._count_material() == -1

    # Test the material score after white has captured one of black's pieces
    def test_count_material_white_up_1(self):
        # Board setup (lowercase are black, uppercase are white): 
        # rook  knight  bishop  queen   king    bishop  knight  rook
        # pawn  pawn    pawn    pawn      -     pawn    pawn    pawn
        #   -     -       -       -       -       -       -       -
        #   -     -       -       -     PAWN      -       -       -
        #   -     -       -       -     PAWN      -       -       -
        #   -     -       -       -       -       -       -       -
        # PAWN  PAWN    PAWN      -       -     PAWN    PAWN    PAWN
        # ROOK  KNIGHT  BISHOP  QUEEN   KING    BISHOP  KNIGHT  ROOK
        board = Board('rnbqkbnr/pppp1ppp/8/4P3/4P3/8/PPP2PPP/RNBQKBNR b KQkq - 0 1')
        assert board._count_material() == 1
        
    # Test the material score if white starts without a queen
    def test_count_material_white_no_queen(self):
        # Board setup (lowercase are black, uppercase are white):
        # rook  knight  bishop  queen   king    bishop  knight  rook
        # pawn  pawn    pawn    pawn    pawn   pawn    pawn    pawn
        #   -     -       -       -       -      -       -       -
        #   -     -       -       -       -      -       -       -
        #   -     -       -       -       -      -       -       -
        #   -     -       -       -       -      -       -       -
        # PAWN  PAWN    PAWN    PAWN    PAWN   PAWN    PAWN    PAWN
        # ROOK  KNIGHT  BISHOP    -     KING   BISHOP  KNIGHT  ROOK
        board = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1')
        assert board._count_material() == -9

    # Test that doubled pawns are counted correctly
    def test_doubled_pawns_white(self):
        # Board setup (lowercase are black, uppercase are white):
        # rook  knight  bishop  queen   king    bishop  knight  rook
        # pawn  pawn    pawn    pawn    pawn   pawn    pawn    pawn
        #   -     -       -       -       -      -       -       -
        #   -     -       -       -       -      -       -       -
        #   -     -       -       -       -      -       -       -
        #   -     -     PAWN      -       -     PAWN     -       -
        # PAWN  PAWN    PAWN      -       -     PAWN    PAWN    PAWN
        # ROOK  KNIGHT  BISHOP  QUEEN   KING    BISHOP  KNIGHT  ROOK
        board = Board('rnbqkbnr/pppppppp/8/8/8/2P2P2/PPP2PPP/RNBQKBNR b KQkq - 0 1')
        # Two instances of doubled pawns for white, one in the C file and the other in the F file
        # Also two instances of blocked pawns in the same files
        assert board._pawn_structure() == 4

    # Test that isolated pawns are counted correctly
    def test_white_isolated_pawn_on_h_file(self):
        # Board setup (lowercase are black, uppercase are white):
        # rook  knight  bishop  queen   king    bishop  knight  rook
        # pawn  pawn    pawn    pawn    pawn    pawn    pawn    pawn
        #   -     -       -       -       -      -       -       -
        #   -     -       -       -       -      -       -       -
        #   -     -       -       -       -      -       -      PAWN
        # PAWN  PAWN    PAWN    PAWN    PAWN    PAWN     -       -
        # ROOK  KNIGHT  BISHOP  QUEEN   KING    BISHOP  KNIGHT  ROOK
        board = Board('rnbqkbnr/pppppppp/8/8/7P/8/PPPPPP2/RNBQKBNR b KQkq - 0 1')
        # There is one isolated pawn on the white side, so the score should be 1
        assert board._pawn_structure() == 1

    # Test if there are two pawns who are both isolated and in adjacent rows
    # They should be counted as doubled, isolated, and blocked
    def test_doubled_isolated_and_blocked_pawns(self):
        # Board setup (lowercase are black, uppercase are white):
        # rook  knight  bishop  queen   king    bishop  knight  rook
        # pawn  pawn    pawn    pawn    pawn    pawn    pawn    pawn
        #   -     -       -       -       -       -       -       -
        #   -     -       -       -       -       -       -       -
        #   -     -       -       -       -       -       -     PAWN
        #   -     -       -       -       -       -       -     PAWN
        # PAWN  PAWN    PAWN    PAWN    PAWN      -       -       -
        # ROOK  KNIGHT  BISHOP  QUEEN   KING    BISHOP  KNIGHT  ROOK
        board = Board('rnbqkbnr/pppppppp/8/8/7P/7P/PPPPP3/RNBQKBNR b KQkq - 0 1')
        assert board.get_fen() == 'rnbqkbnr/pppppppp/8/8/7P/7P/PPPPP3/RNBQKBNR b KQkq - 0 1'
        assert board._pawn_structure() == 4

    
    