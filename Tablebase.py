#import Connect2DB
import Board
import chess
import chess.syzygy
import os

# We will be using Syzygy tablebases for this project. 
# Syzygy tablebases will be uploaded to the VM and will be called to get the WDL and DTZ values.
# https://python-chess.readthedocs.io/en/latest/syzygy.html#chess.syzygy.Tablebase.add_directory


# Constants:
LOCAL_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep + "CETablebase"

# Can't use cause of permission issues on VM
# VM_PATH = "/u/l/a/lao/Public"

class Tablebase:
    # Constructor
    def __init__(self):
        # Initialize the tablebase
        self.tablebase = self.load_tablebase()
        self.board = Board.Board()
        
        # # Connect to the database
        # self.db = Connect2DB.Connect2DB()
        # self.db.connect()
    
    # This public method will load the tablebase from VM
    #
    # Parameters:
    #   None
    #
    # Returns the tablebase object
    # NOTE: The VM Path is not working right now. I think it is because of permission issues
    #      I will try to fix it later when I have permission.
    def load_tablebase(self):
        # Load the tablebase
        
        # This is for local loading
        return chess.syzygy.open_tablebase(LOCAL_PATH)  
              
        # This is for VM loading
        # return chess.syzygy.open_tablebase(VM_PATH)
        
    
    # Public method to get the best move from the tablebase
    #
    # Parameters:
    #   FEN: the fen of the position
    #
    # Returns a string of best move from the tablebase
    def getBestMove(self, fen):
        
        # set the board from the fen
        self.board._set_board_from_fen(fen)
        
        # initialize best move and score
        bestMove = None
        best_wdl = 3
        best_dtz = None
        
        # loop through the legal moves
        for move in self.board.get_all_legal_moves():
            
            # Make move on imaginary board
            self.board.move(move)
            
            # probe the tablebase in chess library with our board fen
            wdl, dtz = self.probeTablebase(self.board.get_fen())
            self.board.undo_move()
            
            # TODO: WDL > 0 other team is winning, but try force a draw by choosing higher distance to 0.
            # TODO: WDL < 0 other team is losing, but try prevent a draw by choosing lower distance to 0.
            
            # if the score is better than the best score
            if wdl < best_wdl or (wdl == best_wdl and dtz > best_dtz):
                # set best move
                bestMove = move
                best_wdl = wdl
                best_dtz = dtz
            
        # return the best move
        return bestMove
    
    # Public method to probe the tablebase
    #
    # Parameters:
    #   fen: the fen of the position
    #
    # Returns a tuple containing the wdl and dtz values
    def probeTablebase(self, fen):
        # create a chess board from the fen
        board = chess.Board(fen)
        
        try:
            # probe the tablebase and get the wdl and dtz values
            wdl = self.tablebase.probe_wdl(board)
            dtz = self.tablebase.probe_dtz(board)
            return wdl, dtz
            # else there is an error
        except chess.syzygy.TablebaseError:
            print(f"Error: {fen}: {chess.syzygy.TablebaseError}")
            return None
