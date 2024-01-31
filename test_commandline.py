import io
from CommandLine import CommandLine

# This class is used to test the CommandLine class. It tests the following methods:
#     - run_command_loop
#     - uci
#     - isready
#     - ucinewgame
#     - position
#     - go
#     - stop
#     - quit
#     - setoption
#     - register
#     - ucinewgame
class TestCommandLine:
    # Tests the run_command_loop method of the CommandLine class. It tests that the uci 
    # command is called when the user types "uci" and that the command loop exits when the user types "quit"
    def test_run_command_loop(self, monkeypatch):
        # Test that the command loop exits when the user types "quit"
        input_str = 'uci\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        assert command_line.run_command_loop() == 0

    # Tests that the run_command_loop method of the CommandLine class works when the user types many commands
    # into the GUI. 
    def test_many_commands(self, capsys, monkeypatch):
        # Test that the command loop outputs the expected output when the user types many commands
        input_str = 'uci\ndebug on\nisready\nsetoption name TestOption value 2\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'readyok' in captured.out

    # Tests that the uci method of the CommandLine class initializes the chess board
    def test_uci_command(self, capsys, monkeypatch):
        # Test that the "uci" command initializes the engine
        input_str = 'uci\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        assert command_line._board != None

    # Tests that the isready method of the CommandLine class prints the expected output
    def test_isready_command(self, capsys, monkeypatch):
        # Test that the "isready" command prints the expected output
        input_str = 'uci\nisready\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'readyok\n' in captured.out

    # Tests that the debug method of the CommandLine class prints the expected output
    def test_debug_on_command(self, capsys, monkeypatch):
        # Test that the "debug on" command prints the expected output
        input_str = 'uci\ndebug on\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'debug - True\n' in captured.out

    # Tests that the ucinewgame method of the CommandLine class prints the expected output
    def test_ucinewgame_command(self, capsys, monkeypatch):
        # Test that the "ucinewgame" command prints the expected output
        input_str = 'uci\nucinewgame\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'readyok\n' in captured.out

    # Tests that the position method of the CommandLine class moves the correct pieces when passed with startpos
    def test_position_command_startpos(self, capsys, monkeypatch):
        # Test that the "position" command prints the expected output
        input_str = 'uci\nposition startpos\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        assert command_line._board.get_fen() == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


    # Tests that the position method of the CommandLine class moves the correct pieces when passed with startpos
    # and a list of moves
    def test_position_command_startpos_with_moves(self, capsys, monkeypatch):
        # Test that the "position" command prints the expected output
        input_str = 'uci\nposition startpos moves e2e4 e7e5\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        assert command_line._board.get_fen() == 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2'

    # Tests that the go method of the CommandLine class prints the expected output
    def test_go_command(self, capsys, monkeypatch):
        # Test that the "go" command prints the expected output
        input_str = 'uci\nposition startpos\ngo depth 2\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'Done generating tree' in captured.out

    # Tests that the go method of the CommandLine class prints the expected output when passed with searchmoves
    # passes one move, this should be considered the best move by the engine
    def test_go_command_with_searchmoves(self, capsys, monkeypatch):
        # Test that the "go" command prints the expected output
        input_str = 'uci\nposition startpos\ngo depth 2 searchmoves e2e4\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'e2e4' in captured.out

    # Tests that the go method of the CommandLine class prints the expected output when given a movetime as a 
    # # time limit
    # def test_go_command_with_movetime(self, capsys, monkeypatch):
    #     # Test that the "go" command prints the expected output
    #     input_str = 'uci\nposition startpos\ngo depth 2 movetime 5\nquit\n'
    #     monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
    #     command_line = CommandLine()
    #     command_line.run_command_loop()
    #     captured = capsys.readouterr()
    #     split_output = captured.out.split('\n')
    #     # Check that the tree is generated in less than 7 seconds (not always exact)
    #     for i in range(len(split_output)):
    #         if 'Tree generated in' in split_output[i]:
    #             assert float(split_output[i].split(' ')[3]) <= 5

    
    # Tests that the stop method of the CommandLine class stops tree generation 
    def test_stop_command(self, capsys, monkeypatch):
        # Test that the "stop" command prints the expected output
        input_str = 'uci\nposition startpos\ngo\nstop\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert command_line._minimax.is_generating() == False

    # Tests that the quit method of the CommandLine class stops tree generation
    def test_quit_command(self, capsys, monkeypatch):
        # Test that the "quit" command prints the expected output
        input_str = 'uci\nposition startpos\ngo depth 3\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert command_line._minimax.is_generating() == False

    # Tests that the setoption method of the CommandLine class prints the expected output
    def test_setoption_command(self, capsys, monkeypatch):
        # Test that the "setoption" command prints the expected output
        input_str = 'uci\nsetoption name TestOption value 2\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'TestOption 2\n' in captured.out

    # Tests that the register method of the CommandLine class prints the expected output
    def test_register_command(self, capsys, monkeypatch):
        # Test that the "register" command prints the expected output
        input_str = 'uci\nregister name Mikkel Hindsbo code 72\nquit\n'
        monkeypatch.setattr('sys.stdin', io.StringIO(input_str))
        command_line = CommandLine()
        command_line.run_command_loop()
        captured = capsys.readouterr()
        assert 'register name:' in captured.out
    