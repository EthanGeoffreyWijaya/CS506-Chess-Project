from __future__ import annotations
from enum import Enum
from collections import deque
import random

# Author: Alex Arovas

# TODO: Update type hints for all methods to be more clear and include None when appropriate

# Enum for the color of a piece or a team
class TeamColor(Enum):
    BLACK = 0
    WHITE = 1

# Enum for the type of a piece
class PieceType(Enum):
    PAWN = 0
    BISHOP = 1
    KNIGHT = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

# Class for a piece including it's team color and piece type
class Piece:
    # Creates a Piece Object
    #
    # Parameters:
    #   Type: The type of the piece
    #   Color: The color of the piece
    def __init__(self, Type: PieceType, Color: TeamColor):
        self.Type: PieceType = Type
        self.Color: TeamColor = Color

    # Find if two pieces are equal or not
    #
    # Parameters:
    #   other: The other piece to compare to
    #
    # Returns if the pieces are equal or not
    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.Type == other.Type and self.Color == other.Color
        else:
            return False
        
    # Get the hash of the piece
    # Used so the piece can be used as a key in a dict
    def __hash__(self):
        return hash((self.Type, self.Color))
        
    # Find if two pieces are not equal
    # Used so both == and != provide valid results
    #
    # Parameters:
    #   other: The other pieces to compare to
    #
    # Returns if the pieces are not equal
    def __ne__(self, other):
        # Return if the pieces are not equal
        return not(self == other)
    
    # Get the string representation of the piece object
    #
    # Returns the string representation of the piece object
    def __repr__(self):
        return "Piece" + self.__str__()
    
    # Get the string representation of the piece object
    #
    # Returns the string representation of the piece object
    def __str__(self):
        return "(" + self.Type.name + ", " + self.Color.name + ")"

# Class for a coordinate including the row and column
class Coordinate:
    # Creates a Coordinate Object
    #
    # Parameters:
    #   row: The row of the coordinate
    #   col: The column of the coordinate
    def __init__(self, row: int, col: int):
        self.row: int = row
        self.col: int = col

    # Find if two coordinates are equal or not
    #
    # Parameters:
    #   other: The other coordinate to compare to
    #
    # Returns if the coordinates are equal or not
    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.row == other.row and self.col == other.col
        else:
            return False
    
    # Get the hash of the coordinate
    # Used so the coordinate can be used as a key in a dict
    def __hash__(self):
        return hash((self.row, self.col))
        
    # Find if two coordinates are not equal
    # Used so both == and != provide valid results
    #
    # Parameters:
    #   other: The other coordinate to compare to
    #
    # Returns if the coordinates are not equal
    def __ne__(self, other):
        # Return if the coordinates are not equal
        return not(self == other)
    
    # Get the string representation of the coordinate object
    #
    # Returns the string representation of the coordinate object
    def __repr__(self):
        return "Coordinate" + self.__str__()
    
    # Get the string representation of the coordinate position
    #
    # Returns the string representation of the coordinate position
    def __str__(self):
        return "(" + str(self.row) + ", " + str(self.col) + ")"

# Class for keeping track of castling rights
class CastlingRights:
    # Creates a CastlingRights Object
    #
    # Parameters:
    #   white_king: Whether white can castle king side
    #   white_queen: Whether white can castle queen side
    #   black_king: Whether black can castle king side
    #   black_queen: Whether black can castle queen side
    def __init__(self, white_kingside: bool = True, white_queenside: bool = True, black_kingside: bool = True, black_queenside: bool = True):
        self.white_kingside: bool = white_kingside
        self.white_queenside: bool = white_queenside
        self.black_kingside: bool = black_kingside
        self.black_queenside: bool = black_queenside

    # Get the string representation of the castling rights object
    #
    # Returns the string representation of the castling rights object
    def __repr__(self):
        return "CastlingRights(" + self.__str__() + ")"
    
    # Get the string representation of the castling rights object
    #
    # Returns the string representation of the castling rights object
    def __str__(self):
        rights_str = "K" if self.white_kingside else ""
        rights_str += "Q" if self.white_queenside else ""
        rights_str += "k" if self.black_kingside else ""
        rights_str += "q" if self.black_queenside else ""
        rights_str = "-" if len(rights_str) == 0 else rights_str
        return rights_str

# Class for a move including the from and to coordinates
class Move:
    # Creates a Move Object
    #
    # Parameters:
    #   from_coord: The from coordinate of the move
    #   to_coord: The to coordinate of the move
    #   promotion: The promotion piece of the move (None if not a promotion)
    def __init__(self, from_coord: Coordinate, to_coord: Coordinate, promotion: PieceType | None = None):
        self.from_coord: Coordinate = from_coord
        self.to_coord: Coordinate = to_coord
        self.promotion: PieceType | None = promotion
    
    # Get the string representation of the move object
    #
    # Returns the string representation of the move object or "Invalid Move" if the move is invalid
    def __str__(self):
        move_str = self.to_uci_str(self)
        return move_str if move_str != None else "Invalid Move"

    # Method that converts a Move object into a move string
    #
    # Returns the move as a string or None if the move is invalid
    #
    # NOTE: Only checks if the move is not out of bounds and if the promotion is to valid piece (knight, rook, bishop, queen) and
    #           does not check if the move is a fully valid move (not capturing a piece on the same team, etc.)
    @staticmethod
    def to_uci_str(move: Move) -> str | None:
        # Check if the move is a valid move
        # Check the from and to coordinates are valid and that they're not the same
        if (Board._coord_in_board(move.from_coord) == False or Board._coord_in_board(move.to_coord) == False or move.from_coord == move.to_coord):
            return None
        
        # Create the move string
        move_str = ''

        # Add the from column
        move_str += chr(move.from_coord.col + ord('a'))

        # Add the from row
        move_str += chr(move.from_coord.row + ord('1'))

        # Add the to column
        move_str += chr(move.to_coord.col + ord('a'))

        # Add the to row
        move_str += chr(move.to_coord.row + ord('1'))

        # Check if the move is a promotion
        if (move.promotion != None):
            # Uncomment to check for invalid promotion moves (based on to and from coordinates)
            # Decided not to check to make it a method that is more predictable in what it checks
            # - whether it's in the board, and the promotion piece is valid
            # Get the promotion row and pawn direction to check if the move is a valid promotion
            # promotion_row = Board._get_pawn_promotion_row(self._turn)
            # pawn_direction = Board._get_pawn_direction(self._turn)
            # Check if move is from the second to last row and ends in last row (+/- 1 or same column)
            # if (move.from_coord.row == promotion_row - pawn_direction and move.to_coord.row == promotion_row and 
            #     abs(move.from_coord.col - move.to_coord.col) <= 1):
            #     pass
            
            # Add the promotion piece to the move string
            if (move.promotion == PieceType.QUEEN):
                move_str += 'q'
            elif (move.promotion == PieceType.ROOK):
                move_str += 'r'
            elif (move.promotion == PieceType.BISHOP):
                move_str += 'b'
            elif (move.promotion == PieceType.KNIGHT):
                move_str += 'n'
            # Invalid promotion
            else:
                return None

        return move_str
    
    # Get the string representation of the move object
    #
    # Returns the string representation of the move object
    def __repr__(self):
        return "Move(\"" + self.__str__() + "\")"
    
    # Private method that converts a move string to a Move object
    #
    # Parameters:
    #   move_str: The move string as specified in UCI
    #
    # Returns the move string values as a Move object or None if the move string is invalid
    @staticmethod
    def from_uci_str(move_str: str) -> Move:
        # Create the dict to return with empty values
        move = Move(from_coord=Coordinate(None, None), to_coord=Coordinate(None, None), promotion=None)

        # Strip any extra characters and use lower case to make it easier to parse for ascii comparison
        move_str = move_str.strip().lower()

        # Check if the move string is the right length (4 for normal moves, 5 for promotion moves)
        if (len(move_str) != 4 and len(move_str) != 5):
            return None
        
        # Check if promotion on and assign Piece to promotion
        if (len(move_str) == 5):
            # Promotion is queen
            if (move_str[4] == 'q'):
                move.promotion = PieceType.QUEEN
            # Promotion is rook
            elif (move_str[4] == 'r'):
                move.promotion = PieceType.ROOK
            # Promotion is bishop
            elif (move_str[4] == 'b'):
                move.promotion = PieceType.BISHOP
            # Promotion is knight
            elif (move_str[4] == 'n'):
                move.promotion = PieceType.KNIGHT
            # Invalid promotion character
            else:
                return None
        
        # Check if the from column is valid
        move.from_coord.col = Board._get_index_in_range(move_str[0], 'a', 'h')

        # Check if the from row is valid
        move.from_coord.row = Board._get_index_in_range(move_str[1], '1', '8')

        # Check if the to column is valid
        move.to_coord.col = Board._get_index_in_range(move_str[2], 'a', 'h')

        # Check if the to row is valid
        move.to_coord.row = Board._get_index_in_range(move_str[3], '1', '8')

        # Check if the move is invalid (any of the indexes are -1)
        if (-1 in [move.from_coord.row, move.from_coord.col, move.to_coord.row, move.to_coord.col]):
            return None

        return move
    
    # Find if two moves are equal or not
    #
    # Parameters:
    #   other: The other move to compare to
    #
    # Returns if the moves are equal or not
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.from_coord == other.from_coord and self.to_coord == other.to_coord and self.promotion == other.promotion
        else:
            return False
        
    # Get the hash of the move
    # Used so the move can be used as a key in a dict
    def __hash__(self):
        return hash((self.from_coord, self.to_coord, self.promotion))
    
    # Find if two moves are not equal
    # Used so both == and != provide valid results
    #
    # Parameters:
    #   other: The other move to compare to
    #
    # Returns if the moves are not equal
    def __ne__(self, other):
        # Return if the moves are not equal
        return not(self == other)

# Class for additional move info necessary for undoing a move including the move (which has the from and to coordinates and the promotion if any), 
#   the previous castling rights, and the previous half moves, the piece type that was captured if any, the previous en passant location, and 
#   if the previous move was an en passant capture
class MoveInfo:
    # Creates a MoveInfo Object
    #
    # Parameters:
    #   move: The move that was made
    #   castling_rights: The previous castling rights
    #   half_moves: The previous half moves
    #   cap_piece_type: The piece type that was captured (None if no piece was captured)
    #   en_passant_avail: The previous en passant location (None if no en passant was available)
    #   en_passant: If the previous move was an en passant capture
    #   valid_moves: The previous valid moves (for the team that moved)
    def __init__(self, move: Move, castling_rights: CastlingRights, half_moves: int, cap_piece_type: PieceType | None = None, 
                 en_passant_avail: Coordinate | None = None, en_passant: bool = False, valid_moves: list[str] = []):
        self.move: Move = move
        self.castling_rights: CastlingRights = castling_rights
        self.half_moves: int = half_moves
        self.cap_piece_type: PieceType = cap_piece_type
        self.en_passant_avail: Coordinate = en_passant_avail
        self.en_passant: bool = en_passant
        self.valid_moves: list[str] = valid_moves

    # Get the string representation of the move info object
    #
    # Returns the string representation of the move info object
    def __str__(self):
        return ("(" + str(self.move) + ", " + str(self.castling_rights) + ", " + str(self.half_moves) + ", " + 
                str(self.cap_piece_type.name if self.cap_piece_type != None else None) + ", " + 
                str(self.en_passant_avail) + ", " + str(self.en_passant) + ", " + str(self.valid_moves) + ")")
    
    # Get the string representation of the move info object
    #
    # Returns the string representation of the move info object
    def __repr__(self):
        return "MoveInfo" + self.__str__() 


# Class for keeping track of a piece's coordinates on the board
class PieceCoordinate:
    # Creates a PieceCoordinate Object
    #
    # Parameters:
    #   piece: The piece
    #   coord: The coordinate (location) of the piece
    def __init__(self, piece: Piece, coord: Coordinate):
        self.Piece: Piece = piece
        self.Coord: Coordinate = coord
    
    # Find if two PieceCoordinates are equal or not
    #
    # Parameters:
    #   other: The other PieceCoordinate to compare to
    #
    # Returns if the PieceCoordinates are equal or not
    def __eq__(self, other):
        if isinstance(other, PieceCoordinate):
            return self.Piece == other.Piece and self.Coord == other.Coord
        else:
            return False
        
    # Get the hash of the PieceCoordinate
    # Used to make testing easier to compare list elements (in any order) as sets
    def __hash__(self):
        return hash((self.Piece.Type.value, self.Piece.Color.value, self.Coord.row, self.Coord.col))
    
    # Find if two PieceCoordinates are not equal
    # Used so both == and != provide valid results
    #
    # Parameters:
    #   other: The other PieceCoordinates to compare to
    #
    # Returns if the PieceCoordinates are not equal
    def __ne__(self, other):
        # Return if the PieceCoordinates are not equal
        return not(self == other)
    
    # Get the string representation of the PieceCoordinate object
    #
    # Returns the string representation of the PieceCoordinate object
    def __repr__(self):
        return "PieceCoordinate" + self.__str__()
    
    # Get the string representation of the PieceCoordinate object
    #
    # Returns the string representation of the PieceCoordinate object
    def __str__(self):
        return "(" + str(self.Piece) + ", " + str(self.Coord) + ")"

# Enum for the sign of a number - used to set a direction
class SignDirection(Enum):
    NEGATIVE = -1
    ZERO = 0
    POSITIVE = 1

# Class used to keep track of the attacking and valid move coordinates for a piece
class PieceActionInfo:
    # Creates a PieceAttackInfo Object
    #
    # Parameters:
    #   valid_move_coords: The coordinates the piece can move to (default is an empty list)
    #   attack_coords: The coordinates the piece can attack (default is an empty list)
    def __init__(self, valid_move_coords: list[Coordinate] = [], attack_coords: list[Coordinate] = []):
        # The coordinates the piece can move to
        self.valid_move_coords: list[Coordinate] = valid_move_coords
        # The coordinates the piece is attacking
        self.attack_coords: list[Coordinate] = attack_coords

    # Get the string representation of the PieceActionInfo object
    #
    # Returns the string representation of the PieceActionInfo object
    def __repr__(self):
        return "PieceActionInfo:\n" + self.__str__()
    
    # Get the string representation of the PieceActionInfo object
    #
    # Returns the string representation of the PieceActionInfo object
    def __str__(self):
        return "Valid Moves: " + str(self.valid_move_coords) + "\nAttack Coords: " + str(self.attack_coords)

# Class used to keep track of all piece locations and where they can capture
class PieceTracker:
    # Creates a PieceTracker Object
    def __init__(self):
        # List of dicts for piece locations
        # Each element of list stores a dict of piece locations for a specific team and piece type
        # White: Pawns (0), Bishops (1), Knights (2), Rooks (3), Queens (4), King (5)
        # Black: Pawns (6), Bishops (7), Knights (8), Rooks (9), Queens (10), King (11)
        # Index is the piece type (0-5) plus 6 if black (Valid indexes 0-11)
        self._piece_locations: list[dict[Coordinate, PieceActionInfo]] = [{} for i in range(12)]

        # Number of pieces
        self._piece_count: int = 0
    
    # Gets the piece index for a specific team and piece type
    #
    # Parameters:
    #   team_color: The team color to get the index for
    #   piece_type: The piece type to get the index for
    #
    # Returns the index for the team and piece type
    def _get_locations_index(self, piece_type: PieceType, team_color: TeamColor) -> int:
        # Get the index of the piece
        index = piece_type.value
        # Add 6 if the piece is black
        if (team_color == TeamColor.BLACK):
            index += 6
        
        return index

    # Gets the number of pieces
    #
    # Returns the number of pieces
    def get_piece_count(self) -> int:
        return self._piece_count
    
    # Adds a piece to the piece tracker
    #
    # Parameters:
    #   piece: The piece to add
    #   coord: The coordinate of the piece
    #   piece_action_info: The piece action info for the piece
    def add_piece(self, piece: Piece, coord: Coordinate, piece_action_info: PieceActionInfo):
        # Add to the piece count
        self._piece_count += 1
        # Add the piece to the piece locations
        self.update_piece(piece, coord, piece_action_info)
    
    # Update a piece to the piece tracker
    #
    # Parameters:
    #   piece: The piece to update
    #   coord: The coordinate of the piece
    #   piece_action_info: The piece action info for the piece
    def update_piece(self, piece: Piece, coord: Coordinate, piece_action_info: PieceActionInfo):
        # Updates the piece to the piece locations
        self._piece_locations[self._get_locations_index(piece.Type, piece.Color)][coord] = piece_action_info

    # Removes a piece from the piece tracker
    #
    # Parameters:
    #   piece: The piece to remove
    #   coord: The coordinate of the piece
    def remove_piece(self, piece: Piece, coord: Coordinate):
        # Remove from the piece count
        self._piece_count -= 1
        # Remove the piece from the piece locations
        del self._piece_locations[self._get_locations_index(piece.Type, piece.Color)][coord]
    
    # Gets the piece locations for a specific team and piece type
    #
    # Parameters:
    #   team_color: The team color of the pieces to get
    #   piece_type: The piece type of the pieces to get
    #
    # Returns the piece locations for the specific team and piece type
    def get_piece_locations_and_action_info(self, piece_type: PieceType, team_color: TeamColor) -> dict[Coordinate, PieceActionInfo]:
        # Get the piece locations
        return self._piece_locations[self._get_locations_index(piece_type, team_color)]

    # Gets the pieces as a list of PieceCoordinate for a specific team and piece type
    #
    # Parameters:
    #   team_color: The team color of the pieces to get
    #   piece_type: The piece type of the pieces to get
    #
    # Returns the pieces as a list of PieceCoordinate for the specific team and piece type
    def get_pieces(self, piece_type: PieceType, team_color: TeamColor) -> list[PieceCoordinate]:
        # Get the piece locations
        piece_locations = self.get_piece_locations_and_action_info(piece_type, team_color)

        # Create a list of PieceCoordinate for the pieces
        pieces = []
        # Loop through the coordinates of pieces (keys of the dict for that type and team) and add the pieces to the list
        for coord in piece_locations:
            pieces.append(PieceCoordinate(Piece(piece_type, team_color), coord))
        
        return pieces
    
    # Gets the king piece coordinate for a specific team
    #
    # Parameters:
    #   team_color: The team color of the king to get   
    #
    # NOTE: Assumes there's exactly one king for the team
    #
    # Returns the king piece coordinate for the specific team
    def get_king(self, team_color: TeamColor) -> PieceCoordinate:
        # Get the dict for the king of the team color
        king_dict = self.get_piece_locations_and_action_info(PieceType.KING, team_color)

        # Return a PieceCoordinate where the coordinate is the key of the first (and only) element of the dict
        return PieceCoordinate(Piece(PieceType.KING, team_color), next(iter(king_dict)))
    
    # Gets the king's coordinate for a specific team
    #
    # Parameters:
    #   team_color: The team color of the king to get   
    #
    # NOTE: Assumes there's exactly one king for the team
    #
    # Returns the king piece coordinate for the specific team
    def get_king_coord(self, team_color: TeamColor) -> Coordinate:
        # Get the dict for the king of the team color
        king_dict = self.get_piece_locations_and_action_info(PieceType.KING, team_color)

        # Return the Coordinate which is the key of the first (and only) element of the dict
        return next(iter(king_dict))



