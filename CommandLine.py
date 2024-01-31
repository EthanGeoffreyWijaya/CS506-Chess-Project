from Board import Board, Move
from MiniMax import MiniMax
from generateTree import Node
from Connect2DB import Connect2DB
from OpeningBook import OpeningBook

# The CommandLine class is used as a GUI to communicate with the chess engine. The CommandLine class will process 
# the commands and send them to the engine for the appropriate action.
class CommandLine:
    # Initializes the CommandLine class. The CommandLine class will be used to communicate with the chess engine.
    def __init__(self):
        # Initialize the engine options here
        # engine_options = ...
        # Initialize the engine here with the given options
        # engine = ...
        # TODO: Add connection to the engine here (Cameron)
        # self.board: Board = Board()
        self._board: Board = None
        self._minimax: MiniMax = None
        self._OpenBook: OpeningBook = None
        self._Bool_OpeningBook: bool = True
        self.__depth = 3
        self.__event = None
        self.__code = None
        self.__name = None
        self.__id_opening_book = -1

    # Executes the main command loop, which goes until the user types "quit" 
    def run_command_loop(self):
        
        # Wait for the user to type 'uci' before initializing the engine
        next_command = ''
        while (True):
            next_command = input()
            if (next_command == 'uci'):
                self.uci()
                break
            if (next_command == 'quit'):
                return 0
        
        # Run the command loop until the user types 'quit'
        while (next_command != 'quit'):
            next_command = input()
            self.process_command(next_command)

        return 0
    
    # Tells the engine to switch to UCI mode. The engine then must identify itself and send the 
    # options command, telling the GUI which settings it supports. The engine also should send "uciok" 
    # or the engine will be killed by the GUI.
    def uci(self):
        # Print the options to the GUI
        # TODO: Launch the engine with the correct settings
        # 5 as the default depth for now, can always change later.
        self._board = Board() 
        self._OpenBook = OpeningBook(self._board)
        self._minimax = MiniMax(self._board, self.__depth)
        self.MYSQLDB = Connect2DB()
        print('id name 4Pawns')
        print('id author 4Pawns')
        print('uciok')

    # Switches the debug mode for the engine on or off. While debugging, the engine sends additional 
    # info to the GUI to help debugging. This mode is off by default, but can be turned on at any time.
    def debug(self, turn_on):
        # Don't know what to do here, maybe output some info? Like PV, evaluation, etc
        print('debug - ' + str(turn_on))
        return 0
    
    # Synchronizes the engine and the GUI.
    def isready(self):
        # Prints readyok whenever the engine is ready to accept extra commands
        print('readyok')

    # Allows the user to change the internal parameters of the engine. Given the name of the option, 
    # set a new value. 

    # Parameters:
    #   name: specifies the option to be changed
    #   value: specifies the new value of the option
    def setoption(self, name, value):
        print(name, value)
        return 0
    
    # Registers the engine's name nad code with the GUI or tells the GUI that the engine will be
    # registered later. This command should always be sent if the engine has sent "registration error"
    # during program startup.
    #
    # @PARMS:
    #     later: the user doesn't want to register the engine now.
    #     name: the engine should be registered with this name.
    #     code: the engine should be registered with this code.
    #
    # Returns 0 is not registered, 1 if registered.
    # NOTE: return boolean value will be used when finding engine id.

    # if user choose later, then return 0
    def register(self, later=False, name=None, code=None):
        if (later):
            # print registration later and return
            print('register - later')
        # else if user choose to register the engine now, then register the engine
        else:
            try:
                # run sql statement
                SQLStmt = "INSERT INTO engine(EngineCode, Username) VALUES (%s, %s)"

                # execute, commit, and close connection to sql db
                self.MYSQLDB.cursor.execute(SQLStmt, (code, name))

                self.__code = code
                self.__name = name

                # print number of rows affected
                print(f"{self.MYSQLDB.cursor.rowcount} row(s) affected.")

                # get primary key (for access to this row)
                # pk = self.MYSQLDB.cursor.lastrowid

            # catch exception
            except Exception as e:
                print(f"Error: {e}")

            # commit and close connection
            self.MYSQLDB.conn.commit()

            # print registration complete
            print(f"register name: {name} engine code: {code}")

    # Resets the board position to its default value, starting a new game. This command should be sent
    # before the first "position" command. This method will always send the "isready" command before 
    # executing, to wait for the engine to finish any previous commands.
    def ucinewgame(self):
        print(self.__name, self.__code)
        if self.__name is not None and self.__code is not None:
            fen = self._board.get_fen()
            move_history = self._board.get_previous_moves_as_str()
            self.MYSQLDB.set_History(move_history, fen, self.__name, self.__code, self.__id_opening_book)
        self._Bool_OpeningBook = True
        self._board.reset_board()
        self.isready()

    # Set up the position described in fenstring on the internal board and play the given moves on the 
    # internal chess board. If startpos is sent, play from the start position. If this differs from the 
    # current positon, the GUI must send the ucinewgame command first. After that set up the position. 
    
    # Parameters:
    #   startpos: the position is set up from the start position
    #   moves: a list of moves to play on the internal chess board
    def position(self, startpos: bool=False, moves: str=None, fen: str=None):
        if startpos:
            self._board = Board()
            self._Bool_OpeningBook = True
        elif fen:
            self._board = Board(fen)
            opening_res = self._OpenBook.compare_Fen(self._board.get_fen())
            if opening_res == None:
                self._Bool_OpeningBook = False
            else:
                self._Bool_OpeningBook = True
                self.__id_opening_book = opening_res[0][0]
        if moves:
            opening_res = self._OpenBook.compare_Fen(self._board.get_fen())
            for move in moves.split(' '):
                self._board.move(Move.from_uci_str(move))
                opening_res = self._OpenBook.compare_Fen(self._board.get_fen())
                if opening_res != None and opening_res[0] != None:
                    self.__id_opening_book = opening_res[0][0]
            
            if (opening_res == None):
                self._Bool_OpeningBook = False
            else:
                self._Bool_OpeningBook = True

    # Start calculating the best move in the current positon given with the "position" command. There are
    # many commands which can be used with this command, all of which will be sent in the same line.
    # Only specified commands should influence the search.

    # Parameters:
    #   searchmoves: restrict search to this moves only
    #   ponder: start searching in pondering mode (more details here)
    #   wtime: white has wtime ms left on the clock
    #   btime: black has btime ms left on the clock
    #   winc: white increment per move in ms if wtime is used
    #   binc: black increment per move in ms if btime is used
    #   movestogo: there are movestogo moves to the next time control, only sent if movestogo > 0.
    #              Otherwise, white and black are in sudden death
    #   depth: search x plies only
    #   nodes: search x nodes only
    #   mate: search for a mate in x moves
    #   movetime: search exactly x ms
    #   infinite: search until the "stop" command. Do not exit the search without being told so in this mode
    def go(self, searchmoves: [Move] = None, ponder=False, wtime: float = None, btime: float = None, winc: float = None,
           binc: float = None, movestogo: int = None, depth: int = 3, nodes: float = float('inf'), mate: int = 0, movetime: float = 0,
            infinite=False):  
        
        print(f"BoolOP: {self._Bool_OpeningBook}")
        
        if self._Bool_OpeningBook:
            id_opening_book, open_move = self._OpenBook.play_Opening_book(self._board)
            if open_move is None:
                self._Bool_OpeningBook = False
            else:
                self.__id_opening_book = id_opening_book
                # print('book id', id_opening_book)
                print('bestmove', open_move)
        if not self._Bool_OpeningBook:
            if ponder:
                self._minimax = MiniMax(self._board, depth, movetime=movetime, searchmoves=searchmoves, node_limit=nodes,
                                        wtime=wtime, btime=btime, winc=winc, binc=binc, movestogo=movestogo, mate=mate,)
                self._minimax.ponder(self.minimax_callback)
            elif infinite:
                self._minimax.run_infinite(self.minimax_callback)
            else:
                # Convert the string of moves to Move objects
                if searchmoves is not None:
                    searchmoves = [Move.from_uci_str(move) for move in searchmoves]
                    
                self._minimax = MiniMax(self._board, depth, movetime=movetime, searchmoves=searchmoves, node_limit=nodes,
                                        wtime=wtime, btime=btime, winc=winc, binc=binc, movestogo=movestogo, mate=mate,)

                self.__event = self._minimax.run(self.minimax_callback)

    # Stops the engine calculating as soon as possible
    def stop(self):
        self._minimax.stop()
        # self._minimax.print_best_line()

    # This is used to find the best move the engine has found so far.  
    def minimax_callback(self, stopped, best_child: Node, depth_to_mate: int):
        self.best_score = best_child.score
        self.best_move = best_child.previous_move
        self.depth_to_mate = depth_to_mate
        print('bestmove', self.best_move)

        self.show_info()

    # This is executed when the user has played the expected move. This will be sent if the engine was told
    # to ponder on the same move the user has played. The engine should continue searching but switch from
    # pondering to normal search.
    def ponderhit(self):
        self._minimax.ponderhit()     

    # Get a dict of all the search info
    def show_info(self):
        info = self._minimax.info()
        print("depth", info['depth'], "score cp", info['cp'], "time", info['time'], "nodes", info['nodes'], 
              "nps", info['nps'], "currmove", info['currmove'], "currmovenumber", info['currmovenumber'], "currline", info['currline'], "pv", info['pv'])

    # Takes in a command and executes the correct function based on the command.

    # Parameters:
    #   command: a string representation of the command to be executed
    def process_command(self, command):
        command_list = command.split(' ')

        match command_list[0]:
            case 'debug':
                if ('on' in command_list):
                    self.debug(True)
                else:
                    self.debug(False)
            
            case 'isready':
                self.isready()

            case 'setoption':
                if ('name' in command_list and 'value' in command_list):
                    # Find the indices of the name and value, then join the strings between them
                    # to create a single string for the name and value
                    start_index = command_list.index('name')
                    end_index = command_list.index('value')
                    self.setoption(name=' '.join(command_list[start_index+1:end_index]), 
                            value=' '.join(command_list[end_index+1:]))
                
            case 'register':
                if ('later' in command_list):
                    self.register(later=True)
                else:
                    # Find the indices of the name and cpde, then join the strings between them
                    # to create a single string for the name and code 
                    start_index = command_list.index('name')
                    end_index = command_list.index('code')
                    self.register(name=' '.join(command_list[start_index+1:end_index]), 
                            code=int(' '.join(command_list[end_index+1:])))
                    
            case 'ucinewgame':
                self.ucinewgame()

            case 'position':
                startpos = False
                if ('startpos' in command_list):
                    startpos = True
                if ('moves' in command_list):
                    idx = command_list.index('moves')
                    if (not startpos and command_list[1] != 'moves'):
                        fen = ' '.join(command_list[1:idx])
                        self.position(startpos=startpos, moves=' '.join(command_list[idx+1:]), fen=fen)
                    else:
                        self.position(startpos=startpos, moves=' '.join(command_list[idx+1:]))
                elif (not startpos):
                    fen = ' '.join(command_list[1:])
                    self.position(startpos=startpos, fen=fen)

            case 'go':
                cmd_dict = {'searchmoves':None, 'ponder':False, 'wtime':None, 'btime':None, 'winc':None, 'binc':None, 
                                'movestogo':None, 'depth':3, 'nodes':float('inf'), 'mate':None, 'movetime':None, 'infinite':False}
                for i in range(1, len(command_list)):
                    # Run through each command and check for any of the keywords found in the dictionary
                    if (command_list[i] in cmd_dict.keys()):
                        # If the keyword is found, parse the input after it appropriately using a match statement
                        param = command_list[i]
                        match param:
                            case 'searchmoves':
                                # If the searchmoves keyword is found, parse the moves after it into a single list
                                moves = []
                                i += 1
                                while (i < len(command_list) and command_list[i] not in cmd_dict.keys()):
                                    moves.append(command_list[i])
                                    i += 1
                                cmd_dict[param] = moves
                        
                            case 'ponder':
                                cmd_dict[param] = True
                            
                            case 'infinite':
                                cmd_dict[param] = True
                            
                            case _:
                                cmd_dict[param] = int(command_list[i+1])

                # print(cmd_dict)
                self.go(searchmoves=cmd_dict['searchmoves'], ponder=cmd_dict['ponder'], wtime=cmd_dict['wtime'],
                        btime=cmd_dict['btime'], winc=cmd_dict['winc'], binc=cmd_dict['binc'], 
                        movestogo=cmd_dict['movestogo'], depth=cmd_dict['depth'], nodes=cmd_dict['nodes'],
                        mate=cmd_dict['mate'], movetime=cmd_dict['movetime'], infinite=cmd_dict['infinite'])
                
            case 'stop':
                self.stop()

            case 'ponderhit':
                self.ponderhit()

            case 'quit':
                if self._minimax.is_generating():
                    self._minimax.stop()
                return 0
            
            case _:
                print('Invalid input')

        return 0
    

if __name__ == "__main__":
    command_line = CommandLine()
    command_line.run_command_loop()