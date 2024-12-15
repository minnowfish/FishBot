from movegen import generate
from eval import eval

class Node:
    def __init__(self, field, piece, score, moves=None, hold=None):
        self.field = field
        self.piece = piece
        self.score = score
        self.initial_moves = moves if moves is not None else []
        self.hold = hold

class Layer:
    def __init__(self):
        self.nodes = []

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def add(self, key, score):
        self.table[key] = score

    def is_better(self, key, score):
        return key not in self.table or self.table[key] < score

def beam_search(initial_field, initial_piece, queue, piece_held):
    DEPTH = 3
    WIDTH = 15

    layers = [Layer() for _ in range(DEPTH + 1)]
    trans_table = TranspositionTable()
    initial_node = Node(initial_field, initial_piece, 0)
    layers[0].nodes.append(initial_node)

    for d in range(DEPTH):
        next_piece = queue[d]
        next_layer_nodes = []

        for node in layers[d].nodes:
            next_moves = generate(node.field, node.piece)
            for move in next_moves:
                initial_moves = node.initial_moves.copy()
                if d == 0:
                    for m in move.moves:
                        initial_moves.append(m)
                new_node = Node(move.field, next_piece, eval(move.field, move.lines_cleared), initial_moves)
                key = move.normalise()
                if trans_table.is_better(key, new_node.score):
                    trans_table.add(key, new_node.score)
                    next_layer_nodes.append(new_node)

            #hold piece generation
            if node.hold is None:
                hold_piece = queue[d + 1]
            else:
                hold_piece = node.hold
            
            if hold_piece != node.piece and not piece_held:
                hold_moves = generate(node.field, hold_piece)
                for move in hold_moves:
                    initial_moves = node.initial_moves.copy()
                    if d == 0:
                        initial_moves.append('hold')
                        for m in move.moves:
                            initial_moves.append(m)
                    new_node = Node(move.field, next_piece, eval(move.field, move.lines_cleared), initial_moves)
                    key = move.normalise()
                    if trans_table.is_better(key, new_node.score):
                        trans_table.add(key, new_node.score)
                        next_layer_nodes.append(new_node)

        next_layer_nodes.sort(key=lambda n: n.score, reverse=True)
        layers[d + 1].nodes = next_layer_nodes[:WIDTH]

    best_node = max(layers[DEPTH].nodes, key=lambda n: n.score)
    return best_node
# TESTING
'''PIECE_LUT = [
    [ #I PIECE
        [(-1,0) , (0,0) , (1,0) , (2,0)],
        [(0,1) , (0,0) , (0,-1) , (0,-2)],
        [(1,0) , (0,0) , (-1,0) , (-2,0)],
        [(0,-1) , (0,0) , (0,1) , (0,2)]
    ],
    [ #T PIECE
        [(-1,0) , (0,0) , (1,0) , (0,1)],
        [(0,1) , (0,0) , (0,-1) , (1,0)],
        [(1,0) , (0,0) , (-1,0) , (0,-1)],
        [(0,-1) , (0,0) , (0,1) , (-1,0)]  
    ],
    [#O PIECE
        [(0,0) , (1,0) , (0,1) , (1,1)],
        [(0,0) , (0,-1) , (1,0) , (1,-1)],
        [(0,0) , (-1,0) , (0,-1) , (-1,-1)],
        [(0,0) , (0,1) , (-1,0) , (-1,1)]
    ],
    [#S PIECE
        [(-1,0) , (0,0) , (0,1) , (1,1)],
        [(0,1) , (0,0) , (1,0) , (1,-1)],
        [(1,0) , (0,0) , (0,-1) , (-1,-1)],
        [(0,-1) , (0,0) , (-1,0) , (-1,1)]
    ],
    [#Z PIECE
        [(-1,1) , (0,1) , (0,0) , (1,0)],
        [(1,1) , (1,0) , (0,0) , (0,-1)],
        [(1,-1) , (0,-1) , (0,0) , (-1,0)],
        [(-1,-1) , (-1,0) , (0,0) , (0,1)]
    ],
    [#L PIECE
        [(-1,0) , (0,0) , (1,0) , (1,1)],
        [(0,1) , (0,0) , (0,-1) , (1,-1)],
        [(1,0) , (0,0) , (-1,0) , (-1,-1)],
        [(0,-1) , (0,0) , (0, 1) , (-1,1)]
    ],
    [#J PIECE
        [(-1,0) , (0,0) , (1,0) , (-1,1)],
        [(0,1) , (0,0) , (0,-1) , (1,1)],
        [(1,0) , (0,0) , (-1,0) , (1,-1)],
        [(0,-1) , (0,0) , (0,1) , (-1,-1)]
    ]
]

class Piece:
    def __init__(self, piece):
        self.x = 5
        self.y = -2
        self.current_rotation = 0 # initial rotation state

        self.piece = piece
        self.locked = False
        self.piece_rotations = PIECE_LUT[piece]

field = [
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0],
    [0, 0, 1, 1, 1, 0 ,0 ,0 ,0 ,0],
    [2, 2, 2, 2, 1, 0 ,0 ,0 ,0 ,0],
]
current_piece = Piece(3)
queue = [Piece(5), Piece(2), Piece(1), Piece(3)]
piece_held = Piece(4)


best_move = beam_search(field, current_piece, queue, piece_held)
print(best_move.initial_moves)'''

