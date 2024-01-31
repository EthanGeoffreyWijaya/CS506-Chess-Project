import pytest
from Board import *
from random import randrange
import random

# Author: Alex Arovas

# Tests the Board class

# Approx percentage of spaces on a board that should have a piece in random tests
RAND_PIECE_PERCENTAGE = 0.4 # Slightly less than starting amount of 50%

# Number of random tests for test_move_str_to_move
NUM_RAND_MOVE_STR_TO_MOVE_TESTS = 100

# Number of random tests for test_move_to_move_str
NUM_RAND_MOVE_TO_MOVE_STR_TESTS = 100

# Number of random tests for counting material
NUM_RAND_COUNT_MATERIAL_TESTS = 100

# Number of random tests for test_get_pieces
NUM_RAND_GET_PIECES_TESTS = 100

# Number of random tests for test_fen_to_board_arr
NUM_RAND_FEN_TO_BOARD_ARR_TESTS = 100

# Pieces for the test board to make it more readable
rook_white = Piece(PieceType.ROOK, TeamColor.WHITE)
knight_white = Piece(PieceType.KNIGHT, TeamColor.WHITE)
bishop_white = Piece(PieceType.BISHOP, TeamColor.WHITE)
queen_white = Piece(PieceType.QUEEN, TeamColor.WHITE)
king_white = Piece(PieceType.KING, TeamColor.WHITE)
pawn_white = Piece(PieceType.PAWN, TeamColor.WHITE)

rook_black = Piece(PieceType.ROOK, TeamColor.BLACK)
knight_black = Piece(PieceType.KNIGHT, TeamColor.BLACK)
bishop_black = Piece(PieceType.BISHOP, TeamColor.BLACK)
queen_black = Piece(PieceType.QUEEN, TeamColor.BLACK)
king_black = Piece(PieceType.KING, TeamColor.BLACK)
pawn_black = Piece(PieceType.PAWN, TeamColor.BLACK)

# Piece values
rook_val = Board.get_piece_value(PieceType.ROOK)
knight_val = Board.get_piece_value(PieceType.KNIGHT)
bishop_val = Board.get_piece_value(PieceType.BISHOP)
queen_val = Board.get_piece_value(PieceType.QUEEN)
king_val = Board.get_piece_value(PieceType.KING)
pawn_val = Board.get_piece_value(PieceType.PAWN)

