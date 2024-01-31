from generateTree import Tree
from Board import *
from threading import Thread, Event, Timer
import time
from typing import Callable

# Author: Alex Arovas

# UCI COMMANDLINE INTEGRATION:
#   - go: Call run() to generate MiniMax in its normal search mode. Will stop search when max_depth reached
#   - go ponder: Call ponder() to generate MiniMax in ponder mode. 
#       - Call ponderhit() to initiate a ponderhit
#       - Call stop() to stop search (Pondermiss)
#       - NOTE: Best to call ponder with some time constraints when testing. Upon ponderhit, will run until the current tree 
#           is done generating, or time constraint reached. If the current tree has a high depth, might take a long time.
#   - go infinite: Call run_infinite() to generate Minimax in infinite mode. Will only stop when stop() is called
#
#   - go searchmoves: Initialize MiniMax with the searchmoves argument, or set searchmoves with the setter and generate
#   - go wtime: Initialize MiniMax with wtime argument, or set wtime with setter and generate
#   - go btime: Initialize MiniMax with btime argument, or set btime with setter and generate
#   - go winc: Initialize MiniMax with winc argument, or set winc with setter and generate
#   - go binc: Initialize MiniMax with binc argument, or set binc with setter and generate
#   - go movestogo: Initialize MiniMax with movestogo argument, or set movestogo with setter and generate
#   - go mate: Initialize MiniMax with mate argument, or set mate with setter and generate
#   - go movetime: Initialize MiniMax with movetime argument, or set movetime with setter (set_time_limit()) and generate
#
#   - go depth: Initialize MiniMax with the desired depth, or call change_board_or_max_depth() with depth argument to change depth
#   - go nodes: Initialize MiniMax with the desired nodes, or call change_board_or_max_depth() with node argument to change nodes
#   - NOTE: change_board_or_max_depth() will call run() immediately after completing
#
#   ENGINE TO GUI
#   - info: call info(). Will return a dict with every possible parameter with the exception of stuff that doesn't apply. 
#       Simply select which ones we want to show. Example info()['depth']
#   - bestmove[ponder]: use callback function. Returns [search stopped: bool, best_child: Node, depth mate found: int]
#       To get ponder move: best_child.best_child. if null, best_child.child

