import pytest
from generateTree import Tree, Node
from Board import Board, Move
import copy

# Tests node initialization values
def test_node_constructor():
    parent1 = None
    # Test initializing root node
    node = Node(parent1)

    # Check proper field initialization values
    assert node.parent == parent1
    assert node.level == 0
    
    # Test initializing child node
    node2 = Node(node)
    
    assert node2.parent == node
    assert node2.level == 1

# Tests node methods load_legal_moves and nextmoves
def test_node_load_legal_moves():
    node = Node(None)
    
    # There should be only eight legal moves
    node._load_legal_moves(Board('3k4/8/1p6/2p5/1P6/2P5/8/3K4 w - - 0 1'))
    m1 = []
    m1.append(node._next_move())
    m1.append(node._next_move())
    m1.append(node._next_move())
    m1.append(node._next_move())
    m1.append(node._next_move())
    m1.append(node._next_move())
    m1.append(node._next_move())
    m1.append(node._next_move())
    
    # Check if there are no more legal moves
    assert node._next_move() == None
    # Check if legal moves are correct 
    assert Move.from_uci_str('c3c4') in m1
    assert Move.from_uci_str('b4b5') in m1
    assert Move.from_uci_str('b4c5') in m1
    assert Move.from_uci_str('d1c1') in m1
    assert Move.from_uci_str('d1c2') in m1
    assert Move.from_uci_str('d1d2') in m1
    assert Move.from_uci_str('d1e2') in m1
    assert Move.from_uci_str('d1e1') in m1

# Tests tree initialization values
def test_tree_constructor():
    board = Board('3k4/8/1p6/2p5/1P6/2P5/8/3K4 w - - 0 1')
    tree = Tree(board, 3)
    
    # Check if the root is properly initialized
    assert tree.board() == board
    # Check if the root's legal moves are initialized
    # There should be only eight legal moves
    m1 = []
    m1.append(tree.root()._next_move())
    m1.append(tree.root()._next_move())
    m1.append(tree.root()._next_move())
    m1.append(tree.root()._next_move())
    m1.append(tree.root()._next_move())
    m1.append(tree.root()._next_move())
    m1.append(tree.root()._next_move())
    m1.append(tree.root()._next_move())
    
    assert tree.root()._next_move() == None
    assert Move.from_uci_str('b4b5') in m1
    assert Move.from_uci_str('c3c4') in m1
    assert Move.from_uci_str('b4c5') in m1
    assert Move.from_uci_str('d1c1') in m1
    assert Move.from_uci_str('d1c2') in m1
    assert Move.from_uci_str('d1d2') in m1
    assert Move.from_uci_str('d1e2') in m1
    assert Move.from_uci_str('d1e1') in m1
    
# Tests tree next() method and if a proper tree is generated
def test_tree_next():
    max_depth = 3
    moves = [0] * int(max_depth + 1)
    tree = Tree(Board('3k4/8/8/8/8/8/8/3K4 w - - 0 1'), max_depth)
    
    nextNode = tree.next()
    while (nextNode):
        # Check if the newly created leaf node is at the proper depth
        #   and that children are populated
        #check_depth(tree.root(), max_depth, 0)
        
        # Check if every legal move is represented by a tree node
        check_moves(copy.deepcopy(tree.board()), tree.root(), moves)

        nextNode = tree.next()

# Traverses the tree to every leaf node and checks if it is at the proper depth
def check_depth(node, depth, level):
    assert node.level == level
    if (node.child == None):
        assert level == depth
        return

    check_depth(node.child, depth, level + 1)
        
# Checks if tree children are accurate to parent legal moves
def check_moves(startboard : Board, node : Node, moves : list):
    if (node.child == None):
        return
    
    moves[node.level] = startboard.get_all_legal_moves()

    assert node.child.previous_move in moves[node.level]
    startboard.move(node.child.previous_move)
    moves[node.level].remove(node.child.previous_move)
    
    check_moves(startboard, node.child, moves)