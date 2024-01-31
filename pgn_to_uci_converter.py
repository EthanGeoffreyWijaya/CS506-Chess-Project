import os
import re
import chess

def get_pgn_file():
    pgn_file = input("Enter the name of the pgn file: ")
    if not os.path.isfile(pgn_file):
        print("File does not exist")
        return None
    return pgn_file

def get_output_file():
    output_file = input("Enter the name of the output file: ")
    if os.path.isfile(output_file):
        print("File already exists")
        get_output_file()
    
    return output_file

def get_pgn_data(pgn_file):
    with open(pgn_file, "r") as f:
        pgn_data = f.read()
    
    return pgn_data

def get_game_data(pgn_data):
    game_data = pgn_data.split("\n\n")
    if len(game_data) < 2:
        print("No games found")
    else:
        game_data = game_data[1]
        game_data = re.sub("\n", " ", game_data)
        game_data = re.sub(" \{.*?\}", "", game_data)
        game_data = re.sub("[0-9]+\. ", "", game_data)
        game_data = re.sub("[0-9]+\... ", "", game_data)
    return game_data

def get_moves(game_data):
    moves = game_data.strip().split(" ")
    moves = [move for move in moves if move != ""]
    if "-" in moves[-1]:
        moves.pop()
    return moves

def algebraic_to_uci(moves):
    board = chess.Board()
    uci_moves = []
    for move in moves:
        uci_moves.append(board.push_san(move).uci())
    return uci_moves

def write_to_file(output_file, uci_moves):
    with open(output_file, "w") as f:
        for move in uci_moves:
            f.write(move + "\n")
    
    print("File written")

def main():
    pgn_file = get_pgn_file()
    while pgn_file == None:
        pgn_file = get_pgn_file()
    # output_file = get_output_file()
    pgn_data = get_pgn_data(pgn_file)
    print("PGN Data:")
    print(pgn_data)
    print()
    game_data = get_game_data(pgn_data)
    print("Game Data:")
    print(game_data)
    print()
    moves = get_moves(game_data)
    print("Moves:")
    print(moves)
    print()
    uci_moves = algebraic_to_uci(moves)
    # write_to_file(output_file, uci_moves)
    print("UCI Moves:")
    print("\n".join(uci_moves))
    print()

if __name__ == "__main__":
    main()