# Class for running the minimax algorithm on a board
class MiniMax:
    __generate_thread: Thread # Used to join the thread that generates the minimax tree
    __inf_generate_thread: Thread # Used to join the thread that generates the tree generation loop
    __callback_function: Callable[[bool, str, int], None] = None # The function to call when the minimax tree is done generating and scoring
    __callback_function_inf: Callable[[bool, str, int], None] = None
    __start_time: float
    __event: Event # Used to wait for the tree to finish if necessary
    __timer: Timer = None # Used to stop generating after a certain time limit
    ESTIMATED_MOVES_UNTIL_GAME_END = 40
    TIME_PADDING = 0.05 # Used to make sure timer is stopped <= to the time specified instead of being a few milliseconds over.

    # Creates a new MiniMax object
    #
    # TODO: See if some of the parameters can be accessable in the Tree class so they don't need to be saved here
    # Ex: __max_depth and __board (__board is technically accessable as __tree.root().board)
    # TODO: Speak with Ethan about consisitent naming to see what we want to name everything (ex: position vs board)
    #
    # Parameters:
    # board: the root to generate the minimax tree from
    # max_depth: limit the depth of the minimax tree
    # searchmoves: a list of moves to search for (default value is None - search all moves)
    def __init__(self, board: Board, max_depth: int, movetime: float = None, q_depth: int = 5, searchmoves: [Move] = None, 
                 node_limit: float = float('inf'), wtime: float = None, btime: float = None, movestogo: int = None,
                 winc: float = 0, binc: float = 0, mate: int = None) -> None:
        # Set stop to false so the tree will generate
        self.__stop: bool = False
        self.__stoploop: bool = False
        # Set generating to false as the tree is not generating yet
        self.__generating: bool = False
        # Set to false as the tree is not generating infinitely or pondering yet
        self.__generating_infinite: bool = False
        self.__pondering: bool = False
        # Create the minimax tree object (not generating the tree yet)
        self.__tree: Tree = Tree(root=board, depth=max_depth, q_depth=q_depth, searchmoves=searchmoves, nodes=node_limit)
        # Set the searchmoves of the tree
        self.__searchmoves = searchmoves
        # Set the q_depth of the tree
        self.__q_depth = q_depth

        # Other uci related fields
        self.__movestogo: int = movestogo
        self.__wtime: float = wtime
        self.__btime: float = btime
        self.__winc: float = winc
        self.__binc: float = binc
        self.__time_limit: int = movetime
        self.__mate: int = mate * 2 if mate != None else mate

    # Setter for time limit
    def set_time_limit(self, time_limit: int):
        self.__time_limit = time_limit
        
    # Setter for movestogo
    def set_movestogo(self, movestogo: int):
        self.__movestogo = movestogo

    # Setter for white's time
    def set_wtime(self, wtime: float):
        self.__wtime = wtime

    # Setter for black's time
    def set_btime(self, btime: float):
        self.__btime = btime

    # Setter for white's increment
    def set_winc(self, winc: float):
        self.__winc = winc

    # Setter for black's increment
    def set_binc(self, binc: float):
        self.__binc = binc

    # Setter for depth of mate to search for
    def set_mate(self, mate: int):
        self.__mate = mate * 2 if mate != None else mate

    # Setter for searchmoves list
    def set_searchmoves(self, searchmoves: [Move]):
        self.__searchmoves = searchmoves

    # Returns the time passed since self.__start_time was set
    def get_time_elapsed(self):
        return (time.time() - self.__start_time) * 1000
    
    # Returns the average nodes searched per second
    def get_nps(self):
        return self.__tree.get_nodes_searched() / self.get_time_elapsed()

    # Used for Engine to UCI info output
    def info(self):
        return {'depth': self.__tree.max_depth(),
                'seldepth': self.__tree.max_depth() + self.__q_depth,
                'time': self.get_time_elapsed(),
                'cp': self.__tree.root().score * 100 if abs(self.__tree.root().score) != float('inf') else 0,
                'mate': self.__tree.get_depth_to_mate(),
                'currmove': self.__tree.get_currmove(),
                'currmovenumber': self.__tree.get_currmovenumber(),
                'nodes': self.__tree.get_nodes_searched(),
                'nps': self.get_nps(),
                'tbhits': self.__tree.get_tbhits(),
                'pv': self.__tree.get_best_line(ucimode=True),
                'currline': self.__tree.get_current_line(ucimode=True)}


    # Runs Minimax on the tree using a different thread. The minimax tree will stop generating and scoring when the 
    # stop() method is called or when the max depth is reached. 
    # Then minimax will run the minimax algorithm on the generated tree.
    #
    # Parameters:
    # callback: The function to call when the minimax tree is done generating and scoring (default value is None - No callback)
    #           The callback function should take three parameters: 
    #               stopped: a boolean that is true if the tree was stopped before it finished generating and scoring
    #               best_child: the best node that is child of the root according to minimax's score
    #               depth_to_mate: if checkmate, the number of plies to reach it. None if no checkmate
    #               ponder
    # 
    # NOTE: Callback is used even if stopped
    def run(self, callback: Callable[[bool, str, int], None]|None = None) -> Event:
        # Create the thread that will run __generate_tree() to generate the minimax tree
        thread = Thread(target=self.__generate_tree)
        # Assign the thread to the __generate_thread field so it can be joined later
        self.__generate_thread = thread
        # Assign the callback function to the __callback_function field so it can be called later
        self.__callback_function = callback
        # Create the event that will be returned so program can wait for the tree to finish generating if necessary
        self.__event = Event()
        self.__stop = False
        # Start the thread and timer
        thread.start()
        self.__set_time()
        self.__start_time = time.time()
        # Return the event
        return self.__event
    
    # Used for UCI go infinite
    # Should not be called with any time limit
    def run_infinite(self, callback: Callable[[bool, str, int], None]|None = None):
        thread = Thread(target=self.run_loop)
        self.__inf_generate_thread = thread
        self.__stop = False
        self.__stoploop = False
        self.__callback_function_inf = callback
        thread.start()
        self.__start_time = time.time()

    # Runs a loop of minimax searches
    # Will increase the max_depth with every iteration
    # Will only be stopped when stop() is called
    def run_loop(self):
        self.__generating_infinite = True
        max_depth = self.__tree.max_depth()
        best_child = None
        old_best_child = None

        while (not self.__stoploop):
            old_best_child = best_child
            if not self.__stop: self.__tree = Tree(self.__tree.board(), max_depth)
            thread = Thread(target=self.__generate_tree)
            self.__generate_thread = thread
            self.__event = Event()
            thread.start()
            thread.join()

            best_child = self.__tree.root().best_child if self.__tree.root().best_child != None else self.__tree.root().child
            max_depth += 1

        if (old_best_child.score > best_child.score):
            best_child = old_best_child
        
        if (self.__callback_function_inf != None):
            self.__callback_function_inf(self.__stoploop and self.__stop, best_child, self.__tree.get_depth_to_mate())

    # UCI ponder command
    # Just calls run_infinite but can be terminated with the unique function ponderhit()
    def ponder(self, callback: Callable[[bool, str, int], None]|None = None):
        self.__pondering = True
        self.run_infinite(callback)

    # Sets the timer from which to stop running depending on user defined parameters
    def __set_time(self):
        # Set the time limit to the user defined time limit
        time_limit = self.__time_limit
        # If user did not provide a time limit, compute other conditions
        if (time_limit == None):
            divider = self.__movestogo if self.__movestogo is not None else self.ESTIMATED_MOVES_UNTIL_GAME_END

            if (self.__tree.board().get_turn_color() == TeamColor.WHITE):
                if (self.__wtime == None): return
                total_incr = self.__winc * divider if self.__winc != None else 0
                time_limit = (self.__wtime + total_incr) / divider
            else:
                if (self.__btime == None): return
                total_incr = self.__binc * divider if self.__binc != None else 0
                time_limit = (self.__btime + total_incr) / divider
                
        # Subtract time limit by set amount of padding to account for threads closing slightly later than the set time
        # Ensure a lower bound for the time limit to ensure no negative time limits
        time_limit /= 1000
        time_limit = time_limit - self.TIME_PADDING if time_limit - self.TIME_PADDING >= 0.1 else 0.1
        
        timer = Timer(time_limit, self.stop)
        self.__timer = timer
        timer.start()
    
    # Private method that starts generating the minimax tree and scoring nodes on a separate thread. This method is 
    # called by the run() method. To stop use the stop() method or the program will stop when max depth is reached.
    def __generate_tree(self) -> None:
        # Set the stop flag to false so the tree can start generating and scoring
        #self.__stop = False
        # Starting generating tree to set __generating to true
        self.__generating = True
        # Get the first node to score (so while loop works as intended)
        nodes_left = self.__tree.next()

        start_time = time.time()
        # Print to show that the tree is generating
        print("Generating tree...")
        # If not stopped and another node is available then score the node
        while (not self.__stop and nodes_left):
            nodes_left = self.__tree.next()
            if (not self.__pondering and self.__mate != None and self.__tree.get_depth_to_mate() != None 
                and self.__tree.get_depth_to_mate() <= self.__mate):
                break
        
        # Call the callback function
        best_child = self.__tree.root().best_child
        if (self.__callback_function != None):
            self.__callback_function(self.__stop, best_child if best_child != None else self.__tree.root().child, self.__tree.get_depth_to_mate())

        # Stop the event to signify that the tree is done generating
        self.__event.set()
        # Stop the timer if still running
        if (self.__timer != None): self.__timer.cancel()

        # self.print_tree()
        # print()
        # self.print_best_line()
        # print()
        # self.__tree.board().get_fen()

        # Print to show that the tree is done generating
        print("Done generating tree")
        print("Tree generated in " + str(time.time() - start_time) + " seconds")

    # Stops the minimax tree from generating and scoring. The tree will stop generating and scoring the minimax nodes
    # in the tree. Then it will generate the best result from the minimax tree and return it.
    def stop(self) -> Move:
        # If the tree is generating stop it and get the best move
        if self.__generating and not self.__generating_infinite:
            # Set the stop flag to true so the tree will stop generating and scoring
            self.__stop = True
            # Join the thread that is generating the tree so the tree will be generated before the best move is returned
            self.__generate_thread.join()
            # Stop the timer if running
            if (self.__timer != None): self.__timer.cancel()
            # No longer generating to set __generating to false
            self.__generating = False

            return self.__tree.best_move()
        elif self.__generating_infinite:
            self.__stop = True
            self.__stoploop = True

            self.__generate_thread.join()
            self.__inf_generate_thread.join()

            self.__generating = False
            self.__generating_infinite = False
            self.__pondering = False

            return self.__tree.best_move()
        else:
            return None
        
    # Upon ponderhit, stop the infinite loop but not the normal tree generation so that minimax won't search at another max_depth
    # Also call set_time() since we are now entering normal search and time constraints must be considered
    def ponderhit(self):
        if (not self.__pondering): return
        self.__pondering = False
        self.__stoploop = True
        self.__set_time()
        
    # Change the board and/or max_depth to generate the minimax tree from
    #
    # Parameters:
    # board: the board to generate the minimax tree from - NOTE: if None (default value) keep the current board
    # max_depth: the max depth of the minimax tree - NOTE: if None (default value) keep the current max depth
    #
    # NOTE: If generating, it will reset the current minimax tree generating and scoring. The tree will re-generated and re-scored
    # except if both board and max_depth stay the same as the tree will not change.
    def change_board_or_max_depth(self, board: Board = None, max_depth: int = None, max_nodes: int = None) -> None:
        # If board is default value of None keep the board the same
        if (board == None):
            board = self.__tree.board()
        # If max_depth is default value of None keep the max_depth the same
        if (max_depth == None):
            max_depth = self.__tree.max_depth()
        # If max nodes is default value of None keep max_nodes the same
        if (max_nodes == None):
            max_nodes = self.__tree.max_nodes()

        # If the board and the max_depth are the same don't change the tree as it will be the same but would restart the 
        # generation / scoring if generating
        if (board == self.__tree.board() and max_depth == self.__tree.max_depth() and max_nodes == self.__tree.max_nodes()):
            return
        else:
            # Sets the tree to a new tree with the new board
            self.__tree = Tree(root=board, depth=max_depth, nodes=max_nodes, q_depth=self.__q_depth, searchmoves=self.__searchmoves)
            # restart the tree generation and scoring if generating
            self.__restart_generation()

    # Private method that restarts the minimax tree generation and scoring
    # Used when the tree was changed while generating the tree
    # 
    # NOTE: If not generating then this method does nothing
    # NOTE: Different than stop() and then run() as stop() will take the time to run minimax on the generated tree
    def __restart_generation(self) -> None:
        # If the tree is generating then stop it
        if (self.__generating):
            # Set the stop flag to true so the tree will stop generating and scoring
            self.__stop = True
            # Join the thread that is generating the tree so the tree will be generated before the best move is returned
            self.__generate_thread.join()
            # No longer generating to set __generating to false
            self.__generating = False
        # Start generating the tree again
        self.run()
    
    # NOTE: For the demo and testing
    # Prints whatever is currently contained in the minimax tree. 
    # Can be used to print the current line that the engine is checking
    def print_tree(self):
        print(self.__tree.get_current_line())

    # NOTE: For testing with the demo file
    # Prints the best move sequence according to minimax
    def print_best_line(self): 
        print(self.get_best_line())
        print("Nodes searched: " + str(self.__tree.get_nodes_searched()))
        print("Depth: " + str(self.__tree.max_depth()))

    # Gets the best line according to minimax
    def get_best_line(self):
        return self.__tree.get_best_line()

    def print_transposition_table(self):
        self.__tree.print_t_table()

    # Returns true if the minimax tree is still generating, false if it is done generating
    def is_generating(self) -> bool:
        return self.__generating
    