# Class for a chess board
# 
# Used to keep track of the chess board and make moves
class Board:
    # Score for a checkmate when evaluated
    CHECKMATE_SCORE: int = 1000000

    # The board 2D array of pieces (8x8 board)
    _board_arr: list[list[Piece]]

    # The team whose turn it is
    _turn: TeamColor

    # En passant capture pawn position
    _en_passant_avail: Coordinate | None

    # The Castling Rights for each team
    _castling_rights: CastlingRights

    # Half moves is a counter that increases everytime white or black moves and it isn't a pawn advance or capture
    # This is used to check for a draw with the 50 move draw rule - so if the half moves gets to 100 then it's a draw
    _half_moves: int

    # Full moves is a counter that increases everytime black moves
    _full_moves: int

    # Save piece locations for each team and piece type for quick access and to store where pieces can attack
    _pieces: PieceTracker

    # Saves the previous moves as a linked list (for saving games and undoing moves for minimax)
    _previous_moves: deque[MoveInfo]

    # A 2D array containing all the pieces attacking each space on the board
    # Each space in the 2D array is a dict with two keys (TeamColor - White and Black) and the value is a dict 
    #   with the key being the PieceType and the value being the number of those piece types attacking that space
    # If not under attack by a team the dict will be an empty dict for that space and team color
    # TODO: Test to see how much faster (if at all) iteratively generating is versus regenerating as needed
    # TODO: Write test for this blocked/blocking condition
    _attack_arr: list[list[dict[TeamColor, dict[PieceType, list[Coordinate]]]]]

    # Each a list of valid move objects that the team can make - used as a cache to prevent regenerating after the first time
    _white_valid_moves: list[Move] | None
    _black_valid_moves: list[Move] | None

    # Keeps track of the current Zobrist table of the position
    _zobrist_table: list[list[int]]

    # Keep track of the current zobrist hash of the position
    _zobrist_hash: int

    # Zobrist value for turn (white or black), castling rights, and en passant file
    # The first list (index 0) is for turn, then castling rights, then en passant
    _zobrist_misc: list[list[int]]

    # Keep track of how many times any position / state of the board has been repeated
    # Used to check for a draw by repetition
    _repeated_positions: dict[int, int]

    # The position causing a draw by repetition
    _draw_by_repetition_position: int | None

    # The maximum number of times a position can be repeated before it's a draw
    _MAX_REPEATED_POSITIONS_BEFORE_DRAW: int

    # The position causing a half move draw (50 move rule - or custom set value)
    _draw_by_half_move_position: int | None

    # The maximum number of half moves before it's a draw
    _MAX_HALF_MOVES_BEFORE_DRAW: int


    # Creates a Board Object and initialized the board to the starting position
    #
    # TODO: Determine a good way to inform the user of an invalid FEN string
    #
    # Parameters:
    #   fen_str: The FEN string of the board to start with (default is None which sets the board to the normal starting position)
    #   max_repeated_positions_before_draw: The maximum number of times a position can be repeated before it's a draw (default is 3, set to None for no limit)
    #   max_half_moves_before_draw: The maximum number of half moves before it's a draw (default is 100 - i.e. the 50 move rule, set to None for no limit)
    def __init__(self, fen_str: str | None = None, max_repeated_positions_before_draw: int | None = 3, 
                 max_half_moves_before_draw: int | None = 100):
        # Create the zobrist tables (for hashing the board)
        self._create_zobrist_tables()

        # Setup the board
        self.reset_board(fen_str, max_repeated_positions_before_draw, max_half_moves_before_draw)

    # Resets the board to the starting position
    #
    # Parameters:
    #   fen_str: The FEN string of the board to start with (default is None which sets the board to the normal starting position)
    #   max_repeated_positions_before_draw: The maximum number of times a position can be repeated before it's a draw (default is 3, set to None for no limit)
    #   max_half_moves_before_draw: The maximum number of half moves before it's a draw (default is 100 - i.e. the 50 move rule, set to None for no limit)
    #
    # Returns if the board was successfully reset or not
    def reset_board(self, fen_str: str | None = None, max_repeated_positions_before_draw: int | None = 3, 
                    max_half_moves_before_draw: int | None = 100) -> bool:
        # Reset the valid moves
        self._white_valid_moves = None
        self._black_valid_moves = None

        # Reset the previous moves
        self._previous_moves = deque()

        # Reset the saved repeated position that caused a draw
        self._draw_by_repetition_position = None

        # Reset the saved half move position that caused a draw
        self._draw_by_half_move_position = None

        # Set the max repeated positions before draw
        self._MAX_REPEATED_POSITIONS_BEFORE_DRAW = max_repeated_positions_before_draw if max_repeated_positions_before_draw != None else float('inf')

        # Set the max half moves before draw
        self._MAX_HALF_MOVES_BEFORE_DRAW = max_half_moves_before_draw if max_half_moves_before_draw != None else float('inf')

        # Set the board to the starting position if a FEN string was not provided
        if (fen_str == None):
            return self._set_board_from_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        # Set the board to the FEN string provided
        else:
            return self._set_board_from_fen(fen_str)
        
    # Gets if the game ended in a half move draw (50 move rule - or custom set value)
    #
    # Parameters:
    #   only_this_position: Whether to only evaluate if this positon causes a draw by half move (default is False)
    #
    # Returns if the game ended in a half move draw (50 move rule - or custom set value)
    def is_half_move_draw(self, only_this_position: bool = False) -> bool:
        return ((self._draw_by_half_move_position != None and not only_this_position) or 
                (self._half_moves >= self._MAX_HALF_MOVES_BEFORE_DRAW))
    
    # Gets if the will game end in a half move draw (50 move rule - or custom set value) after a move
    #
    # Parameters:
    #   move: The move to check if the game will end in a half move draw after
    #
    # Returns if the game will end in a half move draw (50 move rule - or custom set value) after the move
    #
    # NOTE: Assumes the move is valid
    def is_half_move_draw_on_move(self, move: Move) -> bool:
        if (self._draw_by_half_move_position != None):
            return True
        elif (self._board_arr[move.from_coord.row][move.from_coord.col].Type == PieceType.PAWN or
            self._board_arr[move.to_coord.row][move.to_coord.col] != None):
            return False
        return self._half_moves >= (self._MAX_HALF_MOVES_BEFORE_DRAW - 1)
    
    # Gets the current half moves
    #
    # Returns the current half moves
    def get_half_moves(self) -> int:
        return self._half_moves
    
    # Get the current repeated times in the current position
    #
    # Returns the current repeated times in the curret position
    def get_repeated_times(self) -> int:
        # The current position is guaranteed be in the repeated positions dict (as it's appeared at least once)
        return self._repeated_positions[self._zobrist_hash]
    
    # Gets if the game ended in a draw by repetition
    #
    # Parameters:
    #   only_this_position: Whether to only evaluate if this positon causes a draw by repetition (default is False)
    #
    # Returns if the game ended in a draw by repetition
    def is_repetition_draw(self, only_this_position: bool = False) -> bool:
        return ((self._draw_by_repetition_position != None and not only_this_position) or 
                (self._repeated_positions[self._zobrist_hash] >= self._MAX_REPEATED_POSITIONS_BEFORE_DRAW))
    
    # Gets if the game will end in a draw by repetition if position appears again
    #
    # Parameters:
    #   position: The hash of the position to check if it will be a draw by repetition
    #
    # Returns if the game will end in a draw by repetition if position appears again
    def is_repetition_draw_on_position(self, position: int) -> bool:
        if (self._draw_by_repetition_position != None):
            return True
        elif (position in self._repeated_positions):
            return self._repeated_positions[position] >= (self._MAX_REPEATED_POSITIONS_BEFORE_DRAW - 1)
        else:
            return False
    
    # Gets if the game is over (stalemate or checkmate)
    #
    # Returns true if the game is over (stalemate or checkmate) and false otherwise
    #@profile
    def _is_game_over(self) -> bool:
        # The game is over (stalemate or checkmate) if there are no valid moves for the team whose turn it is
        if (self._turn == TeamColor.WHITE):
            # Check if the white valid moves have already been generated
            if (self._white_valid_moves != None):
                # Return if there's no legal moves (stalemate or checkmate)
                return len(self._white_valid_moves) == 0
            
            # Get the other team to check if their king is in check
            other_team = TeamColor.BLACK
        else:
            # Check if the black valid moves have already been generated
            if (self._black_valid_moves != None):
                # Return if there's no legal moves (stalemate or checkmate)
                return len(self._black_valid_moves) == 0
            
            # Get the other team to check if their king is in check
            other_team = TeamColor.WHITE

        # Check if other king is in check (game over by being in checkmate)

        # TODO: Fix when figured out how we're checking game ended state
        # Get the king location for the other team
        other_king_coord = self._pieces.get_king_coord(other_team)

        # Check if their team is in check (if so, game is over - checkmate) - return empty list as no valid moves
        if (self._team_attacking_coord(self._turn, other_king_coord)):
            return True

        # Get the king location for the team who's turn it is
        king_coord = self._pieces.get_king_coord(self._turn)
        # Get the valid check coordinates for the king
        valid_check_coords: list[Coordinate] | None = self._get_valid_check_coords(king_coord, other_team)

        for piece_type in PieceType:
            # Get the pieces for the piece type
            piece_locations = self._pieces.get_piece_locations_and_action_info(piece_type, self._turn)

            # Check if the piece type is a king
            if (piece_type == PieceType.KING):
                # Get the pieces attacking the king from the attack array
                from_attack_dict = self._attack_arr[king_coord.row][king_coord.col][other_team]
                for to_coord in piece_locations[king_coord].valid_move_coords:
                    # Get the row direction fo the move (positive, negative, or zero)
                    row_dir =   (SignDirection.ZERO if to_coord.row == king_coord.row else 
                                (SignDirection.POSITIVE if to_coord.row > king_coord.row else SignDirection.NEGATIVE))
                    
                    # Get the column direction of the move (positive, negative, or zero)
                    col_dir =   (SignDirection.ZERO if to_coord.col == king_coord.col else 
                                (SignDirection.POSITIVE if to_coord.col > king_coord.col else SignDirection.NEGATIVE))

                    # Check if the king is not in check after the move
                    # Checks both if the space the king is moving to is under attack and if any of the pieces previously attacking it still do
                    if (self._team_attacking_coord(other_team, to_coord) or
                        self._move_puts_king_in_check(king_coord, to_coord, row_dir, col_dir, True, from_attack_dict)):
                        continue

                    # Game is not over (there's a legal move)
                    return False
            else:
                # Check if the king is in check
                if (valid_check_coords != None):
                    # Check if double check (meaning multiple pieces are attacking the king)
                    # Check if multiple types of pieces are attacking or if only one type check if multiple of that type are attacking
                    # King must move on double check so no other piece moves are valid, therefore return empty list
                    if (len(valid_check_coords) == 0):
                        # Return empty list as the king must move (no other piece can get the king out of check)
                        continue
                    # Otherwise Single check (continuing signifies single check - no need to set anything)
                
                # Loop through the pieces and get the moves for each piece
                for piece_coord in piece_locations:
                    # Get the pieces attacking the piece from the attack array
                    from_attack_dict = self._attack_arr[piece_coord.row][piece_coord.col][other_team]
                    # Loop through the valid moves piece action info and create a move for each one
                    for to_coord in piece_locations[piece_coord].valid_move_coords:
                        # Check if move causes check
                        if (self._king_in_check_after_non_king_move(piece_coord, to_coord, king_coord, valid_check_coords, from_attack_dict)):
                            continue

                        # Game is not over (there's a legal move)
                        return False
        
        # No legal moves (stalemate or checkmate)
        return True
    
    # Gets a list of all legal next moves for a team
    # Returns the list of moves objects
    #
    # Parameters:
    #   team_color: The team color to get the legal moves for (default is None which gets the legal moves for the current turn)
    #
    # TODO: Return a list of moves instead so no conversion is needed for minimax (currently converting to string and then back to move)
    #
    # Returns a list of all legal next moves as move objects based on the team color
    #@profile
    def get_all_legal_moves(self, team_color: TeamColor | None = None) -> list[Move]:
        # piece_for_logging = self._pieces.get_piece_locations_and_action_info(PieceType.ROOK, TeamColor.WHITE)
        # piece_coord_for_logging = Coordinate(6, 0)
        # piece_to_coord_for_logging = Coordinate(1,0)

        # if (piece_coord_for_logging in piece_for_logging):
        #     if (piece_to_coord_for_logging in piece_for_logging[piece_coord_for_logging].valid_move_coords):
        #         print("Rook (h5) for logging:")
        #         print(piece_for_logging[piece_coord_for_logging])

        # for piece_type in PieceType:
        #     # Get the pieces for the piece type
        #     piece_locations = self._pieces.get_piece_locations_and_action_info(piece_type, team_color)

        #     if (piece_coord_for_logging in piece_locations):
        #         print("Piece (h5):")
        #         print(piece_locations[piece_coord_for_logging])
        #         print(piece_type)

        # If no team color was provided then get the legal moves for the current turn
        if (team_color == None):
            team_color = self._turn

        if (team_color == TeamColor.WHITE):
            # Check if the white valid moves have already been generated
            if (self._white_valid_moves != None):
                # Return the white valid moves
                return self._white_valid_moves
            
            # Get the other team to check if their king is in check
            other_team = TeamColor.BLACK
        else:
            # Check if the black valid moves have already been generated
            if (self._black_valid_moves != None):
                # Return the black valid moves
                return self._black_valid_moves
            
            # Get the other team to check if their king is in check
            other_team = TeamColor.WHITE
        
        # Create a list of all legal moves
        legal_moves = []

        # Check if other king is in check (game over by being in checkmate)

        # TODO: Fix when figured out how we're checking game ended state
        # Get the king location for the other team
        other_king_coord = self._pieces.get_king_coord(other_team)

        # Check if their team is in check (if so, game is over - checkmate) - return empty list as no valid moves
        if (self._team_attacking_coord(team_color, other_king_coord)):
            return legal_moves

        # Get the king location for the team who's turn it is
        king_coord = self._pieces.get_king_coord(team_color)
        # Get the valid check coordinates for the king
        valid_check_coords: list[Coordinate] | None = self._get_valid_check_coords(king_coord, other_team)

        for piece_type in PieceType:
            # Get the pieces for the piece type
            piece_locations = self._pieces.get_piece_locations_and_action_info(piece_type, team_color)

            # Check if the piece type is a king
            if (piece_type == PieceType.KING):
                # Get the pieces attacking the king from the attack array
                from_attack_dict = self._attack_arr[king_coord.row][king_coord.col][other_team]
                for to_coord in piece_locations[king_coord].valid_move_coords:
                    # Get the row direction fo the move (positive, negative, or zero)
                    row_dir =   (SignDirection.ZERO if to_coord.row == king_coord.row else 
                                (SignDirection.POSITIVE if to_coord.row > king_coord.row else SignDirection.NEGATIVE))
                    
                    # Get the column direction of the move (positive, negative, or zero)
                    col_dir =   (SignDirection.ZERO if to_coord.col == king_coord.col else 
                                (SignDirection.POSITIVE if to_coord.col > king_coord.col else SignDirection.NEGATIVE))

                    # Check if the king is not in check after the move
                    # Checks both if the space the king is moving to is under attack and if any of the pieces previously attacking it still do
                    if (self._team_attacking_coord(other_team, to_coord) or
                        self._move_puts_king_in_check(king_coord, to_coord, row_dir, col_dir, True, from_attack_dict)):
                        continue

                    # Add the move
                    legal_moves.append(Move(from_coord=king_coord, to_coord=to_coord, promotion=None))
            else:
                # Check if the king is in check
                if (valid_check_coords != None):
                    # Check if double check (meaning multiple pieces are attacking the king)
                    # Check if multiple types of pieces are attacking or if only one type check if multiple of that type are attacking
                    # King must move on double check so no other piece moves are valid, therefore return empty list
                    if (len(valid_check_coords) == 0):
                        # Return empty list as the king must move (no other piece can get the king out of check)
                        continue
                    # Otherwise Single check (continuing signifies single check - no need to set anything)
                
                # Check if the piece type is a pawn
                if (piece_type == PieceType.PAWN):
                    promotion_row = self._get_pawn_promotion_row(team_color)
                    # Loop through the pieces and get the moves for each piece
                    for piece_coord in piece_locations:
                        # Get the pieces attacking the pawn from the attack array
                        from_attack_dict = self._attack_arr[piece_coord.row][piece_coord.col][other_team]
                        # Loop through the valid moves piece action info and create a move for each one
                        for to_coord in piece_locations[piece_coord].valid_move_coords:
                            # Check if move causes check
                            if (self._king_in_check_after_non_king_move(piece_coord, to_coord, king_coord, valid_check_coords, from_attack_dict)):
                                continue

                            # Check if the move is a promotion
                            if (to_coord.row == promotion_row):
                                # Add the promotion moves (same move but with different promotion pieces)
                                legal_moves.append(Move(from_coord=piece_coord, to_coord=to_coord, promotion=PieceType.QUEEN))
                                legal_moves.append(Move(from_coord=piece_coord, to_coord=to_coord, promotion=PieceType.ROOK))
                                legal_moves.append(Move(from_coord=piece_coord, to_coord=to_coord, promotion=PieceType.BISHOP))
                                legal_moves.append(Move(from_coord=piece_coord, to_coord=to_coord, promotion=PieceType.KNIGHT))
                            else:
                                # Add the move
                                legal_moves.append(Move(from_coord=piece_coord, to_coord=to_coord, promotion=None))
                else:
                    # Loop through the pieces and get the moves for each piece
                    for piece_coord in piece_locations:
                        # Get the pieces attacking the piece from the attack array
                        from_attack_dict = self._attack_arr[piece_coord.row][piece_coord.col][other_team]
                        # Loop through the valid moves piece action info and create a move for each one
                        for to_coord in piece_locations[piece_coord].valid_move_coords:
                            # Check if move causes check
                            if (self._king_in_check_after_non_king_move(piece_coord, to_coord, king_coord, valid_check_coords, from_attack_dict)):
                                # if piece_type == PieceType.KNIGHT and piece_coord == Coordinate(2, 2) and to_coord == Coordinate(3, 4):
                                #     print("Knight (c3) for logging:")
                                #     print(piece_locations[piece_coord])
                                #     print(piece_type)
                                #     print("To Coord:")
                                #     print(to_coord)
                                continue

                            # Add the move
                            # if (piece_coord == piece_coord_for_logging):
                            #     # print("Piece (h5):")
                            #     # print(piece_locations[piece_coord])
                            #     # print(piece_type)
                            #     if (to_coord == piece_to_coord_for_logging):
                            #         print("To Coord:")
                            #         print(to_coord)
                            legal_moves.append(Move(from_coord=piece_coord, to_coord=to_coord, promotion=None))
                
        # # Loop through the moves and convert them to move strings
        # for i in range(len(legal_moves)):
        #     legal_moves[i] = str(legal_moves[i])

        # If the team color is white then save the white valid moves
        if (team_color == TeamColor.WHITE):
            self._white_valid_moves = legal_moves
        # Otherwise save the black valid moves
        else:
            self._black_valid_moves = legal_moves

        return legal_moves

    # Moves the piece using a move object
    #
    # Parameters:
    #   move: The move object
    #
    # Returns if the move was successful (legal or not)
    #@profile
    def move(self, move: Move) -> bool:
        # Check if the move is not None
        if (move == None):
            print("Move is None")
            return False

        # Check if the move doesn't move at all (from and to coordinates are the same) which is invalid
        if (move.from_coord == move.to_coord):
            print("Move Invalid - From and To coordinates are the same")
            return False
        
        # Check what piece is at the from coordinates
        piece = self._board_arr[move.from_coord.row][move.from_coord.col]
        
        # Check if there is a piece at the from coordinates and it is the correct color
        if (piece == None or piece.Color != self._turn):
            if (piece != None):
                print(piece.Color.name + " piece attempted to move but it's " + self._turn.name + "'s turn")
            else:
                print("No piece where the move attempted to move from")
            return False
        # Check if there is a promotion move and confirm the piece is a pawn
        if (move.promotion != None and piece.Type != PieceType.PAWN):
            print("Promotion attempted but piece is not a pawn")
            return False
        
        # Check if to piece doesn't have a piece of the same color (capturing a piece of the same color is not allowed)
        cap_piece = self._board_arr[move.to_coord.row][move.to_coord.col]
        if (cap_piece != None and cap_piece.Color == piece.Color):
            print("Piece attempted to capture a piece of the same color")
            return False
        
        # Check if move is in valid moves
        # Get the valid moves for the piece
        valid_moves = self.get_all_legal_moves()

        # Check if the move is a valid move
        if (move not in valid_moves):
            print("Move is not in valid moves")
            print("Move: " + str(move))
            print("Valid Moves: " + str(valid_moves))
            print("Previous Moves: " + str(self._previous_moves))
            print("Pieces: " + str(self._get_pieces(team_color=self._turn)))
            print("En Passant: " + str(self._en_passant_avail))
            self.print_board()
            self._print_attack_arr()
            return False
            # raise Exception("Move is not in valid moves")
        
        # Confirmed valid move

        # # Update the repeated positions
        # print("Repeated Positions: " + str(self._repeated_positions))
        # print("Zobrist Hash: " + str(self._zobrist_hash))
        # print("Fen: " + self.get_fen())
        # if (self._zobrist_hash not in self._repeated_positions):
        #     self._repeated_positions[self._zobrist_hash] = 1
        # else:
        #     self._repeated_positions[self._zobrist_hash] += 1
        
        # Save the en passant position before the move
        old_en_passant_avail = self._en_passant_avail

        # Save the castling rights before the move
        old_castling_rights = CastlingRights(self._castling_rights.white_kingside, self._castling_rights.white_queenside,
                                         self._castling_rights.black_kingside, self._castling_rights.black_queenside)

        # Variable for if move was en passant
        en_passant = False
        
        # Move the piece
        self._move_piece(move)

        # Check if the move is a pawn move
        if (piece.Type == PieceType.PAWN):
            # Get the pawn direction for the team whose turn it is (used for en passant)
            pawn_direction = self._get_pawn_direction(self._turn)
            
            # Check if the move was a double fourward pawn move
            if (abs(move.to_coord.row - move.from_coord.row) == 2):
                # Set the en passant position to the space the pawn it moving to
                self._en_passant_avail = move.to_coord
            # If not, check for en passant
            # Check that en passant is available
            # Then check that the capture is in the right row (one beyond the pawn being captured) and column (same as the pawn being captured)
            # Make sure there isn't already a capture piece - piece captured on square moved to (i.e. if there is then en passant doesn't occur)
            elif (self._en_passant_avail != None and self._en_passant_avail.row == move.to_coord.row - pawn_direction and 
                self._en_passant_avail.col == move.to_coord.col and abs(move.to_coord.col - move.from_coord.col) == 1 and cap_piece == None):
                # Is en passant
                en_passant = True

                # Set the capture pieces to the piece at the en_passant position
                cap_piece = self._board_arr[self._en_passant_avail.row][self._en_passant_avail.col]
            
                # Remove captured pawn
                self._board_arr[self._en_passant_avail.row][self._en_passant_avail.col] = None

                # Get the captured pawn's attack coordinates
                cap_attack_coords = self._pieces.get_piece_locations_and_action_info(cap_piece.Type, cap_piece.Color)[self._en_passant_avail].attack_coords
                # Remove the captured pawn's attack coordinates from the attack array
                self._remove_piece_from_attack_arr(cap_piece, self._en_passant_avail, cap_attack_coords)
                
                # Remove captured pawn from piece locations
                self._pieces.remove_piece(cap_piece, self._en_passant_avail)

                # Update pieces blocked by the captured en passant pawn
                self._update_pieces_blocked(self._en_passant_avail, cap_piece.Color)

                # Update pawns now unblocked by the captured en passant pawn
                self._update_pawn_non_capture_coord(self._en_passant_avail)

                # Set en passant to None as it's no longer available next move
                self._en_passant_avail = None
            # Otherwise set en passant to None
            else:
                self._en_passant_avail = None
        
        # Check if a rook move
        elif (piece.Type == PieceType.ROOK):
            # Check if the rook moved from the starting position and if so remove the castling rights for that side
            # Don't need to check for team as if the rook moved from a starting position it means either the starting rook isn't there
            if (move.from_coord.row == 0 and move.from_coord.col == 0):
                self._castling_rights.white_queenside = False
            elif (move.from_coord.row == 0 and move.from_coord.col == 7):
                self._castling_rights.white_kingside = False
            elif (move.from_coord.row == 7 and move.from_coord.col == 0):
                self._castling_rights.black_queenside = False
            elif (move.from_coord.row == 7 and move.from_coord.col == 7):
                self._castling_rights.black_kingside = False
        
        # Check for valid king moves
        elif (piece.Type == PieceType.KING):
            # If castling move the rook (the king moves 2 spaces - horizontally - only when castling)
            if (abs(move.to_coord.col - move.from_coord.col) == 2):
                # Check if the move is a king side castle
                if (move.to_coord.col == 6):
                    # Move the rook
                    # print("KingMove -  KingCastle Rook: " + str(Coordinate(move.to_coord.row, 7)) + " -> " + str(Coordinate(move.to_coord.row, 5)))
                    castle_move = Move(Coordinate(move.to_coord.row, 7), Coordinate(move.to_coord.row, 5))
                    self._move_piece(castle_move)
                # Check if the move is a queen side castle
                elif (move.to_coord.col == 2):
                    # Move the rook
                    # print("KingMove -  QueenCastle Rook: " + str(Coordinate(move.to_coord.row, 0)) + " -> " + str(Coordinate(move.to_coord.row, 3)))
                    castle_move = Move(Coordinate(move.to_coord.row, 0), Coordinate(move.to_coord.row, 3))
                    self._move_piece(castle_move)
                else:
                    return False

            # Remove castling rights for the team who's king moved
            if (self._turn == TeamColor.WHITE):
                self._castling_rights.white_queenside = False
                self._castling_rights.white_kingside = False
            elif (self._turn == TeamColor.BLACK):
                self._castling_rights.black_queenside = False
                self._castling_rights.black_kingside = False

        # Move is complete

        # add the move to the previous moves stack
        # Do this before resetting the en_passant_avail and changing the half moves
        move_info = MoveInfo(move, old_castling_rights, self._half_moves, cap_piece.Type if cap_piece != None else None, 
                                             old_en_passant_avail, en_passant, valid_moves)
        self._previous_moves.append(move_info)
        
        # If piece captured was rook, change castling rights if necessary
        if (cap_piece != None and cap_piece.Type == PieceType.ROOK):
            # Check if the rook was a starting rook and if so remove the castling rights for that side
            # Don't need to check for team as if the rook moved from a starting position it means either the starting rook isn't there
            if (move.to_coord.row == 0 and move.to_coord.col == 0):
                self._castling_rights.white_queenside = False
            elif (move.to_coord.row == 0 and move.to_coord.col == 7):
                self._castling_rights.white_kingside = False
            elif (move.to_coord.row == 7 and move.to_coord.col == 0):
                self._castling_rights.black_queenside = False
            elif (move.to_coord.row == 7 and move.to_coord.col == 7):
                self._castling_rights.black_kingside = False

        # If not a pawn move (which sets en passant to the correct value) then set en passant to None
        # Do it down here so it's only on completed moves
        if (not piece.Type == PieceType.PAWN):
            self._en_passant_avail = None
        
        # If pawn move or capture then set half moves to 0
        if (piece.Type == PieceType.PAWN or cap_piece != None):
            self._half_moves = 0
        # Otherwise increment half moves
        else:
            self._half_moves += 1

        # If black moved increment full moves
        if (self._turn == TeamColor.BLACK):
            self._full_moves += 1
            # Switch turns to White
            self._turn = TeamColor.WHITE
        # Otherwise switch turns to Black
        else:
            self._turn = TeamColor.BLACK
        
        # If there was an en passant available previously then remove it from the valid moves as it's no longer available
        # NOTE: Needs to be after the turn has switched - assumes turn is over
        if (old_en_passant_avail != None):
            self._remove_previous_en_passant_moves(old_en_passant_avail)

        # If there's an en passant available add it to the valid moves
        # NOTE: Needs to be after the turn has switched - assumes turn is over
        if (self._en_passant_avail != None):
            # Add the en passant position to valid moves
            self._add_en_passant_moves()
        
        # Update castling moves
        # Castling Rights checked in _update_castling_moves
        # Only update for the team who's turn it is
        if (self._turn == TeamColor.WHITE):
            self._update_castling_moves(TeamColor.WHITE, True)
            self._update_castling_moves(TeamColor.WHITE, False)
        else:
            self._update_castling_moves(TeamColor.BLACK, True)
            self._update_castling_moves(TeamColor.BLACK, False)
        
        # Reset the valid moves
        self._white_valid_moves = None
        self._black_valid_moves = None

        # Set the new zobrist hash
        self._zobrist_hash = self.update_zobrist_hash_from_move_info(move_info)

        # Update the repeated positions
        # print("Repeated Positions: " + str(self._repeated_positions))
        # print("Zobrist Hash: " + str(self._zobrist_hash))
        # print("Fen: " + self.get_fen())
        if (self._zobrist_hash not in self._repeated_positions):
            self._repeated_positions[self._zobrist_hash] = 1
        else:
            self._repeated_positions[self._zobrist_hash] += 1

        # Save if the repititon draw happened for minimax at further depth
        if (self._draw_by_repetition_position == None and self.is_repetition_draw()):
            self._draw_by_repetition_position = self._zobrist_hash

        # Save if the half move draw happened for minimax at further depth
        if (self._draw_by_half_move_position == None and self.is_half_move_draw()):
            self._draw_by_half_move_position = self._zobrist_hash

        # print("Move: " + str(move))
        # print("Repeated Times: " + str(self._repeated_positions[self._zobrist_hash]))
        # print("Is Repetition Draw: " + str(self.is_repetition_draw()))
        # print("Max Repeated Times: " + str(self._MAX_REPEATED_POSITIONS_BEFORE_DRAW))
        # print()
        # print("Half Moves: " + str(self._half_moves))
        # print("Is Half Move Draw: " + str(self.is_half_move_draw()))
        # print("Max Half Moves: " + str(self._MAX_HALF_MOVES_BEFORE_DRAW))
        # print()
        # print()

        
        # Valid move return true
        return True
    
    # Undoes the previous move made (can be called mutliple times to undo that many moves)
    #
    # Returns if the undo was successful or not
    #
    # NOTE: If there are no previous moves to undo then the board will not change and False will be returned
    # NOTE: Does not check if the previous move is valid or not (assumes the preivous move is valid and may cause issues/errors if not)
    #@profile
    def undo_move(self) -> bool:
        # Make sure there is a previous move to undo
        if (len(self._previous_moves) == 0):
            return False
        
        # Get the previous move
        prev_move = self._previous_moves.pop()

        # Remove the current position from the repeated positions
        # Since this was a previous move we can assume it was added to the repeated positions
        # print("Repeated Positions: " + str(self._repeated_positions))
        # print("Zobrist Hash: " + str(self._zobrist_hash))
        # print("Fen: " + self.get_fen())
        # print('Zobrist if updated: ', self.update_zobrist_hash_from_move_info(prev_move))
        # if self._zobrist_hash not in self._repeated_positions:
        #     self._zobrist_hash = self.update_zobrist_hash_from_move_info(prev_move)
        if (self._repeated_positions[self._zobrist_hash] == 1):
            del self._repeated_positions[self._zobrist_hash]
        else:
            self._repeated_positions[self._zobrist_hash] -= 1

        old_zobrist_hash = self._zobrist_hash

        # Remove the saved draw by repetition position if it was caused by the previous move
        if (self._draw_by_repetition_position == self._zobrist_hash and not self.is_repetition_draw(only_this_position=True)):
            self._draw_by_repetition_position = None

        # Update the zobrist hash for the move
        self._zobrist_hash = self.update_zobrist_hash_from_move_info(prev_move)

        # print('Zobrist after undo: ', self._zobrist_hash)

        # Get the piece to move back
        piece = self._board_arr[prev_move.move.to_coord.row][prev_move.move.to_coord.col]

        # Save the en passant available to be undone
        old_en_passant_avail = self._en_passant_avail

        # Set the capture piece to undo intially to None
        undo_cap_piece = None
        # If en_passant then add the captured piece back by setting variable to undo a en passant move in _move_piece
        undoing_en_passant = prev_move.en_passant
        # If a capture then add the piece back by setting variable to add the captured piece back in _move_piece
        if (prev_move.cap_piece_type != None):
            # Recreate the captured piece (will be same color as current turn - as the piece was captured by the other team on the previous turn)
            undo_cap_piece = Piece(prev_move.cap_piece_type, self._turn)

        # print("Undoing Move")

        # Undo the move
        # Move the piece back (switch to and from coord, then undo promotion to pawn if any)
        self._move_piece(Move(prev_move.move.to_coord, prev_move.move.from_coord, None if prev_move.move.promotion == None else PieceType.PAWN), 
                         undo_cap_piece, undoing_en_passant)
        
        # If castling move then move the rook back
        if (abs(prev_move.move.to_coord.col - prev_move.move.from_coord.col) == 2 and piece.Type == PieceType.KING):
            # Check if kingside castle
            if (prev_move.move.to_coord.col == 6):
                # print("Undoing Castle Kingside")
                # Move the rook back (can't capture on castle)
                castle_move = Move(Coordinate(prev_move.move.to_coord.row, 5), Coordinate(prev_move.move.to_coord.row, 7))
                self._move_piece(castle_move)
            # Check if queenside castle
            elif (prev_move.move.to_coord.col == 2):
                # print("Undoing Castle Queenside")
                # Move the rook back (can't capture on castle)
                castle_move = Move(Coordinate(prev_move.move.to_coord.row, 3), Coordinate(prev_move.move.to_coord.row, 0))
                self._move_piece(castle_move)
        
        # Successfully undid the move
        # Decrement full moves if black moved
        if (self._turn == TeamColor.WHITE):
            self._turn = TeamColor.BLACK
            self._full_moves -= 1

            # Set black's legal moves to the previous legal moves
            self._black_valid_moves = prev_move.valid_moves

            # Reset white's legal moves
            self._white_valid_moves = None
        # Otherwise switch turns to White
        else:
            self._turn = TeamColor.WHITE

            # Set white's legal moves to the previous legal moves
            self._white_valid_moves = prev_move.valid_moves

            # Reset the black's legal move
            self._black_valid_moves = None
        
        # Reset half moves to previous value
        self._half_moves = prev_move.half_moves

        # Remove the saved draw by half move position if it was caused by the previous move
        if (self._draw_by_half_move_position == old_zobrist_hash and not self.is_half_move_draw(only_this_position=True)):
            self._draw_by_half_move_position = None

        # Reset en passant to previous value
        self._en_passant_avail = prev_move.en_passant_avail

        # Reset castling rights to previous value
        self._castling_rights = prev_move.castling_rights

        # If there was an en passant available previously then remove it from the valid moves as it's no longer available
        # NOTE: Needs to be after the turn has switched - assumes turn is over
        if (old_en_passant_avail != None):
            self._remove_previous_en_passant_moves(old_en_passant_avail)

        # If there's an en passant available add it to the valid moves
        # NOTE: Needs to be after the turn has switched - assumes turn is over
        if (self._en_passant_avail != None):
            # Add the en passant position to valid moves
            self._add_en_passant_moves()
        
        # Update castling moves
        # Castling Rights checked in _update_castling_moves
        # Only update for the team who's turn it is
        if (self._turn == TeamColor.WHITE):
            self._update_castling_moves(TeamColor.WHITE, True)
            self._update_castling_moves(TeamColor.WHITE, False)
        else:
            self._update_castling_moves(TeamColor.BLACK, True)
            self._update_castling_moves(TeamColor.BLACK, False)        

        # Completed undoing move return True
        return True



    # Private method that moves a piece on the board array and updates the piece locations (including attack coordinates)
    #
    # Parameters:
    #   move: The move to make
    #   undo_cap_piece: The piece that was captured on the from_coord if any (since only for undoing - it was the previous move's to_coord)
    #                   Used ONLY for undoing the move (otherwise it should be the default - None)
    #   undoing_en_passant: Whether the move to undo is an en passant move or not (undo_cap_piece should be PieceType.PAWN if undoing_en_passant is True)
    #                       Set to True ONLY for undoing en passant moves (otherwise it should be the default - False)
    #
    # NOTE: This method does NOT check if the move is valid or not (assumes the move is valid)
    # NOTE: This method does NOT account for en passant (however, it does account for promotion as promotion is in the move object)
    # NOTE: undo_cap_piece should only be used when undoing a move that had a capture (if undoing en passant undo_cap_piece should be PieceType.PAWN)
    # NOTE: undoing_en_passant should only be used when undoing an en passant move
    #@profile
    def _move_piece(self, move: Move, undo_cap_on_space_piece: Piece = None, undoing_en_passant: bool = False):
        # Get the piece at the from coordinates
        piece = self._board_arr[move.from_coord.row][move.from_coord.col]

        # print("Moving Piece: " + str(piece))

        # Check if there is a piece at the to coordinates
        cap_piece = self._board_arr[move.to_coord.row][move.to_coord.col]

        # Get all the old attack coordinates for the piece
        old_attack_coords = self._pieces.get_piece_locations_and_action_info(piece.Type, piece.Color)[move.from_coord].attack_coords
        
        # Save the old piece
        old_piece = piece

        # Check if promotion and change the new piece to the promotion piece
        if (move.promotion != None):
            # Change the piece to the promotion piece
            piece = Piece(move.promotion, piece.Color)
        
        # Moves the piece on the board
        self._board_arr[move.to_coord.row][move.to_coord.col] = piece
        # Check if undoing en passant and if so add the captured pawn and set the from_coord to None
        if (undoing_en_passant):
            # If en passant move then set en passant available to correct location (to row (from on previous move), and from col (to on previous move))
            undo_coord = Coordinate(move.to_coord.row, move.from_coord.col)
            self._board_arr[move.from_coord.row][move.from_coord.col] = None
            self._board_arr[undo_coord.row][undo_coord.col] = undo_cap_on_space_piece
        # Otherwise undo the capture if any, if not undoing or no capture undo_cap_on_space_piece should always be None
        else:
            undo_coord = move.from_coord
            self._board_arr[move.from_coord.row][move.from_coord.col] = undo_cap_on_space_piece

        # Remove all the old attack coordinates for the piece
        # Must be done after the piece is moved so blocking pieces are updated correctly
        self._remove_piece_from_attack_arr(old_piece, move.from_coord, old_attack_coords)

        # Remove the old piece from the piece locations
        self._pieces.remove_piece(old_piece, move.from_coord)

        # If undoing a capture on the space the previous piece moved to then add the piece back to the piece locations
        if (undo_cap_on_space_piece != None):
            # Get all the captured piece's attack coordinates for the piece
            cap_action_info = self._get_action_info_for_piece(PieceCoordinate(undo_cap_on_space_piece, undo_coord))
            # Add all the new attack coordinates for the piece to the attack array
            self._add_piece_to_attack_arr(undo_cap_on_space_piece, undo_coord, cap_action_info.attack_coords)

            # Add the captured piece back to the piece locations
            self._pieces.add_piece(undo_cap_on_space_piece, undo_coord, cap_action_info)

            # If en passant then update pieces blocked for the captured pawn
            if (undoing_en_passant):
                # Update all the pawns the en passant pawn is now blocking (non capture moves)
                self._update_pawn_non_capture_coord(undo_coord)
                # Update all the other pieces this capture piece was blocking
                self._update_pieces_blocked(move.from_coord, piece.Color)
                # Update all the other pieces the captured en passant pawn is now blocking
                self._update_pieces_blocked(undo_coord, undo_cap_on_space_piece.Color, move.from_coord, move.to_coord)
            # Normal Undo Capture - Allows for special case for more efficient updating blocked pieces
            else:
                # Update all the other pieces this piece was blocking (knowing it was a capture we can update more efficiently)
                # From coord was the capture sinc this is an undo move
                self._update_pieces_blocked_when_undoing_capture(move.from_coord, move.to_coord)
            
            # Update all the other pieces this piece is blocking
            self._update_pieces_blocked(move.to_coord, piece.Color, move.from_coord)
            
        # Otherwise no capture so update pieces blocked for the piece moved to
        else:
            # If there was a capture then remove the piece from the piece locations
            if (cap_piece != None):
                # Get all the captured piece's attack coordinates for the piece
                cap_attack_coords = self._pieces.get_piece_locations_and_action_info(cap_piece.Type, cap_piece.Color)[move.to_coord].attack_coords
                # Remove all the old attack coordinates for the piece
                self._remove_piece_from_attack_arr(cap_piece, move.to_coord, cap_attack_coords)

                # Remove the captured piece from the piece locations
                self._pieces.remove_piece(cap_piece, move.to_coord)

                # Update all the other pieces this piece is blocking (knowing it was a capture we can update more efficiently)
                self._update_pieces_blocked_after_capture(move.to_coord)
            # No Capture so update pieces blocked for the piece moved to
            else:
                # Update all the other pieces this piece is blocking
                self._update_pieces_blocked(move.to_coord, piece.Color, move_from_coord=move.from_coord)

            # Update all the other pieces this piece was blocking
            self._update_pieces_blocked(move.from_coord, piece.Color)
        
        # Get new action info for the piece
        new_action_info = self._get_action_info_for_piece(PieceCoordinate(piece, move.to_coord))
        # Add all the new attack coordinates for the piece to the attack array
        self._add_piece_to_attack_arr(piece, move.to_coord, new_action_info.attack_coords)

        # Add the new piece to the piece locations
        self._pieces.add_piece(piece, move.to_coord, new_action_info)

        # Update all the pawns this peice was blocking (non capture moves)
        self._update_pawn_non_capture_moves(move)



    # Remove a piece's attack coordinates from the attack array
    #
    # Parameters:
    #   piece: The piece to remove
    #   coord: The coordinate of the piece to remove
    #   attack_coords: The attack coordinates of the piece
    #@profile
    def _remove_piece_from_attack_arr(self, piece: Piece, coord: Coordinate, attack_coords: list[Coordinate]):
        # print("Removing Piece: " + str(piece) + " at " + str(coord) + " with attack coords: " + str(attack_coords))
        # Remove all the attack coordinates for the piece
        for attack_coord in attack_coords:

            # Get the attack list for the coordinate, team, and piece type
            try:
                attack_list = self._attack_arr[attack_coord.row][attack_coord.col][piece.Color][piece.Type]
            except KeyError:
                print("Removing Piece: " + str(piece) + " at " + str(coord) + " with attack coords: " + str(attack_coords))
                self.print_board()
                self._print_attack_arr()
                raise Exception("KeyError: " + str(piece) + " at " + str(coord) + " with attack coords: " + str(attack_coords))
            # Remove the piece from the attack dict
            attack_list.remove(coord)
            
            # Check if there's no more pieces of this type and color at this coordinate after removing the piece
            if (len(attack_list) == 0):
                # Remove the piece type dict from the attack dict for the coordinate and color
                del self._attack_arr[attack_coord.row][attack_coord.col][piece.Color][piece.Type]

    # Add a piece's attack coordinates to the attack array
    #
    # Parameters:
    #   piece: The piece to add
    #   coord: The coordinate of the piece to add
    #   attack_coords: The attack coordinates of the piece
    #@profile
    def _add_piece_to_attack_arr(self, piece: Piece, coord: Coordinate, attack_coords: list[Coordinate]):
        # print("Adding Piece: " + str(piece) + " at " + str(coord) + " with attack coords: " + str(attack_coords))
        # Add all the attack coordinates for the piece
        for attack_coord in attack_coords:
            # Get the attack dict for the coordinate
            attack_dict = self._attack_arr[attack_coord.row][attack_coord.col][piece.Color]

            # Check if the attack dict already has the piece
            if (piece.Type in attack_dict):
                # Add the piece to the attack dict
                attack_dict[piece.Type].append(coord)
            else:
                # Add the piece to the attack dict
                attack_dict[piece.Type] = [coord]

    # Updates the attack array with the new attack coordinates for the pieces that attack the coordinate after a capture 
    # This means that the same pieces will be blocked and the attack coordinates will be the same however whether or not the piece can move to the
    # coordinate will change as the piece on the coordinate will now be on the opposite team of the one captured
    # 
    # Parameters:
    #   coord: The coordinate of the piece that was captured (same as the coordinate of the piece that moved to the capture coordinate)
    #
    # NOTE: Assumes that there is a piece at the coordinate (coord)
    #@profile
    def _update_pieces_blocked_after_capture(self, coord: Coordinate):
        attack_dict = self._attack_arr[coord.row][coord.col]

        piece = self._board_arr[coord.row][coord.col]

        # Loop through the teams
        for team in attack_dict:
            # Loop through the piece types (get it as a list now, since we'll be modifying the dict)
            for piece_type in list(attack_dict[team]):
                # Loop through the pieces
                for blocked_coord in attack_dict[team][piece_type]:
                    # Only update valid moves depending on if this move is available for the piece 
                    blocked_piece = self._board_arr[blocked_coord.row][blocked_coord.col]

                    # If the piece that captured (remains on board) is the same as the piece attacking, remove the legal move
                    if (piece.Color == blocked_piece.Color):
                        # Remove coord from the piece's valid move coordinates
                        self._remove_valid_move(piece_type, team, blocked_coord, coord)
                    # Otherwise the piece can capture so add the piece to the valid moves (couldn't capture before as the captured piece was on it's team)
                    else:
                        # Add coord to the piece's valid move coordinates
                        self._add_valid_move(piece_type, team, blocked_coord, coord)

    # Updates the attack array with the new attack coordinates for the pieces that attack the coordinate when undoing a capture 
    # This means that the same pieces will be blocked and the attack coordinates will be the same however whether or not the piece can move to the
    # coordinate will change as the piece on the coordinate will now be on the opposite team of the one captured. However also need to check to make
    # sure the piece that captured isn't from a position that blocks the piece being considered.
    # 
    # Parameters:
    #   capt_coord: The coordinate of the piece that was captured (same as the coordinate of the piece that moved to the capture coordinate)
    #   prev_coord: The coordinate the piece moved from to capture
    #
    # NOTE: Assumes that there is a piece at the coordinate (coord)
    #@profile
    def _update_pieces_blocked_when_undoing_capture(self, capt_coord: Coordinate, prev_coord: Coordinate):
        attack_dict = self._attack_arr[capt_coord.row][capt_coord.col]

        to_prev_is_valid_dir = (capt_coord.row == prev_coord.row) or (capt_coord.col == prev_coord.col) or (abs(capt_coord.row - prev_coord.row) == abs(capt_coord.col - prev_coord.col))
        if (to_prev_is_valid_dir):
            prev_row_dir = SignDirection.ZERO if capt_coord.row == prev_coord.row else SignDirection.NEGATIVE if capt_coord.row > prev_coord.row else SignDirection.POSITIVE
            prev_col_dir = SignDirection.ZERO if capt_coord.col == prev_coord.col else SignDirection.NEGATIVE if capt_coord.col > prev_coord.col else SignDirection.POSITIVE

        piece = self._board_arr[capt_coord.row][capt_coord.col]

        # CAN'T DO THIS
        # Need to check if new piece is in way of piece checking
        # Queen could both be in the prev attack dict and the new one and not have the capture piece in the way

        # Loop through the teams
        for team in attack_dict:
            # Loop through the piece types (get it as a list now, since we'll be modifying the dict)
            for piece_type in list(attack_dict[team]):
                # Loop through the pieces
                for blocked_coord in attack_dict[team][piece_type]:
                    # Only update valid moves depending on if this move is available for the piece 
                    blocked_piece = self._board_arr[blocked_coord.row][blocked_coord.col]

                    # If the piece that captured (remains on board) is the same as the piece attacking, remove the legal move
                    if (piece.Color == blocked_piece.Color):
                        # Remove coord from the piece's valid move coordinates
                        self._remove_valid_move(piece_type, team, blocked_coord, capt_coord)
                    # Otherwise the piece can capture so add the piece to the valid moves (couldn't capture before as the captured piece was on it's team)
                    # Only do this if the piece that captured isn't blocking the piece being considered (not in the attack array for the 
                    # location the capture piece is now)
                    else:
                        # Check if the piece could be blocking another piece that could capture (must be in valid direction to block)
                        if (to_prev_is_valid_dir):
                            blocked_coord_row_dir = SignDirection.ZERO if capt_coord.row == blocked_coord.row else SignDirection.NEGATIVE if capt_coord.row > blocked_coord.row else SignDirection.POSITIVE
                            blocked_coord_col_dir = SignDirection.ZERO if capt_coord.col == blocked_coord.col else SignDirection.NEGATIVE if capt_coord.col > blocked_coord.col else SignDirection.POSITIVE

                            # Check if blocking - if it is (same direction in row and col) then skip
                            if (prev_row_dir == blocked_coord_row_dir and prev_col_dir == blocked_coord_col_dir):
                                continue
                        # Add coord to the piece's valid move coordinates
                        self._add_valid_move(piece_type, team, blocked_coord, capt_coord)
    
    # Updates the attack array with the new attack coordinates for the pieces that attack the coordinate (means either were blocked or will be blocked)
    #
    # Parameters:
    #   coord: The coordinate of the piece that was moved
    #   move_color: The color of the piece that was moved
    #   move_from_coord: The coordinate the piece moved from (default None if coord is the from coordinate)
    #   undoing_en_passant_coord: The coordinate of the capturing piece after undoing en passant (default None if not undoing en passant)
    # 
    # NOTE: This does not include pawn pieces that are blocked for non attacting (capture) moves
    # NOTE: This assumed this was either (the from coordinate) or (the to coordinate on a non-capture move)
    #       Use _update_pieces_blocked_after_capture for the to coordinate on a capture move
    # NOTE: Assumes that move_from_coord is NOT coord.
    #       So if coord is the from coordinate (or there wasn't a from coordinate) then move_from_coord should be None
    #
    # TODO: See if there's ways to avoid updating piece twice when affected by both from and to coordinates
    # TODO: See if there's a way to just do one update (for to and from) instead of two for each move in castling
    #@profile
    def _update_pieces_blocked(self, coord: Coordinate, move_color: TeamColor, move_from_coord: Coordinate | None = None, 
                               undoing_en_passant_coord: Coordinate | None = None):
        attack_dict = self._attack_arr[coord.row][coord.col]

        piece = self._board_arr[coord.row][coord.col]

        # Loop through the teams
        for team in attack_dict:
            # Loop through the piece types (get it as a list now, since we'll be modifying the dict)
            for piece_type in list(attack_dict[team]):
                # Loop through the pieces
                for blocked_coord in attack_dict[team][piece_type]:
                    # Get the piece being blocked
                    blocked_piece = self._board_arr[blocked_coord.row][blocked_coord.col]

                    # print("Updating Piece Blocked: " + str(blocked_piece) + " - " + str(blocked_coord) + " - " + str(piece) + " - " + str(coord))

                    # Check if the piece type is a pawn (pawn can't be blocked for attack coordinates)
                    if (piece_type == PieceType.PAWN):
                        # Always check for capture move (only ones kept by the attack array)
                        # If piece is not there or the piece is the same color as the piece that moved then remove the piece from the valid moves
                        if (piece == None or piece.Color == blocked_piece.Color):
                            # Remove coord from the piece's valid move coordinates
                            self._remove_valid_move(piece_type, team, blocked_coord, coord)
                        # Otherwise add the piece to the valid moves
                        else:
                            # Add coord to the piece's valid move coordinates
                            self._add_valid_move(piece_type, team, blocked_coord, coord)
                    # Check if the piece type is a knight or king (these pieces can't be blocked for attack coordinates)
                    elif (piece_type == PieceType.KNIGHT or piece_type == PieceType.KING):
                        # If piece isn't there or is not the same color as the piece that moved then add the piece to the valid moves
                        if (piece == None or piece.Color != blocked_piece.Color):
                            # Add coord to the piece's valid move coordinates
                            # TODO: Need to check it's not already added
                            self._add_valid_move(piece_type, team, blocked_coord, coord)
                        # Otherwise remove the piece from the valid moves (as it can't capture piece on it's team)
                        else:
                            # Remove coord from the piece's valid move coordinates
                            self._remove_valid_move(piece_type, team, blocked_coord, coord)
                    else:
                        # Check if the move_from_coord is the same as blocked coord 
                        # Means it's an undo capture move and the blocking piece has already been updated
                        # As such skip updating this piece 
                        if (move_from_coord != blocked_coord):
                            # Get the direction from the blocked piece to the piece that moved
                            row_dir =   (SignDirection.POSITIVE if coord.row > blocked_coord.row else 
                                        (SignDirection.NEGATIVE if coord.row < blocked_coord.row else SignDirection.ZERO))
                            col_dir =   (SignDirection.POSITIVE if coord.col > blocked_coord.col else 
                                        (SignDirection.NEGATIVE if coord.col < blocked_coord.col else SignDirection.ZERO))
                            
                            # Get the max spaces to move (if the from coord is in the same direction - don't move past the from coord)
                            # Except if coord is the from coord (then no issue)
                            max_spaces = 7
                            # Check that's there's a from coord and that it's in a blocking position (same row, column, or diagonal)
                            if (move_from_coord != None and (move_from_coord.row == coord.row or move_from_coord.col == coord.col or 
                                                             abs(move_from_coord.row - coord.row) == abs(move_from_coord.col - coord.col))):
                                # Get the direction from the the piece that moved to move_from_coord
                                from_row_dir =  (SignDirection.POSITIVE if move_from_coord.row > coord.row else 
                                                (SignDirection.NEGATIVE if move_from_coord.row < coord.row else SignDirection.ZERO))
                                from_col_dir =  (SignDirection.POSITIVE if move_from_coord.col > coord.col else 
                                                (SignDirection.NEGATIVE if move_from_coord.col < coord.col else SignDirection.ZERO))
                                
                                # Check if the blocked piece is in the same direction as the from coord
                                if (row_dir == from_row_dir and col_dir == from_col_dir):
                                    # Get the distance from the blocked piece to the from coord
                                    row_dist = abs(move_from_coord.row - coord.row)
                                    col_dist = abs(move_from_coord.col - coord.col)

                                    # Get the max spaces to move
                                    max_spaces = max(row_dist, col_dist)
                                # Otherwise check if it's in the other direction (means its already been checked by from coord)
                                else:
                                    # Get the direction from the the piece that moved to move_from_coord
                                    opposite_from_row_dir =  (SignDirection.NEGATIVE if move_from_coord.row > coord.row else 
                                                             (SignDirection.POSITIVE if move_from_coord.row < coord.row else SignDirection.ZERO))
                                    opposite_from_col_dir =  (SignDirection.NEGATIVE if move_from_coord.col > coord.col else 
                                                             (SignDirection.POSITIVE if move_from_coord.col < coord.col else SignDirection.ZERO))
                                    if (row_dir == opposite_from_row_dir and col_dir == opposite_from_col_dir):
                                        # Skip updating this piece
                                        continue

                                    # Check if the piece is the same color as the piece that moved
                                    # This indicates that the piece that moved was not at a valid move coordinate for the blocked piece
                                    # As such subtract one as we don't want to remove that piece from the valid move coordinates (aready removed)
                                    # if (move_color == blocked_piece.Color):
                                    #     max_spaces -= 1
                            
                            # Check if this is an undo en passant where the piece blocked is blcoked by both the captured and capturing piece
                            # This is a special case if the captured piece is closer to the blocked piece, as it will see the capturing piece as blocking
                            # despite it not previously blocking as they were both moved in the same move.
                            # NOTE: Since this is udoing en passant this can only occur horizontally as that's where the pieces begin in an en passant move
                            if (undoing_en_passant_coord != None and undoing_en_passant_coord.row == coord.row and 
                                undoing_en_passant_coord.row == blocked_coord.row and 
                                abs(undoing_en_passant_coord.col - blocked_coord.col) > abs(coord.col - blocked_coord.col)):
                                # Get the piece action info for the blocked_piece in the direction specified
                                # Starting from the capturing coord as there was previously no piece blocking there (also purposely ignore that piece)
                                # NOTE: _get_action_info_for_piece_in_dir does not include the capturing piece's coord
                                # NOTE: Don't need to change max_spaces as the capturing piece moved in a different diagonally, where this is only horizontal
                                new_action_info = self._get_action_info_for_piece_in_dir(PieceCoordinate(blocked_piece, undoing_en_passant_coord), 
                                                                                        row_dir, col_dir, max_spaces=max_spaces)
                                
                                # Add the capturing piece's coord to the action info to remove for both the attack and valid move coordinates
                                # We skipped this piece to prevent it from thinking it was blocking, but it still isn't a valid move or attack coordinate
                                new_action_info.attack_coords.append(undoing_en_passant_coord)
                                new_action_info.valid_move_coords.append(undoing_en_passant_coord)

                            else:
                                # Get the piece action info for the blocked_piece in the direction specified
                                # Starting from coord as that's where the piece was/is blocking from
                                # NOTE: _get_action_info_for_piece_in_dir does not include coord
                                new_action_info = self._get_action_info_for_piece_in_dir(PieceCoordinate(blocked_piece, coord), 
                                                                                        row_dir, col_dir, max_spaces=max_spaces)

                            # Add coord to the piece's add/remove move coordinates depending if the move piece's color is the same as the blocked piece's color
                            # When adding, the piece previously couldn't move to coord as it can't capture a piece on the same team, so needs to be added
                            # When removing, the piece can no longer move to coord as it can't capture a piece on the same team, so needs to be remvoed 
                            if (move_color == blocked_piece.Color):
                                # Add coord to the piece's valid move coordinates
                                new_action_info.valid_move_coords.append(coord)
                                # Also if the from coord is in valid moves then remove it
                                # This is because the piece couldn't have moved to that spot before as it would have captured a piece on it's team
                                if (move_from_coord != None):
                                    try:
                                        new_action_info.valid_move_coords.remove(move_from_coord)
                                    except ValueError:
                                        pass
                            
                            # Check if there's a piece at the blocking position
                            if (piece != None):
                                # print("Removing: " + str(new_action_info))
                                # The piece is now blocking
                                # Remove the piece from the attact array at all the new action info's attack_coords as the piece is now blocked
                                self._remove_piece_from_attack_arr(blocked_piece, blocked_coord, new_action_info.attack_coords)
                                # Remove the new action info's attack_coords and valid_move_coords from the piece's action info as the piece is now blocked
                                self._remove_action_info_after_block(piece_type, team, blocked_coord, new_action_info)
                            else:
                                # print("Adding: " + str(new_action_info))
                                # The piece is no longer blocking
                                # Add the piece to the attact array at all the new action info's attack_coords as the piece is no longer blocked
                                self._add_piece_to_attack_arr(blocked_piece, blocked_coord, new_action_info.attack_coords)
                                # Add the new action info's attack_coords and valid_move_coords to the piece's action info as the piece is no longer blocked
                                self._add_action_info_after_unblock(piece_type, team, blocked_coord, new_action_info)

    # Add available en passant moves after a move
    #
    # NOTE: This method should only be called after a move is made and a new en passant position is available
    def _add_en_passant_moves(self):
        # Check for the new en passant position
        if (self._en_passant_avail != None):
            # Get the pawn direction for the team whose turn it is (used for en passant)
            # Assumes the move has already been made so the turn is the team who can capture the pawn
            pawn_direction = self._get_pawn_direction(self._turn)
            # Get the en passant capture coordinate
            en_passant_capture_coord = Coordinate(self._en_passant_avail.row + pawn_direction, self._en_passant_avail.col)
            # Get the pawns attacking the en passant capture coordinate
            attacking_en_passant = self._attack_arr[en_passant_capture_coord.row][en_passant_capture_coord.col][self._turn]

            # Check if there are any pawns attacking the en passant capture coordinate
            if (PieceType.PAWN in attacking_en_passant):
                # Get the pawns attacking the en passant capture coordinate
                pawns_attacking_en_passant = attacking_en_passant[PieceType.PAWN]

                # Loop through the pawns attacking the en passant capture coordinate
                for pawn_coord in pawns_attacking_en_passant:
                    # Only add to valid move coordinates as the attack coordinates are already correct
                    # Impossible for there to already be this valid move as for en passant to happen no piece can be on the capture spot
                    # Add the en passant capture coordinate to the piece's valid move coordinates
                    self._add_valid_move(PieceType.PAWN, self._turn, pawn_coord, en_passant_capture_coord)
                    
    # Remove previously available en passant moves after a move
    #
    # Parameters:
    #   prev_en_passant_avail: The previous en passant available position
    #
    # NOTE: This method should only be called after a move is made and a new en passant position is available
    def _remove_previous_en_passant_moves(self, prev_en_passant_avail: Coordinate):
        # Check for the new en passant position
        if (prev_en_passant_avail != None):
            # Get the pawn direction for the team whose turn it is (used for en passant)
            # Assumes the move has already been made so the turn is the team who can capture the pawn
            pawn_direction = self._get_pawn_direction(self._turn)
            # Get the en passant capture coordinate
            en_passant_capture_coord = Coordinate(prev_en_passant_avail.row - pawn_direction, prev_en_passant_avail.col)

            # Check if piece at en passant capture coordinate and if so is it the capture color (current turn color)
            if (self._board_arr[en_passant_capture_coord.row][en_passant_capture_coord.col] != None and
                self._board_arr[en_passant_capture_coord.row][en_passant_capture_coord.col].Color == self._turn):
                # Can still capture piece so don't need to remove the en passant capture coordinate from the pawn's valid move coordinates 
                return
            
            # Get the other team color (the team who's turn it isn't)
            # Need other team as they just moved and could previously capture en passant
            other_team = TeamColor.WHITE if self._turn == TeamColor.BLACK else TeamColor.BLACK
            
            # Get the pawns attacking the en passant capture coordinate
            attacking_en_passant = self._attack_arr[en_passant_capture_coord.row][en_passant_capture_coord.col][other_team]
            # Check if there are any pawns attacking the en passant capture coordinate
            if (PieceType.PAWN in attacking_en_passant):
                # Get the pawns attacking the en passant capture coordinate
                pawns_attacking_en_passant = attacking_en_passant[PieceType.PAWN]

                # Loop through the pawns attacking the en passant capture coordinate
                for pawn_coord in pawns_attacking_en_passant:
                    # Remove the en passant capture coordinate from the pawn's valid move coordinates
                    # Might've already been removed if move was to a position it's attacking (_remove_valid_move then does nothing - no error)
                    self._remove_valid_move(PieceType.PAWN, other_team, pawn_coord, en_passant_capture_coord)


    # Adds a valid move to a piece's valid moves
    #
    # Parameters:
    #   piece_type: The type of piece to add the valid move to
    #   team_color: The color of the team to add the valid move to
    #   piece_coord: The coordinate of the piece to add the valid move to
    #   move_coord: The coordinate of the valid move
    #
    # NOTE: If the move is already in the valid moves then nothing happens
    def _add_valid_move(self, piece_type: PieceType, team_color: TeamColor, piece_coord: Coordinate, move_coord: Coordinate):
        # Get the piece's action info
        action_info = self._pieces.get_piece_locations_and_action_info(piece_type, team_color)[piece_coord]
        # print("Adding Piece: " + str(piece_type) + " - " + str(team_color) + " - " + str(piece_coord) + " with move coord: " + str(move_coord))
        # Check if the move coordinate is already in the piece's valid move coordinates
        if (move_coord not in action_info.valid_move_coords):
            # Add the move coordinate to the piece's valid move coordinates
            action_info.valid_move_coords.append(move_coord)
            # Update the piece's action info
            self._pieces.update_piece(Piece(piece_type, team_color), piece_coord, action_info)

    # Remove a valid move from a piece's valid moves
    #
    # Parameters:
    #   piece_type: The type of piece to remove the valid move from
    #   team_color: The color of the team to remove the valid move from
    #   piece_coord: The coordinate of the piece to remove the valid move from
    #   move_coord: The coordinate of the valid move
    #
    # NOTE: If the move is not in the valid moves then nothing happens
    def _remove_valid_move(self, piece_type: PieceType, team_color: TeamColor, piece_coord: Coordinate, move_coord: Coordinate):
        # Get the piece's action info
        action_info = self._pieces.get_piece_locations_and_action_info(piece_type, team_color)[piece_coord]
        # print("Removing Piece: " + str(piece_type) + " - " + str(team_color) + " - " + str(piece_coord) + " with move coord: " + str(move_coord))
        # Try to remove coordinate from the piece's valid move coordinates 
        try:
            # Remove the move coordinate from the piece's valid move coordinates
            action_info.valid_move_coords.remove(move_coord)
        except ValueError:
            # Already removed (not in valid moves) (no need to update the piece)
            return
        # Update the piece's action info
        self._pieces.update_piece(Piece(piece_type, team_color), piece_coord, action_info)

    # Adds the action info to a piece's action info
    #
    # Parameters:
    #   piece_type: The type of piece to add the action info to
    #   team_color: The color of the team to add the action info to
    #   piece_coord: The coordinate of the piece to add the action info to
    #   add_action_info: The action info to add
    #
    # NOTE: ASSUMES the action info is NOT already in the piece's action info as we know it isn't after an unblock
    def _add_action_info_after_unblock(self, piece_type: PieceType, team_color: TeamColor, piece_coord: Coordinate, add_action_info: PieceActionInfo):
        # Get the piece's action info
        action_info = self._pieces.get_piece_locations_and_action_info(piece_type, team_color)[piece_coord]

        # print("Adding Piece: " + str(piece_type) + " - " + str(team_color) + " - " + str(piece_coord) + " with action info: " + str(add_action_info))

        # for coord in add_action_info.attack_coords:
        #     if (coord in action_info.attack_coords):
        #         print("ERROR: Trying to add attack coord that's already in attack coords")
        #         self.print_board()
        #         self._print_attack_arr()
        #         raise ValueError
        
        # for coord in add_action_info.valid_move_coords:
        #     if (coord in action_info.valid_move_coords):
        #         print("ERROR: Trying to add valid move coord that's already in valid move coords")
        #         self.print_board()
        #         self._print_attack_arr()
        #         raise ValueError

        # Add the attack coordinates to the piece's attack coordinates
        action_info.attack_coords.extend(add_action_info.attack_coords)

        # Add the move coordinates to the piece's valid move coordinates
        action_info.valid_move_coords.extend(add_action_info.valid_move_coords)                
        
        # Update the piece's action info
        self._pieces.update_piece(Piece(piece_type, team_color), piece_coord, action_info)

    # Remove the action info from a piece's action info
    #
    # Parameters:
    #   piece_type: The type of piece to remove the action info from
    #   team_color: The color of the team to remove the action info from
    #   piece_coord: The coordinate of the piece to remove the action info from
    #   remove_action_info: The action info to remove
    #
    # NOTE: ASSUMES the action info is already in the piece's action info as we know it is after an block
    # NOTE: If any of the coordinates (attack or valid move) is not in the appropriate action info field then there's a value error
    def _remove_action_info_after_block(self, piece_type: PieceType, team_color: TeamColor, piece_coord: Coordinate, remove_action_info: PieceActionInfo):
        # Get the piece's action info
        action_info = self._pieces.get_piece_locations_and_action_info(piece_type, team_color)[piece_coord]

        # print("Removing Piece: " + str(piece_type) + " - " + str(team_color) + " - " + str(piece_coord) + " with action info: " + str(remove_action_info))

        # Loop through the attack coordinates
        for attack_coord in remove_action_info.attack_coords:
            # Remove the attack coordinate from the piece's attack coordinates
            action_info.attack_coords.remove(attack_coord)

        # Loop through the move coordinates
        for move_coord in remove_action_info.valid_move_coords:
            # Remove the move coordinate from the piece's valid move coordinates
            # if (move_coord not in action_info.valid_move_coords):
            #     print("Removing: " + str(move_coord) + " from " + str(action_info.valid_move_coords))
            #     print("Piece: " + str(piece_type) + " - " + str(team_color) + " - " + str(piece_coord))
            #     print("ERROR: Trying to remove valid move coord that's not in valid move coords")
            #     self.print_board()
            #     self._print_attack_arr()
            #     raise ValueError
            action_info.valid_move_coords.remove(move_coord)

        # Update the piece's action info
        self._pieces.update_piece(Piece(piece_type, team_color), piece_coord, action_info)

    # Update the pawn non capture moves based off a coordinate
    #
    # Parameters:
    #   coord: The coordinate of the piece that moved (either to or from)
    def _update_pawn_non_capture_coord(self, coord: Coordinate):
        # Update white pawns on the coord
        self._update_blocks_on_pawn_non_capture_moves(TeamColor.WHITE, coord)
        # Update black pawns on the coord
        self._update_blocks_on_pawn_non_capture_moves(TeamColor.BLACK, coord)

    # Update the pawn non capture moves based off a previous move
    #
    # Parameters:
    #   move: The move to update the pawn moves based off of
    def _update_pawn_non_capture_moves(self, move: Move):
        # Update white pawns on the from coord
        self._update_blocks_on_pawn_non_capture_moves(TeamColor.WHITE, move.from_coord)
        # Update black pawns on the from coord
        self._update_blocks_on_pawn_non_capture_moves(TeamColor.BLACK, move.from_coord)
        # Update white pawns on the to coord
        self._update_blocks_on_pawn_non_capture_moves(TeamColor.WHITE, move.to_coord)
        # Update black pawns on the to coord
        self._update_blocks_on_pawn_non_capture_moves(TeamColor.BLACK, move.to_coord)
        

    # Change the pawn no capture moves based off move for a coordinate
    #
    # Parameters:
    #   team: The team whose pawn moves to change
    #   coord: The coordinate of the piece that moved (either to or from)
    #@profile
    def _update_blocks_on_pawn_non_capture_moves(self, team: TeamColor, coord: Coordinate):
        # Get the pawn direction for the team
        pawn_direction = self._get_pawn_direction(team)
        # Get the starting row for the team
        starting_row = self._get_pawn_starting_row(team)
        # Get the row of the pawn to check for
        new_row = coord.row - pawn_direction
        if (self._ind_in_board(new_row)):
            # Get the piece to be updated if a pawn
            piece = self._board_arr[new_row][coord.col]

            if (piece != None and piece.Type == PieceType.PAWN and piece.Color == team):
                # Get whether the pawn is blocked or not
                blocked = self._board_arr[coord.row][coord.col] != None
                # Check if blocked
                if (blocked):
                    # Remove the pawn's move to the valid moves
                    self._remove_valid_move(PieceType.PAWN, team, Coordinate(new_row, coord.col), 
                                             Coordinate(coord.row, coord.col))
                else:
                    # Add the pawn's move to the valid moves
                    self._add_valid_move(PieceType.PAWN, team, Coordinate(new_row, coord.col), 
                                             Coordinate(coord.row, coord.col))
                
                # Check if the pawn is in the starting row
                if (new_row == starting_row):
                    # Check if pawn can move two spaces
                    if (self._ind_in_board(coord.row + pawn_direction)):
                        # Check if blocked
                        if (not blocked and self._board_arr[coord.row + pawn_direction][coord.col] == None):
                            # Add the pawn's move to the valid moves
                            self._add_valid_move(PieceType.PAWN, team, Coordinate(new_row, coord.col), 
                                                 Coordinate(coord.row + pawn_direction, coord.col))
                        else:
                            # Remove the pawn's move to the valid moves
                            self._remove_valid_move(PieceType.PAWN, team, Coordinate(new_row, coord.col), 
                                                    Coordinate(coord.row + pawn_direction, coord.col))
        # Now check for two space moves from two spaces away
        new_row -= pawn_direction
        if (new_row == starting_row and self._ind_in_board(new_row)):
            # Get the piece to be updated if a pawn
            piece = self._board_arr[new_row][coord.col]

            if (piece != None and piece.Type == PieceType.PAWN and piece.Color == team):
                # Check if blocked (in either space, first space is coord.row - pawn_direction, and second is already checked by blocked)
                if (self._board_arr[coord.row][coord.col] == None and
                    self._board_arr[coord.row - pawn_direction][coord.col] == None):
                    # Add the pawn's move to the valid moves
                    self._add_valid_move(PieceType.PAWN, team, Coordinate(new_row, coord.col), 
                                         Coordinate(coord.row, coord.col))
                else:
                    # Remove the pawn's move to the valid moves
                    self._remove_valid_move(PieceType.PAWN, team, Coordinate(new_row, coord.col), 
                                            Coordinate(coord.row, coord.col))
        
    # Update the castling moves available
    #
    # Parameters:
    #   team: The team whose castling moves to change
    #   kingside: Whether to change the kingside castling move or the queenside castling move
    #@profile
    def _update_castling_moves(self, team: TeamColor, kingside: bool):
        # Starting coord
        start_coord = self._get_king_starting_coordinate(team)
        king_coord = self._pieces.get_king_coord(team)

        # If king has moved we can't remove the castling move as it's already removed
        if (start_coord != king_coord):
            return

        # Row of castling
        row = start_coord.row
        # Column of castling
        col = start_coord.col + 2 if kingside else start_coord.col - 2

        # Check if castle is valid then add it to the valid moves
        if (self._valid_castle(team, kingside)):
            self._add_valid_move(PieceType.KING, team, start_coord, Coordinate(row, col))
        # Otherwise remove the move from the valid moves
        else:
            self._remove_valid_move(PieceType.KING, team, start_coord, Coordinate(row, col))

    # Private method that takes a FEN string and sets the board and it's properties to the FEN string
    #
    # Parameters:
    #   fen_str: The FEN string to set the board to
    #
    # Returns True if the FEN string was valid and the board could be set up correctly, otherwise returns False
    def _set_board_from_fen(self, fen_str: str) -> bool:
        # Split the FEN string by spaces to get the different properties
        fen_arr = fen_str.strip().split(' ')

        # Check the fen array is the correct length
        if (len(fen_arr) != 6):
            return False
        
        # BOARD
        # Get the board from the FEN string
        board_arr = self._fen_to_board_arr(fen_arr[0])
        # Check if the board is valid
        if (board_arr == None):
            return False
        
        # TURNS
        # Get the turn from the FEN string
        turn = self._fen_to_turn(fen_arr[1])
        # Check if the turn is valid
        if (turn == None):
            return False
        
        # CASTLING RIGHTS
        # Get the castling rights from the FEN string
        castling_rights = self._fen_to_castling_rights(fen_arr[2])
        # Check if the castling rights is valid
        if (castling_rights == None):
            return False
        # Check if the castling rights are valid for the board
        # Check if the white king is in the correct spot if white can castle kingside or queenside
        if ((castling_rights.white_kingside or castling_rights.white_queenside) and board_arr[0][4] != Piece(PieceType.KING, TeamColor.WHITE)):
            return False
        # Check if the black king is in the correct spot if black can castle kingside or queenside
        if ((castling_rights.black_kingside or castling_rights.black_queenside) and board_arr[7][4] != Piece(PieceType.KING, TeamColor.BLACK)):
            return False
        # Check if the white kingside rook is in the correct spot if white can castle kingside
        if (castling_rights.white_kingside and board_arr[0][7] != Piece(PieceType.ROOK, TeamColor.WHITE)):
            return False
        # Check if the white queenside rook is in the correct spot if white can castle queenside
        if (castling_rights.white_queenside and board_arr[0][0] != Piece(PieceType.ROOK, TeamColor.WHITE)):
            return False
        # Check if the black kingside rook is in the correct spot if black can castle kingside
        if (castling_rights.black_kingside and board_arr[7][7] != Piece(PieceType.ROOK, TeamColor.BLACK)):
            return False
        # Check if the black queenside rook is in the correct spot if black can castle queenside
        if (castling_rights.black_queenside and board_arr[7][0] != Piece(PieceType.ROOK, TeamColor.BLACK)):
            return False
        
        # EN PASSANT
        # Check if en passant available
        en_passant_arr = fen_arr[3]
        # Check if the en passant available is '-' (no en passant available)
        if (en_passant_arr == '-'):
            en_passant_avail = None
        # Check if the en passant available is valid
        else:
            # Check if the en passant available position is valid
            # Check the length of the en passant available position string is 2
            if (len(en_passant_arr) != 2):
                return False
            
            # Set the en passant available position
            col = self._get_index_in_range(en_passant_arr[0], 'a', 'h')
            row = self._get_index_in_range(en_passant_arr[1], '1', '8')

            # Make sure the row and column were valid values
            if (col == -1 or row == -1):
                return False

            # Make sure the en passant is on the correct row for the team whose turn it is 
            #   row indices: 2 for Black to capture White pawn - 5 for White to capture Black pawn
            # Also modify the row to be the row of the pawn to capture (row indices 3 or 4) not the en passant capture spot (row indices 2 or 5)
            if (row == 2 and turn == TeamColor.BLACK):
                # White pawn available for en passant
                row = 3
            elif (row == 5 and turn  == TeamColor.WHITE):
                # Black pawn available for en passant
                row = 4
            else:
                # Invalid en passant row
                return False
            
            # Make sure there is a pawn to capture
            if (board_arr[row][col] != Piece(PieceType.PAWN, TeamColor.WHITE if row == 3 else TeamColor.BLACK)):
                return False
            
            # Set the en passant available position
            en_passant_avail = Coordinate(row, col)
        
        # HALF MOVES
        # Get the half moves from the FEN string
        half_moves = self._str_to_int(fen_arr[4])
        # Check if the half moves is valid
        if (half_moves == None):
            return False
        # Check that half moves are 0 if en passant is available (means last move was a pawn advancement)
        if (en_passant_avail != None and half_moves != 0):
            return False
        
        # FULL MOVES
        # Get the full moves from the FEN string
        full_moves = self._str_to_int(fen_arr[5])
        # Check if the full moves is valid
        if (full_moves == None):
            return False
        
        # Set the properties to the values from the FEN string now that we know the FEN string is valid
        self._board_arr = board_arr
        self._turn = turn
        self._castling_rights = castling_rights
        self._en_passant_avail = en_passant_avail
        self._half_moves = half_moves
        self._full_moves = full_moves

        # PIECE LOCATIONS
        # Knowing the board is valid now, and the board is set, we can set the piece locations and where they can attack
        # NOTE: Must be done after the new board is set or attack coordinates will be wrong
        # Set pieces to the new piece locations for the board with their attack coordinates
        self._reset_piece_locations()

        # Set the initial zobrist hash
        self._set_zobrist_hash()

        # Set the repetition dictionary to the current board hash
        self._repeated_positions = {self._zobrist_hash : 1}

        return True

    
    # Private method that returns a board array of pieces from a FEN string
    #
    # Parameters:
    #   fen_str: The first part of the FEN string (before the first space) detailing the piece positions to convert to a board array
    #
    # Returns the board array of pieces or None if the FEN string was invalid
    #
    # NOTE: Invalid FEN strings are when the board is incorrectly formatted (as specified by FEN), there aren't two kings (one for each team),
    #           there's multiple kings on a team, there's pawn(s) in the promotion row, or pawns below the starting row.
    @staticmethod
    def _fen_to_board_arr(fen_str: str) -> list[list[Piece]]:
        # Set the board to the position specified in the FEN string
        # Split the first fen_str property by '/' to get the rows
        fen_board_arr = fen_str.strip().split('/')

        # Create a temp board 2D-array and set the correct dimensions of 8x8 so we don't need to adjust the current board until we know the FEN string is valid
        temp_board_arr: list[list[Piece]] = [[None for i in range(8)] for j in range(8)]

        # Check the board array is the correct length
        if (len(fen_board_arr) != 8):
            return None
        
        white_king = False
        black_king = False

        pieces = PieceTracker()

        # loop through the board array strings (rows) - confirmed length of 8 above
        for row in range(8):
            # Set the column to 0
            col = 0
            # Loop through the characters in the row string
            for char in fen_board_arr[row]:
                # Check if the character is a digit
                if (char.isdigit()):
                    # Don't need to adjust the board because it's already defaulted to None
                    # Add the number of empty spaces to the column
                    col += int(char)
                # Check if the character is piece letter (p, b, n, r, q, k)
                else:
                    # Lower char to make it easier to see what type of piece it is
                    lower_char = char.lower()

                    # Create a variable for the piece type
                    pieceType = None
                    # Set the team color (WHITE if character is uppercase otherwise BLACK)
                    teamColor = TeamColor.WHITE if char.isupper() else TeamColor.BLACK
                    
                    # Check if the character is a pawn
                    if (lower_char == 'p'):
                        # Check to make sure the pawn isn't in the promotion row or below the starting row (i.e. in the top or bottom row)
                        if (row == 0 or row == 7):
                            return None
                        
                        # Set the piece type to a pawn
                        pieceType = PieceType.PAWN
                    # Check if the character is a bishop
                    elif (lower_char == 'b'):
                        # Set the piece type to a bishop
                        pieceType = PieceType.BISHOP
                    # Check if the character is a knight
                    elif (lower_char == 'n'):
                        # Set the piece type to a knight
                        pieceType = PieceType.KNIGHT
                    # Check if the character is a rook
                    elif (lower_char == 'r'):
                        # Set the piece type to a rook
                        pieceType = PieceType.ROOK
                    # Check if the character is a queen
                    elif (lower_char == 'q'):
                        # Set the piece type to a queen
                        pieceType = PieceType.QUEEN
                    # Check if the character is a king
                    elif (lower_char == 'k'):
                        pieceType = PieceType.KING
                        # Check if there's too many kings
                        if teamColor == TeamColor.WHITE:
                            # White king
                            # If there's already a white king then the FEN string is invalid
                            if white_king:
                                return None
                            # Otherwise set the white king to True
                            else:
                                white_king = True
                        else:
                            # Black king
                            # If there's already a black king then the FEN string is invalid
                            if black_king:
                                return None
                            # Otherwise set the black king to True
                            else:
                                black_king = True
                    # Invalid character
                    else:
                        return None
                    
                    # Set the piece to the correct piece type and color
                    piece = Piece(pieceType, teamColor)

                    # Check if the column greater than the max (7). If so then the row string the wrong length
                    if (col > 7):
                        return None

                    # Set the board at the current position to the piece
                    # FEN has the first row as the bottom row so need to flip the row index
                    temp_board_arr[7 - row][col] = piece
                    # Increment the column
                    col += 1
            
            # Check if the column is 8 (if not then the row string the wrong length)
            if (col != 8):
                return None

        # Check if there's not a king for both teams
        if (not white_king or not black_king):
            return None
        
        # Return the temp board array
        return temp_board_arr
    
    # Private method that returns the turn depending on the FEN string turn property
    #
    # Parameters:
    #   fen_str: The second part of the FEN string (after the first space but before the second) detailing the turn
    #
    # Returns the turn or None if the FEN string was invalid
    @staticmethod
    def _fen_to_turn(fen_str: str) -> TeamColor:
        fen_str = fen_str.strip().lower()
        # Check if the turn is 'w' (white turn)
        if (fen_str == 'w'):
            return TeamColor.WHITE
        # Check if the turn is 'b' (black turn)
        elif (fen_str == 'b'):
            return TeamColor.BLACK
        # Invalid turn
        else:
            return None
        
    
    # Private method that returns the castling rights depending on the FEN string castling rights property
    #
    # Parameters:
    #   fen_str: The third part of the FEN string (after the second space but before the third) detailing the castling rights
    #
    # Returns the castling rights or None if the FEN string was invalid
    @staticmethod
    def _fen_to_castling_rights(fen_str: str) -> CastlingRights:
        # Check if the castling rights is '-' (no castling rights)
        if (fen_str == '-'):
            # Set all castling rights to False
            temp_castling_rights = CastlingRights(False, False, False, False)
        # Check if the castling rights is valid
        else:
            # Set all castling rights to False (set to True if the rights are enabled in string)
            temp_castling_rights = CastlingRights(False, False, False, False)

            # Loop through the characters in the castling rights string
            for char in fen_str:
                # Check if the character is a valid castling right
                if (char == 'K'):
                    temp_castling_rights.white_kingside = True
                elif (char == 'Q'):
                    temp_castling_rights.white_queenside = True
                elif (char == 'k'):
                    temp_castling_rights.black_kingside = True
                elif (char == 'q'):
                    temp_castling_rights.black_queenside = True
                # Invalid character
                else:
                    return None

        # Return the castling rights
        return temp_castling_rights
    
    # Gets the FEN string for the board
    #
    # Returns the FEN string for the board
    def get_fen(self) -> str:
        # Create the FEN string
        fen_str = ""

        # Loop through the board array rows
        for row in range(7, -1, -1):
            # Set the empty spaces to 0
            empty_spaces = 0
            # Loop through the board array columns
            for col in range(8):
                # Get the piece at the current position
                piece = self._board_arr[row][col]
                # Check if the piece is None
                if (piece == None):
                    # Increment the empty spaces
                    empty_spaces += 1
                # Otherwise there's a piece
                else:
                    # Check if there's empty spaces
                    if (empty_spaces > 0):
                        # Add the empty spaces to the FEN string
                        fen_str += str(empty_spaces)
                        # Reset the empty spaces
                        empty_spaces = 0
                    
                    # Add the piece to the FEN string
                    fen_str += self._piece_to_fen(piece)
            
            # Check if there's empty spaces
            if (empty_spaces > 0):
                # Add the empty spaces to the FEN string
                fen_str += str(empty_spaces)
            
            # Check if there's another row
            if (row > 0):
                # Add the row separator to the FEN string
                fen_str += '/'
        
        # Add the turn to the FEN string
        fen_str += ' ' + ('w' if self._turn == TeamColor.WHITE else 'b')

        # Add the castling rights to the FEN string
        fen_str += ' ' + self._castling_rights_to_fen(self._castling_rights)

        # Add the en passant to the FEN string
        fen_str += ' ' + self._en_passant_to_fen(self._en_passant_avail)

        # Add the half moves to the FEN string
        fen_str += ' ' + str(self._half_moves)

        # Add the full moves to the FEN string
        fen_str += ' ' + str(self._full_moves)

        # Return the FEN string
        return fen_str
    
    # Gets the FEN char for the piece
    #
    # Parameters:
    #   piece: The piece to get the FEN char for
    #
    # Returns the FEN char for the piece
    @staticmethod
    def _piece_to_fen(piece: Piece) -> str:
        # Check if the piece is a pawn
        if (piece.Type == PieceType.PAWN):
            return 'p' if piece.Color == TeamColor.BLACK else 'P'
        # Check if the piece is a bishop
        elif (piece.Type == PieceType.BISHOP):
            return 'b' if piece.Color == TeamColor.BLACK else 'B'
        # Check if the piece is a knight
        elif (piece.Type == PieceType.KNIGHT):
            return 'n' if piece.Color == TeamColor.BLACK else 'N'
        # Check if the piece is a rook
        elif (piece.Type == PieceType.ROOK):
            return 'r' if piece.Color == TeamColor.BLACK else 'R'
        # Check if the piece is a queen
        elif (piece.Type == PieceType.QUEEN):
            return 'q' if piece.Color == TeamColor.BLACK else 'Q'
        # Check if the piece is a king
        elif (piece.Type == PieceType.KING):
            return 'k' if piece.Color == TeamColor.BLACK else 'K'
        # Invalid piece
        else:
            return None
    
    # Gets the FEN string for the castling rights
    #
    # Returns the FEN string for the castling rights
    @staticmethod
    def _castling_rights_to_fen(castling_rights: CastlingRights) -> str:
        # Create the FEN string
        fen_str = ""

        # Check if white can castle kingside
        if (castling_rights.white_kingside):
            # Add the white kingside castling right to the FEN string
            fen_str += 'K'
        # Check if white can castle queenside
        if (castling_rights.white_queenside):
            # Add the white queenside castling right to the FEN string
            fen_str += 'Q'
        # Check if black can castle kingside
        if (castling_rights.black_kingside):
            # Add the black kingside castling right to the FEN string
            fen_str += 'k'
        # Check if black can castle queenside
        if (castling_rights.black_queenside):
            # Add the black queenside castling right to the FEN string
            fen_str += 'q'
        
        # Check if there's no castling rights
        if (fen_str == ""):
            # Set the FEN string to no castling rights
            fen_str = '-'
        
        # Return the FEN string
        return fen_str
    
    # Gets the FEN string for the en passant available
    #
    # Returns the FEN string for the en passant available
    @staticmethod
    def _en_passant_to_fen(en_passant_avail: Coordinate | None) -> str:
        # Check if en passant available
        if (en_passant_avail != None):
            # Add the en passant available to the FEN string
            # Change the row to be the position of the en passant capture spot (where the capture piece moves to, not the piece to capture)
            # This is the row - the pawn direction (1 for white, -1 for black) - (row 3 -> 2 if white, row 4 -> 5 if black)
            en_passant_row = 2 if (en_passant_avail.row == 3) else 5
            return chr(en_passant_avail.col + ord('a')) + chr(en_passant_row + ord('1'))
        # Otherwise no en passant available
        else:
            # Set the FEN string to no en passant available
            return '-'


    # Private method that clears and sets the piece locations for the board from the board array
    def _reset_piece_locations(self):
        # Create a new piece locations object
        self._pieces = PieceTracker()
        # Create a new attack array
        self._attack_arr = [[{TeamColor.WHITE: {}, TeamColor.BLACK: {}} for i in range(8)] for j in range(8)]

        # Set the king locations in _pieces so _get_action_info_for_piece can check for check for getting legal moves
        for row in range(8):
            for col in range(8):
                # Check if there's a king at the current position
                if (self._board_arr[row][col] != None and self._board_arr[row][col].Type == PieceType.KING):
                    # Get the king
                    king = self._board_arr[row][col]
                    # Assign the new coord to the king's coord
                    king_coord = Coordinate(row, col)

                    # Add the king to the piece locations
                    self._pieces.add_piece(king, king_coord, PieceActionInfo())
        
        # Loop through the board array
        for row in range(8):
            for col in range(8):
                # Check if there's a piece at the current position
                if (self._board_arr[row][col] != None):
                    # Get the piece
                    piece = self._board_arr[row][col]
                    # Get the piece action info
                    action_info = self._get_action_info_for_piece(PieceCoordinate(piece, Coordinate(row, col)))

                    # Check if piece is a king
                    # Already added kings to _pieces but now need to add their action info so need to update not add piece
                    if (piece.Type == PieceType.KING):
                        # Update the king's action info
                        self._pieces.update_piece(piece, Coordinate(row, col), action_info)
                    # Otherwise not a king
                    else:
                        # Add the piece to the piece locations
                        self._pieces.add_piece(piece, Coordinate(row, col), action_info)
                    
                    # Add the piece to all the attack coordinates in the attack array
                    self._add_piece_to_attack_arr(piece, Coordinate(row, col), action_info.attack_coords)
        
        # Add en passant moves if available
        if (self._en_passant_avail != None):
            self._add_en_passant_moves()
        
        # Update castling (_update_castling_moves checks for CastlingRights) only for the team whose turn it is
        if (self._turn == TeamColor.WHITE):
            self._update_castling_moves(TeamColor.WHITE, True)
            self._update_castling_moves(TeamColor.WHITE, False)
        else:
            self._update_castling_moves(TeamColor.BLACK, True)
            self._update_castling_moves(TeamColor.BLACK, False)
    
    # Private method that converts a string to an int if all characters are digits. Otherwise returns None
    #
    # Parameters:
    #   str: The string to convert to an int
    #
    # Returns the string as an int or None if the string was invalid
    @staticmethod
    def _str_to_int(str: str) -> int:
        # Check if the string is a digit
        if (not str.isdigit()):
            return None
        
        # Return the string as an int
        return int(str)
    
    # Private method that gets the pawn direction for a team
    #
    # Parameters:
    #   team_color: The team to get the pawn direction for
    #
    # Returns the pawn direction for the team
    @staticmethod
    def _get_pawn_direction(team_color: TeamColor) -> int:
        return 1 if (team_color == TeamColor.WHITE) else -1
    
    # Private method that gets the starting row of a pawn for a team
    #
    # Parameters:
    #   team_color: The team to get the starting row for
    #
    # Returns the starting row for the team
    @staticmethod
    def _get_pawn_starting_row(team_color: TeamColor) -> int:
        return 1 if (team_color == TeamColor.WHITE) else 6
    
    # Private method that gets the promotion row of a pawn for a team
    #
    # Parameters:
    #   team_color: The team to get the promotion row for
    #
    # Returns the promotion row for the team
    @staticmethod
    def _get_pawn_promotion_row(team_color: TeamColor) -> int:
        return 7 if (team_color == TeamColor.WHITE) else 0

    # Private method that gets the starting coordinate of a king for a team
    #
    # Parameters:
    #   team_color: The team to get the starting coordinate for
    #
    # Returns the starting coordinate for the team's king
    @staticmethod
    def _get_king_starting_coordinate(team_color: TeamColor) -> Coordinate:
        return Coordinate(0, 4) if (team_color == TeamColor.WHITE) else Coordinate(7, 4)
        
    # Private method that checks if a castle is valid for a team on a specific side
    # 
    # Parameters:
    #   team_color: The team to check if they can castle
    #   kingside: Whether to check if the team can castle kingside or not 
    #
    # Returns if the team can castle on the specified side or not
    #
    # NOTE: Assumes the castling rights are correct - uses them to ensure the king and rook are in the correct positions
    #       Returns false if castling rights for the team and side are false
    #@profile
    def _valid_castle(self, team_color: TeamColor, kingside: bool) -> bool:
        # Get the castling rights for the team and side
        if (kingside):
            castling_right = self._castling_rights.white_kingside if (team_color == TeamColor.WHITE) else self._castling_rights.black_kingside
        else:
            castling_right = self._castling_rights.white_queenside if (team_color == TeamColor.WHITE) else self._castling_rights.black_queenside
        
        # Check if the team has castling rights for the side
        if (not castling_right):
            return False
        
        # Variable for which direction in horizontally (columns) the king is moving
        # castle_dir = SignDirection.POSITIVE if kingside else SignDirection.NEGATIVE

        # Get the coordinate of the king
        king_coord = self._get_king_starting_coordinate(team_color)

        # Get the other team's color to check if that team is attacking the king or any of the spaces the king moves through or to
        other_team = TeamColor.WHITE if team_color == TeamColor.BLACK else TeamColor.BLACK
        
        # Check for kingside case
        if (kingside):
            # Check if the king is attacked in any of the spaces it was on, moves through, or is moving to
            if (self._team_attacking_coord(other_team, Coordinate(king_coord.row, king_coord.col)) or 
                self._team_attacking_coord(other_team, Coordinate(king_coord.row, king_coord.col + 1)) or
                self._team_attacking_coord(other_team, Coordinate(king_coord.row, king_coord.col + 2))):
                return False
            
            # Check if there are pieces in the way
            if (self._board_arr[king_coord.row][king_coord.col + 1] == None and self._board_arr[king_coord.row][king_coord.col + 2] == None):
                return True
            else:
                return False
        else:
            # Check if the king is attacked in any of the spaces it was on, moves through, or is moving to
            if (self._team_attacking_coord(other_team, Coordinate(king_coord.row, king_coord.col)) or 
                self._team_attacking_coord(other_team, Coordinate(king_coord.row, king_coord.col - 1)) or
                self._team_attacking_coord(other_team, Coordinate(king_coord.row, king_coord.col - 2))):
                return False

            # Check if there are pieces in the way
            if (self._board_arr[king_coord.row][king_coord.col - 1] == None and self._board_arr[king_coord.row][king_coord.col - 2] == None and 
                self._board_arr[king_coord.row][king_coord.col - 3] == None):
                return True
            else:
                return False
        
        # # Variable for the number of spaces to check between the king and rook
        # spaces_to_check = 2 if kingside else 3
        
        # # Get the number of spaces available from the king to rook
        # available_spaces = self._get_spaces_available_in_move_dir(king_coord, SignDirection.ZERO, castle_dir, False, spaces_to_check)
        
        # # Check if there's a piece in the way of the king and rook (as the number spaces available between them should be the spaces_to_check)
        # if (available_spaces != spaces_to_check):
        #     return False
        # else:
        #     return True
    
    # Method that gets the previous moves as a list of MoveInfo objects
    #
    # Returns the previous moves as a list of MoveInfo objects
    def get_previous_moves(self) -> list[MoveInfo]:
        return list(self._previous_moves)

    # Method that gets the previous moves as a string separated by spaces
    #
    # Returns the previous moves as a string separated by spaces
    def get_previous_moves_as_str(self) -> str:
        # Create the previous moves string
        prev_moves_str = ''

        # Loop through the previous moves
        for moveInfo in self._previous_moves:
            # Add the move to the previous moves string
            prev_moves_str += str(moveInfo.move) + ' '
        
        # Return the previous moves string
        return prev_moves_str.strip()
    
    # Private method that checks if a coordinate is in the board
    #
    # Parameters:
    #   coord: The coordinate to check
    #
    # Returns if the coordinate is in the board or not
    @staticmethod
    def _coord_in_board(coord: Coordinate) -> bool:
        return coord.row >= 0 and coord.row <= 7 and coord.col >= 0 and coord.col <= 7
    
    # Private method that checks if a row or column is in the board
    #
    # Parameters:
    #   ind: The row or column index to check
    #
    # Returns if the row or column index is in the board or not
    @staticmethod
    def _ind_in_board(ind: int) -> bool:
        return ind >= 0 and ind <= 7
    
    # Private method that gets the index in the range of the character or returns -1 if the character is not in the range
    # Ex: range is 'a'-'h' and character is 'c' then returns 2
    # Ex: range is '1'-'8' and character is '9' then returns -1
    #
    # Parameters:
    #   character: The character to get the index of
    #   range_start: The start of the range
    #   range_end: The end of the range
    #
    # Returns the index of the character in the range or -1 if the character is not in the range
    #
    # NOTE: Returns -1 if the range is invalid (range_start is before range_end) or if any input is not a single character
    @staticmethod
    def _get_index_in_range(character: str, range_start: str, range_end: str) -> int:
        # Check if the character is in the range
        if (character < range_start or character > range_end or max(len(character), len(range_start), len(range_end)) != 1 or 
            min(len(character), len(range_start), len(range_end)) != 1):
            return -1
        else:
            return ord(character) - ord(range_start)
    
    # Private method that checks if there are no pieces in the way of a rook or bishop move (includes Queen moves as they are just a 
    #   bishop or rook move). Will return false if not a rook or bishop move (not diagonal, veritcal, or horizontal)
    #
    # Parameters:
    #   move: The move as a Move object
    #
    # Returns if there are no pieces in the way of the move or not
    #
    # NOTE: Does not check the starting or ending spaces of the move (as it's already checked by the move method)
    # NOTE: Assumes the move is a valid move (not out of bounds)
    # NOTE: Assumes the starting and ending spaces of a move are valid (not caputring a piece on the same team and the starting space 
    #         has a piece of the correct type and color)
    def _rook_or_bishop_clear_path(self, move: Move) -> bool:
        # Get the diference in rows and columns for the move
        row_diff = move.to_coord.row - move.from_coord.row
        col_diff = move.to_coord.col - move.from_coord.col

        # Get the directions
        row_dir = SignDirection.POSITIVE if row_diff > 0 else (SignDirection.NEGATIVE if row_diff < 0 else SignDirection.ZERO)
        col_dir = SignDirection.POSITIVE if col_diff > 0 else (SignDirection.NEGATIVE if col_diff < 0 else SignDirection.ZERO)

        # Set max spaces (don't include the last space as it's already checked by the move method so subtract 1)
        max_spaces = abs(row_diff) if (row_diff != 0) else abs(col_diff)
        max_spaces -= 1

        # Get the spaces available in the move direction (not including last space (as already checked my move), so ignore captures)
        spaces_available = self._get_spaces_available_in_move_dir(from_coord=move.from_coord, row_dir=row_dir, col_dir=col_dir, team_color=False, max_spaces=max_spaces)

        # Returns if the move has a clear path (no pieces in the way) (spaces available is the max spaces)
        return max_spaces == spaces_available

    # Private method that returns the max number of spaces a piece can move in the direction specified. Includes captures as a valid space to move to.
    #   Will return 0 if the move is not in any direction
    #
    # Parameters:
    #   from_coord: The coordinate of the piece to move
    #   row_dir: The direction to move in the row
    #   col_dir: The direction to move in the column
    #   team_color: The team color of the piece moving (False to exclude possible captures - default, team_color moving (can capture opposite team), 
    #               or True to include the blocking (capture) piece no matter the color)
    #   max_spaces: The maximum number of spaces to check (default is 7 - max number of spaces available to move on the board)
    #
    # Returns the max number of spaces a piece can move in the direction specified. Will return 0 if the move is not in any direction
    #@profile
    def _get_spaces_available_in_move_dir(self, from_coord: Coordinate, row_dir: SignDirection, col_dir: SignDirection, 
                                          team_color: TeamColor | bool = False, max_spaces: int = 7) -> int:
        # If the move is not in any direction return 0
        if (col_dir == SignDirection.ZERO and row_dir == SignDirection.ZERO):
            return 0
        
        # Calculate the max spaces to check (either max spaces or the max spaces to the edge of the board in the direction specified)
        # Max row / col index is 7
        row_max_spaces = (7 - from_coord.row) if row_dir == SignDirection.POSITIVE else (from_coord.row if row_dir == SignDirection.NEGATIVE else 7)
        col_max_spaces = (7 - from_coord.col) if col_dir == SignDirection.POSITIVE else (from_coord.col if col_dir == SignDirection.NEGATIVE else 7)
        max_spaces = min(max_spaces, row_max_spaces, col_max_spaces)
        
        # Get the row and column direction values (-1 if negative, 0 if zero, 1 if positive)
        row_dir = 1 if row_dir == SignDirection.POSITIVE else (-1 if row_dir == SignDirection.NEGATIVE else 0)
        col_dir = 1 if col_dir == SignDirection.POSITIVE else (-1 if col_dir == SignDirection.NEGATIVE else 0)

        # Sets the row to be the from row adjusted 1 (to exclude the starting space) in the row direction (1 for positive, -1 for negative, 0 for zero)
        row = from_coord.row + row_dir
        # Sets the column to be the from column adjusted 1 (to exclude the starting space) in the column direction (1 for positive, -1 for negative, 0 for zero)
        col = from_coord.col + col_dir

        # Save the number of spaces moved (starts at 1 because starting with first space after starting space)
        total_spaces = 1

        # Loops through the board until max_spaces is reached, it reaches the end of the board (max_spaces is also reached) or a piece is in the way
        while (total_spaces <= max_spaces):
            # Check if there's a piece in the way
            piece = self._board_arr[row][col]

            if (piece != None):
                # If can't capture this piece (or capturing turned off - team_color = False)
                if (team_color != True and (not team_color or piece.Color == team_color)):
                    # Can't capture a piece on the same team so return the total spaces - 1
                    return total_spaces - 1
                # Can capture this piece (or including the blocking (capture) piece no matter the color is turned on)
                else:
                    return total_spaces
            
            # Increment counters
            row += row_dir # -1 if negative, 0 if zero, 1 if positive
            col += col_dir # -1 if negative, 0 if zero, 1 if positive
            total_spaces += 1
        
        # After exiting loop return the total spaces - 1 (-1 since it increments total spaces at the end of loop)
        return total_spaces - 1
    
    # Private method that gets all the pieces of a specified type and team color
    #
    # Parameters:
    #   piece_type: The type of piece to get or None (default) to get all pieces
    #   team_color: The team color of the pieces to get or None (default) to get all pieces
    #
    # Returns a list of all the pieces of the specified type and team color
    def _get_pieces(self, piece_type: PieceType = None, team_color: TeamColor = None) -> list[PieceCoordinate]:
        pieces: list[PieceCoordinate] = []

        if piece_type != None and team_color != None:
            pieces = self._pieces.get_pieces(piece_type=piece_type, team_color=team_color)
        elif piece_type != None:
            for team_color in TeamColor:
                pieces += self._pieces.get_pieces(piece_type=piece_type, team_color=team_color)
        elif team_color != None:
            for piece_type in PieceType:
                pieces += self._pieces.get_pieces(piece_type=piece_type, team_color=team_color)
        else:
            for team_color in TeamColor:
                for piece_type in PieceType:
                    pieces += self._pieces.get_pieces(piece_type=piece_type, team_color=team_color)

        return pieces
    
    # Gets the number of pieces on the board
    #
    # Returns the number of pieces on the board
    def get_piece_count(self) -> int:
        return self._pieces.get_piece_count()

    
    # Private method that returns if a team is attacking a specific space
    #
    # Parameters:
    #   team_color: The team color to check if attacking
    #   coord: The coordinate to check if attacked
    #
    # Returns if the team is attacking the coordinate
    def _team_attacking_coord(self, team_color: TeamColor, coord: Coordinate) -> bool:
        # If the dict for the team is not empty then the team is attacking the coordinate 
        #   dicts evaluate to True when not empty and False when empty when converted to a bool
        return bool(self._attack_arr[coord.row][coord.col][team_color])
    
    # Gets the valid blocking / capturing coordinates to get the king out of check
    #
    # Parameters:
    #   king_loc: The PieceCoordinate of the king to get the valid blocking / capturing coordinates for
    #   other_team: The team color of the other team
    #
    # Returns a list of valid blocking / capturing coordinates (as a list of Coordinate objects)
    #
    # NOTE: Returns None if the king is not in check
    # NOTE: Returns empty list if the king is in double check (if single check there will always be a coordinate to capture)
    def _get_valid_check_coords(self, king_coord: Coordinate, other_team: TeamColor) -> list[Coordinate]:
        # King attack dict
        king_attack_dict = self._attack_arr[king_coord.row][king_coord.col][other_team]
        # Determine if King in check
        king_in_check = bool(king_attack_dict)
        # Valid check blocking / capture moves (move to coordinates that any piece but the king could move to in order to block check)
        valid_check_coords: list[Coordinate] = []

        # Check if king is in check 
        # and the piece is not a king (check for blocking / capture that would change check)
        # King can move out of check so need to check that separately than for all other pieces
        if (king_in_check):
            # Get the first attack piece
            attack_piece = next(iter(king_attack_dict))
            # Check if double check (meaning multiple pieces are attacking the king)
            # Check if multiple types of pieces are attacking or if only one type check if multiple of that type are attacking
            # King must move on double check so no other piece moves are valid, therefore return empty list
            if (len(king_attack_dict) >= 2 or len(king_attack_dict[attack_piece]) >= 2):
                # Return empty list as the king must move (no other piece can get the king out of check)
                return valid_check_coords
            # Single check
            else:
                # Get the attack piece's coordinate (first key in the dict)
                attack_coord = next(iter(king_attack_dict[attack_piece]))
                # Add the attack piece's coordinate to the valid check coordinates as if it's captured, the king is no longer in check
                valid_check_coords.append(attack_coord)
                # If the attack piece is a rook, bishop or queen, add the coordinates between the attack piece and the king to the 
                #   valid check coordinates (as any piece but the king can move to any of these spaces to block the check)
                if (attack_piece == PieceType.ROOK or attack_piece == PieceType.BISHOP or attack_piece == PieceType.QUEEN):
                    # Get the difference in rows and columns for the move
                    row_diff = attack_coord.row - king_coord.row
                    col_diff = attack_coord.col - king_coord.col

                    # Get the directions
                    row_dir = SignDirection.POSITIVE if row_diff > 0 else (SignDirection.NEGATIVE if row_diff < 0 else SignDirection.ZERO)
                    col_dir = SignDirection.POSITIVE if col_diff > 0 else (SignDirection.NEGATIVE if col_diff < 0 else SignDirection.ZERO)

                    # Start at 1 to exclude the starting space
                    # End at the second to last space as the last space is the attack piece's space (already in the valid check coordinates)
                    #   This is just normal range end values as it ends just before the end value (ex: range(6) ends at 5)
                    # Number of spaces to move is the abs of the row difference (for vertical and diagonal) unless we're moving horitizontal 
                    #   (row_diff == 0) then it's the abs of the column difference
                    for i in range(1, abs(row_diff) if (row_diff != 0) else abs(col_diff)):
                        # Add the coordinate to the valid check coordinates
                        valid_check_coords.append(Coordinate(king_coord.row + (i * row_dir.value), king_coord.col + (i * col_dir.value)))
        # King not in check
        else:
            # Return None as the king is not in check
            return None
        
        return valid_check_coords
                    
    # Private method that checks if the king is in check after a non-king move
    #
    # Parameters:
    #   from_coord: The coordinate the piece is moving from
    #   to_coord: The coordinate the piece is moving to
    #   king_loc: The PieceCoordinate of the king
    #   valid_check_coords: The valid coordinates to block check for the king (None if king is not in check)
    #   from_attack_dict: The pieces on the other team attacking the from space from the attack array
    #
    # Returns if the king is in check after the non king move
    #@profile
    def _king_in_check_after_non_king_move(self, from_coord: Coordinate, to_coord: Coordinate, king_coord: Coordinate, 
                                  valid_check_coords: list[Coordinate], from_attack_dict: dict[PieceType, list[Coordinate]]) -> bool:
        # Check if in check and did not move to a valid check coordinate
        if (valid_check_coords != None and to_coord not in valid_check_coords):
            # Didn't block check - still in check
            return True
        
        # Check if there's no pieces attacking the from space (from_attack_dict is empty)
        if (not from_attack_dict):
            # No pieces attacking from space - wasn't in check - not blocking check - so not in check
            return False
        
        # Check if any pieces could have been blocked from check before the move (only possible if from_coord is horizontal, vertical, or 
        #   diagonal space from the king location, i.e. can be captured by a piece that can be blocked - rook, bishop, or queen)
        row_diff = from_coord.row - king_coord.row
        col_diff = from_coord.col - king_coord.col
        # Check if not horizontal, vertical, or diagonal
        if (row_diff != 0 and col_diff != 0 and abs(row_diff) != abs(col_diff)):
            # No pieces were blocked from check - not in check
            return False
        
        # Is horizontal or vertical or diagonal
        # Get the direction required for piece to put king in check
        row_dir = SignDirection.POSITIVE if row_diff > 0 else (SignDirection.NEGATIVE if row_diff < 0 else SignDirection.ZERO)
        col_dir = SignDirection.POSITIVE if col_diff > 0 else (SignDirection.NEGATIVE if col_diff < 0 else SignDirection.ZERO)

        
        # Get the distance between the king and the piece - 1 (max spaces available to have been blocking check)
        max_block_spaces = max(abs(row_diff), abs(col_diff)) - 1
        spaces_available = self._get_spaces_available_in_move_dir(from_coord=king_coord, row_dir=row_dir, col_dir=col_dir, 
                                                                  team_color=False, max_spaces=max_block_spaces)

        # Check if king check is being blocked by piece already in the way
        if (spaces_available != max_block_spaces):
            # Piece is already blocking check - not in check
            return False

        # Check if king check is being blocked by piece that moved to the space
        return self._move_puts_king_in_check(from_coord, to_coord, row_dir, col_dir, False, from_attack_dict)

    # Private method that checks if any of the pieces a piece previously blocked before a move are now attacking the king
    # 
    # Parameters:
    #  from_coord: The coordinate the piece is moving from
    #  to_coord: The coordinate the piece is moving to
    #  row_dir: The direction in the row the piece moved
    #  col_dir: The direction in the column the piece moved
    #  king_move: Whether the piece moving is the king or not
    #  from_attack_dict: The pieces on the other team attacking the from space from the attack array
    # 
    # Returns if the move puts the kings in check
    #@profile
    def _move_puts_king_in_check(self, from_coord: Coordinate, to_coord: Coordinate,row_dir: SignDirection, col_dir: SignDirection, 
                                 king_move: bool, from_attack_dict: dict[PieceType, list[Coordinate]]) -> bool:
        # Loop through the pieces attacking the from space
        for piece_type in from_attack_dict:
            # Skip if piece that can't be blocked (pawn, knight, king)
            if (piece_type == PieceType.PAWN or piece_type == PieceType.KNIGHT or piece_type == PieceType.KING):
                continue

            # Check if the piece can move in the direction required to put king in check
            # Check if horizontal or vertical is correct direction (rook or queen - not bishop since pawn, knight, king already skipped)
            # Check if diagonal is correct direction (bishop or queen - not rook since pawn, knight, king already skipped)
            if (((row_dir == SignDirection.ZERO or col_dir == SignDirection.ZERO) and piece_type != PieceType.BISHOP) or 
                ((row_dir != SignDirection.ZERO or col_dir != SignDirection.ZERO) and piece_type != PieceType.ROOK)):
                # Loop through the attack coordinates for the piece
                for attack_coord in from_attack_dict[piece_type]:
                    # Checks if attacking piece is being captured (Piece can no longer capture the king, so continue)
                    if (to_coord == attack_coord):
                        continue

                    # Get the directions
                    attack_row_dir = (SignDirection.ZERO if attack_coord.row == from_coord.row else 
                                     (SignDirection.POSITIVE if attack_coord.row > from_coord.row else SignDirection.NEGATIVE))
                    attack_col_dir = (SignDirection.ZERO if attack_coord.col == from_coord.col else 
                                     (SignDirection.POSITIVE if attack_coord.col > from_coord.col else SignDirection.NEGATIVE))
                    # Check if king move
                    # When the piece moving is the king, we have to check both the direction and the negated direction 
                    # as moving towards or away (same direction just negated) from the attacking piece still puts the king in check.
                    if (king_move):
                        negated_row_dir = (row_dir if row_dir == SignDirection.ZERO else 
                                          (SignDirection.POSITIVE if row_dir == SignDirection.NEGATIVE else SignDirection.NEGATIVE))
                        negated_col_dir = (col_dir if col_dir == SignDirection.ZERO else 
                                          (SignDirection.POSITIVE if col_dir == SignDirection.NEGATIVE else SignDirection.NEGATIVE))
                        # Check if the piece can move in the direction required to put king in check (same direction as the piece was from the king)
                        if ((attack_row_dir == row_dir and attack_col_dir == col_dir) or 
                            (attack_row_dir == negated_row_dir and attack_col_dir == negated_col_dir)):
                            # Piece can move in direction required to put king in check and attacker not captured - king now in check
                            return True 
                    else:
                        # Check if the piece can move in the direction required to put king in check (same direction as the piece was from the king)
                        if (attack_row_dir == row_dir and attack_col_dir == col_dir):
                            # Piece can move in direction required to put king in check and attacker not captured - king now in check
                            return True 
        
        # No pieces can move in direction required to put king in check - king not in check
        return False


    # Private method that gets all the valid coordinates a piece can moves
    #
    # Parameters:
    #   piece_loc: The PieceCoordinate to get the moves for
    #
    # NOTE: Does not get en passant moves as they are added in the move method (as they change independent of if anything affects the pawn)
    # NOTE: Does not get the castling moves for the king as they are added in the move method (as they change independent of if anything affects the king)
    # NOTE: Assumes the attack array is correct (as it's updated after every move)
    #
    # Returns a list of all the valid coordinates the piece can move to (as a list of Coordinate objects)
    #@profile
    def _get_action_info_for_piece(self, piece_loc: PieceCoordinate) -> PieceActionInfo:
        # Create a list of valid coordinates
        valid_move_coords: list[Coordinate] = []
        valid_attack_coords: list[Coordinate] = []
        
        # Check if piece is a pawn
        if (piece_loc.Piece.Type == PieceType.PAWN):
            # Three options (up one, up two (from starting place), and diagonal capture)
            # Check up one
            # Get the pawn direction (1 for white, -1 for black)
            pawn_direction = self._get_pawn_direction(piece_loc.Piece.Color)

            # Only for move generation - Moving pawn for non-capture moves

            # Get the new row to check
            new_row = piece_loc.Coord.row + pawn_direction
            # Check if space up one is in bounds
            if (self._ind_in_board(new_row)):
                # Check if the space is empty
                if (self._board_arr[new_row][piece_loc.Coord.col] == None):
                    # Add the space to the valid coordinates
                    valid_move_coords.append(Coordinate(new_row, piece_loc.Coord.col))
                        

            # Check up two (if starting place)
            # Get the starting row (1 for white, 6 for black)
            starting_row = self._get_pawn_starting_row(piece_loc.Piece.Color)

            # Check if the piece is on the starting row
            if (piece_loc.Coord.row == starting_row):
                # Get the new row to check
                new_row = piece_loc.Coord.row + (pawn_direction * 2)
                # Check if space up two is in bounds
                if (self._ind_in_board(new_row)):
                    # Check if the space is empty and the space between the start and end is empty
                    if (self._board_arr[new_row][piece_loc.Coord.col] == None and self._board_arr[new_row - pawn_direction][piece_loc.Coord.col] == None):
                        # Add the space to the valid coordinates
                        valid_move_coords.append(Coordinate(new_row, piece_loc.Coord.col))

            # End Only for Move Generation - Moving pawn for non-capture moves
            
            # Check diagonal capture (if diagonal space has a piece on the other team or en passant available)
            # Loop through two possibilities (right diagonal and left diagonal)
            for col_dir in range(2):
                # Get the new row and column to check
                new_row = piece_loc.Coord.row + pawn_direction
                new_col = piece_loc.Coord.col + (1 if col_dir == 0 else -1)

                # The coord to add if valid
                new_coord = Coordinate(new_row, new_col)

                # Check if the space is in bounds
                if (Board._coord_in_board(new_coord)):
                    # Get the piece at the new row and column to check
                    piece = self._board_arr[new_row][new_col]

                    # Add the space to the valid attack coordinates 
                    # As the pawn captures diagonally that space is always under attack - even if it can't move there yet
                    valid_attack_coords.append(new_coord)

                    # Check if the space has a piece on the other team
                    # En passant not added in this method
                    if (piece != None and piece.Color != piece_loc.Piece.Color):
                        # Add the space to the valid coordinates
                        valid_move_coords.append(new_coord)
                            
        else:
            # Loop through the directions the piece can move (all 8 or 4 directions - excluding pawn)
            #   Knight - 8 directions (up 2 right 1, up 2 left 1, up 1 right 2, up 1 left 2, down 2 right 1, down 2 left 1, down 1 right 2, down 1 left 2)
            #   Bishop - 4 directions (up left, up right, down left, down right)
            #   Rook - 4 directions (up, down, left, right)
            #   Queen - 8 directions (up, down, left, right, up left, up right, down left, down right)
            #   King - 8 directions (up, down, left, right, up left, up right, down left, down right)

            # Check if the piece can move in 4 directions not 8
            four_dir_piece = piece_loc.Piece.Type == PieceType.BISHOP or piece_loc.Piece.Type == PieceType.ROOK
            for dir in range(4 if four_dir_piece else 8):
                # row_dir and col_dir are only used for rook, bishop, and queen and of type SignDirection
                # row_adj and col_adj are only used for knight and are of type int
                if (piece_loc.Piece.Type == PieceType.ROOK):
                    # Set row dir to be Positive if dir is 0 (up), Negative if dir is 1 (down), ZERO otherwise
                    row_dir = SignDirection.POSITIVE if dir == 0 else (SignDirection.NEGATIVE if dir == 1 else SignDirection.ZERO)
                    # Set col dir to be Positive if dir is 2 (right), Negative if dir is 3 (left), ZERO otherwise
                    col_dir = SignDirection.POSITIVE if dir == 2 else (SignDirection.NEGATIVE if dir == 3 else SignDirection.ZERO)
                elif (piece_loc.Piece.Type == PieceType.BISHOP):
                    # Set row dir to be Positive if dir // 2 is 0 (up), otherwise Negative (down)
                    row_dir = SignDirection.POSITIVE if dir // 2 == 0 else SignDirection.NEGATIVE
                    # Set col dir to be Positive if dir % 2 is 0 (right), otherwise Negative (left)
                    col_dir = SignDirection.POSITIVE if dir % 2 == 0 else SignDirection.NEGATIVE
                elif (piece_loc.Piece.Type == PieceType.KNIGHT):
                    # Set row adjustment to be 2 if dir % 2 is 0 otherwise 1 (amount up or down)
                    # Set row adjustment to be Positive if dir // 4 is 0 (up), Negative othwerise
                    row_adj = 2 if dir % 2 == 0 else 1
                    row_adj = row_adj if dir // 4 == 0 else -row_adj

                    # Set col adjustment to be 1 if dir % 2 is 0 otherwise 2 (amount left or right)
                    # Set col adjustment to be Positive if (dir // 2) % 2 is 0 (right), Negative othwerise
                    col_adj = 1 if dir % 2 == 0 else 2
                    col_adj = col_adj if (dir // 2) % 2 == 0 else -col_adj
                else:
                    # Can move in all directions
                    # Set row dir to be Positive if dir // 3 is 0 (up), Negative if dir // 3 is 1 (down), ZERO otherwise
                    row_dir = SignDirection.POSITIVE if dir // 3 == 0 else (SignDirection.NEGATIVE if dir // 3 == 1 else SignDirection.ZERO)
                    # Set col dir to be Positive if dir % 3 is 0 (right), Negative if dir % 3 is 1 (left), ZERO otherwise
                    col_dir = SignDirection.POSITIVE if dir % 3 == 0 else (SignDirection.NEGATIVE if dir % 3 == 1 else SignDirection.ZERO)

                # Check if the piece is a knight
                if (piece_loc.Piece.Type == PieceType.KNIGHT):
                    # Get the new row and column to check
                    new_row = piece_loc.Coord.row + row_adj
                    new_col = piece_loc.Coord.col + col_adj

                    # The coord to add if valid
                    new_coord = Coordinate(new_row, new_col)

                    # Check if the knight can't move in this direction
                    if (Board._coord_in_board(new_coord) == False):
                        continue
                    
                    # Get the piece at the new row and column to check
                    piece = self._board_arr[new_row][new_col]

                    # Add the space to the valid attack coordinates
                    # As the knight has all positions under attack, even if it can't move there yet
                    valid_attack_coords.append(new_coord)

                    # Check if there can be valid moves and the knight can be moved to the space (no piece or piece is not on the same team)
                    # NOTE: Knights can jump over pieces so no need to check if there's a piece in the way
                    if (piece == None or piece.Color != piece_loc.Piece.Color):
                        # Add the space to the valid move coordinates
                        valid_move_coords.append(new_coord)
                            

                # Otherwise it's a rook, queen, bishop, or king
                else:
                    # Get the piece action info for the piece in the direction specified
                    new_action_info = self._get_action_info_for_piece_in_dir(piece_loc, row_dir, col_dir)

                    # Add the valid coordinates to the valid coordinates list
                    valid_attack_coords.extend(new_action_info.attack_coords)
                    valid_move_coords.extend(new_action_info.valid_move_coords)
                    
        # Return the valid coordinates as a PieceActionInfo object
        return PieceActionInfo(valid_move_coords, valid_attack_coords)
    
    # Gets the piece action info for a non knight or pawn piece in a specific direction
    #
    # Parameters:
    #   piece_loc: The PieceCoordinate to get the moves for
    #   row_dir: The direction in the row the piece moved
    #   col_dir: The direction in the column the piece moved
    #   max_spaces: The maximum number of spaces to check (default is 7 - max number of spaces available to move on the board)
    #
    # Returns the piece action info for the piece in the direction specified
    #
    # NOTE: This is only for non knight or pawn pieces (Bishop, Rook, Queen, or King)
    #@profile
    def _get_action_info_for_piece_in_dir(self, piece_loc: PieceCoordinate, row_dir: SignDirection, col_dir: SignDirection, 
                                          max_spaces: int = 7) -> PieceActionInfo:
        # King can only move one space - (no limit (max possible is 7) for rook, queen, or bishop)
        max_spaces = 1 if piece_loc.Piece.Type == PieceType.KING else max_spaces
        # Get the spaces available in the move direction (include blocking piece if for mask (not is_for_move_generation))
        # If for attack arr (not move generation) then include the blocking piece no matter the color (team_color = True)
        # Doesn't include last piece if it's on the same team
        #   - This is done below by checking if it's the last space and if it's on the same team
        spaces_available = self._get_spaces_available_in_move_dir(from_coord=piece_loc.Coord, row_dir=row_dir, col_dir=col_dir, 
                                                                    team_color=True, max_spaces=max_spaces)
        
        # Create the PieceActionInfo object
        piece_action_info = PieceActionInfo([], [])

        # Check that there's a space available (necessary for special case and more efficient if we check here)
        if (spaces_available != 0):
            # Get the new row and column to check
            new_row = piece_loc.Coord.row
            new_col = piece_loc.Coord.col
            
            # Get the directions value
            row_dir = row_dir.value
            col_dir = col_dir.value

            # Set the mask to true for all the spaces available 
            # Start at 1 since we don't include the current location of the piece
            for i in range(1, spaces_available):
                # Get the new row and column to check
                new_row += row_dir
                new_col += col_dir

                # Get the new coordinate
                new_coord = Coordinate(new_row, new_col)

                # Add the space to the valid attack coordinates
                # As the piece has all positions under attack in the spaces available, even if it can't move there yet
                piece_action_info.attack_coords.append(new_coord)

                # Add the space to the valid move coordinates
                piece_action_info.valid_move_coords.append(new_coord)

            # Last piece done outside loop as it's a special case
            # Get the new row and column to check
            new_row += row_dir
            new_col += col_dir

            # Get the new coordinate
            new_coord = Coordinate(new_row, new_col)

            # Add the space to the valid attack coordinates
            # As the piece has all positions under attack in the spaces available, even if it can't move there yet
            piece_action_info.attack_coords.append(new_coord)

            # Only for move generation - Check if the last piece can move to the space

            # Check if last space in spaces available and if so, if it's occupied by the opposite team
            # If occupied by the same team then it's not a valid move but still a valid attacking space
            if (self._board_arr[new_row][new_col] == None or 
                self._board_arr[new_row][new_col].Color != piece_loc.Piece.Color):
                # Add the space to the valid move coordinates
                piece_action_info.valid_move_coords.append(new_coord)

            # End Only for Move Generation - Check if the piece can move to the space
        
        # Return the piece action info
        return piece_action_info

    
    # Private method that adds a coordinate to valid coords only if the king isn't in check after the move
    
    # Protected Method that prints the attack arr in a more readable format
    #
    # NOTE: Used for debugging
    def _print_attack_arr(self):
        # Number of tabs for a full line (2 for number label and 3 per column) (plus one char for the final |) - 26
        num_tabs_per_line = 26

        # Print a newline to create a little space for the board
        print()

        # Print the first separator based on number of tabs per line
        for _ in range(num_tabs_per_line):
            print("--------", end="")
        # Extra one for the final |
        print("-")
        
        # Print the column labels
        print("|\t\t\tA\t\t\tB\t\t\tC\t\t\tD\t\t\tE\t\t\tF\t\t\tG\t\t\tH\t\t|")
        # Loop through the board and print the row labels and pieces
        for row in range(len(self._board_arr)):
            # Print the separator based on number of tabs per line
            for _ in range(num_tabs_per_line):
                print("--------", end="")
            # Extra one for the final |
            print("-")

            # Print the row label
            print("|\t" + str(row+1) + "\t|", end="")

            for col in range(len(self._attack_arr[row])):
                attack_dict = self._attack_arr[row][col]
                # Print the initial tab separator
                print("\t", end="")

                # Count number of attack pieces for this space
                piece_cnt = 0

                # Print the pieces
                for team_color in attack_dict:
                    for piece_type in attack_dict[team_color]:
                        for _ in attack_dict[team_color][piece_type]:
                            # Increment the counter
                            piece_cnt += 1
                            # Get the character that represents the piece
                            piece_char = "n" if piece_type == PieceType.KNIGHT else piece_type.name[0]
                            # Print the piece type and color
                            print(piece_char.upper() if team_color == TeamColor.WHITE else piece_char.lower(), end="")

                # If no pieces print none
                if (piece_cnt == 0):
                    # Print None for empty spaces
                    print("None", end="\t\t|")
                elif (piece_cnt < 8):
                    # Print the extra tabs
                    print("\t\t|", end="")
                elif (piece_cnt < 16):
                    # Print the extra tab
                    print("\t|", end="")
                else:
                    # Print the end char
                    print("|", end="")
            # Print the new line for the next row
            print()

        # Print the final separator
        for _ in range(num_tabs_per_line):
            print("--------", end="")
        print("-")
        print()
    
    # Prints the board in a more readable format
    #
    # NOTE: Used for debugging and demoes
    def print_board(self):
        # Number of tabs for a full line (2 for number label and 3 per column) (plus one char for the final |) - 26
        num_tabs_per_line = 26

        # Print a newline to create a little space for the board
        print()

        # Print the first separator based on number of tabs per line
        for _ in range(num_tabs_per_line):
            print("--------", end="")
        # Extra one for the final |
        print("-")
        
        # Print the column labels
        print("|\t\t\tA\t\t\tB\t\t\tC\t\t\tD\t\t\tE\t\t\tF\t\t\tG\t\t\tH\t\t|")
        # Loop through the board and print the row labels and pieces
        for i in range(len(self._board_arr)):
            row = self._board_arr[i]

            # Print the separator based on number of tabs per line
            for _ in range(num_tabs_per_line):
                print("--------", end="")
            # Extra one for the final |
            print("-")

            # Print the row label
            print("|\t" + str(i+1) + "\t|", end="")
            # Print the pieces
            for piece in row:
                # Print the initial tab separator
                print("\t", end="")
                if (piece == None):
                    # Print None for empty spaces
                    print("None", end="\t\t|")
                else:
                    # Print the piece type and color
                    print(piece.Type.name.lower() + "_" + piece.Color.name.lower(), end="\t|")
            # Print the new line for the next row
            print()
        # Print the final separator
        for _ in range(num_tabs_per_line):
            print("--------", end="")
        print("-")
        print()
        
    # Retruns the color who's turn it is
    def get_turn_color(self) -> TeamColor:
        return self._turn

    # Gets the value of a piece
    #
    # Parameters:
    #   piece_type: The type of piece to get the value of
    #
    # Returns the value of the piece
    @staticmethod
    def get_piece_value(piece_type: PieceType) -> int:
        if (piece_type == PieceType.PAWN):
            return 1
        elif (piece_type == PieceType.BISHOP or piece_type == PieceType.KNIGHT):
            return 3
        elif (piece_type == PieceType.ROOK):
            return 5
        elif (piece_type == PieceType.QUEEN):
            return 9
        elif (piece_type == PieceType.KING):
            return 200
        else:
            return 0
    
    # Gets the total material on the board
    #
    # Returns the total material on the board
    def get_total_material(self) -> int:
        # Run through the board and count each piece's value
        # Pawn = 1, Knight = 3, Bishop = 3, Rook = 5, Queen = 9
        # Return the sum of white and black's material 
        # material score = piece_value * (white + black)
        total_material = 0  
        for piece_type in PieceType:
            w_piece = self._get_pieces(piece_type, TeamColor.WHITE)
            b_piece = self._get_pieces(piece_type, TeamColor.BLACK)
            total_material += self.get_piece_value(piece_type) * (len(w_piece) + len(b_piece))
        return total_material
    
    # Finds and returns the difference between the material value of white and black pieces on the board
    def _count_material(self) -> int:
        # Run through the board and count each piece's value
        # Pawn = 1, Knight = 3, Bishop = 3, Rook = 5, Queen = 9
        # Return the difference between white and black's material 
        # material score = piece_value * (white - black)
        # Checkmate = no legal moves and in check
        # Stalemate if not in check
        # Checkmate evaluates to large value
        total_material = 0  
        for piece_type in PieceType:
            w_piece = self._get_pieces(piece_type, TeamColor.WHITE)
            b_piece = self._get_pieces(piece_type, TeamColor.BLACK)
            total_material += self.get_piece_value(piece_type) * (len(w_piece) - len(b_piece))
        return total_material
    
    # Gets the number of doubled, isolated, blocked, and passed pawns
    def _pawn_structure(self) -> int:
        # Count the number of doubled pawns
        # Store an array for white and black representing how many pawns are in each column
        # Would look something like [1, 1, 1, 2, 0, 1, 0, 2]
        # Count it the number of entries that are > 1, these are doubled pawns
        blocked_pawns = 0
        white_pawns = self._get_pieces(PieceType.PAWN, TeamColor.WHITE)
        black_pawns = self._get_pieces(PieceType.PAWN, TeamColor.BLACK)
        w_cols = [0 for i in range(8)]
        b_cols = [0 for i in range(8)]
        for pawn in white_pawns:
            w_cols[pawn.Coord.col] += 1
        for pawn in black_pawns:
            b_cols[pawn.Coord.col] += 1

        # Count the number of doubled pawns, which is white doubled pawns minus black doubled pawns
        doubled_pawns = 0
        for i in range(len(w_cols)):
            if (w_cols[i] > 1):
                doubled_pawns += (w_cols[i] - 1)
            if (b_cols[i] > 1):
                doubled_pawns -= (b_cols[i] - 1)
        
        # Count the number of isolated pawns, which is white isolated pawns minus black isolated pawns
        isolated_pawns = 0
        isolated_pawns = self._find_isolated_pawns(w_cols) - self._find_isolated_pawns(b_cols)
        
        # Count the number of blocked pawns
        # blocked_pawns is defined as the number of blocked white pawns minus blocked black pawns
        # Loop through each pawn, check if there is a piece in front of it
        # If there is, count it as a blocked pawn
        for pawn in white_pawns:
            if (self._board_arr[pawn.Coord.row + 1][pawn.Coord.col] != None):
                blocked_pawns += 1
        for pawn in black_pawns:
            if (self._board_arr[pawn.Coord.row - 1][pawn.Coord.col] != None):
                blocked_pawns -= 1

        # Get the number of passed pawns. This is the number of passed white pawns minus the 
        # number of passed black pawns. This will be subtracted from the final pawn structure score
        passed_pawns = self._passed_pawns(w_cols, b_cols)

        return doubled_pawns + isolated_pawns + blocked_pawns - passed_pawns
    

    # Count the number of isolated pawns
    # isolated_pawns is defined as the number of isolated white pawns minus isolated black pawns
    
    def _find_isolated_pawns(self, column_count: list[int]) -> int:
        # Check the columns on either side of the pawn, or one side if the pawn is at the edge of the board
        # If there are no piece in either column, count it as an isolated pawn
        isolated_pawns = 0
        for i in range(len(column_count)):
            if (column_count[i] >= 1):
                isolated_pawns += self.__check_adjacent_columns_isolated(column_count, i) * (column_count[i])

        return isolated_pawns
    

    # Private method for checking adjacent columns, useful for finding isolated pawns and passed pawns
    # Returns 1 if the piece is isolated on the row, 0 otherwise
    def __check_adjacent_columns_isolated(self, column_count: [int], i: int) -> int:
        isolated = 0
        if (i == 0):
            if (column_count[i + 1] == 0):
                isolated = 1
        elif (i == 7):
            if (column_count[i - 1] == 0):
                isolated = 1
        else:
            if (column_count[i - 1] == 0 and column_count[i + 1] == 0):
                isolated = 1
        return isolated
        

    # Count the number of passed pawns
    # passed pawns are pawns that cannot be blocked by an opposing pawn
    # This method returns the number of passed pawns for white minus the number of passed pawns for black
    def _passed_pawns(self, w_cols: [int], b_cols: [int]) -> int:
        # Check the column arrays of the white and black pawns. If or black has a column which is > 1
        # and the columns adjacent to it in the other column array are empty, count it as a passed pawn
        passed_pawns = 0
        for i in range(len(w_cols)):
            # If there is no black pawn in the column and there is a white pawn, check the adjacent columns
            if (w_cols[i] > 0 and b_cols[i] == 0):
                passed_pawns += self.__check_adjacent_columns_isolated(b_cols, i)
            # If there is no white pawn in the column and there is a black pawn, check the adjacent columns
            elif (b_cols[i] > 0 and w_cols[i] == 0):
                passed_pawns -= self.__check_adjacent_columns_isolated(w_cols, i)
        return passed_pawns
    
    # Get the difference in the number of legal moves between white and black
    #
    # Returns the difference in the number of legal moves between white and black
    def _get_mobility(self):
        # Subtract the moves for black from the moves for white
        return len(self.get_all_legal_moves(TeamColor.WHITE)) - len(self.get_all_legal_moves(TeamColor.BLACK))
    
    # Gets the combined values for the pieces under attack and not protected. This is the value of white pieces unprotected minus the 
    # value of black pieces unprotected
    #
    # TODO: Update this to check if king is in check and piece isn't causing it so can't be captured that turn
    # TODO: Update this so it checks if piece is trapped (i.e. can't move out of way)
    #
    # Returns the combined values for the pieces under attack and not protected
    def _get_attack_protection(self):
        white_score = self._get_attack_protection_score_for_team(TeamColor.WHITE)
        # print("White score: " + str(white_score))
        black_score = self._get_attack_protection_score_for_team(TeamColor.BLACK)
        # print("Black score: " + str(black_score))
        
        # Subtract the value of black pieces under attack and not protected from the value of white pieces under attack and not protected
        return white_score - black_score
        
    def _get_attack_protection_score_for_team(self, team_color: TeamColor) -> int:
        # Ignore the max piece value unprotected as they can move out of the way (only for team moving (team_color))
        # TODO: Update this so it checks if piece is trapped (i.e. can't move out of way)
        max_piece_value_unprotected = 0

        # Modifier for the max_piece value 
        # diff in score based on max_piece_value_unprotected is MAX_PIECE_VALUE_MODIFIER * max_piece_value_unprotected
        # If max_piece_value_unprotected is for a king the modifier is 0 so the king is ignored (as the king has to move out of check)
        # NOTE: max_piece_value_unprotected is only non-zero if team_color is the team moving (self._turn)
        MAX_PIECE_VALUE_MODIFIER = 0.05

        # Set piece value to 0 outside loop so not created on each iteration
        pieceValue = 0

        # Dict of coordinates and the max piece they're attacking
        # Used to check if piece is attacking multiple pieces to not count them twice
        piece_cap_val = {}

        score = 0
        other_team = TeamColor.WHITE if team_color == TeamColor.BLACK else TeamColor.BLACK

        for piece_loc in self._get_pieces(team_color=team_color):
            # Check if the piece is under attack (black has at least one piece attacking the space) and 
            # not protected (white has no pieces attacking/protecting the space)
            if (len(self._attack_arr[piece_loc.Coord.row][piece_loc.Coord.col][other_team]) > 0 and 
                len(self._attack_arr[piece_loc.Coord.row][piece_loc.Coord.col][team_color]) == 0):
                if (piece_loc.Piece.Type == PieceType.KING):
                    if (self._turn == team_color):
                        max_piece_value_unprotected = self.get_piece_value(PieceType.KING)
                    continue

                coord_arr = []
                for piece_type in self._attack_arr[piece_loc.Coord.row][piece_loc.Coord.col][other_team]:
                    coord_arr.extend(self._attack_arr[piece_loc.Coord.row][piece_loc.Coord.col][other_team][piece_type])
                
                pieceValue = self.get_piece_value(piece_loc.Piece.Type)

                min_val = pieceValue
                min_coord = None
                added = False
                for coord in coord_arr:
                    # Check if the piece is already in the dict
                    if (coord in piece_cap_val):
                        if (piece_cap_val[coord] < min_val):
                            min_val = piece_cap_val[coord]
                            min_coord = coord
                    else:
                        # Add the piece to the dict
                        piece_cap_val[coord] = pieceValue
                        score += pieceValue
                        added = True
                        break
                
                # Check if the piece was added to the dict
                if (not added):
                    # Check if the piece is the min piece value attacking the space
                    if (min_val < pieceValue):
                        # Add the new piece
                        piece_cap_val[min_coord] = pieceValue
                        score += pieceValue - min_val

                # Check if the piece is the max piece value unprotected
                if (pieceValue > abs(max_piece_value_unprotected) and self._turn == team_color):
                    max_piece_value_unprotected = pieceValue
        
        # If the max piece is a king, don't include in the score as it can't be captured
        if (abs(max_piece_value_unprotected) == self.get_piece_value(PieceType.KING)):
            adjusted_max_value_unprotected = 0#max_piece_value_unprotected
        else: 
            adjusted_max_value_unprotected = (1 - MAX_PIECE_VALUE_MODIFIER) * max_piece_value_unprotected

        # print("Max val: " + str(max_piece_value_unprotected))

        return score - adjusted_max_value_unprotected
    
    # Evaluates the position given different factors such as material score, pawn structure, mobility,
    # king safety
    # Returns a score for the position (positive for white, negative for black)
    #
    # NOTE: Does not check for half move or repitition draw
    #@profile
    def evaluate(self):
        # Check if the game is over (checkmate or stalemate)
        if (self._is_game_over()):
            # Check if the king is in checkmate
            other_team = TeamColor.WHITE if self._turn == TeamColor.BLACK else TeamColor.BLACK
            if (self._team_attacking_coord(other_team, self._pieces.get_king_coord(self._turn))):
                # Other team won
                # Check if white won
                if (other_team == TeamColor.WHITE):
                    # White won - return the max score (won)
                    return self.CHECKMATE_SCORE
                else:
                    # Black won - return the max negative score (won)
                    return -self.CHECKMATE_SCORE
            else:
                # Stalemate - return 0
                return 0
        # Evaluation heuristic:
        # self._count_material = 200(K-K')+ 9(Q-Q') + 5(R-R') + 3(B-B' + N-N') + 1(P-P')
        # self.pawn_structure = (D-D' + S-S' + I-I' - (PP-PP'))
        # self._passed_pawns = (PP-PP')
        # self._get_mobility = (M-M') + ...

        # KQRBNP = number of kings, queens, rooks, bishops, knights and pawns
        # D,S,I,PP = doubled, blocked, isolated, and passed pawns
        # M = Mobility (the number of legal moves) 
        # ' represents a black piece
        eval = self._count_material()
        # This value could probably be lower
        eval -= (0.1 * self._pawn_structure())
        # Checks the difference in unprotected pieces under attack (want lower value - so subtract)
        eval -= (0.6 * self._get_attack_protection())
        # This value could probably also be lower (centipawn)
        eval += (0.01 * self._get_mobility())
        return eval
    
    # Create the values for zobrist to use when hasing
    # NOTE: This should only be called once - when the board is created
    # NOTE: Calling more than once will cause the zobrist hash to not line up with previous hashes (however this may not matter if called between games)
    def _create_zobrist_tables(self):
        # Zobrist hash is a 64 bit integer, representing the current position. It is generated
        # from random numbers, and updated every time a move is made
        # Generate a 12*64 list of random numbers, one for each piece type in each square
        # Create a list for each piece, 0-5 for black, 6-11 for white
        # The order is pawn, bishop, knight, rook, queen, king. 
        # Each piece's list has 64 random numbers, one for each square. The index 0 is for A1, 1 for B1, 9 for A2, etc

        # Create a list of random numbers for each piece type
        self._zobrist_table = []
        curr_squares = [0 for i in range(64)]
        for color in TeamColor:
            for piece_type in PieceType:
                for i in range(64):
                    curr_squares[i] = random.randint(0, pow(2, len(curr_squares)))
                self._zobrist_table.append(curr_squares)
        
        # Set the rest of the random numbers for zobrist hashing (turn, castling rights, en passant)
        # Set the turn random number as the first element of the misc list
        self._zobrist_misc = [random.randint(0, pow(2, 64))]
        curr_list = []
        for i in range(1, 3):
            curr_list = []
            # Turn has 1 value, castling has 4, and en passant has 8, so use power of 2 for each
            for j in range(4 * i):
                curr_list.append(random.randint(0, pow(2, 64)))
            self._zobrist_misc.append(curr_list)

    # Sets the initial Zobrist hash for the board. This should only be done once per game, as soon as the board is reset
    def _set_zobrist_hash(self):
        # Create the initial hash by running through each piece in the board and XORing the random number
        # by that piece's zobrist table value in that square
        self._zobrist_hash = 0
        for i in range(len(self._board_arr)):
            for j in range(len(self._board_arr)):
                if self._board_arr[i][j] is not None:
                    piece_index = self._board_arr[i][j].Color.value * 6 + self._board_arr[i][j].Type.value
                    self._zobrist_hash ^= self._zobrist_table[piece_index][j]

        # NOTE: XOR the turn random number on each turn not at the start of the game (doesn't really matter, but more efficient this way)

        # XOR by the castling rights random number, for each castling right there is
        if (self._castling_rights.black_kingside):
            self._zobrist_hash ^= self._zobrist_misc[1][0]
        if (self._castling_rights.black_queenside):
            self._zobrist_hash ^= self._zobrist_misc[1][1]
        if (self._castling_rights.white_kingside):
            self._zobrist_hash ^= self._zobrist_misc[1][2]
        if (self._castling_rights.white_queenside):
            self._zobrist_hash ^= self._zobrist_misc[1][3]

        # XOR by the en passant random number, if there is an en passant square
        if (self._en_passant_avail):
            self._zobrist_hash ^= self._zobrist_misc[2][self._en_passant_avail.col]
    
    # Gets the zobrist hash for the board if it was updated for a move (does not actually update the board's hash)
    #
    # Parameters:
    #   move: The move to update the hash for
    #
    # Returns the updated zobrist hash
    #
    # NOTE: This only works for making a move (not undoing a move) as it doesn't update the en passant square
    # NOTE: This should only be called before the move has been made
    # NOTE: Assumes the move is a valid move
    def update_zobrist_hash(self, move : Move) -> int:
        # Get the index of the piece's square for the zobrist table
        # Take 16.5% of the time?
        row1, col1 = move.from_coord.row, move.from_coord.col
        # Only takes 1.4%
        row2, col2 = move.to_coord.row, move.to_coord.col
        square1 = row1 * 8 + col1
        square2 = row2 * 8 + col2
        # print(move, col1, col2, row1, row2)
        # TODO: Figure out a better way to do this, the first one is 8% of the time, the second is 20%
        # color_vals = {TeamColor.WHITE: 0, TeamColor.BLACK: 1}
        
        # piece_vals = {PieceType.PAWN: 0, PieceType.BISHOP: 1, PieceType.KNIGHT: 2, PieceType.ROOK: 3, PieceType.QUEEN: 4, PieceType.KING: 5}
        # Get the piece, if using move, the piece is at row1 col1. If using undo_move, the piece is at
        # row2 col2, so check which one to use
        piece: Piece = self._board_arr[row1][col1]
        captured_piece = None
        if piece is None:
            piece: Piece = self._board_arr[row2][col2]
        else:
            # TODO: Figure out what the captured piece is if it is en passant
            captured_piece: Piece = self._board_arr[row2][col2]
        # XOR the zobrist hash by the piece's random number in the square it's moving from and to
        piece_index = piece.Color.value * 6 + piece.Type.value

        curr_hash = self._zobrist_hash

        curr_hash ^= self._zobrist_table[piece_index][square1]

        curr_hash ^= self._zobrist_table[piece_index][square2]

        # XOR by the current turn's random number (alternates between being added and removed, so one team has it added and the other removed)
        curr_hash ^= self._zobrist_misc[0]

        piece_type = piece.Type

        # XOR by the castling rights random number, for each castling right there is
        # Check if the castling rights have changed, which happens on both sides if the king is moving, 
        # or on one side if a rook piece is moving from either side
        if (self._castling_rights.black_kingside and
            ((piece_type == PieceType.KING and piece.Color == TeamColor.BLACK) or 
             (piece_type == PieceType.ROOK and piece.Color == TeamColor.BLACK and (row1 == 7 and col1 == 7)) or (captured_piece is not None and
             (captured_piece.Type == PieceType.ROOK and captured_piece.Color == TeamColor.BLACK and (row2 == 7 and col2 == 7))))):
            curr_hash ^= self._zobrist_misc[1][0]
        if (self._castling_rights.black_queenside and
            ((piece_type == PieceType.KING and piece.Color == TeamColor.BLACK) or 
             (piece_type == PieceType.ROOK and piece.Color == TeamColor.BLACK and (row1 == 7 and col1 == 0)) or (captured_piece is not None and
             (captured_piece.Type == PieceType.ROOK and captured_piece.Color == TeamColor.BLACK and (row2 == 7 and col2 == 0))))):
            curr_hash ^= self._zobrist_misc[1][1]
        if (self._castling_rights.white_kingside and
            ((piece_type == PieceType.KING and piece.Color == TeamColor.WHITE) or 
             (piece_type == PieceType.ROOK and piece.Color == TeamColor.WHITE and (row1 == 0 and col1 == 7)) or (captured_piece is not None and 
             (captured_piece.Type == PieceType.ROOK and captured_piece.Color == TeamColor.WHITE and (row2 == 0 and col2 == 7))))):
            curr_hash ^= self._zobrist_misc[1][2]
        if (self._castling_rights.white_queenside and
            ((piece_type == PieceType.KING and piece.Color == TeamColor.WHITE) or 
             (piece_type == PieceType.ROOK and piece.Color == TeamColor.WHITE and (row1 == 0 and col1 == 0)) or (captured_piece is not None and
             (captured_piece.Type == PieceType.ROOK and captured_piece.Color == TeamColor.WHITE and (row2 == 0 and col2 == 0))))):
            curr_hash ^= self._zobrist_misc[1][3]

        # XOR by the en passant random number, if there is an en passant square  or if the piece is a pawn and moving 2 spaces
        # If there is an en passant square, XOR by the random number for that column
        if (self._en_passant_avail is not None):
            # This is removing the en passant square by XORing by the random number for that column 
            # which was XORed in when the en passant square was added
            curr_hash ^= self._zobrist_misc[2][self._en_passant_avail.col]
        # If the piece is a pawn and moving 2 spaces, XOR by the random number for that column
        if (piece_type == PieceType.PAWN and abs(row1 - row2) == 2):
            # This is adding the en passant square by XORing by the random number for that column
            curr_hash ^= self._zobrist_misc[2][col1]

        # XOR by the captured piece's random number, if there is a captured piece
        if captured_piece is not None:
            piece_index = captured_piece.Color.value * 6 + captured_piece.Type.value
            curr_hash ^= self._zobrist_table[piece_index][square2]
        # Check for en passant capture
        elif (piece_type == PieceType.PAWN and col1 != col2):
            # XOR by the en passant random number, if there is an en passant square
            curr_hash ^= self._zobrist_misc[2][col2]

        return curr_hash

    # Gets the zobrist hash for the board if it was updated for a move / undone move (does not actually update the board's hash)
    #
    # Parameters:
    #   move_info: The move info to update the hash for
    #
    # Returns the updated zobrist hash
    #
    # NOTE: Use the same move_info for both the move and undo_move
    # NOTE: This should be called after a move has been made or before a move has been undone
    # NOTE: Assumes the MoveInfo was the previous move made
    def update_zobrist_hash_from_move_info(self, move_info: MoveInfo) -> int:
        # Get the index of the piece's square for the zobrist table
        # Take 16.5% of the time?
        row1, col1 = move_info.move.from_coord.row, move_info.move.from_coord.col
        # Only takes 1.4%
        row2, col2 = move_info.move.to_coord.row, move_info.move.to_coord.col
        # print(move, col1, col2, row1, row2)
        square1 = row1 * 8 + col1
        square2 = row2 * 8 + col2

        # Get the piece, if using move, the piece is at row1 col1. If using undo_move, the piece is at
        # row2 col2, so check which one to use
        piece: Piece = self._board_arr[row1][col1]
        captured_piece = move_info.cap_piece_type
        if piece is None:
            piece: Piece = self._board_arr[row2][col2]

        # color_index = 1 if piece.Color == TeamColor.WHITE else 0
        
        # XOR the zobrist hash by the piece's random number in the square it's moving from and to
        color_val = piece.Color.value * 6
        piece_index = color_val + piece.Type.value
        # print('Move: ', row1, col1, row2, col2)
        # print('Move Info: ', move_info.move, move_info.castling_rights, move_info.en_passant_avail)
        # print(piece_index, square1, square2)

        curr_hash = self._zobrist_hash
        curr_hash ^= self._zobrist_table[piece_index][square1]
        curr_hash ^= self._zobrist_table[piece_index][square2]

        # XOR by the turn random number (alternates between being added and removed, so one team has it added and the other removed)
        curr_hash ^= self._zobrist_misc[0]

        if (self._castling_rights.black_kingside ^ move_info.castling_rights.black_kingside):
            # print('castling bk')
            curr_hash ^= self._zobrist_misc[1][0]
        if (self._castling_rights.black_queenside ^ move_info.castling_rights.black_queenside):
            # print('castling bq')
            curr_hash ^= self._zobrist_misc[1][1]
        if (self._castling_rights.white_kingside ^ move_info.castling_rights.white_kingside):
            # print('castling wk')
            curr_hash ^= self._zobrist_misc[1][2]
        if (self._castling_rights.white_queenside ^ move_info.castling_rights.white_queenside):
            # print('castling wq')
            curr_hash ^= self._zobrist_misc[1][3]

        # XOR by the en passant random number, if there is an en passant square
        if (self._en_passant_avail is not None and move_info.en_passant_avail is not None):
            # print('Multiple En passants')
            curr_hash ^= self._zobrist_misc[2][self._en_passant_avail.col]
            curr_hash ^= self._zobrist_misc[2][move_info.en_passant_avail.col]
        elif ((self._en_passant_avail is not None or move_info.en_passant_avail is not None)):
            # print('En passant')
            col = move_info.en_passant_avail.col if move_info.en_passant_avail is not None else self._en_passant_avail.col
            curr_hash ^= self._zobrist_misc[2][col]

        # XOR by the captured piece's random number, if there is a captured piece
        # First check if capture is en passant (capture not at to coord)
        if (move_info.en_passant):
            # print('en passant capture')
            en_passant_square = move_info.en_passant_avail.row * 8 + move_info.en_passant_avail.col
            curr_hash ^= self._zobrist_table[color_val + PieceType.PAWN.value][en_passant_square]
        # Then check if capture is normal
        elif captured_piece is not None:
            # print('capture')
            piece_index = color_val + captured_piece.value
            curr_hash ^= self._zobrist_table[piece_index][square2]

        return curr_hash

    # Gets the Zobrist hash for the current board
    def get_zobrist_hash(self) -> int:
        return self._zobrist_hash

    # Checks if a move causes check by checking if the king is in check after the move
    # This should be used for move ordering
    #
    # Returns True if the move causes check, False otherwise 
    def move_causes_check(self, move: Move) -> bool:
        # Get the piece which is moving, and the location of the king
        piece: Piece = self._board_arr[move.from_coord.row][move.from_coord.col]
        other_team = TeamColor.WHITE if piece.Color == TeamColor.BLACK else TeamColor.BLACK
        king_coord = self._pieces.get_king_coord(other_team)

        if piece.Type == PieceType.KING:
            return False

        # Pawn - Check if the move is diagonal and if the piece is attacking the king
        if piece.Type == PieceType.PAWN:
            # Check if the king is diagonal to the pawn
            if abs(move.to_coord.row - king_coord.row) == 1 and abs(move.to_coord.col - king_coord.col) == 1:
                capture_row = move.to_coord.row + 1 if piece.Color == TeamColor.WHITE else move.to_coord.row - 1
                if capture_row == king_coord.row and (move.to_coord.col - 1 == king_coord.col or move.to_coord.col + 1 == king_coord.col):
                    return True
        
        # Knight - Check all knight spots
        elif piece.Type == PieceType.KNIGHT:
            # Check if the knight moves to a spot where they are within reach of the king
            if (abs(move.to_coord.row - king_coord.row) == 2 and abs(move.to_coord.col - king_coord.col) == 1) or \
                (abs(move.to_coord.row - king_coord.row) == 1 and abs(move.to_coord.col - king_coord.col) == 2):
                # If the knight can reach the king, get the distance between the knight and the king and call
                # the helper function to check if the move results in check
                row_diff = king_coord.row - move.to_coord.row
                col_diff = king_coord.col - move.to_coord.col 
                return self.__knight_move_causes_check(move, row_diff, col_diff)
        
        # Others - Diagonal or orthogonal, get 
        elif piece.Type == PieceType.BISHOP:
            # Check if the king is directly diagonal to the bishop
            if (abs(move.to_coord.row - king_coord.row) == abs(move.to_coord.col - king_coord.col)):
                # If it is, get the direction to move in for the possible check and call the helper function
                # to check if the move results in a check
                row_diff = king_coord.row - move.to_coord.row
                col_diff = king_coord.col - move.to_coord.col
                row_dir = SignDirection.POSITIVE if row_diff > 0 else SignDirection.NEGATIVE
                col_dir = SignDirection.POSITIVE if col_diff > 0 else SignDirection.NEGATIVE
                return self.__bishop_move_causes_check(move, row_dir, col_dir)
        
        # Check the squares in between, if it can see a king then it is check
        elif piece.Type == PieceType.ROOK:
            # Check if the row is the same and the column isn't, or vice versa
            if (move.to_coord.row == king_coord.row ^ move.to_coord.col == king_coord.col):
                # If it is, get the direction to move in for the possible check and call the helper function
                # to check if the move results in a check
                row_diff = move.to_coord.row - king_coord.row
                col_diff = move.to_coord.col - king_coord.col
                row_dir = SignDirection.POSITIVE if row_diff > 0 else SignDirection.NEGATIVE
                col_dir = SignDirection.POSITIVE if col_diff > 0 else SignDirection.NEGATIVE
                if row_diff == 0:
                    row_dir = SignDirection.ZERO
                if col_diff == 0:
                    col_dir = SignDirection.ZERO

                return self.__rook_move_causes_check(move, row_dir, col_dir)
        
        # If the piece is a queen
        # Check if the piece is moving diagonally or orthogonally
        if (abs(move.to_coord.row - king_coord.row) == abs(move.to_coord.col - king_coord.col)) or \
            (move.to_coord.row == king_coord.row ^ move.to_coord.col == king_coord.col):
            # If it is, get the direction to move in for the possible check and call the helper function
            # for both the bishop and the rook piece, as queen has the same legal moves as both
            row_diff = king_coord.row - move.to_coord.row 
            col_diff = king_coord.col - move.to_coord.col
            row_dir = SignDirection.POSITIVE if row_diff > 0 else SignDirection.NEGATIVE
            col_dir = SignDirection.POSITIVE if col_diff > 0 else SignDirection.NEGATIVE
            if row_diff == 0:
                row_dir = SignDirection.ZERO
            if col_diff == 0:
                col_dir = SignDirection.ZERO
            if self.__bishop_move_causes_check(move, row_dir, col_dir):
                return True
            else:
                return self.__rook_move_causes_check(move, row_dir, col_dir)
                
        return False
    
    # Checks which squares the knight can see, and if the king is in one of those squares
    # Returns true if the king is in check, false otherwise
    def __knight_move_causes_check(self, move: Move, row_dir: int, col_dir: int) -> bool:
        # Check if there is a piece where the knight could potentially move to, if there is and it is a king,
        # return True. Otherwise, return False
        piece: Piece = self._board_arr[move.to_coord.row + row_dir][move.to_coord.col + col_dir]
        if piece is None:
            return False
        # print(piece.Type)
        return piece.Type == PieceType.KING and piece.Color != self._turn

    # Checks which squares the bishop can see, and if the king is in one of those squares
    # Returns true if the king is in check, false otherwise
    def __bishop_move_causes_check(self, move: Move, row_dir: SignDirection, col_dir: SignDirection) -> bool:
        # Check if the piece is moving up or down
        if row_dir  == SignDirection.POSITIVE:
            row_dir = 1
        else:
            row_dir = -1

        # Check if the piece is moving left or right
        if col_dir == SignDirection.POSITIVE:
            col_dir = 1
        else:
            col_dir = -1

        # Loop through the squares in between the piece's current position and the square it's moving to
        # Check if the square is occupied by a piece, if so return false
        # If the square is occupied by the king, return true
        curr_row = move.to_coord.row
        curr_col = move.to_coord.col
        # Check the diagonal until the edge of the board is reached or a piece is hit
        while (curr_row < 8 and curr_row > 0) and (curr_col < 8 and curr_col > 0):
            piece: Piece = self._board_arr[curr_row][curr_col] 
            # If a piece is hit, return True if it is a king of the opposite color, False otherwise
            if piece is not None:
                return piece.Type == PieceType.KING and piece.Color != self._turn
            # Continue checking the diagonal if no piece is hit
            curr_row += row_dir
            curr_col += col_dir
        return False

    # Checks which squares the rook can see, and if the king is in one of those squares
    # Returns true if the king is in check after the move, false otherwise
    def __rook_move_causes_check(self, move: Move, row_dir: SignDirection, col_dir: SignDirection) -> bool:
        # Check if the piece is moving up or down
        if row_dir  == SignDirection.POSITIVE:
            row_dir = 1
        elif row_dir == SignDirection.NEGATIVE:
            row_dir = -1
        else:
            row_dir = 0

        # Check if the piece is moving left or right
        if col_dir == SignDirection.POSITIVE:
            col_dir = 1
        elif col_dir == SignDirection.NEGATIVE:
            col_dir = -1
        else:
            col_dir = 0

        # Loop through the squares in between the piece's current position and the square it's moving to
        # Check if the square is occupied by a piece, if so return false
        # If the square is occupied by the king, return true
        curr_row = move.to_coord.row
        curr_col = move.to_coord.col
        while (curr_row < 8 and curr_row > 0) and (curr_col < 8 and curr_col > 0):
            piece: Piece = self._board_arr[curr_row][curr_col] 
            if piece is not None:
                return piece.Type == PieceType.KING and piece.Color != self._turn
            curr_row += row_dir
            curr_col += col_dir
        return False