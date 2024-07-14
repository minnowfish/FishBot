from Tetris.define import PIECE_LUT, SRS_LUT
from numpy import subtract

class Move:
    def __init__(self, x, y, piece, rotation):
        self.x = x
        self.y = y
        self.piece = piece
        self.rotation = rotation

    def to_tuple(self):
        return (self.x, self.y, self.piece, self.rotation)

class PositionTracker:
    def __init__(self):
        self.data = set()
        self.positions = []

    def push(self, move):
        key = move.to_tuple()
        self.data.add(key)
        self.positions.append(move)

    def exist(self, move):
        key = move.to_tuple()
        return key in self.data

def expand(field, parent, children, children_count):

    x = parent.x
    y = parent.y
    piece = parent.piece
    rotation = parent.rotation
    rotations = PIECE_LUT[piece]

    if check_move(x-1, y, rotation, rotations, field):
        children.append(Move(x-1, y, piece, rotation))
        children_count += 1

    if check_move(x+1, y, rotation, rotations, field):
        children.append(Move(x+1, y, piece, rotation))
        children_count += 1

    if piece != 2: # check if not O piece
        if rotate_cw(x, y, piece, rotation, rotations, field):
            cw_rotation = (rotation + 1) % 4
            if piece == 0 or piece == 3 or piece == 4:
                children.append(Move(x, y, piece, cw_rotation % 2))
            else:
                children.append(Move(x, y, piece, cw_rotation))
            children_count += 1

        if rotate_ccw(x, y, piece, rotation, rotations, field):
            ccw_rotation = (rotation - 1) % 4
            if piece == 0 or piece == 3 or piece == 4:
                children.append(Move(x, y, piece, ccw_rotation % 2))
            else:
                children.append(Move(x, y, piece, ccw_rotation))
            children_count += 1

    return children, children_count

def generate(field, current_piece):
    result_count = 0

    MAX_GENERATION_POSITION = 128

    above_stack = PositionTracker()
    floating = PositionTracker()

    current_x, current_y = current_piece.x, current_piece.y
    type = current_piece.piece
    rotation = current_piece.current_rotation
    piece_rotations = current_piece.piece_rotations

    initial_move = Move(current_x, current_y, type, rotation)
    floating.push(initial_move)
    floating_count = 1

    drop_y = hard_drop(current_x, current_y, rotation, piece_rotations, field)
    above_stack.push(Move(current_x, drop_y, type, rotation))
    above_stack_count = 1

    while floating_count > 0:
        parent = floating.positions[0]
        floating.positions[0] = floating.positions[floating_count - 1]
        floating_count -= 1
        print("processing:", parent.to_tuple())

        children = []
        children_count = 0

        children, children_count = expand(field, parent, children, children_count)

        for i in range(children_count):
            child = children[i]
            if not floating.exist(child):
                ("child", child.to_tuple())
                floating.push(child)
                floating.positions[floating_count] = child
                floating_count += 1
                child.y = hard_drop(child.x, child.y, child.rotation, PIECE_LUT[child.piece], field)

                if not above_stack.exist(child):
                    above_stack.push(child)
                    above_stack_count += 1

    result_map = PositionTracker()

    for i in range(above_stack_count):
        if not result_map.exist(above_stack.positions[i]):
            result_map.push(above_stack.positions[i])
            result_count += 1
            

    return result_map.data

def hard_drop(x, y, current_rotation, piece_rotations, field):
    while check_move(x, y + 1, current_rotation, piece_rotations, field):
        y += 1
    return y

def check_move(x, y, rotation, piece_rotations, field):
    piece_rotation = piece_rotations[rotation]
    for offset in piece_rotation:
        off_x, off_y = offset
        try:
            if field[y - off_y + 3][x + off_x - 1] != 0 or off_x + x < 1:
                return False
        except IndexError:
            return False
    return True

def hard_drop(x, y, current_rotation, piece_rotations, field):
    while check_move(x, y + 1, current_rotation, piece_rotations, field):
        y += 1
    return y

def check_move(x, y, rotation, piece_rotations, field):
    piece_rotation = piece_rotations[rotation]
    for offset in piece_rotation:
        off_x, off_y = offset
        try:
            if field[y - off_y + 3][x + off_x - 1] != 0 or off_x + x < 1:
                return False
        except IndexError:
            return False
    return True

def rotate_cw(x, y, piece, current_rotation, piece_rotations, field):
    next_rotation = (current_rotation + 1) % 4

    if piece == 0:
        srs_index = 0
    else:
        srs_index = 1

        for i in range(5):
            off_x, off_y = tuple(subtract(SRS_LUT[srs_index][current_rotation][i], SRS_LUT[srs_index][next_rotation][i]))

            if check_move(x + off_x, y - off_y, next_rotation, piece_rotations, field):
                x += off_x
                y = y - off_y
                current_rotation = next_rotation
                return True
    return False
    
def rotate_ccw(x, y, piece, current_rotation, piece_rotations, field):
    next_rotation = (current_rotation - 1) % 4
    if piece != 2:
        if piece == 0:
            srs_index = 0
        else:
            srs_index = 1

        for i in range(5):
            off_x, off_y = tuple(subtract(SRS_LUT[srs_index][current_rotation][i], SRS_LUT[srs_index][next_rotation][i]))

            if check_move(x + off_x, y - off_y, next_rotation, piece_rotations, field):
                x += off_x
                y = y - off_y
                current_rotation = next_rotation
                return True
    return False


# TESTING

class Piece:
    def __init__(self, piece):
        self.x = 5
        self.y = -2
        self.current_rotation = 0 # initial rotation state

        self.piece = piece
        self.locked = False
        self.piece_rotations = PIECE_LUT[piece]


field = [[0 for _ in range(10)] for _ in range(23)]
current_piece = Piece(5)
print(generate(field, current_piece))


