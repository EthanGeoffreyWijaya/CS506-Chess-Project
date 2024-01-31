import Connect2DB
from Board import Board, Move
from mysql.connector import Error # use for checking errors
import random # use to randomly choose opening book when WinRate tied

# openingBook need to input all in long notation

class OpeningBook:
    
    # Constructor: set up connection to MySQL DB
    #
    # return None
    def __init__(self, board: Board) -> None:
        # set up connection to MySQL DB
        self.conn = Connect2DB.Connect2DB()
    
    # This function will get the best opening book variation from DB
    #
    # @PARMS
    #   string: string of moves
    #
    # return a tuple of the best opening book (idOpeningBook, Moves)
    # NOTE: This function will filter down the opening books since there can be mulitple 
    #       opening books with the same fen
    def get_Best_opening_Book(self, Id_Num):
        
        # get idOpeningBook from tuple
        idOpeningBook = [x[0] for x in Id_Num]
        
        # convert list to tuple
        idOB_Tuple = tuple(idOpeningBook)
        
        # convert tuple to string
        idOB_String = ', '.join(map(str, idOB_Tuple))
        
        # set up query to get opening book from DB
        sql = f"SELECT idOpeningBook, Moves \
                FROM openingbook \
                WHERE WinRate = \
                    (SELECT MAX(WinRate) \
                    FROM openingbook) \
                AND idOpeningBook IN ({idOB_String})"

        # execute query
        self.conn.cursor.execute(sql)
        
        # get result from query
        results = self.conn.cursor.fetchall()
        
        # NOTE: Doesn't matter how many opening books are in the results,
        #       we will randomly choose one of them
        if results:
            # choose the best opening book
            best_OB = random.choice(results)
            
            # get the index of the best opening book
            index = idOpeningBook.index(best_OB[0])
            
            # get the corresponding move number
            corresponding_move_Num = Id_Num[index][1]
            
            return best_OB, corresponding_move_Num
        
        # else something went wrong
        else:
            print("Something went wrong. :(")
            return None

    # This function is called to compare board's state's fen with DB Fen
    #
    # @PARMS
    #   board_state: string of board's state's fen
    #
    # return a move string of the best opening book
    def compare_Fen(self, board_state):
            
        # set up query to get opening book from DB
        sql = "SELECT idOpeningBook, MoveNumber \
                FROM openingbookfen \
                WHERE Fen = %s"
        
        # execute query
        self.conn.cursor.execute(sql, (board_state,))
        
        # get result from query
        result = self.conn.cursor.fetchall()
        
        # if there is a result(idOpeningBook, MoveNumber), return the best opening book
        if result:
            return self.get_Best_opening_Book(result)
        
        # else quit Opening Book
        else:
            return None
    
    # This function is called to get the next best move from opening book in DB
    #
    # return a string of the move
    def play_Opening_book(self, board: Board):
        # get board state
        board_state = board.get_fen()
        
        # call to function to compare board's fen with DB Fen
        # compare_Fen will return result(move_String, move_Number)
        result, move_Num = self.compare_Fen(board_state)
        
        if result is None:
            return (None, None)
        else:
            # get best move from string using move_Num as index
            best_Move = result[1].split()[move_Num]
            return (result[0], best_Move)
            
    
    # # TODO: need to update win rate at the end of the game
    # def update_WinRate(self, opening_name, win_Rate):
    #     # update win rate in DB
    #     sql = "UPDATE opening_book SET win_Rate = %s WHERE opening_name = %s"
    #     self.conn.cursor.execute(sql, (win_Rate, opening_name))
    #     self.conn.commit()
    #     print(self.conn.cursor.rowcount, "record(s) affected")