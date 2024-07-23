from movegen import generate
from eval import eval

class Node:
    def __init__(self, field, piece, score):
        self.field = field
        self.piece = piece
        self.score = score

class Layer:
    def __init__(self):
        self.nodes = []

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def add(self, key, score):
        if key not in self.table or self.table[key] < score:
            self.table[key] = score

    def is_better(self, key, score):
        return key not in self.table or self.table[key] < score

def beam_search(initial_field, initial_piece, queue):
    DEPTH = 3
    WIDTH = 3

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
                new_node = Node(move.field, next_piece, eval(move.field))
                key = move.normalise()
                if trans_table.is_better(key, new_node.score):
                    trans_table.add(key, new_node.score)
                    next_layer_nodes.append(new_node)

        next_layer_nodes.sort(key=lambda n: n.score, reverse=True)
        layers[d + 1].nodes = next_layer_nodes[:WIDTH]

    best_node = max(layers[DEPTH].nodes, key=lambda n: n.score)
    return best_node