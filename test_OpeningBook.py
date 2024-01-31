import pytest
from OpeningBook import OpeningBook
from Board import Board
from unittest.mock import patch

# Test the initialization of OpeningBook
def test_opening_book_constructor():
    board = Board('3k4/8/1p6/2p5/1P6/2P5/8/3K4 w - - 0 1')
    opening_book = OpeningBook(board)
    
    # Check if the connection to the database is set up
    assert opening_book.conn is not None
    # Check if the board is set up correctly
    assert opening_book.board == board

# Test the get_Best_opening_Book method
def test_get_best_opening_book():
    board = Board()
    opening_book = OpeningBook(board)
    
    # Mocking the result from the database query
    result = [(93, 'e2e4 c7c6 g1f3'), (152, 'd2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 f2f4'), (206, 'c2c4 e7e5 b1c3 g8f6 g1f3 b8c6')]
    
    # Mocking the index and corresponding move number
    id_num = [(93, 0), (152, 0), (206, 0)]
    
    # Mocking the random choice of the best opening book
    best_ob = (93, 'e2e4 c7c6 g1f3')
    
    # Mocking the expected return value
    expected_result = (best_ob, 0)
    
    # Patching the execute and fetchall methods of the database connection
    with patch.object(opening_book.conn.cursor, 'execute') as mock_execute:
        with patch.object(opening_book.conn.cursor, 'fetchall') as mock_fetchall:
            with patch('random.choice', return_value=best_ob) as mock_choice:
                mock_execute.return_value = None
                mock_fetchall.return_value = result
                
                # Call the method under test
                actual_result = opening_book.get_Best_opening_Book(id_num)
                
                # Check if the method returns the expected result
                assert actual_result == expected_result

# Test the compare_Fen method
def test_compare_fen():
    board = Board()
    opening_book = OpeningBook(board)
    
    # Mocking the result from the database query
    result = [(93, 'e2e4 c7c6 g1f3')]
    
    # Mocking the expected return value
    expected_result = (93, 'e2e4 c7c6 g1f3')
    
    # Patching the execute and fetchall methods of the database connection
    with patch.object(opening_book.conn.cursor, 'execute') as mock_execute:
        with patch.object(opening_book.conn.cursor, 'fetchall') as mock_fetchall:
            with patch('random.choice', return_value=expected_result) as mock_choice:
                
                mock_execute.return_value = None
                mock_fetchall.return_value = result
                
                # Call the method under test
                actual_result = opening_book.compare_Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
                
                # Check if the method returns the expected result
                assert actual_result[0] == expected_result

# Test the play_Opening_book method
def test_play_opening_book():
    board = Board()
    opening_book = OpeningBook(board)
    
    # Mocking the result from the compare_Fen method
    result = (93, 'e2e4 c7c6 g1f3')
    move_num = 0
    
    # Mocking the best move
    best_move = 'e2e4'
    
    # Patching the compare_Fen method
    with patch.object(opening_book, 'compare_Fen') as mock_compare_fen:
        mock_compare_fen.return_value = (result, move_num)
        
        # Patching the move method of the board
        with patch.object(board, 'move') as mock_move:
            mock_move.return_value = None
            
            # Call the method under test
            actual_result = opening_book.play_Opening_book()
            
            # Check if the method returns the expected result
            assert actual_result == best_move