# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from Board import Board, Move, PieceType
from MiniMax import MiniMax
from generateTree import Node
from datetime import datetime
import os
import math

hostName = "localhost"
serverPort = 8080
board: Board = Board()
moveScoresList = []

def write_move_scores_to_file():
    global moveScoresList
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%m-%d-%Y_%H:%M:%S")

    # Create the directory if it doesn't exist
    if not os.path.exists("move_scores"):
        os.makedirs("move_scores")
    
    # Write the move scores to a file
    with open(os.path.dirname(os.path.realpath(__file__)) + os.sep + "move_scores" + os.sep + "move_scores_" + dt_string + ".txt", "w") as file:
        for item in moveScoresList:
            for move, score in item.items():
                file.write(move + ": " + str(score) + "\n")

class MyServer(BaseHTTPRequestHandler):
    best_move = None
    best_score = None
    depth_to_mate = None
    max_depth = 3
    max_q_depth = 5

    def minimax_callback(self, stopped, best_child: Node, depth_to_mate: int):
        self.best_score = best_child.score
        self.best_move = best_child.previous_move
        self.depth_to_mate = depth_to_mate

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        # self.send_header('Access-Control-Allow-Origin', '*')
        # self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        # self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        # self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # self.send_header("Content-Length", str(5))
        # # self.send_header("Content-type", "text/plain")
        # self.end_headers()
    
    def do_GET(self):
        global board
        global moveScoresList
        # Parse the query string
        query_components = parse_qs(self.path[1:])

        print(query_components)
        print(self.path)

        # If the query has a fen, set the board to the fen
        if "fen_str" in query_components:
            fen = query_components["fen_str"][0]
            board = Board(fen)
            if len(moveScoresList) > 0:
                write_move_scores_to_file()
                moveScoresList.clear()
                moveScoresList.append({"ROOT": board.evaluate()})

        print("Old Board: ")
        board.print_board()
        board._print_attack_arr()

        # If the query has a prev_move, move the board
        if "prev_move" in query_components:
            prev_move = query_components["prev_move"][0]
            board.move(Move.from_uci_str(prev_move))
            print("Current Board: ")
            board.print_board()
            board._print_attack_arr()
            moveScoresList.append({prev_move: board.evaluate()})

        # Get the total material captured of the board not including the king values
        starting_material = (16 * Board.get_piece_value(PieceType.PAWN) + 4 * Board.get_piece_value(PieceType.KNIGHT) + 
                             4 * Board.get_piece_value(PieceType.BISHOP) + 4 * Board.get_piece_value(PieceType.ROOK) + 
                             2 * Board.get_piece_value(PieceType.QUEEN))
        total_material = board.get_total_material() - 2 * Board.get_piece_value(PieceType.KING)

        print("Total Material - Kings: " + str(total_material))
        print("Starting Material: " + str(starting_material))
        print("Total Material: " + str(board.get_total_material()))
        print("Log2 of Total Material: " + str(math.log2(total_material)))
        print("Log2 of Starting Material: " + str(math.log2(starting_material)))
        print("Log2 of Starting Material - Total Material: " + str(2 * math.floor(math.log(starting_material, 4) - math.log(total_material, 4))))

        # Increase the depth as the total material decreases
        new_max_depth = self.max_depth + (2 * math.floor(math.log(starting_material, 4) - math.log(total_material, 4)))

        print("new_max_depth: " + str(new_max_depth))
        print("max_depth: " + str(self.max_depth))

        # Generate the minimax tree
        minimax = MiniMax(board, new_max_depth, q_depth=self.max_q_depth)
        event = minimax.run(self.minimax_callback)
        # Wait for the tree to finish generating
        event.wait()

        print("Best Move: " + str(self.best_move))
        print("Best Score: " + str(self.best_score))
        # Set a new max depth if checkmate is found. depth_to_mate is the depth where mate was found 
        # Subtract depth_to_mate by 2 to account for enemy playing their turn, then it being the engine's turn again
        self.max_depth = self.depth_to_mate - 2 if self.depth_to_mate != None else self.max_depth

        # Move the board to the best move
        board.move(self.best_move)
        print("New Board: ")
        board.print_board()
        board._print_attack_arr()
        moveScoresList.append({str(self.best_move): {"Eval": board.evaluate(), "Minimax": str(self.best_score), "Best Line": minimax.get_best_line()}})

        self.send_response(200)
        self.send_GET_headers()
        self.wfile.write(bytes(str(self.best_move), "utf-8"))

    # Sends the headers for a GET request
    def send_GET_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-type", "text/plain")
        self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")