# The default chess starting board
default_board = [   [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]

# Test the constructor
# Make sure the board is set up correctly
# Make sure en_passant_avail is None
# Make sure White has the turn
def test_board_constructor():
    # The test board (how a chess board should be set up)
    test_board = default_board
    
    # Create the board
    board = Board()

    # Test if the board array is set up correctly
    assert_boards_are_same(test_board, board)

    # Test if en_passant_avail is None
    assert board._en_passant_avail == None

    # Test if White has the turn
    assert board._turn == TeamColor.WHITE

    # Test castling rights
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Test Halfmove counter
    assert board._half_moves == 0

    # Test fullmove counter
    assert board._full_moves == 1

    # Test creating the default board with a FEN string
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert_boards_are_same(test_board, board)
    # Test if en_passant_avail is None
    assert board._en_passant_avail == None
    # Test if White has the turn
    assert board._turn == TeamColor.WHITE
    # Test castling rights
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True
    # Test Halfmove counter
    assert board._half_moves == 0
    # Test fullmove counter
    assert board._full_moves == 1

    test_board = [  [None,          None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           None,           queen_white,    knight_white,   None,           bishop_white,   None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_white,     None,           None,           None,           pawn_white,     None,           None],
                    [None,          pawn_black,     None,           None,           None,           None,           pawn_black,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          bishop_black,   None,           knight_black,   queen_black,    None,           pawn_white,     None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           None]]

    # Test creating a unique board with FEN string
    board = Board("r3k3/1b1nq1P1/8/1p4p1/pP3P2/8/3QN1B1/4K2R b Kq b3 0 34")
    assert_boards_are_same(test_board, board)
    # Test if en_passant_avail is None
    assert board._en_passant_avail == Coordinate(3, 1)
    # Test if black has the turn
    assert board._turn == TeamColor.BLACK
    # Test castling rights
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == False
    # Test Halfmove counter
    assert board._half_moves == 0
    # Test fullmove counter
    assert board._full_moves == 34

    print("Test Board Constructor Passed!!!")

# Test _get_index_in_range
# Test with a few valid characters and ranges
# Test with a few characters that are out of range
# Test with a few invalid inputs to ensure -1 is returned
def test_get_index_in_range():
    # Create the board
    board = Board()

    # Test with a few valid characters and ranges
    # Test first element 0 with characters
    assert board._get_index_in_range("a", "a", "c") == 0
    assert board._get_index_in_range("D", "D", "G") == 0

    # Test with numeric characters
    assert board._get_index_in_range("6", "6", "9") == 0

    # Test some in the middle of the range
    assert board._get_index_in_range("j", "a", "z") == 9
    assert board._get_index_in_range("V", "F", "Y") == 16
    assert board._get_index_in_range("5", "0", "9") == 5
    assert board._get_index_in_range("5", "3", "9") == 2

    # Test last element of range
    assert board._get_index_in_range("Z", "A", "Z") == 25
    assert board._get_index_in_range("w", "i", "w") == 14
    assert board._get_index_in_range("9", "0", "9") == 9
    assert board._get_index_in_range("6", "3", "6") == 3

    # Test some special characters (an scenarios)
    assert board._get_index_in_range(" ", " ", "/") == 0
    assert board._get_index_in_range("(", "!", ".") == 7
    assert board._get_index_in_range("~", ":", "~") == 68
    assert board._get_index_in_range("c", "A", "z") == 34

    print("Test Get Index in Range Passed!!!")

# Test _move_str_to_move
# Test with a few valid moves
# Test moves with promotion
# Test with a few invalid moves (off the board, invalid character or length, etc.)
def test_move_str_to_move():
    # Test with a few valid moves
    # Test at 0,0
    assert_moves_are_equal(Move.from_uci_str("a1a2"), Move(Coordinate(0, 0), Coordinate(1, 0), None))
    assert_moves_are_equal(Move.from_uci_str("f5a1"), Move(Coordinate(4, 5), Coordinate(0, 0), None))

    # Test at 0,7
    assert_moves_are_equal(Move.from_uci_str("h1b3"), Move(Coordinate(0, 7), Coordinate(2, 1), None))
    assert_moves_are_equal(Move.from_uci_str("g4h1"), Move(Coordinate(3, 6), Coordinate(0, 7), None))

    # Test at 7,0
    assert_moves_are_equal(Move.from_uci_str("a8c4"), Move(Coordinate(7, 0), Coordinate(3, 2), None))
    assert_moves_are_equal(Move.from_uci_str("h3a8"), Move(Coordinate(2, 7), Coordinate(7, 0), None))

    # Test at 7,7
    assert_moves_are_equal(Move.from_uci_str("h8d5"), Move(Coordinate(7, 7), Coordinate(4, 3), None))
    assert_moves_are_equal(Move.from_uci_str("a2h8"), Move(Coordinate(1, 0), Coordinate(7, 7), None))

    # Test in the middle of the board and that any case works and the string is stripped
    assert_moves_are_equal(Move.from_uci_str("H5A1"), Move(Coordinate(4, 7), Coordinate(0, 0), None))
    assert_moves_are_equal(Move.from_uci_str("B8c1"), Move(Coordinate(7, 1), Coordinate(0, 2), None))
    assert_moves_are_equal(Move.from_uci_str("  d3E4  \t"), Move(Coordinate(2, 3), Coordinate(3, 4), None))
    assert_moves_are_equal(Move.from_uci_str(" f6g7"  ), Move(Coordinate(5,5), Coordinate(6, 6), None))
    assert_moves_are_equal(Move.from_uci_str("\tf2g8\t"), Move(Coordinate(1, 5), Coordinate(7, 6), None))

    # Test moves with promotion
    # Queen promotion
    assert_moves_are_equal(Move.from_uci_str("a7b8q"), Move(Coordinate(6, 0), Coordinate(7, 1), PieceType.QUEEN))
    # Knight promotion
    assert_moves_are_equal(Move.from_uci_str("b7a8n"), Move(Coordinate(6, 1), Coordinate(7, 0), PieceType.KNIGHT))
    # Bishop promotion
    assert_moves_are_equal(Move.from_uci_str("c7d8b"), Move(Coordinate(6, 2), Coordinate(7, 3), PieceType.BISHOP))
    # Rook promotion
    assert_moves_are_equal(Move.from_uci_str("e7f8r"), Move(Coordinate(6, 4), Coordinate(7, 5), PieceType.ROOK))
    # Queen promotion
    assert_moves_are_equal(Move.from_uci_str("h7g8q"), Move(Coordinate(6, 7), Coordinate(7, 6), PieceType.QUEEN))

    # Test invalid moves (off the board, invalid character or length, etc.)

    # Test invalid row
    # Test first row (from)
    assert Move.from_uci_str("a0a2") == None
    assert Move.from_uci_str("b9c2") == None

    # Test larger than 9 (2 digits)
    assert Move.from_uci_str("d10h10") == None
    assert Move.from_uci_str("a10c8") == None
    assert Move.from_uci_str("g2h10") == None

    # Test second row (t0)
    assert Move.from_uci_str("c2g9") == None
    assert Move.from_uci_str("e3d0") == None
    assert Move.from_uci_str("a0c9") == None

    # Test alphabet characters and special characters
    assert Move.from_uci_str("gahh") == None
    assert Move.from_uci_str("chda") == None
    assert Move.from_uci_str("a!b2") == None
    assert Move.from_uci_str("b2c:") == None

    # Test invalid column
    # Test first column (from)
    assert Move.from_uci_str("i1a2") == None
    assert Move.from_uci_str("12c3") == None

    # Test second column (to)
    assert Move.from_uci_str("a2i1") == None
    assert Move.from_uci_str("c312") == None

    # Test special characters
    assert Move.from_uci_str("{2b3") == None
    assert Move.from_uci_str("c3)7") == None

    # Test invalid promotion character
    assert Move.from_uci_str("a7b8x") == None
    assert Move.from_uci_str("c6d4k") == None
    assert Move.from_uci_str("d6g35") == None
    assert Move.from_uci_str("a5e3~") == None

    # Test invalid length
    assert Move.from_uci_str("a2b3c4") == None
    assert Move.from_uci_str("c6d") == None
    assert Move.from_uci_str("d4") == None

    # Test some random moves
    for _ in range(NUM_RAND_MOVE_STR_TO_MOVE_TESTS):
        # Generate random rows and columns
        rand_from_row = randrange(8) # 0-7 for Move class -> 1-8 for move string
        rand_from_col = randrange(8)

        rand_to_row = randrange(8) # 0-7 for Move class -> 1-8 for move string
        rand_to_col = randrange(8)

        # Generate random move
        rand_move = chr(rand_from_col + ord('a')) + str(rand_from_row + 1) + chr(rand_to_col + ord('a')) + str(rand_to_row + 1)
        print(rand_move)

        # Test the move
        assert_moves_are_equal(Move.from_uci_str(rand_move), Move(Coordinate(rand_from_row, rand_from_col), Coordinate(rand_to_row, rand_to_col), None))
    
    print("Test Move to Indexes Passed!!!")

# Test making pawn moves
# Make sure the pawn is moved
# Make sure the turn is switched
# Make sure nothing else moved
# Then do additional moves to test for moving two spaces and en passant
def test_pawn_moves():
    board = Board()
    # Make the move pawn a2 to a4
    assert board.move(Move.from_uci_str("a2a4")) == True
    # The test board (how a chess board should be set up)
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_white,    None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if the turn switched
    assert board._turn == TeamColor.BLACK

    # Move the black pawn a7 to a6
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_white,    None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    None,           None,           None,           None,           None,           None,           None],
                    [None,          pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Move the black 
    assert board.move(Move.from_uci_str("a7a6")) == True
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if the turn switched
    assert board._turn == TeamColor.WHITE

    # Move the white pawn a4 to a5
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_white,    None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    None,           None,           None,           None,           None,           None,           None],
                    [None,          pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Move the black 
    assert board.move(Move.from_uci_str("a4a5")) == True
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if the turn switched
    assert board._turn == TeamColor.BLACK

    # Move the black pawn b7 to b5
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_white,    pawn_black,     None,           None,           None,           None,           None,           None],
                    [pawn_black,    None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Move the black 
    assert board.move(Move.from_uci_str("b7b5")) == True
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if the turn switched
    assert board._turn == TeamColor.WHITE

    # Move the white pawn a5 to b6 with en passant capture
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_white,     None,           None,           None,           None,           None,           None],
                    [None,          None,           pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Move the black 
    assert board.move(Move.from_uci_str("a5b6")) == True
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if the turn switched
    assert board._turn == TeamColor.BLACK

    # Move the black pawn c7 to b6 with capture
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Move the black 
    assert board.move(Move.from_uci_str("c7b6")) == True
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if the turn switched
    assert board._turn == TeamColor.WHITE

    # Test creating a unique board with FEN for another en passant check
    board = Board("r3k3/1b1nq1P1/8/1p4p1/pP3P2/8/3QN1B1/4K2R b Kq b3 0 34")

    test_board = [  [None,          None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           None,           queen_white,    knight_white,   None,           bishop_white,   None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_white,     None,           None,           None,           pawn_white,     None,           None],
                    [None,          pawn_black,     None,           None,           None,           None,           pawn_black,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          bishop_black,   None,           knight_black,   queen_black,    None,           pawn_white,     None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           None]]

    assert_boards_are_same(test_board, board)
    # Test if en_passant_avail is None
    assert board._en_passant_avail == Coordinate(3, 1)
    # Test if black has the turn
    assert board._turn == TeamColor.BLACK
    # Test castling rights
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == False
    # Test Halfmove counter
    assert board._half_moves == 0
    # Test fullmove counter
    assert board._full_moves == 34

    # Check en passant works
    assert board.move(Move.from_uci_str("a4b3")) == True

    test_board = [  [None,          None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           None,           queen_white,    knight_white,   None,           bishop_white,   None],
                    [None,          pawn_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_white,     None,           None],
                    [None,          pawn_black,     None,           None,           None,           None,           pawn_black,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          bishop_black,   None,           knight_black,   queen_black,    None,           pawn_white,     None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           None]]
    
    assert_boards_are_same(test_board, board)
    # Test if en_passant_avail is None
    assert board._en_passant_avail == None
    # Test if White has the turn
    assert board._turn == TeamColor.WHITE

    print("Test Pawn Moves Passed!!!")


# Test promotion works
def test_pawn_promotion():
    # Create new board where's it's easy to promote
    board = Board("3b4/PPP4k/8/8/8/8/ppp5/3Q3K w - - 0 1")
    test_board = [  [None,          None,           None,           queen_white,    None,           None,           None,           king_white],
                    [pawn_black,    pawn_black,     pawn_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_white,    pawn_white,     pawn_white,     None,           None,           None,           None,           king_black],
                    [None,          None,           None,           bishop_black,   None,           None,           None,           None]]
    assert_boards_are_same(test_board, board)
    # Test if White has the turn
    assert board._turn == TeamColor.WHITE

    # Test promotion to knight
    assert board.move(Move.from_uci_str("a7a8n")) == True
    test_board = [  [None,          None,           None,           queen_white,    None,           None,           None,           king_white],
                    [pawn_black,    pawn_black,     pawn_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          pawn_white,     pawn_white,     None,           None,           None,           None,           king_black],
                    [knight_white,  None,           None,           bishop_black,   None,           None,           None,           None]]
    assert_boards_are_same(test_board, board)
    # Test if Black has the turn
    assert board._turn == TeamColor.BLACK

    # Test promotion to bishop
    assert board.move(Move.from_uci_str("a2a1b")) == True
    test_board = [  [bishop_black,  None,           None,           queen_white,    None,           None,           None,           king_white],
                    [None,          pawn_black,     pawn_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          pawn_white,     pawn_white,     None,           None,           None,           None,           king_black],
                    [knight_white,  None,           None,           bishop_black,   None,           None,           None,           None]]
    assert_boards_are_same(test_board, board)
    # Test if White has the turn
    assert board._turn == TeamColor.WHITE

    # Test promotion to rook
    assert board.move(Move.from_uci_str("b7b8r")) == True
    test_board = [  [bishop_black,  None,           None,           queen_white,    None,           None,           None,           king_white],
                    [None,          pawn_black,     pawn_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           pawn_white,     None,           None,           None,           None,           king_black],
                    [knight_white,  rook_white,     None,           bishop_black,   None,           None,           None,           None]]
    assert_boards_are_same(test_board, board)
    # Test if Black has the turn
    assert board._turn == TeamColor.BLACK

    # Test promotion to queen
    assert board.move(Move.from_uci_str("b2b1q")) == True
    test_board = [  [bishop_black,  queen_black,    None,           queen_white,    None,           None,           None,           king_white],
                    [None,          None,           pawn_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           pawn_white,     None,           None,           None,           None,           king_black],
                    [knight_white,  rook_white,     None,           bishop_black,   None,           None,           None,           None]]
    assert_boards_are_same(test_board, board)
    # Test if White has the turn
    assert board._turn == TeamColor.WHITE    

    # Test White promotion while capture
    assert board.move(Move.from_uci_str("c7d8q")) == True
    test_board = [  [bishop_black,  queen_black,    None,           queen_white,    None,           None,           None,           king_white],
                    [None,          None,           pawn_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [knight_white,  rook_white,     None,           queen_white,    None,           None,           None,           None]]
    assert_boards_are_same(test_board, board)
    # Test if Black has the turn
    assert board._turn == TeamColor.BLACK

    # Test Black promotion while capture
    assert board.move(Move.from_uci_str("c2d1n")) == True
    test_board = [  [bishop_black,  queen_black,    None,           knight_black,   None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [knight_white,  rook_white,     None,           queen_white,    None,           None,           None,           None]]
    assert_boards_are_same(test_board, board)
    # Test if White has the turn
    assert board._turn == TeamColor.WHITE

    print("Test Pawn Promotion Passed!!!")

# Test making king moves
# Make sure the king is moved
# Make sure the turn is switched
# Make sure nothing else moved
# Then do additional moves to test for castling
def test_king_moves():
    # Create the board
    board = Board()

    # The test board (how a chess board should be set up)
    test_board = default_board
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Make sure the king can't move through other pieces (in up, right, left, up right, up left directions)
    assert board.move(Move.from_uci_str("e1e2")) == False
    assert board.move(Move.from_uci_str("e1f1")) == False
    assert board.move(Move.from_uci_str("e1d1")) == False
    assert board.move(Move.from_uci_str("e1f2")) == False
    assert board.move(Move.from_uci_str("e1d2")) == False

    # Create default board just black moves first to test that the king can't move through other pieces
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Make sure the king can't move through other pieces (in down, right, left, down right, down left directions)
    assert board.move(Move.from_uci_str("e8e7")) == False
    assert board.move(Move.from_uci_str("e8f8")) == False
    assert board.move(Move.from_uci_str("e8d8")) == False
    assert board.move(Move.from_uci_str("e8f7")) == False
    assert board.move(Move.from_uci_str("e8d7")) == False

    # Create a new board where the king can move
    board = Board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    
    test_board = [  [rook_white,    None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that all castling rights are enabled
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure the king can move to the right
    # Also ensure that castling rights are removed for white
    assert board.move(Move.from_uci_str("e1f1")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           king_white,     None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if white castling rights are removed
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == False
    assert board._castling_rights.white_queenside == False

    # Make sure the king can move to the left
    # Also ensure that castling rights are removed for black
    assert board.move(Move.from_uci_str("e8d8")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           king_white,     None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           king_black,     None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check if white castling rights are removed
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == False
    assert board._castling_rights.white_kingside == False
    assert board._castling_rights.white_queenside == False

    # When refering to up and down, it is from the perspective of the white player (up is increase in row, down is decrease in row)
    # Make sure the king can move up
    assert board.move(Move.from_uci_str("f1f2")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           king_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           king_black,     None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    
    # Make sure the king can move down
    assert board.move(Move.from_uci_str("d8d7")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           king_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           king_black,     None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the king can move up right
    assert board.move(Move.from_uci_str("f2g3")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           king_white,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           king_black,     None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the king can move down right
    assert board.move(Move.from_uci_str("d7e6")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           king_white,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           king_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the king can move up left
    assert board.move(Move.from_uci_str("g3f4")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           king_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           king_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the king can move down left
    assert board.move(Move.from_uci_str("e6d5")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           king_white,     None,           None],
                    [None,          None,           None,           king_black,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    print("Test King Moves Passed!!!")

# Test Castling
def test_king_castling():
    castling_str = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
    board = Board(castling_str)

    # Use this castling board multiple times so assign to variable
    castling_board = [  [rook_white,    None,           None,           None,           king_white,     None,           None,           rook_white],
                        [None,          None,           None,           None,           None,           None,           None,           None],
                        [None,          None,           None,           None,           None,           None,           None,           None],
                        [None,          None,           None,           None,           None,           None,           None,           None],
                        [None,          None,           None,           None,           None,           None,           None,           None],
                        [None,          None,           None,           None,           None,           None,           None,           None],
                        [None,          None,           None,           None,           None,           None,           None,           None],
                        [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    test_board = castling_board

    # Check that castling is enabled for all teams
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure the white king can castle kingside
    assert board.move(Move.from_uci_str("e1g1")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           rook_white,     king_white,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for white
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == False
    assert board._castling_rights.white_queenside == False

    # Make sure the black king can castle queenside (can't castle kingside as white rook is attacking castling space)
    assert board.move(Move.from_uci_str("e8c8")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           rook_white,     king_white,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           king_black,     rook_black,     None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for black
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == False

    # Reset board and test queenside castling
    board = Board(castling_str)
    test_board = castling_board

    # Check that castling is enabled for all teams
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure the white king can castle queenside
    assert board.move(Move.from_uci_str("e1c1")) == True
    test_board = [  [None,          None,           king_white,     rook_white,     None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for white
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == False
    assert board._castling_rights.white_queenside == False

    # Make sure the black king can castle kingside (can't castle queenside as white rook is attacking castling space)
    assert board.move(Move.from_uci_str("e8g8")) == True
    test_board = [  [None,          None,           king_white,     rook_white,     None,           None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           None,           rook_black,     king_black,     None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for black
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == False
    assert board._castling_rights.white_kingside == False
    assert board._castling_rights.white_queenside == False

    # Make sure king can't castle when there is a piece in the way
    board = Board("rn2k2r/8/8/8/8/8/8/R3KB1R b KQkq - 0 1") # Note it's black's turn first
    test_board = [  [rook_white,    None,           None,           None,           king_white,     bishop_white,   None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    knight_black,   None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is enabled for all teams
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure the black king can't castle queenside
    assert board.move(Move.from_uci_str("e8c8")) == False
    # Castle kingside to make it whites's turn
    assert board.move(Move.from_uci_str("e8g8")) == True
    test_board = [  [rook_white,    None,           None,           None,           king_white,     bishop_white,   None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    knight_black,   None,           None,           None,           rook_black,     king_black,     None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for black
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == False
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure the white king can't castle kingside
    assert board.move(Move.from_uci_str("e1g1")) == False
    # Castle queenside to confirm the castle
    assert board.move(Move.from_uci_str("e1c1")) == True
    test_board = [  [None,          None,           king_white,     rook_white,     None,           bishop_white,   None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    knight_black,   None,           None,           None,           rook_black,     king_black,     None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for white
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == False
    assert board._castling_rights.white_kingside == False
    assert board._castling_rights.white_queenside == False
    
    # Check that black can't castle after moving
    board = Board("r3k2r/4B3/8/8/8/8/2b5/R3K2R b KQkq - 0 1") # Note it's black's turn first
    test_board = [  [rook_white,    None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           bishop_black,   None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           bishop_white,   None,           None,           None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is enabled for all teams
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure the black king can't castle either way as the space between where the king is and moves to is under attack
    assert board.move(Move.from_uci_str("e8g8")) == False
    assert board.move(Move.from_uci_str("e8c8")) == False
    # Move the black king to the down right to make it white's turn
    assert board.move(Move.from_uci_str("e8f7")) == True
    test_board = [  [rook_white,    None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           bishop_black,   None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           bishop_white,   king_black,     None,           None],
                    [rook_black,    None,           None,           None,           None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for black
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == False
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure the king can't castle, or spaces between the king and where it moves in the castle, when under attack
    board = Board("r3k2r/4B3/8/8/8/2b5/8/R3K2R w KQkq - 0 1") # Note it's black's turn first
    test_board = [  [rook_white,    None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           bishop_black,   None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           bishop_white,   None,           None,           None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the white king can't castle kingside nor queenside as the king is under attack
    assert board.move(Move.from_uci_str("e1g1")) == False
    assert board.move(Move.from_uci_str("e1c1")) == False

    # Test for black that if the position between where the rook starts and where the king will move (only on queenside) is 
    #   under attack it will not prevent castling
    # Test for white when attacking the position the king moves to (not in between) prevents castle
    board = Board("r3k2r/B7/8/8/8/4b3/8/R3K2R b KQkq - 0 1") # Note it's black's turn first
    test_board = [  [rook_white,    None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           bishop_black,   None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [bishop_white,  None,           None,           None,           None,           None,           None,           None],
                    [rook_black,    None,           None,           None,           king_black,     None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is enabled for all teams
    assert board._castling_rights.black_kingside == True
    assert board._castling_rights.black_queenside == True
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Castle queenside with the black king
    assert board.move(Move.from_uci_str("e8c8")) == True
    test_board = [  [rook_white,    None,           None,           None,           king_white,     None,           None,           rook_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           bishop_black,   None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [bishop_white,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,          king_black,      rook_black,     None,           None,           None,           rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Check that castling is disabled for black
    assert board._castling_rights.black_kingside == False
    assert board._castling_rights.black_queenside == False
    assert board._castling_rights.white_kingside == True
    assert board._castling_rights.white_queenside == True

    # Make sure white can't castle either way as the space the king moves to is under attack
    assert board.move(Move.from_uci_str("e1g1")) == False
    assert board.move(Move.from_uci_str("e1c1")) == False

    print("Test King Castling Passed!!!")


# Test king capturing
def test_king_capturing():
    # Create a new board where the king can capture
    board = Board("8/3P4/3PkP2/3NP3/8/3ppp2/3pKp2/3b4 w - - 0 1")
    # Set the test board to the initial capture board
    test_board = [  [None,          None,           None,           bishop_black,   None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     king_white,     pawn_black,     None,           None],
                    [None,          None,           None,           pawn_black,     pawn_black,     pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           knight_white,   pawn_white,     None,           None,           None],
                    [None,          None,           None,           pawn_white,     king_black,     pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Initially test left, up, right, down right, down left captures (then reset board and test down, up left, up right captures)
    # Make sure the white king can capture up-left
    assert board.move(Move.from_uci_str("e2d3")) == True
    test_board = [  [None,          None,           None,           bishop_black,   None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           king_white,     pawn_black,     pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           knight_white,   pawn_white,     None,           None,           None],
                    [None,          None,           None,           pawn_white,     king_black,     pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture down-left
    assert board.move(Move.from_uci_str("e6d5")) == True
    test_board = [  [None,          None,           None,           bishop_black,   None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           king_white,     pawn_black,     pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           king_black,     pawn_white,     None,           None,           None],
                    [None,          None,           None,           pawn_white,     None,           pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Up is from the perspective of the white player (up is increase in row, down is decrease in row)
    # Make sure the white king can capture right
    assert board.move(Move.from_uci_str("d3e3")) == True
    test_board = [  [None,          None,           None,           bishop_black,   None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           king_white,     pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           king_black,     pawn_white,     None,           None,           None],
                    [None,          None,           None,           pawn_white,     None,           pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture right
    assert board.move(Move.from_uci_str("d5e5")) == True
    test_board = [  [None,          None,           None,           bishop_black,   None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           king_white,     pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           king_black,     None,           None,           None],
                    [None,          None,           None,           pawn_white,     None,           pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the white king can capture down-left
    assert board.move(Move.from_uci_str("e3d2")) == True
    test_board = [  [None,          None,           None,           bishop_black,   None,           None,           None,           None],
                    [None,          None,           None,           king_white,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           king_black,     None,           None,           None],
                    [None,          None,           None,           pawn_white,     None,           pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture up-left
    assert board.move(Move.from_uci_str("e5d6")) == True
    test_board = [  [None,          None,           None,           bishop_black,   None,           None,           None,           None],
                    [None,          None,           None,           king_white,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           king_black,     None,           pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the white king can capture down
    assert board.move(Move.from_uci_str("d2d1")) == True
    test_board = [  [None,          None,           None,           king_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           king_black,     None,           pawn_white,     None,           None],
                    [None,          None,           None,           pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture up
    assert board.move(Move.from_uci_str("d6d7")) == True
    test_board = [  [None,          None,           None,           king_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_white,     None,           None],
                    [None,          None,           None,           king_black,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Reset the board to the capture board so we can test down, up left, and up right captures
    board = Board("4NR2/4kN2/8/8/8/3p1p2/4Kn2/4nb2 w - - 0 1")
    # Set the test board to the next capture board
    test_board = [  [None,          None,           None,           None,           knight_black,   bishop_black,   None,           None],
                    [None,          None,           None,           None,           king_white,     knight_black,   None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           king_black,     knight_white,   None,           None],
                    [None,          None,           None,           None,           knight_white,   rook_white,   None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the white king can capture down-right
    assert board.move(Move.from_uci_str("e2f1")) == True
    test_board = [  [None,          None,           None,           None,           knight_black,   king_white,     None,           None],
                    [None,          None,           None,           None,           None,           knight_black,   None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           king_black,     knight_white,   None,           None],
                    [None,          None,           None,           None,           knight_white,   rook_white,     None,           None]]
    # Check if the boards are the same
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture up-right
    assert board.move(Move.from_uci_str("e7f8")) == True
    test_board = [  [None,          None,           None,           None,           knight_black,   king_white,     None,           None],
                    [None,          None,           None,           None,           None,           knight_black,   None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           knight_white,   None,           None],
                    [None,          None,           None,           None,           knight_white,   king_black,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the white king can capture left
    assert board.move(Move.from_uci_str("f1e1")) == True
    test_board = [  [None,          None,           None,           None,           king_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           knight_black,   None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           knight_white,   None,           None],
                    [None,          None,           None,           None,           knight_white,   king_black,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture left
    assert board.move(Move.from_uci_str("f8e8")) == True
    test_board = [  [None,          None,           None,           None,           king_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           knight_black,   None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           knight_white,   None,           None],
                    [None,          None,           None,           None,           king_black,     None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the white king can capture up-right
    assert board.move(Move.from_uci_str("e1f2")) == True
    test_board = [  [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           king_white,     None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           knight_white,   None,           None],
                    [None,          None,           None,           None,           king_black,     None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture down-right
    assert board.move(Move.from_uci_str("e8f7")) == True
    test_board = [  [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           king_white,     None,           None],
                    [None,          None,           None,           pawn_black,     None,           pawn_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           king_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    
    # Make sure the white king can capture up
    assert board.move(Move.from_uci_str("f2f3")) == True
    test_board = [  [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     None,           king_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           king_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Reset the board to the capture board so we can test down for black (impossible to do with previous board)
    board = Board("8/5k2/5P2/8/3p1K2/8/8/8 b - - 0 1")
    # Set the test board to the next capture board
    test_board = [  [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     None,           king_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_white,     None,           None],
                    [None,          None,           None,           None,           None,           king_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Make sure the black king can capture down
    assert board.move(Move.from_uci_str("f7f6")) == True
    test_board = [  [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           pawn_black,     None,           king_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           king_black,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]

    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Tested capture in every direction
    # Test passed!
    print("Test King Capture Passed!!!")

# Test making invalid pawn moves
# Test moving more than 2 is invalid
# Test moving 2 not in starting position is invalid
# Test moving 1 when there is a piece in front is invalid
# Test moving 2 when there's a piece in the way is invalid
# Test moving 2 when there's a piece on the ending spot is invalid
# Test moving diagonal when no piece to capture is invalid
# Test en passant move is invalid after 1 turn
# Test invalid promotion by being in wrong row
# Test invalid promotion by sending invalid promotion piece type
def test_pawn_invalid_moves():
    pawn_inv_board_str = 'rnbqkbnr/pp1p1p1p/8/5Pp1/4p3/P1p5/1PPPP1PP/RNBQKBNR w KQkq g6 0 1'
    board = Board(pawn_inv_board_str)
    pawn_inv_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                        [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     None,           pawn_white,     pawn_white],
                        [pawn_white,    None,           pawn_black,     None,           None,           None,           None,           None],
                        [None,          None,           None,           None,           pawn_black,     None,           None,           None],
                        [None,          None,           None,           None,           None,           pawn_white,     pawn_black,     None],
                        [None,          None,           None,           None,           None,           None,           None,           None],
                        [pawn_black,    pawn_black,     None,           pawn_black,     None,           pawn_black,     None,           pawn_black],
                        [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    test_board = pawn_inv_board
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test moving pawn more than 2 is invalid
    assert board.move(Move.from_uci_str("a3a6")) == False
    assert board.move(Move.from_uci_str("b2a5")) == False
    assert board.move(Move.from_uci_str("b2a6")) == False

    # Test moving pawn 2 not in starting position is invalid
    assert board.move(Move.from_uci_str("a3a5")) == False

    # Test moving pawn 1 when there is a piece in front is invalid
    assert board.move(Move.from_uci_str("c2c3")) == False

    # Test moving pawn 2 when there's a piece in the way is invalid
    assert board.move(Move.from_uci_str("c2c4")) == False

    # Test moving 2 when there's a piece on the ending spot is invalid
    assert board.move(Move.from_uci_str("e2c4")) == False

    # Test moving diagonal when no piece to capture is invalid
    assert board.move(Move.from_uci_str("e2d3")) == False

    # Test en passant move is invalid after 1 turn
    # Check en passant is valid for pawn at g5
    print(board._en_passant_avail)
    assert board.move(Move.from_uci_str("f5g6")) == True
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     None,           pawn_white,     pawn_white],
                    [pawn_white,    None,           pawn_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           pawn_white,     None],
                    [pawn_black,    pawn_black,     None,           pawn_black,     None,           pawn_black,     None,           pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    
    # Reload board to test en passant is invalid after a move
    board = Board(pawn_inv_board_str)
    test_board = pawn_inv_board
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # First make a valid move as en passant is currently valid
    assert board.move(Move.from_uci_str("a3a4")) == True
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     None,           pawn_white,     pawn_white],
                    [None,          None,           pawn_black,     None,           None,           None,           None,           None],
                    [pawn_white,    None,           None,           None,           pawn_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_white,     pawn_black,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     None,           pawn_black,     None,           pawn_black,     None,           pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Second make another valid move for black so we can test next move
    assert board.move(Move.from_uci_str("b7b5")) == True
    test_board = [  [rook_white,    knight_white,   bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [None,          pawn_white,     pawn_white,     pawn_white,     pawn_white,     None,           pawn_white,     pawn_white],
                    [None,          None,           pawn_black,     None,           None,           None,           None,           None],
                    [pawn_white,    None,           None,           None,           pawn_black,     None,           None,           None],
                    [None,          pawn_black,     None,           None,           None,           pawn_white,     pawn_black,     None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    None,           None,           pawn_black,     None,           pawn_black,     None,           pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)
    # Now test en passant is invalid for pawn at g5
    assert board.move(Move.from_uci_str("f5g6")) == False

    # Test invalid promotion by being in wrong row
    # Create new board where's it's easy to promote
    board = Board("3b3k/1PP5/P7/8/8/p7/1pp5/3Q3K w - - 0 1")
    test_board = [  [None,          None,           None,           queen_white,    None,           None,           None,           king_white],
                    [None,          pawn_black,     pawn_black,     None,           None,           None,           None,           None],
                    [pawn_black,    None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_white,    None,           None,           None,           None,           None,           None,           None],
                    [None,          pawn_white,     pawn_white,     None,           None,           None,           None,           None],
                    [None,          None,           None,           bishop_black,   None,           None,           None,           king_black]]
    assert_boards_are_same(test_board, board)
    
    # Test promoting from wrong row is invalid
    assert board.move(Move.from_uci_str("a6a7q")) == False

    # Test promoting with invalid promotion piece type
    assert board.move(Move.from_uci_str("b7b8k")) == False
    assert board.move(Move.from_uci_str("c7c8p")) == False
    assert board.move(Move.from_uci_str("c7d8x")) == False

    print("Test Pawn Invalid Moves Passed!!!")
    

# Test making knight moves
# Test making valid knight moves in all directions
#   - up 2 left 1, up 2 right 1, up 1 left 2, up 1 right 2, down 2 left 1, down 2 right 1, down 1 left 2, down 1 right 2
# Test making capture as knight is valid
def test_knight_moves():
    board = Board()
    test_board = default_board
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making valid knight moves in all directions
    # up 2 left 1
    assert board.move(Move.from_uci_str("b1a3")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [knight_white,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    knight_black,   bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down 2 left 1
    assert board.move(Move.from_uci_str("b8a6")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [knight_white,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [knight_black,  None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # up 2 right 1
    assert board.move(Move.from_uci_str("a3b5")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          knight_white,   None,           None,           None,           None,           None,           None],
                    [knight_black,  None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down 2 right 1
    assert board.move(Move.from_uci_str("a6b4")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          knight_black,   None,           None,           None,           None,           None,           None],
                    [None,          knight_white,   None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down 1 right 2
    assert board.move(Move.from_uci_str("b5d4")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          knight_black,   None,           knight_white,   None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # up 1 right 2
    assert board.move(Move.from_uci_str("b4d5")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           knight_white,   None,           None,           None,           None],
                    [None,          None,           None,           knight_black,   None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # up 1 left 2
    assert board.move(Move.from_uci_str("d4b5")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          knight_white,   None,           knight_black,   None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down 1 left 2
    assert board.move(Move.from_uci_str("d5b4")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          knight_black,   None,           None,           None,           None,           None,           None],
                    [None,          knight_white,   None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making capture as knight is valid
    assert board.move(Move.from_uci_str("b5c7")) == True
    test_board = [  [rook_white,    None,           bishop_white,   queen_white,    king_white,     bishop_white,   knight_white,   rook_white],
                    [pawn_white,    pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white,     pawn_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          knight_black,   None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [pawn_black,    pawn_black,     knight_white,   pawn_black,     pawn_black,     pawn_black,     pawn_black,     pawn_black],
                    [rook_black,    None,           bishop_black,   queen_black,    king_black,     bishop_black,   knight_black,   rook_black]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    print("Test Knight Moves Passed!!!")


# Test making invalid knight moves
# Test moving correctly but piece on same team in spot to move is invalid
# Test moving an incorrect amount is invalid
def test_knight_invalid_moves():
    board = Board()
    test_board = default_board
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test moving correctly but piece on same team in spot to move is invalid
    assert board.move(Move.from_uci_str("b1d2")) == False
    assert board.move(Move.from_uci_str("g1e2")) == False

    # Test moving an incorrect amount is invalid
    assert board.move(Move.from_uci_str("b1c4")) == False
    assert board.move(Move.from_uci_str("b1d3")) == False
    assert board.move(Move.from_uci_str("b1d1")) == False
    assert board.move(Move.from_uci_str("b1c2")) == False

    assert board.move(Move.from_uci_str("g1f2")) == False
    assert board.move(Move.from_uci_str("g1d2")) == False
    assert board.move(Move.from_uci_str("g1f4")) == False
    assert board.move(Move.from_uci_str("g1e1")) == False

    print("Test Knight Invalid Moves Passed!!!")

# Test making bishop moves
# Test making valid bishop moves in all directions
#   - up left, up right, down left, down right
# Test making capture as bishop is valid
def test_bishop_moves():
    board = Board("1b3R2/8/8/7k/8/7K/8/1r3B2 w - - 0 1")
    test_board = [  [None,          rook_black,     None,           None,           None,           bishop_white,   None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          bishop_black,   None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making valid bishop moves in all directions
    # up left
    assert board.move(Move.from_uci_str("f1c4")) == True
    test_board = [  [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           bishop_white,   None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          bishop_black,   None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down right
    assert board.move(Move.from_uci_str("b8f4")) == True
    test_board = [  [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           bishop_white,   None,           None,           bishop_black,   None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down left
    assert board.move(Move.from_uci_str("c4a2")) == True
    test_board = [  [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [bishop_white,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           bishop_black,   None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # up right
    assert board.move(Move.from_uci_str("f4h6")) == True
    test_board = [  [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [bishop_white,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           bishop_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making capture as bishop is valid
    assert board.move(Move.from_uci_str("a2b1")) == True
    test_board = [  [None,          bishop_white,   None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           bishop_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Second test of making capture as bishop is valid
    assert board.move(Move.from_uci_str("h6f8")) == True
    test_board = [  [None,          bishop_white,   None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           bishop_black,   None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    print("Test Bishop Moves Passed!!!")


# Test making invalid bishop moves
# Test moving correctly but piece on same team in spot to move is invalid
# Test moving correctly but piece in way on other team is invalid
# Test moving an incorrect amount is invalid
def test_bishop_invalid_moves():
    board = Board("5R2/7k/4r3/1b6/2B2b2/7K/8/5B2 w - - 0 1")
    test_board = [  [None,          None,           None,           None,           None,           bishop_white,   None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           bishop_white,   None,           None,           bishop_black,   None,           None],
                    [None,          bishop_black,   None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           rook_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    board.print_board()
    assert_boards_are_same(test_board, board)

    # Test moving correctly but piece on same team in spot to move is invalid
    assert board.move(Move.from_uci_str("c4f1")) == False
    assert board.move(Move.from_uci_str("f1c3")) == False
    assert board.move(Move.from_uci_str("f1h3")) == False

    # Test moving correctly but piece in way on other team is invalid
    assert board.move(Move.from_uci_str("c4g8")) == False
    assert board.move(Move.from_uci_str("c4a6")) == False

    # Test moving an incorrect amount is invalid
    assert board.move(Move.from_uci_str("c4d6")) == False
    assert board.move(Move.from_uci_str("c4b2")) == False
    assert board.move(Move.from_uci_str("c4a3")) == False
    assert board.move(Move.from_uci_str("c4e5")) == False

    print("Test Bishop Invalid Moves Passed!!!")

# Test making rook moves
# Test making valid rook moves in all directions
#   - up, down, left, right
# Test making capture as rook is valid
def test_rook_moves():
    board = Board("1r3R2/4P2k/8/8/8/8/7K/br3R2 w - - 0 1")
    test_board = [  [bishop_black,  rook_black,     None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           king_black],
                    [None,          rook_black,     None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making valid rook moves in all directions
    # up
    assert board.move(Move.from_uci_str("f1f4")) == True
    test_board = [  [bishop_black,  rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           king_black],
                    [None,          rook_black,     None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down
    assert board.move(Move.from_uci_str("b8b3")) == True
    test_board = [  [bishop_black,  rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           king_black],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # left
    assert board.move(Move.from_uci_str("f8a8")) == True
    test_board = [  [bishop_black,  rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           king_black],
                    [rook_white,    None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # right
    assert board.move(Move.from_uci_str("b1e1")) == True
    test_board = [  [bishop_black,  None,           None,           None,           rook_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           king_black],
                    [rook_white,    None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making capture as rook is valid
    assert board.move(Move.from_uci_str("a8a1")) == True
    test_board = [  [rook_white,    None,           None,           None,           rook_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test again making capture as rook is valid with black
    assert board.move(Move.from_uci_str("e1e7")) == True
    test_board = [  [rook_white,    None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          rook_black,     None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           rook_black,     None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    print("Test Rook Moves Passed!!!")

# Test making invalid rook moves
# Test moving correctly but piece on same team in spot to move is invalid
# Test moving correctly but piece in the way is invalid
# Test moving in multiple directions is invalid
def test_rook_invalid_moves():
    board = Board("1r3R2/7k/8/8/5P2/8/7K/nr3R2 w - - 0 1")
    test_board = [  [knight_black,  rook_black,     None,           None,           None,           rook_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          rook_black,     None,           None,           None,           rook_white,     None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test moving correctly but piece on same team in spot to move is invalid
    assert board.move(Move.from_uci_str("f1f4")) == False
    assert board.move(Move.from_uci_str("f8f4")) == False

    # Test moving correctly but piece in the way is invalid
    assert board.move(Move.from_uci_str("f1f7")) == False
    assert board.move(Move.from_uci_str("f8f2")) == False
    assert board.move(Move.from_uci_str("f1a1")) == False
    assert board.move(Move.from_uci_str("f8a8")) == False

    # Test moving in multiple directions is invalid
    assert board.move(Move.from_uci_str("f1e3")) == False
    assert board.move(Move.from_uci_str("f8d6")) == False
    assert board.move(Move.from_uci_str("f1h3")) == False
    assert board.move(Move.from_uci_str("f8h6")) == False

    print("Test Rook Invalid Moves Passed!!!")

# Test making queen moves
# Test making valid queen moves in all directions
#   - up, down, left, right, up left, up right, down left, down right
# Test making capture as queen is valid (in both diagonal and straight directions)
def test_queen_moves():
    board = Board("1q6/4P3/8/7K/8/8/7k/b4Q2 w - - 0 1")
    test_board = [  [bishop_black,  None,           None,           None,           None,           queen_white,    None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          queen_black,    None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making valid queen moves in all directions
    # up
    assert board.move(Move.from_uci_str("f1f6")) == True
    test_board = [  [bishop_black,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           queen_white,    None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          queen_black,    None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down
    assert board.move(Move.from_uci_str("b8b1")) == True
    test_board = [  [bishop_black,  queen_black,    None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           queen_white,    None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # left
    assert board.move(Move.from_uci_str("f6a6")) == True
    test_board = [  [bishop_black,  queen_black,    None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [queen_white,   None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # right
    assert board.move(Move.from_uci_str("b1g1")) == True
    test_board = [  [bishop_black,  None,           None,           None,           None,           None,           queen_black,    None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [queen_white,   None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down right
    assert board.move(Move.from_uci_str("a6d3")) == True
    test_board = [  [bishop_black,  None,           None,           None,           None,           None,           queen_black,    None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           queen_white,    None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # up left
    assert board.move(Move.from_uci_str("g1b6")) == True
    test_board = [  [bishop_black,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           queen_white,    None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          queen_black,    None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # down left
    assert board.move(Move.from_uci_str("d3b1")) == True
    test_board = [  [bishop_black,  queen_white,    None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          queen_black,    None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # up right
    assert board.move(Move.from_uci_str("b6d8")) == True
    test_board = [  [bishop_black,  queen_white,    None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           queen_black,    None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test making capture as queen is valid (in both diagonal and straight directions)
    # Straight direction
    assert board.move(Move.from_uci_str("b1a1")) == True
    test_board = [  [queen_white,  None,            None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           pawn_white,     None,           None,           None],
                    [None,          None,           None,           queen_black,    None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Diagonal direction
    assert board.move(Move.from_uci_str("d8e7")) == True
    test_board = [  [queen_white,  None,            None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           queen_black,    None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    print("Test Queen Moves Passed!!!")

# Test making invalid queen moves
# Test moving correctly but piece on same team in spot to move is invalid
# Test moving correctly but with a piece in way is invalid
# Test moving an incorrect amount is invalid
def test_queen_invalid_moves():
    board = Board("8/7k/5P2/2r1p3/8/Q2p4/7K/B1N5 w - - 0 1")
    test_board = [  [bishop_white,  None,           knight_white,   None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white],
                    [queen_white,   None,           None,           pawn_black,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           rook_black,     None,           pawn_black,     None,           None,           None],
                    [None,          None,           None,           None,           None,           pawn_white,     None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test moving correctly but piece on same team in spot to move is invalid
    assert board.move(Move.from_uci_str("a3a1")) == False
    assert board.move(Move.from_uci_str("a3c1")) == False

    # Test moving correctly but with a piece in way is invalid
    assert board.move(Move.from_uci_str("a3d6")) == False
    assert board.move(Move.from_uci_str("a3h3")) == False

    # Test moving an incorrect amount is invalid
    assert board.move(Move.from_uci_str("a3b5")) == False
    assert board.move(Move.from_uci_str("a3c2")) == False
    assert board.move(Move.from_uci_str("a3h8")) == False
    assert board.move(Move.from_uci_str("a3e1")) == False

# Test making invalid king moves
# Test moving correctly but piece on same team in spot to move is invalid
# Test king cannot move more than one in any direction
def test_king_invalid_moves():
    board = Board("8/7k/8/2r5/4N3/Q4K2/8/B7 w - - 0 1")
    test_board = [  [bishop_white,  None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [queen_white,   None,           None,           None,           None,           king_white,     None,           None],
                    [None,          None,           None,           None,           knight_white,   None,           None,           None],
                    [None,          None,           rook_black,     None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_black],
                    [None,          None,           None,           None,           None,           None,           None,           None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test moving correctly but piece on same team in spot to move is invalid
    assert board.move(Move.from_uci_str("f3e4")) == False

    # Test king cannot move more than one in any direction
    assert board.move(Move.from_uci_str("f3f5")) == False
    assert board.move(Move.from_uci_str("f3d5")) == False
    assert board.move(Move.from_uci_str("f3d3")) == False
    assert board.move(Move.from_uci_str("f3d1")) == False
    assert board.move(Move.from_uci_str("f3f1")) == False
    assert board.move(Move.from_uci_str("f3h1")) == False
    assert board.move(Move.from_uci_str("f3h3")) == False
    assert board.move(Move.from_uci_str("f3h5")) == False


# Test get_turn_color
# Init the board to white turn and make sure it returns correctly
# Do the same for black
def test_get_turn_color():
    board = Board()
    assert board.get_turn_color() == board._turn and board._turn == TeamColor.WHITE
    board.move(Move.from_uci_str("e2e4")) # Move white pawn just to change turn
    assert board.get_turn_color() == board._turn and board._turn == TeamColor.BLACK

    # Start with black
    board = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1')
    assert board.get_turn_color() == board._turn and board._turn == TeamColor.BLACK
    board.move(Move.from_uci_str("e7e5")) # Move black pawn just to change turn
    assert board.get_turn_color() == board._turn and board._turn == TeamColor.WHITE

# Test _ind_in_board
# Test with valid indexes
# Test with invalid indices in each direction (< 0 and > 7)
def test_ind_in_board():
    board = Board()
    # Test with valid indexes
    assert board._ind_in_board(0) == True
    assert board._ind_in_board(7) == True
    assert board._ind_in_board(4) == True

    # Test with invalid indices in each direction (< 0 and > 7)
    assert board._ind_in_board(-1) == False
    assert board._ind_in_board(8) == False
    assert board._ind_in_board(100) == False

# Test _coord_in_board
# Test with valid coordinates
# Test with invalid coordinates in each direction (< 0 and > 7 for row and for column)
def test_coord_in_board():
    board = Board()
    # Test with valid coordinates
    assert board._coord_in_board(Coordinate(0, 0)) == True
    assert board._coord_in_board(Coordinate(7, 7)) == True
    assert board._coord_in_board(Coordinate(4, 5)) == True

    # Test with invalid coordinates in each direction (< 0 and > 7 for row and for column)
    assert board._coord_in_board(Coordinate(-1, 0)) == False
    assert board._coord_in_board(Coordinate(0, -1)) == False
    assert board._coord_in_board(Coordinate(-1, -1)) == False
    assert board._coord_in_board(Coordinate(-10, -4)) == False
    assert board._coord_in_board(Coordinate(8, 0)) == False
    assert board._coord_in_board(Coordinate(0, 8)) == False
    assert board._coord_in_board(Coordinate(8, 8)) == False
    assert board._coord_in_board(Coordinate(12, 19)) == False

# Test _str_to_int
# Test string of digits
# Test string without digits is invalid (returns none)
# Test string with some digits but not fully digits is invalid (returns none)
def test_str_to_int():
    board = Board()
    # Test string of digits
    assert board._str_to_int("123") == 123
    assert board._str_to_int("00") == 0
    assert board._str_to_int("0001") == 1
    assert board._str_to_int("99999") == 99999

    # Test string without digits is invalid (returns none)
    assert board._str_to_int("abcd") == None
    assert board._str_to_int("~ms#") == None
    assert board._str_to_int("m sq") == None
    assert board._str_to_int("ABCD") == None

    # Test string with some digits but not fully digits is invalid (returns none)
    assert board._str_to_int("a123") == None
    assert board._str_to_int("123a") == None
    assert board._str_to_int("a1b2") == None
    assert board._str_to_int("~1#2") == None

# Test _get_pawn_direction
# Test white pawn direction
# Test black pawn direction
def test_get_pawn_direction():
    board = Board()
    # Test white pawn direction
    assert board._get_pawn_direction(TeamColor.WHITE) == 1

    # Test black pawn direction
    assert board._get_pawn_direction(TeamColor.BLACK) == -1

# Test _get_pawn_starting_row
# Test white pawn starting row
# Test black pawn starting row
def test_get_pawn_starting_row():
    board = Board()
    # Test white pawn starting row
    assert board._get_pawn_starting_row(TeamColor.WHITE) == 1

    # Test black pawn starting row
    assert board._get_pawn_starting_row(TeamColor.BLACK) == 6

# Test _get_pawn_promotion_row
# Test white pawn promotion row
# Test black pawn promotion row
def test_get_pawn_promotion_row():
    board = Board()
    # Test white pawn promotion row
    assert board._get_pawn_promotion_row(TeamColor.WHITE) == 7

    # Test black pawn promotion row
    assert board._get_pawn_promotion_row(TeamColor.BLACK) == 0

# Test Coordinate equivalence
# Test set of coordinates are equivalent (same row and column)
# Test set of coordinates are not equivalent (different row or column - make sure sometimes one is the same)
def test_coordinate_equivalence():
    board = Board()
    # Test set of coordinates are equivalent (same row and column)
    assert Coordinate(0, 0) == Coordinate(0, 0)
    assert Coordinate(7, 7) == Coordinate(7, 7)
    assert Coordinate(4, 5) == Coordinate(4, 5)

    # Test set of coordinates are not equivalent (different row or column - make sure sometimes one is the same)
    assert Coordinate(0, 0) != Coordinate(0, 1)
    assert Coordinate(0, 0) != Coordinate(1, 0)
    assert Coordinate(1, 0) != Coordinate(1, 1)
    assert Coordinate(4, 3) != Coordinate(7, 7)
    assert Coordinate(3, 1) != Coordinate(7, 0)
    assert Coordinate(1, 7) != Coordinate(0, 7)

# Test Piece equivalence
# Test set of pieces are equivalent (same type and color)
# Test set of pieces are not equivalent (different type or color - make sure sometimes one is the same)
def test_piece_equivalence():
    board = Board()
    # Test set of pieces are equivalent (same type and color)
    assert Piece(PieceType.PAWN, TeamColor.WHITE) == Piece(PieceType.PAWN, TeamColor.WHITE)
    assert Piece(PieceType.ROOK, TeamColor.BLACK) == Piece(PieceType.ROOK, TeamColor.BLACK)
    assert Piece(PieceType.KNIGHT, TeamColor.WHITE) == Piece(PieceType.KNIGHT, TeamColor.WHITE)
    assert Piece(PieceType.BISHOP, TeamColor.BLACK) == Piece(PieceType.BISHOP, TeamColor.BLACK)
    assert Piece(PieceType.QUEEN, TeamColor.WHITE) == Piece(PieceType.QUEEN, TeamColor.WHITE)
    assert Piece(PieceType.KING, TeamColor.BLACK) == Piece(PieceType.KING, TeamColor.BLACK)

    # Test set of pieces are not equivalent (different type or color - make sure sometimes one is the same)
    # Different color
    assert Piece(PieceType.PAWN, TeamColor.WHITE) != Piece(PieceType.PAWN, TeamColor.BLACK)
    assert Piece(PieceType.ROOK, TeamColor.WHITE) != Piece(PieceType.ROOK, TeamColor.BLACK)
    assert Piece(PieceType.KNIGHT, TeamColor.WHITE) != Piece(PieceType.KNIGHT, TeamColor.BLACK)
    assert Piece(PieceType.BISHOP, TeamColor.WHITE) != Piece(PieceType.BISHOP, TeamColor.BLACK)
    assert Piece(PieceType.QUEEN, TeamColor.WHITE) != Piece(PieceType.QUEEN, TeamColor.BLACK)

    # Different type
    assert Piece(PieceType.PAWN, TeamColor.WHITE) != Piece(PieceType.ROOK, TeamColor.WHITE)
    assert Piece(PieceType.ROOK, TeamColor.WHITE) != Piece(PieceType.KNIGHT, TeamColor.WHITE)
    assert Piece(PieceType.KNIGHT, TeamColor.WHITE) != Piece(PieceType.BISHOP, TeamColor.WHITE)
    assert Piece(PieceType.BISHOP, TeamColor.BLACK) != Piece(PieceType.QUEEN, TeamColor.BLACK)
    assert Piece(PieceType.QUEEN, TeamColor.BLACK) != Piece(PieceType.KING, TeamColor.BLACK)

    # Different type and color
    assert Piece(PieceType.PAWN, TeamColor.WHITE) != Piece(PieceType.ROOK, TeamColor.BLACK)
    assert Piece(PieceType.ROOK, TeamColor.WHITE) != Piece(PieceType.KNIGHT, TeamColor.BLACK)
    assert Piece(PieceType.KNIGHT, TeamColor.WHITE) != Piece(PieceType.BISHOP, TeamColor.BLACK)
    assert Piece(PieceType.BISHOP, TeamColor.BLACK) != Piece(PieceType.QUEEN, TeamColor.WHITE)
    assert Piece(PieceType.QUEEN, TeamColor.BLACK) != Piece(PieceType.KING, TeamColor.WHITE)

# Test _move_to_move_str
# Test with valid indexes without promotion
# Test with valid indexes with promotion
# Test with invalid indexes (invalid promotion)
# Random generate indexes and make sure they are valid
def test_move_to_move_str():
    # Test with valid indexes without promotion
    assert Move.to_uci_str(Move(Coordinate(0, 0), Coordinate(0, 1), None)) == "a1b1"
    assert Move.to_uci_str(Move(Coordinate(7, 7), Coordinate(7, 6), None)) == "h8g8"
    assert Move.to_uci_str(Move(Coordinate(1, 4), Coordinate(6, 2), None)) == "e2c7"

    # Test with valid indexes with promotion
    assert Move.to_uci_str(Move(Coordinate(1, 3), Coordinate(0, 4), PieceType.QUEEN)) == "d2e1q"
    assert Move.to_uci_str(Move(Coordinate(6, 7), Coordinate(7, 7), PieceType.ROOK)) == "h7h8r"
    assert Move.to_uci_str(Move(Coordinate(1, 6), Coordinate(0, 5), PieceType.KNIGHT)) == "g2f1n"
    assert Move.to_uci_str(Move(Coordinate(6, 0), Coordinate(7, 1), PieceType.BISHOP)) == "a7b8b"

    # Test with invalid indexes (invalid promotion)
    assert Move.to_uci_str(Move(Coordinate(6, 0), Coordinate(7, 1), PieceType.KING)) == None
    assert Move.to_uci_str(Move(Coordinate(3, 4), Coordinate(1, 4), PieceType.PAWN)) == None

    # Random generate indexes and make sure they are valid
    for _ in range(NUM_RAND_MOVE_STR_TO_MOVE_TESTS):
        # Generate random rows and columns
        rand_from_row = randrange(8) # 0-7 for Move class -> 1-8 for move string
        rand_from_col = randrange(8)

        rand_to_row = randrange(8) # 0-7 for Move class -> 1-8 for move string
        rand_to_col = randrange(8)

        # If moving to the same spot (invalid) then generate new random to spot
        while (rand_from_row == rand_to_row and rand_from_col == rand_to_col):
            rand_to_row = randrange(8)
            rand_to_col = randrange(8)

        # Generate random move
        rand_move = Move(Coordinate(rand_from_row, rand_from_col), Coordinate(rand_to_row, rand_to_col), None)
        rand_move_str = chr(rand_from_col + ord('a')) + str(rand_from_row + 1) + chr(rand_to_col + ord('a')) + str(rand_to_row + 1)
        print(rand_move_str)

        # Test the move
        assert Move.to_uci_str(rand_move) == rand_move_str

# Test score
# Test even score with same pieces on both sides
# Test white winning
# Test black winning
# Test random values
def test_score():
    board = Board()

    # Test even score with same pieces on both sides
    assert board._count_material() == 0

    # Test white winning
    board = Board("4k3/p7/8/8/8/8/8/RNBQKBNR w - - 0 1")
    # kings on opposite teams cancel out
    pos_score =  2 * rook_val + 2 * knight_val + 2 * bishop_val + queen_val - pawn_val
    assert board._count_material() == pos_score

    # Test black winning
    board = Board("r2qkbn1/p7/8/8/8/8/8/4K3 b - - 0 1")
    # kings on opposite teams cancel out
    pos_score = rook_val + knight_val + bishop_val + queen_val + pawn_val
    assert board._count_material() == -pos_score

    # Test random values
    for _ in range(NUM_RAND_COUNT_MATERIAL_TESTS):
        fen_str = generate_random_fen_str()
        white_score = get_white_score_from_fen_str(fen_str)

        # Create the board and test the score
        board = Board(fen_str)
        print(fen_str)
        board.print_board()
        assert board._count_material() == white_score

# Test _get_pieces
# Test getting all pieces
# Test getting only white pieces
# Test getting only black pieces
# Test getting only of each piece type
# Test getting a specfic piece type for a specfic team
# Test randomly generated boards
def test_get_pieces():
    board = Board()
    # Test getting all pieces
    all_pieces = board._get_pieces()
    # Go through board and ensure all pieces are in list
    for row in range(len(board._board_arr)):
        for col in range(len(board._board_arr[0])):
            # If there is a piece at this coordinate then make sure it's in the list
            if board._board_arr[row][col] != None:
                # Create the piece coordinate for the piece at this coordinate
                piece_coord = PieceCoordinate(board._board_arr[row][col], Coordinate(row, col))
                # Make sure the piece coordinate is in the list
                assert piece_coord in all_pieces
                # Remove piece coordinate from list so we can check if there are any pieces left at the end
                all_pieces.remove(piece_coord)
    # Make sure there are no pieces left in the list
    assert len(all_pieces) == 0

    # Test getting only white pieces
    white_pieces = board._get_pieces(team_color=TeamColor.WHITE)
    # Go through board and ensure all pieces are in list
    for row in range(len(board._board_arr)):
        for col in range(len(board._board_arr[0])):
            # If there is a piece at this coordinate then make sure it's in the list
            if board._board_arr[row][col] != None:
                 # Create the piece coordinate for the piece at this coordinate
                piece_coord = PieceCoordinate(board._board_arr[row][col], Coordinate(row, col))
                # Check if the piece is white
                if board._board_arr[row][col].Color == TeamColor.WHITE:
                    # Make sure the piece coordinate is in the list
                    assert piece_coord in white_pieces
                    # Remove piece coordinate from list so we can check if there are any pieces left at the end
                    white_pieces.remove(piece_coord)
                else:
                    # Black piece
                    # Make sure the piece coordinate is not in the list
                    assert piece_coord not in white_pieces
    # Make sure there are no pieces left in the list
    assert len(white_pieces) == 0

    # Test getting only black pieces
    black_pieces = board._get_pieces(team_color=TeamColor.BLACK)
    # Go through board and ensure all pieces are in list
    for row in range(len(board._board_arr)):
        for col in range(len(board._board_arr[0])):
            # If there is a piece at this coordinate then make sure it's in the list
            if board._board_arr[row][col] != None:
                 # Create the piece coordinate for the piece at this coordinate
                piece_coord = PieceCoordinate(board._board_arr[row][col], Coordinate(row, col))
                # Check if the piece is black
                if board._board_arr[row][col].Color == TeamColor.BLACK:
                    # Make sure the piece coordinate is in the list
                    assert piece_coord in black_pieces
                    # Remove piece coordinate from list so we can check if there are any pieces left at the end
                    black_pieces.remove(piece_coord)
                else:
                    # White piece
                    # Make sure the piece coordinate is not in the list
                    assert piece_coord not in black_pieces
    # Make sure there are no pieces left in the list
    assert len(black_pieces) == 0

    # Test getting only of each piece type
    # Pawn pieces
    pawn_pieces = board._get_pieces(piece_type=PieceType.PAWN)
    # Go through board and ensure all pieces are in list
    for row in range(len(board._board_arr)):
        for col in range(len(board._board_arr[0])):
            # If there is a piece at this coordinate then make sure it's in the list
            if board._board_arr[row][col] != None:
                 # Create the piece coordinate for the piece at this coordinate
                piece_coord = PieceCoordinate(board._board_arr[row][col], Coordinate(row, col))
                # Check if the piece is a pawn
                if board._board_arr[row][col].Type == PieceType.PAWN:
                    # Make sure the piece coordinate is in the list
                    assert piece_coord in pawn_pieces
                    # Remove piece coordinate from list so we can check if there are any pieces left at the end
                    pawn_pieces.remove(piece_coord)
                else:
                    # Not a pawn piece
                    # Make sure the piece coordinate is not in the list
                    assert piece_coord not in pawn_pieces
    # Make sure there are no pieces left in the list
    assert len(pawn_pieces) == 0

    # Rook pieces
    rook_pieces = board._get_pieces(piece_type=PieceType.ROOK)
    rook_expected_pieces = [    PieceCoordinate(Piece(PieceType.ROOK, TeamColor.WHITE), Coordinate(0, 0)), 
                                PieceCoordinate(Piece(PieceType.ROOK, TeamColor.WHITE), Coordinate(0, 7)), 
                                PieceCoordinate(Piece(PieceType.ROOK, TeamColor.BLACK), Coordinate(7, 0)), 
                                PieceCoordinate(Piece(PieceType.ROOK, TeamColor.BLACK), Coordinate(7, 7))]
    # Check that the expected pieces and the pieces returned are the same
    # Use set to ignore order
    assert set(rook_pieces) == set(rook_expected_pieces)

    # Knight pieces
    knight_pieces = board._get_pieces(piece_type=PieceType.KNIGHT)
    knight_expected_pieces = [  PieceCoordinate(Piece(PieceType.KNIGHT, TeamColor.WHITE), Coordinate(0, 1)),
                                PieceCoordinate(Piece(PieceType.KNIGHT, TeamColor.WHITE), Coordinate(0, 6)),
                                PieceCoordinate(Piece(PieceType.KNIGHT, TeamColor.BLACK), Coordinate(7, 1)),
                                PieceCoordinate(Piece(PieceType.KNIGHT, TeamColor.BLACK), Coordinate(7, 6))]
    # Check that the expected pieces and the pieces returned are the same
    assert set(knight_pieces) == set(knight_expected_pieces)

    # Bishop pieces
    bishop_pieces = board._get_pieces(piece_type=PieceType.BISHOP)
    bishop_expected_pieces = [  PieceCoordinate(Piece(PieceType.BISHOP, TeamColor.WHITE), Coordinate(0, 2)),
                                PieceCoordinate(Piece(PieceType.BISHOP, TeamColor.WHITE), Coordinate(0, 5)),
                                PieceCoordinate(Piece(PieceType.BISHOP, TeamColor.BLACK), Coordinate(7, 2)),
                                PieceCoordinate(Piece(PieceType.BISHOP, TeamColor.BLACK), Coordinate(7, 5))]
    # Check that the expected pieces and the pieces returned are the same
    assert set(bishop_pieces) == set(bishop_expected_pieces)
    
    # Queen pieces
    queen_pieces = board._get_pieces(piece_type=PieceType.QUEEN)
    queen_expected_pieces = [   PieceCoordinate(Piece(PieceType.QUEEN, TeamColor.WHITE), Coordinate(0, 3)),
                                PieceCoordinate(Piece(PieceType.QUEEN, TeamColor.BLACK), Coordinate(7, 3))]
    # Check that the expected pieces and the pieces returned are the same
    assert set(queen_pieces) == set(queen_expected_pieces)

    # King pieces
    king_pieces = board._get_pieces(piece_type=PieceType.KING)
    king_expected_pieces = [    PieceCoordinate(Piece(PieceType.KING, TeamColor.WHITE), Coordinate(0, 4)),
                                PieceCoordinate(Piece(PieceType.KING, TeamColor.BLACK), Coordinate(7, 4))]
    # Check that the expected pieces and the pieces returned are the same
    assert set(king_pieces) == set(king_expected_pieces)

    # Test getting a specfic piece type for a specfic team
    # White pawn pieces
    white_pawn_pieces = board._get_pieces(PieceType.PAWN, TeamColor.WHITE)
    white_pawn_expected_pieces = [  PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 0)),
                                    PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 1)),
                                    PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 2)),
                                    PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 3)),
                                    PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 4)),
                                    PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 5)),
                                    PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 6)),
                                    PieceCoordinate(Piece(PieceType.PAWN, TeamColor.WHITE), Coordinate(1, 7))]
    # Check that the expected pieces and the pieces returned are the same
    assert set(white_pawn_pieces) == set(white_pawn_expected_pieces)

    # Black bishop pieces
    black_bishop_pieces = board._get_pieces(PieceType.BISHOP, TeamColor.BLACK)
    black_bishop_expected_pieces = [    PieceCoordinate(Piece(PieceType.BISHOP, TeamColor.BLACK), Coordinate(7, 2)),
                                        PieceCoordinate(Piece(PieceType.BISHOP, TeamColor.BLACK), Coordinate(7, 5))]
    # Check that the expected pieces and the pieces returned are the same
    assert set(black_bishop_pieces) == set(black_bishop_expected_pieces)

    # Test randomly generated boards
    for _ in range(NUM_RAND_GET_PIECES_TESTS):
        # Get random piece and color to test getting pieces for (if none just means all of that type)
        #   EX: None for color means both black and white teams
        random_piece = randrange(7)
        random_piece = PieceType(random_piece) if random_piece != 6 else None

        random_color = randrange(3)
        random_color = TeamColor(random_color) if random_color != 2 else None

        random_num_moves = randrange(5)

        move_failed = True
        while (move_failed):
            # Generate random board
            fen_str = generate_random_fen_str()
            print("FEN Str: " + fen_str)
            # Create the board
            board = Board(fen_str)
            board.print_board()
            board._print_attack_arr()

            # Make random number of moves (up to 4)
            for _ in range(random_num_moves):
                # Get all the legal moves
                moves = board.get_all_legal_moves()
                if (len(moves) > 0):
                    # Choose a random move
                    random_move_ind = randrange(len(moves))
                    print("Move: " + str(moves[random_move_ind]))
                    assert board.move(moves[random_move_ind]) == True
                    board.print_board()
                    board._print_attack_arr()
                else:
                    # Ideally wouldn't be in checkmake in under 4 moves but not impossible (not testing get_all_legal_moves here, so just generate new string)
                    # Break so we can try loop again
                    break
            
            # All moves were made and none failed (break loop)
            move_failed = False


        # Get all the pieces
        all_pieces = board._get_pieces(random_piece, random_color)
        # Go through board and ensure all pieces are in list
        for row in range(len(board._board_arr)):
            for col in range(len(board._board_arr[0])):
                # If there is a piece at this coordinate then make sure it's in the list
                if board._board_arr[row][col] != None:
                    # Create the piece coordinate for the piece at this coordinate
                    piece_coord = PieceCoordinate(board._board_arr[row][col], Coordinate(row, col))
                    # Check if the piece is the right type and/or color (if None just ignore that part of the check)
                    if ((random_piece == None or board._board_arr[row][col].Type == random_piece) and 
                        (random_color == None or board._board_arr[row][col].Color == random_color)):
                        # Make sure the piece coordinate is in the list
                        assert piece_coord in all_pieces
                        # Remove piece coordinate from list so we can check if there are any pieces left at the end
                        all_pieces.remove(piece_coord)
                    else:
                        # Make sure the piece coordinate is not in the list
                        assert piece_coord not in all_pieces
        # Make sure there are no pieces left in the list
        assert len(all_pieces) == 0


# Test _rook_or_bishop_clear_path
# Test clear path for rook with no pieces in the way
# Test clear path for rook with pieces in the way
# Test clear path for bishop with no pieces in the way
# Test clear path for bishop with pieces in the way
def test_rook_or_bishop_clear_path():
    board = Board("5Kn1/6p1/P2B4/1P4R1/1p6/p1rb4/4k3/8 w - - 0 1")
    test_board = [  [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          None,           None,           None,           king_black,     None,           None,           None],
                    [pawn_black,    None,           rook_black,     bishop_black,   None,           None,           None,           None],
                    [None,          pawn_black,     None,           None,           None,           None,           None,           None],
                    [None,          pawn_white,     None,           None,           None,           None,           rook_white,     None],
                    [pawn_white,    None,           None,           bishop_white,   None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           pawn_black,     None],
                    [None,          None,           None,           None,           None,           king_white,     knight_black,    None]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test clear path for rook with no pieces in the way (or piece on place it's moving to - just not in the middle) is valid
    # White rook
    assert board._rook_or_bishop_clear_path(Move(Coordinate(4, 6), Coordinate(0, 6))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(4, 6), Coordinate(6, 6))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(4, 6), Coordinate(4, 2))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(4, 6), Coordinate(4, 1))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(4, 6), Coordinate(4, 7))) == True

    # Black rook
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 2), Coordinate(0, 2))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 2), Coordinate(7, 2))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 2), Coordinate(2, 3))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 2), Coordinate(2, 1))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 2), Coordinate(2, 0))) == True

    # Test clear path for rook with pieces in the way is not valid
    # White rook
    assert board._rook_or_bishop_clear_path(Move(Coordinate(4, 6), Coordinate(7, 6))) == False
    assert board._rook_or_bishop_clear_path(Move(Coordinate(4, 6), Coordinate(4, 0))) == False

    # Black rook
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 2), Coordinate(2, 4))) == False

    # Test clear path for bishop with no pieces in the way (or piece on place it's moving to - just not in the middle) is valid
    # White bishop
    assert board._rook_or_bishop_clear_path(Move(Coordinate(5, 3), Coordinate(1, 7))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(5, 3), Coordinate(7, 1))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(5, 3), Coordinate(7, 5))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(5, 3), Coordinate(3, 1))) == True

    # Black bishop
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 3), Coordinate(0, 1))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 3), Coordinate(1, 4))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 3), Coordinate(6, 7))) == True
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 3), Coordinate(4, 1))) == True

    # Test clear path for bishop with pieces in the way is not valid
    # White bishop
    assert board._rook_or_bishop_clear_path(Move(Coordinate(5, 3), Coordinate(2, 0))) == False

    # Black bishop
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 3), Coordinate(0, 5))) == False
    assert board._rook_or_bishop_clear_path(Move(Coordinate(2, 3), Coordinate(5, 0))) == False

# Test _get_spaces_available_in_move_dir
# Test with no spaces available in all directions (should return 0)
# Test with at least 1 space available in all directions
# Test with max space avaiable (should be the max_spaces input)
def test_get_spaces_available_in_move_dir():
    board = Board("7K/1NPP4/1PqP1Q2/1PPP4/8/1ppp4/1pqp3k/1nnn4 w - - 0 1")
    test_board = [  [None,          knight_black,   knight_black,   knight_black,   None,           None,           None,           None],
                    [None,          pawn_black,     queen_black,    pawn_black,     None,           None,           None,           king_black],
                    [None,          pawn_black,     pawn_black,     pawn_black,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           None],
                    [None,          pawn_white,     pawn_white,     pawn_white,     None,           None,           None,           None],
                    [None,          pawn_white,     queen_black,    pawn_white,     None,           queen_white,    None,           None],
                    [None,          knight_white,   pawn_white,     pawn_white,     None,           None,           None,           None],
                    [None,          None,           None,           None,           None,           None,           None,           king_white]]
    # Check if the boards are the same
    assert_boards_are_same(test_board, board)

    # Test with no spaces available in all directions (should return 0)
    # Black Queen at Coordinate(1, 2) with No team color
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.POSITIVE, SignDirection.POSITIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.POSITIVE, SignDirection.ZERO) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.POSITIVE, SignDirection.NEGATIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.ZERO, SignDirection.POSITIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.ZERO, SignDirection.NEGATIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.NEGATIVE, SignDirection.POSITIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.NEGATIVE, SignDirection.ZERO) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.NEGATIVE, SignDirection.NEGATIVE) == 0

    # Test should be the same with team color
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.POSITIVE, SignDirection.POSITIVE, TeamColor.BLACK) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.POSITIVE, SignDirection.ZERO, TeamColor.BLACK) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.POSITIVE, SignDirection.NEGATIVE, TeamColor.BLACK) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.ZERO, SignDirection.POSITIVE, TeamColor.BLACK) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.ZERO, SignDirection.NEGATIVE, TeamColor.BLACK) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.NEGATIVE, SignDirection.POSITIVE, TeamColor.BLACK) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.NEGATIVE, SignDirection.ZERO, TeamColor.BLACK) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.NEGATIVE, SignDirection.NEGATIVE, TeamColor.BLACK) == 0

    # Black Queen at Coordinate(5, 2) with No team color
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.POSITIVE, SignDirection.POSITIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.POSITIVE, SignDirection.ZERO) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.POSITIVE, SignDirection.NEGATIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.ZERO, SignDirection.POSITIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.ZERO, SignDirection.NEGATIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.POSITIVE) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.ZERO) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.NEGATIVE) == 0

    # Test should be different with team color (should be 1 as piece can be captured)
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.POSITIVE, SignDirection.POSITIVE, TeamColor.BLACK) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.POSITIVE, SignDirection.ZERO, TeamColor.BLACK) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.POSITIVE, SignDirection.NEGATIVE, TeamColor.BLACK) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.ZERO, SignDirection.POSITIVE, TeamColor.BLACK) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.ZERO, SignDirection.NEGATIVE, TeamColor.BLACK) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.POSITIVE, TeamColor.BLACK) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.ZERO, TeamColor.BLACK) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.NEGATIVE, TeamColor.BLACK) == 1

    # Test with at least 1 space available in all directions
    # White Queen at Coordinate(5, 5) with No team color
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.POSITIVE, SignDirection.POSITIVE) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.POSITIVE, SignDirection.ZERO) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.POSITIVE, SignDirection.NEGATIVE) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.ZERO, SignDirection.POSITIVE) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.ZERO, SignDirection.NEGATIVE) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.POSITIVE) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.ZERO) == 5
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.NEGATIVE) == 2

    # Negative Negative test should be different with team color (ensure others are the same)
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.POSITIVE, SignDirection.POSITIVE, TeamColor.WHITE) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.POSITIVE, SignDirection.ZERO, TeamColor.WHITE) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.POSITIVE, SignDirection.NEGATIVE, TeamColor.WHITE) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.ZERO, SignDirection.POSITIVE, TeamColor.WHITE) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.ZERO, SignDirection.NEGATIVE, TeamColor.WHITE) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.POSITIVE, TeamColor.WHITE) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.ZERO, TeamColor.WHITE) == 5
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.NEGATIVE, TeamColor.WHITE) == 3

    # Test with max space avaiable (should be the max_spaces input)
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.NEGATIVE, TeamColor.BLACK, 1) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.ZERO, max_spaces=3) == 3
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.POSITIVE, SignDirection.NEGATIVE, max_spaces=1) == 1
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.NEGATIVE, TeamColor.WHITE, 2) == 2

    # Test with max space not limiting factor
    assert board._get_spaces_available_in_move_dir(Coordinate(1, 2), SignDirection.POSITIVE, SignDirection.POSITIVE, TeamColor.BLACK, 3) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.POSITIVE, max_spaces=1) == 0
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.ZERO, TeamColor.WHITE, 7) == 5
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 5), SignDirection.NEGATIVE, SignDirection.NEGATIVE, max_spaces=3) == 2
    assert board._get_spaces_available_in_move_dir(Coordinate(5, 2), SignDirection.NEGATIVE, SignDirection.ZERO, max_spaces=0) == 0

# Test _fen_to_castling_rights
# Test with no castling rights
# Test with all castling rights
# Teach each castling right individually with all others off
# Test with some mix of castling rights
# Test with invalid castling rights string
def test_fen_to_castling_rights():
    # Test with no castling rights
    castling_rights = Board._fen_to_castling_rights("-")
    assert castling_rights.white_kingside == False
    assert castling_rights.white_queenside == False
    assert castling_rights.black_kingside == False
    assert castling_rights.black_queenside == False

    # Test with all castling rights
    castling_rights = Board._fen_to_castling_rights("KQkq")
    assert castling_rights.white_kingside == True
    assert castling_rights.white_queenside == True
    assert castling_rights.black_kingside == True
    assert castling_rights.black_queenside == True

    # Teach each castling right individually with all others off
    castling_rights = Board._fen_to_castling_rights("K")
    assert castling_rights.white_kingside == True
    assert castling_rights.white_queenside == False
    assert castling_rights.black_kingside == False
    assert castling_rights.black_queenside == False

    castling_rights = Board._fen_to_castling_rights("Q")
    assert castling_rights.white_kingside == False
    assert castling_rights.white_queenside == True
    assert castling_rights.black_kingside == False
    assert castling_rights.black_queenside == False

    castling_rights = Board._fen_to_castling_rights("k")
    assert castling_rights.white_kingside == False
    assert castling_rights.white_queenside == False
    assert castling_rights.black_kingside == True
    assert castling_rights.black_queenside == False

    castling_rights = Board._fen_to_castling_rights("q")
    assert castling_rights.white_kingside == False
    assert castling_rights.white_queenside == False
    assert castling_rights.black_kingside == False
    assert castling_rights.black_queenside == True

    # Test with some mix of castling rights (also test mixing up the order)
    castling_rights = Board._fen_to_castling_rights("Kq")
    assert castling_rights.white_kingside == True
    assert castling_rights.white_queenside == False
    assert castling_rights.black_kingside == False
    assert castling_rights.black_queenside == True

    castling_rights = Board._fen_to_castling_rights("kQ") # Switched order
    assert castling_rights.white_kingside == False
    assert castling_rights.white_queenside == True
    assert castling_rights.black_kingside == True
    assert castling_rights.black_queenside == False

    castling_rights = Board._fen_to_castling_rights("QqK") # Switched order
    assert castling_rights.white_kingside == True
    assert castling_rights.white_queenside == True
    assert castling_rights.black_kingside == False
    assert castling_rights.black_queenside == True

    castling_rights = Board._fen_to_castling_rights("qKk") # Switched order
    assert castling_rights.white_kingside == True
    assert castling_rights.white_queenside == False
    assert castling_rights.black_kingside == True
    assert castling_rights.black_queenside == True

# Test _fen_to_turn
# Test with white turn
# Test with black turn
# Test with invalid turn string
def test_fen_to_turn():
    # Test with white turn (with leading space - should be trimmed)
    assert Board._fen_to_turn(" w") == TeamColor.WHITE
    # Test with black turn (uppercase - should still work)
    assert Board._fen_to_turn("B") == TeamColor.BLACK
    # Test with invalid turn string
    assert Board._fen_to_turn("a") == None
    assert Board._fen_to_turn("z~B ") == None
        

# Test _fen_to_board_arr
# Test with board that test every piece and color
# Test with invalid board string due to length
# Test with invalid board string due to invalid characters
# Test with invalid board string due to invalid / locations
# Test with invalid pawn position of pawns in promotion row or below starting row
# Test with invalid board with no kings for both and one team
# Randomly test based on randomly generated boards
def test_fen_to_board_arr():
    # Test with board that test every piece and color (default board)
    board = Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    test_board = default_board
    # Check if the boards are the same (both are lists now so we can't use assert_boards_are_same)
    assert test_board == board

    # Test same board but with space to be stripped
    board = Board._fen_to_board_arr(' rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR\t')
    test_board = default_board
    # Check if the boards are the same
    assert test_board == board

    # Test with invalid board string due to length
    # Too short
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP') == None # Missing last row
    assert Board._fen_to_board_arr('pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') == None # Missing first row
    assert Board._fen_to_board_arr('8/8/8/8') == None
    assert Board._fen_to_board_arr('nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')  == None # Missing first character

    # Too long
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/8') == None # Extra row
    assert Board._fen_to_board_arr('8/rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') == None # Extra row
    assert Board._fen_to_board_arr('8/rnbqkbnr/pppppppp/8/8/8/8/8/8/8/8/PPPPPPPP/RNBQKBNR') == None # A lot of extra rows
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRR') == None # Extra char in last row

    # Test with invalid board string due to invalid characters
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNZ') == None # Invalid char in last row
    assert Board._fen_to_board_arr('znbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') == None # Invalid char in first row
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/7~/8/8/8/PPPPPPPP/RNBQKBNR') == None # Invalid char in third row special character
    assert Board._fen_to_board_arr('aslkdnlneoifeownewocn!#%#@123343443edno32') == None # Invalid text

    # Test with invalid board string due to invalid / locations
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/0/8/8/8/PPPPPPPP/RNBQKBNR')  == None # Row 3 (index 2) has 0 spaces
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/7/8/8/PPPPPPPP/RNBQKBNR')  == None # Row 4 (index 3) is too short only 7 spaces
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/9/8/PPPPPPPP/RNBQKBNR')  == None # Row 5 (index 4) is too long 9 spaces
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/10/PPPPPPPP/RNBQKBNR')  == None # Row 6 (index 5) is too long 10 spaces
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/10/PPPPPPPP/RNBQKBNR/')  == None # Ends with extra /
    assert Board._fen_to_board_arr('/rnbqkbnr/pppppppp/8/8/8/10/PPPPPPPP/RNBQKBNR')  == None # Starts with extra /
    assert Board._fen_to_board_arr('rnbqkbnr/pppp/pppp/8/8/8/PPPPPPPP/RNBQKBNR')  == None # / Too early in row 2 (index 1)
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp//8/8/8/8/PPPPPPPP/RNBQKBNR')  == None # Double / in after row 2 (index 1)

    # Test with invalid pawn position of pawns in promotion row or below starting row
    assert Board._fen_to_board_arr('Pnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') == None # White pawn in promotion row
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNp') == None # Black pawn in promotion row
    assert Board._fen_to_board_arr('PnbqkPPr/pppppppp/8/8/8/8/PPPPPPPP/RpBpKBNp') == None # Multiple pawns in both promotion rows
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNP') == None # Black pawn below starting row
    assert Board._fen_to_board_arr('pnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') == None # White pawn below starting row
    assert Board._fen_to_board_arr('pnbqkppr/pppppppp/8/8/8/8/PPPPPPPP/RPBPKBNP') == None # Multiple pawns below starting row

    # Test with invalid board with no kings for both and one team
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQQBNR') == None # No king for White
    assert Board._fen_to_board_arr('rnbqnbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') == None # No king for Black
    assert Board._fen_to_board_arr('rnbq1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQRBNR') == None # No king for either team

    # Test with invalid board with multiple kings for both and one team
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPKP/RNBQKBNR') == None # Two kings for White
    assert Board._fen_to_board_arr('rnbqkbnr/pppppppp/k7/8/8/8/PPPPPPPP/RNBQKBNR') == None # Two kings for Black
    assert Board._fen_to_board_arr('rnbqkbnk/ppppppkp/8/8/3k4/6K1/PPPPPPPK/RNBQKBNR') == None # Multipme kings for both teams

    # Randomly test based on randomly generated boards
    for _ in range(NUM_RAND_FEN_TO_BOARD_ARR_TESTS):
        # Generate random FEN string and board
        fen_str, test_board = generate_random_fen_str_and_board(False)

        # Convert the FEN string to a board
        board = Board._fen_to_board_arr(fen_str)

        # Check if the boards are the same
        assert test_board == board

# Test _set_board_from_fen
# Test with set of boards that test every piece and color
# Test with invalid castling rights based on the board setup (king / rook moved)
# Test with invalid en passant based on the board setup (no pawn in correct position)

# Test _update_mask_for_piece
# Test _get_valid_moves_for_piece
# Test _get_valid_move_coordinates_for_piece
# Test each type of piece on a board and give empty mask to make sure it updates correctly
# Test each type of piece again and make sure it updates the mask correctly 

# Test reset_board
# Test to make sure all attributes are reset to defaults when without FEN string
# Test to make sure all attributes are reset based on provided FEN string

# Test get_all_legal_moves
# Test different boards with different pieces and make sure the moves are correct

# Test half moves
# Test full moves

# Helper method to check if moves are equal
def assert_moves_are_equal(move1: Move, move2: Move):
    # Check if all the elements of move1 are equal to move2
    if move1 == None or move2 == None:
        # Both must be invalid moves (None)
        assert move1 == move2
    else:
        assert move1.from_coord.row == move2.from_coord.row
        assert move1.from_coord.col == move2.from_coord.col
        assert move1.to_coord.row == move2.to_coord.row
        assert move1.to_coord.col == move2.to_coord.col
        assert move1.promotion == move2.promotion

# Checks if the boards are the same using pytest assert
def assert_boards_are_same(test_board: list, board: Board):
    # Check if the boards are the same
    assert test_board == board._board_arr
    # for row in range(len(test_board)):
    #     for col in range(len(test_board[0])):
    #         if test_board[row][col] == None:
    #             assert board._board_arr[row][col] == None
    #         else:
    #             assert board._board_arr[row][col].Type == test_board[row][col].Type
    #             assert board._board_arr[row][col].Color == test_board[row][col].Color

# Generates random FEN string
def generate_random_fen_str(add_example_other_params=True):
    return generate_random_fen_str_and_board(add_example_other_params)[0]

# Generates random FEN string and board
# Returns as a tuple (fen_str, board)
def generate_random_fen_str_and_board(add_example_other_params=True):
    fen_str = ""
    board = [[None for _ in range(8)] for _ in range(8)]

    white_king = False
    black_king = False

    # Generate random board
    for row in range(8):
        # Count the number of empty spaces between pieces for FEN string
        cnt = 0
        # Add a / between rows but not at start of FEN string
        if (row != 0):
            fen_str += "/"
        
        # Generate a random row
        for col in range(8):
            # Save last 3rd to last space and last space for kings if they have not been generated
            if (row == 7 and col == 5 and not white_king):
                # Add previous cnt to fen_str
                if cnt != 0:
                    fen_str += str(cnt)
                    cnt = 0
                # Add king to fen_str and board
                fen_str += 'K'
                board[7 - row][col] = Piece(PieceType.KING, TeamColor.WHITE)
                # Set white_king to True
                white_king = True
                continue
            elif (row == 7 and col == 7 and not black_king):
                # Add previous cnt to fen_str
                if cnt != 0:
                    fen_str += str(cnt)
                    cnt = 0
                # Add king to fen_str and board
                fen_str += 'k'
                board[7 - row][col] = Piece(PieceType.KING, TeamColor.BLACK)
                # Set black_king to True
                black_king = True
                continue
            # Randomly decide if there is a piece or not in this space
            if random.random() < RAND_PIECE_PERCENTAGE:
                # Add previous cnt to fen_str
                if cnt != 0:
                    fen_str += str(cnt)
                    cnt = 0

                # Generate random piece
                # PieceType and TeamColor are both enums with values from 0-5 and 0-1 respectively
                rand_piece = PieceType(randrange(6))
                rand_color = TeamColor(randrange(2))
                rand_piece_fen_chr = ''

                no_pawn = (row == 0 or row == 7)

                # Check if pawn and if it's in the promotion row or below starting row
                if (rand_piece == PieceType.PAWN and no_pawn):
                    # Generate a new piece that's not a pawn (PieceType(0) is pawn)
                    rand_piece = PieceType(randrange(5) + 1)
                    no_pawn = True
                
                # Check if king and if there is already a king of the same color
                if (rand_piece == PieceType.KING):
                    if (rand_color == TeamColor.WHITE):
                        if (white_king):
                            # Generate a new piece that's not a king (PieceType(5) is king)
                            rand_piece = PieceType(randrange(5) if (not no_pawn) else (randrange(4) + 1))
                        else:
                            white_king = True
                    else:
                        if (black_king):
                            # Generate a new piece that's not a king (PieceType(5) is king)
                            rand_piece = PieceType(randrange(5) if (not no_pawn) else (randrange(4) + 1))
                        else:
                            black_king = True
                # Assign the piece to the board
                board[7 - row][col] = Piece(rand_piece, rand_color)

                # Get the FEN character for the piece
                if (rand_piece == PieceType.PAWN):
                    rand_piece_fen_chr = 'p'
                elif (rand_piece == PieceType.ROOK):
                    rand_piece_fen_chr = 'r'
                elif (rand_piece == PieceType.KNIGHT):
                    rand_piece_fen_chr = 'n'
                elif (rand_piece == PieceType.BISHOP):
                    rand_piece_fen_chr = 'b'
                elif (rand_piece == PieceType.QUEEN):
                    rand_piece_fen_chr = 'q'
                elif (rand_piece == PieceType.KING):
                    rand_piece_fen_chr = 'k'

                # Get the capitalization of the piece which is based on the color
                if (rand_color == TeamColor.WHITE):
                    rand_piece_fen_chr = rand_piece_fen_chr.upper()

                # Add the piece to the fen_str
                fen_str += rand_piece_fen_chr
            else:
                # Empty space
                cnt += 1
        
        if (cnt != 0):
            fen_str += str(cnt)
    
    # Add the other parameters (irrelevant to scoring) to the board part of the FEN string
    if add_example_other_params:
        fen_str += " w - - 0 1"

    return (fen_str, board)
    
# Gets what the score shoudl be for white based off a fen string
def get_white_score_from_fen_str(fen_str: str):
    # Get the board part of the FEN string
    fen_str = fen_str.split(" ")[0]

    # Get the score for each piece
    score = 0
    for char in fen_str:
        # Get the piece char as lower case to make it easier to parse
        char_lower = char.lower()
        # Get the score to add or subtract based on the piece (don't add if it's not a piece (empty space or /))
        score_to_add = 0
        # Determine which piece it is
        if char_lower == 'p':
            score_to_add = pawn_val
        elif char_lower == 'r':
            score_to_add = rook_val
        elif char_lower == 'n':
            score_to_add = knight_val
        elif char_lower == 'b':
            score_to_add = bishop_val
        elif char_lower == 'q':
            score_to_add = queen_val
        elif char_lower == 'k':
            score_to_add = king_val

        # Add score to total score if white piece, subtract if black piece
        score += score_to_add if char.isupper() else -score_to_add
    
    return score