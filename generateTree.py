# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:47:31 2023

@author: Ethan Geoffrey Wijaya
"""
import copy
import random
from Board import Board, TeamColor, Move
from collections import deque
from Board import Piece
from Tablebase import Tablebase

# NOTE:
#   - Added some major optimizations
#   - Capture moves in quiescence now ordered
#   - Any code that adds to transposition tables now commented out until positions matching transposition tables are handled
#       Currently, if a position exists in the transposition table, the tree will still search every node from that position.
#       Since the move_ordering function prioritizes hash moves first, it will force the tree to prioritize searching positions
#       that have already been searched. This is why I commented out adding anything to the transposition tables until we find a
#       way to handle a transposition table match. Once we do, most likely speed will significantly increase
#   - Fixed minor bug where in move ordering victim was taken from from_coords and attacker was taken from to_coords, causing capture
#       moves to be ordered in reverse. Resulted in pretty good performance increase
# NOTE: Minimax now extremely fast at depth 3. It can run our slowest MinimaxDemo test position (1k1q2b1/1pp1r3/p4r2/3n4/5N2/P7/BPPQ4/1KR5 w - - 0 1) in 
#           less than 2 seconds for depth 3. For depth 5, it runs on average 61 seconds. Depth 5 might be viable after transposition table fixes.

# The Node class which makes up the tree.
# Important public fields:
#   position - A Board object representing the Node's board position
#   parent - This node's parent
#   children - This node's children that are currently accessible in the tree
#   alpha - A field used for storing alpha. Must be filled by the user
#   beta - A field used for storing beta. Must be filled by the user
#   score - A field representing the score assigned to this position. Must be filled by the user
#
# Parameters:
#   position - A Board object representing this Node's board position
#   parent - A Node object representing this node's parent
class Node:
    def __init__(self, parent):
        self.parent: Node = parent
        self.__legalMoves: deque[Move] = deque()
        self.__legalCaptures: deque[Move] = deque()
        self.child: Node = None
        self.previous_move: Move = None
        self.best_child: Node = None

        self.alpha: float = float('-inf') if parent == None else parent.alpha
        self.beta: float = float('inf') if parent == None else parent.beta

        if (parent != None):
            self.level: int = parent.level + 1
        else:
            self.level: int = 0

        self.score: float = float('-inf') if self.level % 2 == 0 else float('inf')
        
    # Uses the Board class to generate all possible legal moves from this position and store it in the Node
    #
    # Returns true if legal moves exist
    # @profile
    def _load_legal_moves(self, board: Board) -> bool:
        self.__legalMoves.extend(board.get_all_legal_moves())
        # x = self.parent
        # s = "None" if self.previous_move == None else self.previous_move
        # while x != None: s = ("Root" if x.previous_move == None else x.previous_move) + " -> " + s; x = x.parent
        # print("Known Moves (" + s + "): " + str(self.__legalMoves))
        return len(self.__legalMoves) > 0
    
    # Uses the Board class to generate all possible legal captures from this position and store it in the Node
    #
    # Returns true if legal captures exist
    # @profile
    def _load_legal_captures(self, board: Board) -> bool:
        if (len(self.__legalMoves) == 0):
            self._load_legal_moves(board)
        for move in self.__legalMoves:
            x1, y1 = move.from_coord.row, move.from_coord.col
            x2, y2 = move.to_coord.row, move.to_coord.col
            piece1: Piece = board._board_arr[x1][y1]
            piece2: Piece = board._board_arr[x2][y2]
            if ((piece1 is not None and piece2 is not None) and piece1.Color != piece2.Color):
                # TODO: Potential optimiziation: Move ordering might be useful
                self.__legalCaptures.append(move)
        return len(self.__legalCaptures) > 0
    
    # Get the legal moves for the position, this is to be called from move ordering
    def _get_legal_moves(self) -> list[Move]:
        return list(self.__legalMoves)
    
    # Set the legal moves for this position, this will be set from the move ordering function
    # @profile
    def _set_legal_moves(self, moves: list[Move]):
        self.__legalMoves = deque(moves)

    # Getter for legalCaptures list
    def _get_legal_captures(self):
        return list(self.__legalCaptures)

    # Set the legal captures for this position, this will be set from the move ordering function
    def _set_legal_captures(self, moves: list[Move]):
        self.__legalCaptures = deque(moves)
    
    # Returns the next available move in the __legalMoves private field.
    def _next_move(self) -> Move:
        if (len(self.__legalMoves) > 0):
            return self.__legalMoves.popleft()
        else:
            return None
    
    # Returns the next available capture move in the __legalCaptures private field.
    def _next_capture(self) -> str:
        if (len(self.__legalCaptures) > 0):
            return self.__legalCaptures.popleft()
        else:
            return None
        
    # Setter for score field. Also updates parent's minimax score and best_child field
    def _set_minimax_values(self, score: float):
        # Set the score of this node
        self.score = score

        # If the parent does not exist do not attempt to alter it
        if (self.parent == None):
            return
        
        # Update parent score and alpha beta values
        # The root is always a maximizer, so even levels are maximizers, odd are minimizers
        # NOTE: Score comparison is done with an if statement and not max() or min() so that 
        #   best_child can be properly updated on condition success
        # NOTE: self.child is set to none so that the parent's best child will not hold a reference
        #   to a node that won't be traversed. Thus saving space.
        if (self.parent.level % 2 == 0):
            # Parent is maximizer. Check if current child's score is greater than the
            #   parent's score, which should be the max child score.
            if (self.parent.score < self.score):
                self.parent.score = self.score
                self.parent.alpha = self.score
                self.parent.best_child = self
                self.child = None
        else:
            # Parent is minimizer. Check if current child's score is less than the
            #   parent's score, which should be the min child score.
            if (self.parent.score > self.score):
                self.parent.score = self.score
                self.parent.beta = self.score
                self.parent.best_child = self
                self.child = None

    def _set_quiescence_values(self, score):
        self.score = score
        if (self.level % 2 == 0):
            # Parent is maximizer. Check if current child's score is greater than its
            #   alpha, which should be the max child score.
            if (self.alpha < score):
                self.alpha = score
        else:
            # Parent is minimizer. Check if current child's score is less than its
            #   beta, which should be the min child score.
            if (self.beta > score):
                self.beta = score

# The main Tree class to be accessed by the user.
#
# Creates the Tree iteratively. This basically means the Tree will start as only the root node
#   and its branches will only be created whenever a leaf node needs to be searched. The user must
#   create the tree by repeatedly calling Tree.next().
#
# Will automatically update minimax scores while using the alpha beta pruning algorithm, such that
#   the best move and score can be attainable from the root.
#
# Parameters:
#   root - A Board object meant to serve as the starting position from which to create the tree
#   depth - An int representing how deep the user wants the tree to be
#
# NOTE: The Tree can still be traversed by accessing the root node and its children. Only creating
#   the tree works like an iterable.
class Tree:
    def __init__(self, root: Board, depth: int, q_depth: int = 5, searchmoves: [Move] = None, nodes: float = float('inf')):
        self.__root: Node = Node(None)
        self.__root._load_legal_moves(root)
        self.__current: Node = self.__root
        self.__board: Board = root
        self.__TB: Tablebase = Tablebase()

        # UCI related fields
        if searchmoves is not None:
            self.__root._set_legal_moves(searchmoves)
        self.__node_limit = nodes
        self.__nodes_searched = 0 # Incremented in Tree.__move()
        self.__tbhits = 0 # Incremented in score upon tablebase hit

        
        # Traversal board this board is meant to be used for tree traversal, utilizing move and undo_move
        #   to avoid use of deep copying.
        self.__tboard: Board = copy.deepcopy(root)

        self.__depth: int = depth
        self.__q_depth: int = q_depth
        self.__starting_turn: TeamColor = root.get_turn_color()

        self.__transposition_table: dict[int, float] = dict()

        # Order the moves
        self.__root._set_legal_moves(self.move_ordering(self.__root))
    
    # Returns the next leaf node needed to be searched by the alpha beta pruning algorithm (Basically follows
    #   depth-first-search). Will create all Nodes necessary to reach the leaf node, extending the tree.
    #
    # Returns True if next node was succesfully found, false if there are no more nodes to search
    # @profile
    def next(self) -> bool:
        # Iteratively access every node and see if there are any children to be created
        # Exit the while loop if no more children can be created
        # NOTE: self.__current should only be None if we moved up from the root node whose parent is None [See MOVEUP]
        while (self.__current != None):
            if (self.__nodes_searched >= self.__node_limit): return False
            #print('Level: ', self.__current.level)
            nextMove = self.__current._next_move()
            #print('Next Move: ', nextMove)

            if (nextMove == None or self.__current.beta <= self.__current.alpha):
                # [MOVEUP] There are no more children to create so move up to the parent to look for more
                # Must set minimax values for the parent, and undo the latest move to the traversal board
                # Don't update transposition table if there is a half move draw or repetition draw (not based on position)
                if (self.__tboard.is_half_move_draw() or self.__tboard.is_repetition_draw()):
                    self.__current._set_minimax_values(0)
                else:
                    self.__current._set_minimax_values(self.__current.score)
                    # Add the score the the transposition table
                    self.__transposition_table[self.__tboard.get_zobrist_hash()] = self.__current.score
                #print(nextMove, self.__current.score)
                self.__current = self.__current.parent
                if (self.__current != None):
                    self.__undo_move()
                # Restart the while loop
                continue
            
            # Create a new node and set the necessary fields
            self.__current.child = Node(self.__current)
            self.__current.child.previous_move = nextMove

            # Skip node if found in transposition table
            if (self.__current.level == self.__depth):
                next_board_hash = self.__tboard.update_zobrist_hash(nextMove)
                if (next_board_hash in self.__transposition_table):
                    # If half move draw or repitition draw, set minimax values to 0 (draw)
                    # This will likely be different than transposition table value
                    # Check if draw by half move rule (usually 100 half moves - 50 move rule) or repetition (usually 3 fold repetition)
                    # if (self.__tboard.is_half_move_draw_on_move(nextMove) or self.__tboard.is_repetition_draw_on_position(next_board_hash)):
                    #     # Set minimax values to 0 (draw)
                    #     self.__current.child._set_minimax_values(0)
                    # else:
                    self.__current.child._set_minimax_values(self.__transposition_table[next_board_hash])
                    continue

            # Make the move
            self.__move(nextMove)
            
            hasLegalMoves = self.__current.child._load_legal_moves(self.__tboard)
            useTB = self.__tboard.get_piece_count() < 6
            # If we are not at the specified depth and there exist more legal moves, go to a lower level
            if (self.__current.child.level < self.__depth and hasLegalMoves and not useTB):
                self.__current = self.__current.child
                # Order the moves
                self.__current._set_legal_moves(self.move_ordering(self.__current))
            else:
                # If we are at the specified depth or there are no legal moves available,
                #   consider newNode a leaf node then score and return True since one was found
                if hasLegalMoves and not useTB and self.__q_depth > 0:
                    self.quiescence()
                else:
                    # Don't update transposition table if there is a half move draw or repetition draw (not based on position)
                    if (self.__tboard.is_half_move_draw() or self.__tboard.is_repetition_draw()):
                        self.__current.child._set_minimax_values(0)
                    else:
                        self.__current.child._set_minimax_values(self.__score(tb=useTB))
                        self.__transposition_table[self.__tboard.get_zobrist_hash()] = self.__current.child.score
                    self.__undo_move()

                return True
            
        # If we exit the while loop, it means there are no nodes left to create so return None
        return False
    
    # Quiescence search method. This is meant to be used in conjunction with the alpha beta pruning algorithm.
    # It is meant to be called on a leaf node that is not a terminal node. It will search the capturable moves
    # until no more capturable moves can be made. It will then return the score of the final position.
    # This method seeks to find any tactical moves that increase alpha
    # Pruning is also used to limit the tree generation.
    # @profile
    def quiescence(self):
        self.__current = self.__current.child
        self.__current._load_legal_captures(self.__tboard)
        self.__current._set_legal_captures(self.order_captures(self.__current))
        self.__current._set_quiescence_values(self.__score())

        # While the node is not the terminal node's parent, keep searching for capturable moves
        while (self.__current.level >= self.__depth):
            # Check if we exceeded the node limit
            if (self.__nodes_searched >= self.__node_limit): return False
            next_move = self.__current._next_capture()
        
            # If there is no move or if the alpha exceeds the beta value, move up in the tree
            if (next_move == None or self.__current.beta <= self.__current.alpha or self.__check_delta_cutoff(self.__current)):
                # [MOVEUP] There are no more children to create so move up to the parent to look for more
                # Must set minimax values for the parent, and undo the latest move to the traversal board
                # Don't need to check for halfmoves or repititions because quiescence is only called on captures
                self.__current._set_minimax_values(self.__current.score)
                # Add the score the the transposition table
                self.__transposition_table[self.__tboard.get_zobrist_hash()] = self.__current.score
                self.__current = self.__current.parent
                self.__undo_move()
                # Restart the while loop
                continue

            # x1, y1 = next_move.to_coord.row, next_move.to_coord.col
            # cap_value = self.__tboard.get_piece_value(self.__tboard._board_arr[x1][y1].Type)
            
            # Create a new node and set the necessary fields
            self.__current.child = Node(self.__current)
            self.__current.child.previous_move = next_move

            # Skip node if found in transposition table
            # if (self.__current.level == self.__depth):
            #     next_board_hash = self.__tboard.update_zobrist_hash(next_move)
            #     if (next_board_hash in self.__transposition_table):
            #         # Set the minimax values to the transposition table value
            #         self.__current.child._set_minimax_values(self.__transposition_table[next_board_hash])
            #         continue

            # Make the move
            self.__move(next_move)

            useTB = self.__tboard.get_piece_count() < 6
            # If we are not at the specified depth and there exist more legal moves, go to a lower level
            if (self.__current.child.level < self.__depth + self.__q_depth 
                and self.__current.child._load_legal_captures(self.__tboard) and not useTB):
                self.__current = self.__current.child
                # Score the node to set the stand_pat. Used to evaluate if doing nothing is better than making a capture
                stand_pat = self.__score()
                self.__current._set_legal_captures(self.order_captures(self.__current))
                #self.__transposition_table[self.__tboard.get_zobrist_hash()] = self.__current.score
                self.__current._set_quiescence_values(stand_pat)
            else:
                # If we are at the specified depth or there are no legal moves available,
                #   consider newNode a leaf node then score and return it
                self.__current.child._set_minimax_values(self.__score(tb=useTB))
                self.__transposition_table[self.__tboard.get_zobrist_hash()] = self.__current.child.score
                self.__undo_move()

    # Checks if any captures can possibly improve the position for a given node
    #
    # Parameters:
    #   - node: The Node in Tree whose score to check
    #
    # Returns true if no captures can improve the position false if captures can improve the position
    def __check_delta_cutoff(self, node):
        # The intuition behind delta pruning is to not enter positions where no capture can improve the position
        #   for a given side as doing so would be a waste of time

        # Set DELTA to the highest possible swing of material value (queen value)
        DELTA = 9
        if (node.level % 2 == 0):
            # If node is maximizer check if alpha could be raised by a capture
            return node.score < node.alpha - DELTA
        else:
            # If node is minimzer check if beta could be lowered by a capture
            return node.score > node.beta + DELTA 
        
    # Scores self.__tboard
    #
    # Returns the score of __tboard from board.evaluate or tablebases
    # @profile
    def __score(self, q=False, tb=False):
        # Used at end of method to adjust score for color of the starting position
        turn_adjuster = 1 if self.__starting_turn == TeamColor.WHITE else -1

        # If board has >5 pieces, we are not in tablebase territory so score normally, else use tablebase to score
        if tb:
            self.__tbhits += 1
            # Reset turn_adjuster since tablebase scoring works differently
            turn_adjuster = -1 if self.__starting_turn != self.__tboard.get_turn_color() else 1
            # Get tablebase values for current position
            wdl, dtz = self.__TB.probeTablebase(self.__tboard.get_fen())
            dtz = dtz + self.__tboard.get_half_moves() if dtz > 0 else dtz - self.__tboard.get_half_moves()
            # Get the repeated times (must be at least 1 as the current position is currently on the board)
            # Negate it to be the correct sign for the score
            repeated_times = self.__tboard.get_repeated_times() if dtz > 0 else -self.__tboard.get_repeated_times()
            # Magnify the repeated times to be more significant
            repeated_times *= 30

            # On scoring, TB values must be translated to board evaluation scores for the case where we must 
            #   compare <6 piece positions to >=6 piece positions in minimax
            #
            # Explanation:
            #   For wdl == 0, draw so just set score to 0 and minimax will look for better moves
            #
            #   For abs(wdl) == 1, win/loss but draw under 50 move rule. 
            #       wdl value is multiplied by 1000 so score is higher/lower than any possible board evaluation score 
            #           to incentivize regarding it as a winning/losing option:
            #       Board evaluation can only exist in range -103 >= score <= 103 purely based on material count 
            #           (One side has 9 queens and all other pieces, enemy side has only king)
            #       Under this condition, the winning side wants to minimize dtz to reduce chances of a draw. 
            #           The losing side wants to maximize dtz to increase draw chances
            #       thus, 99900 is divided by dtz and added to the score (abs(dtz) > 100 for wdl == 1 so score will always be in range 1000 > score < 2000). 
            #       This incentivizes choosing lower dtz for the winning side, higher dtz for the losing side
            #
            #       TODO: Consider if this case should just be considered a draw (Just set score to 0), since we assume this is a draw with optimal play
            #
            #   For abs(wdl) == 2, win/loss is guaranteed
            #       wdl value is multiplied by 1000, making it 2000 or -2000, outside the range of score for wdl==1. 
            #       This incentivizes minimax to view the position as a stronger win/loss over wdl==1 positions.
            #       Since for wdl==2, 1 >= abs(dtz) <= 100. 990 is divided by dtz to incentivize lower dtz for winning side, 
            #           higher dtz for losing side(same reasoning as above).
            #       This doesn't help find the fastest mate, since syzgy doesn't include that as a feature anyway, 
            #           but considers the best scoring move to be the one that reduces the most risk of drawing under the 50 move rule.
            if (wdl == 0):
                # Reset the turn adjuster (Won't affect tablebase score of 0)
                turn_adjuster = 1 if self.__starting_turn == TeamColor.WHITE else -1
                # Use normal evaluate if it is better than 0. This incentivizes choosing best move even if it's a tablebase draw
                score = max(0, self.__tboard.evaluate()) if self.__tboard.get_turn_color() == self.__starting_turn else min(0, self.__tboard.evaluate())
            elif (abs(wdl) == 1):
                score = wdl * 1000 + 99900 / (dtz + repeated_times)
            elif (abs(wdl) == 2):
                score = wdl * 1000 + 990 / (dtz + repeated_times)
        elif q:
             # Experimental scoring specifically for quiescence. Not used as it doesn't seem to boost performance
             score = self.__tboard._count_material()
        else:
            # Score normally
            score = self.__tboard.evaluate()
            if abs(score) == self.__board.CHECKMATE_SCORE:
                # If checkmate is found, add large number divided by the current depth being searched
                # This will allow minimax to find the quickest checkmate available
                # This in conjunction with updating max depth using get_depth_to_mate() should lead to much faster checkmates overall
                # Make sure to use score so it subtracts instead of adds when it's black's turn and has chackmate
                score += (score / 10) / (self.__current.child.level if self.__current.child != None else self.__current.level)
        
        return score * turn_adjuster
    
    # Moves a piece on __tboard. Includes log statements for debugging
    #
    # Parameters:
    #   - nextMove: The move to make on __tboard
    def __move(self, nextMove):
        # print()
        # print("Move: " + str(nextMove))
        # print(self.get_current_line())
        res = self.__tboard.move(nextMove)
        # self.__tboard.print_board()

        # Print output if there is an error with tboard.move() for debugging
        if res == False:
            print("Something went wrong with moving")
            print("Move: " + str(nextMove))
            print("Turn: " + str(self.__tboard.get_turn_color()))
            print("Previous Moves: " + str(self.__tboard._previous_moves))
            print("Legal Moves: " + str(self.__tboard.get_all_legal_moves()))
            print("Known Moves: " + str(self.__current._Node__legalMoves))
            print("Current Line: " + self.get_current_line())
            print("Board: ")
            self.__tboard.print_board()
            raise Exception("Move Error")
        self.__nodes_searched += 1
    
    # Undoes a move on __tboard. Includes log statements for debugging
    def __undo_move(self):
        # print()
        # print("Undo Move")
        # print(self.get_current_line())
        res = self.__tboard.undo_move()
        # self.__tboard.print_board()
        if res == False:
            print("Something went wrong with undoing move")
            print("Previous Moves: " + str(self.__tboard._previous_moves))
            print("Turn: " + str(self.__tboard.get_turn_color()))
            print("Current Line: " + self.get_current_line())
            raise Exception("Undo Move Error")
                
    # Getter method for the Tree's root node. Useful for traversing the tree.
    def root(self) -> Node:
        return self.__root
    
    # Getter method for the Tree's depth field.
    def max_depth(self) -> int:
        return self.__depth
    
    # Getter method for the root board
    def board(self) -> Board:
        return self.__board
    
    # Getter for the max nodes
    def max_nodes(self) -> int:
        return self.__node_limit
    
    # Getter for number of nodes searched
    def get_nodes_searched(self) -> int:
        return self.__nodes_searched
    
    # Getter for number of tablebase hits
    def get_tbhits(self) -> int:
        return self.__tbhits

    # Returns the best move found using minimax as a move object
    def best_move(self) -> Move:
        # The strongest move found by the engine will be contained in the root node's best_child field
        best_child = self.root().best_child

        # If the best_child field is not set, that means not enough information has been found to determine the current
        #   best move. The tree has likely only generated the first child from the root.
        # In this case, simply return the current root child being traversed
        if (best_child == None):
            best_child = self.root().child

        # Return the best move
        return best_child.previous_move
    
    # Returns a string representing the best line found by the engine
    def get_best_line(self, ucimode=False) -> str:
        # Begin at the root
        current_node = self.__root
        node_str = "Best line: (root|S:" + str(current_node.score) + "|A:" + str(current_node.alpha) + "|B:" + str(current_node.beta) + ")"
        uci_str = ""

        # Check the best_child field
        best_child = current_node.best_child

        # If there is no best child, traverse down the children until best_child is available
        # Add the current children to the best line string
        while (best_child == None and current_node.child != None):
            current_node = current_node.child
            node_str += " -> (" + str(current_node.previous_move) + "|S:" + str(current_node.score) + "|A:" + str(current_node.alpha) + "|B:" + str(current_node.beta) + ")"
            uci_str += str(current_node.previous_move) + " "
            best_child = current_node.best_child

        # Once best child is found, starting traversing through node best_childs
        #   and adding them to the best line string
        while (best_child != None):
            node_str += " -> (" + str(best_child.previous_move) + "|S:" + str(best_child.score) + "|A:" + str(best_child.alpha) + "|B:" + str(best_child.beta) + ")"
            uci_str += str(best_child.previous_move) + " "
            best_child = best_child.best_child

        return uci_str if ucimode else node_str
    
    # Returns a string representing the current line the engine is searching
    # Includes scores and alpha beta values
    def get_current_line(self, ucimode=False) -> str:
        # Start at root
        curr_node = self.__root
        node_str = "Current line: (root|S:" + str(curr_node.score) + "|A:" + str(curr_node.alpha) + "|B:" + str(curr_node.beta) + ")"
        uci_str = ""
        curr_node = curr_node.child

        # Traverse down tree children until none are left
        while (curr_node != None):
            node_str += " -> (" + str(curr_node.previous_move) + "|S:" + str(curr_node.score) + "|A:" + str(curr_node.alpha) + "|B:" + str(curr_node.beta) + ")"
            uci_str += str(curr_node.previous_move) + " "
            curr_node = curr_node.child

        return uci_str if ucimode else node_str
    
    # Returns the depth where checkmate was found if checkmate was found, None if no checkmate was found
    def get_depth_to_mate(self) -> int:
        if (self.root().score >= self.__board.CHECKMATE_SCORE):
            depth = -1
            current = self.root()
            while (current != None):
                current = current.best_child
                depth += 1
            return depth
        return None
    
    # Returns the current move being searched
    def get_currmove(self) -> Move:
        return self.__current.previous_move if self.__current != None and self.__current.previous_move != None else None
    
    # Gets the current move number (current depth being searched in moves not plies)
    def get_currmovenumber(self) -> int:
        return int(self.__current.level / 2) if self.__current != None else 0
    
    # Gets the best move after the best move is played (The ponder move)
    def ponder_move(self) -> Move:
        pm = self.best_move().best_child
        return pm if pm != None else self.best_move().child.previous_move
    
    # NOTE: For debugging
    # Will return true if a specific move is found in a tree
    # Can be used to print specific tree branches containing certain moves you want to investigate
    # Feel free to change this method depending on whatever you're testing
    def inspect(self, moves: [str]) -> bool:
        current = self.__root.child
        i = 0
        while (current != None and i < len(moves)):
            if (str(current.previous_move) != moves[i]):
                return False
            i += 1
            current = current.child
        return True
    
    # Another debugging function
    # Use to check if certain move is in the tree, regardless of where it's located in the line
    def contains(self, move: Move):
        current = self.__root.child
        while (current != None):
            if (str(current.previous_move) == move):
                return True
            current = current.child
        return False
    
    # Checks if a move is a capture move
    #
    # Returns true if it is a capture move, false otherwise
    def is_capture(self, move: Move) -> bool:
        x1, y1 = move.from_coord.row, move.from_coord.col
        x2, y2 = move.to_coord.row, move.to_coord.col
        if (self.__tboard._board_arr[x1][y1] is not None and self.__tboard._board_arr[x2][y2] is not None):
            return True
        return False
    
    # Move Ordering: 
    # First Hash Moves
    # Hash moves are stored in a transposition table, and are moves that have been searched before
    # Then search for captures using the MVVLA heuristic
    # MVVLA (Most Valuable Victim, Least Valuable Attacker):
    # Find the most valuable victim that can be captured in a position
    # Search in order of the least valuable attacker that can capture the most valuable victim
    # Then search for killer moves
    # Killer moves are moves that have caused a beta cutoff in the past
    # Checkmate killer moves are checked first, then beta cutoff killer moves
    # @profile
    def move_ordering(self, node: Node) -> [Move]:
        # Potential order:
        # Hash moves
        # Mate-killer-moves (checkmates)
        # Winning capture moves (hanging pieces, MVVLVA, Static Exchange Evaluator)
        # Queen captures w/ promotion
        # Queen promotion w/o capture
        # Killer moves (anything that raises the alpha value)
        #   - Moves that should not be considered killer: winning material, good captures, promotions 
        #   - These are considered above and shouldn't be counted double
        # Losing captures

        legal_moves: list[Move] = node._get_legal_moves()
        # Create an empty list to store each type of move and a score associated with the move
        ordered_moves = []
        hash_moves = []
        checks = []
        captures = []
        promotions = []
        other_moves = []

        # Iterate through each move and sort them into their respective lists
        for move in legal_moves:
            # Hash moves
            zobrist_hash = self.__tboard.update_zobrist_hash(move)
            if zobrist_hash in self.__transposition_table:
                # print("REUSED HASH: " + str(zobrist_hash))
                hash_moves.append((move, self.__transposition_table[zobrist_hash]))

            # Checks
            elif self.__tboard.move_causes_check(move):
                if self.is_capture(move):
                    # print('Capture Check: ', move)
                    checks.append((move, 10))
                else:
                    # print('Check: ', move)
                    captures.append((move, 0))

            # MVV/LVA captures
            # If the move is a capture move, get the victim and the attacker and assign a score to the move 
            # based on the MVV/LVA heuristic
            elif self.is_capture(move):
                x1, y1 = move.from_coord.row, move.from_coord.col
                x2, y2 = move.to_coord.row, move.to_coord.col

                victim: Piece = self.__tboard._board_arr[x2][y2]
                attacker: Piece = self.__tboard._board_arr[x1][y1]
                score = self.__tboard.get_piece_value(victim.Type) * 10
                score -= self.__tboard.get_piece_value(attacker.Type)
                if move.promotion is not None:
                    score += self.__tboard.get_piece_value(move.promotion)
                captures.append((move, score))

            # Add promotions, with the material value of the piece being promoted to
            elif move.promotion is not None:
                promotions.append((move, self.__tboard.get_piece_value(move.promotion)))

            # Any other move that doesn't fit into the above categories
            else:
                other_moves.append((move, 0))
            # Killer moves
            # Get king, check if any attacks in attack array
            # If there are no valid moves and the king is in check, it is checkmate
            # If there are no valid moves and there is no check, it is a draw
            # killer_moves = self.killer_moves.get(node.level, [])
            # killer_moves = [move for move in killer_moves if move not in hash_moves and move not in captures]

        # Sort the moves by their score
        hash_moves.sort(key=lambda x: x[1], reverse=True)
        checks.sort(key=lambda x: x[1], reverse=True)
        captures.sort(key=lambda x: x[1], reverse=True)
        promotions.sort(key=lambda x: x[1], reverse=True)

        # Add the moves to the ordered moves list
        ordered_moves = hash_moves + checks + captures + promotions + other_moves
        ordered_moves = [move[0] for move in ordered_moves]

        # print('New Order: ', ordered_moves)

        return ordered_moves

    # Similar to move_ordering() but only for captures. Will assume each move passed into it is a capture without 
    # checking it. Should only be called in quiescence() or any situation where a list of moves is guaranteed to only be captures.
    def order_captures(self, node: Node) -> [Move]:
        legal_moves: list[Move] = node._get_legal_captures()
        hash_moves = []
        checks = []
        captures = []

        for move in legal_moves:
            # Hash moves
            zobrist_hash = self.__tboard.update_zobrist_hash(move)
            if zobrist_hash in self.__transposition_table:
                # print("REUSED HASH: " + str(zobrist_hash))
                hash_moves.append((move, self.__transposition_table[zobrist_hash]))
            # Checks
            elif self.__tboard.move_causes_check(move):
                # print('Capture Check: ', move)
                checks.append((move, 10))
            # MVV/LVA captures
            # If the move is a capture move, get the victim and the attacker and assign a score to the move 
            # based on the MVV/LVA heuristic
            else:
                x1, y1 = move.from_coord.row, move.from_coord.col
                x2, y2 = move.to_coord.row, move.to_coord.col

                victim: Piece = self.__tboard._board_arr[x2][y2]
                attacker: Piece = self.__tboard._board_arr[x1][y1]
                score = self.__tboard.get_piece_value(victim.Type) * 10
                score -= self.__tboard.get_piece_value(attacker.Type)
                if move.promotion is not None:
                    score += self.__tboard.get_piece_value(move.promotion)
                captures.append((move, score))

        #hash_moves.sort(key=lambda x: x[1], reverse=True)
        captures.sort(key=lambda x: x[1], reverse=True)
        ordered_captures = hash_moves + checks + captures
        ordered_captures = [move[0] for move in ordered_captures]
        return ordered_captures
