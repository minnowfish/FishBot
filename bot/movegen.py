from Tetris.define import PIECE_LUT, SRS_LUT
from numpy import subtract
from copy import deepcopy

class Move:
    def __init__(self, x, y, piece, rotation, field):
        self.x = x
        self.y = y
        self.piece = piece
        self.rotation = rotation
        self.field = field
        self.score = 0

    def to_tuple(self):
        return (self.x, self.y, self.piece, self.rotation)
    
    def normalise(self):
        match self.piece:
            case 0:
                if self.rotation == 2:
                    return(self.x - 1, self.y, self.piece, 0)
                if self.rotation == 3:
                    return(self.x, self.y - 1, self.piece, 1)
                return self.to_tuple()
            
            case 3 | 4:
                if self.rotation == 2:
                    return(self.x, self.y + 1, self.piece, 0)
                if self.rotation == 3:
                    return(self.x - 1, self.y, self.piece, 1)
                return self.to_tuple()
            
            case _:
                return self.to_tuple()


class PositionTracker:
    def __init__(self):
        self.data = set()
        self.positions = []

    def push(self, move):
        key = move.normalise()
        self.data.add(key)
        self.positions.append(move)

    def exist(self, move):
        key = move.normalise()
        return key in self.data

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
                return x, y
    return None, None
    
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
                return x, y
    return None, None

def get_new_field(x, y, piece, rotation, rotations, new_field):
    new_field = deepcopy(new_field)
    piece_rotation = rotations[rotation]
    for offset in piece_rotation:
        off_x, off_y = offset
        new_field[y - off_y + 3][x + off_x - 1] = piece + 1
    
    return clear_lines(new_field)

def clear_lines(new_field):
    lines_cleared = 0
    for row in range(len(new_field)-1, -1, -1):
        line = new_field[row]
        if check_full_line(line):
            new_field.pop(row)
            lines_cleared += 1

    for i in range(lines_cleared):
        new_field.insert(0, [0 for _ in range(10)])

    return new_field

def check_full_line(line):
    for i in line:
        if i == 0:
            return False
    return True



def expand(field, parent, children):
    x = parent.x
    y = parent.y
    piece = parent.piece
    rotation = parent.rotation
    rotations = PIECE_LUT[piece]

    if check_move(x-1, y, rotation, rotations, field):

        children.append(Move(x-1, y, piece, rotation, None))

    if check_move(x+1, y, rotation, rotations, field):
        children.append(Move(x+1, y, piece, rotation, None))

    if piece != 2: # check if not O piece
        new_x, new_y = rotate_cw(x, y, piece, rotation, rotations, field)
        if new_x != None:
            cw_rotation = (rotation + 1) % 4
            children.append(Move(new_x, new_y, piece, cw_rotation, None))

        new_x, new_y = rotate_ccw(x, y, piece, rotation, rotations, field)
        if new_x != None:
            ccw_rotation = (rotation - 1) % 4
            children.append(Move(new_x, new_y, piece, ccw_rotation, None))

    return children

def generate(field, current_piece):
    result_count = 0

    above_stack = PositionTracker()
    floating = PositionTracker()

    current_x, current_y = current_piece.x, current_piece.y
    type = current_piece.piece
    rotation = current_piece.current_rotation
    piece_rotations = current_piece.piece_rotations

    initial_move = Move(current_x, current_y, type, rotation, None)
    floating.push(initial_move)
    floating_count = 1

    drop_y = hard_drop(current_x, current_y, rotation, piece_rotations, field)
    new_field = get_new_field(current_x, drop_y, type, rotation, piece_rotations, field)
    above_stack.push(Move(current_x, drop_y, type, rotation, new_field))
    above_stack_count = 1

    while floating_count > 0:
        parent = floating.positions[0]
        floating.positions[0] = floating.positions[floating_count - 1]
        floating_count -= 1
#        print("processing:", parent.to_tuple())

        children = []

        children = expand(field, parent, children)

        for child in children:
            if not floating.exist(child):
                floating.push(child)
                floating.positions[floating_count] = child
                floating_count += 1

                above_stack_y = hard_drop(child.x, child.y, child.rotation, PIECE_LUT[child.piece], field)
                child_copy = Move(child.x, above_stack_y, child.piece, child.rotation, None)

                if not above_stack.exist(child_copy):
                    above_stack_field = get_new_field(child.x, above_stack_y, child.piece, child.rotation, PIECE_LUT[child.piece], field)
                    child_copy.field = above_stack_field
                    above_stack.push(child_copy)
                    above_stack_count += 1

    result_map = PositionTracker()

    for i in range(above_stack_count):
        if not result_map.exist(above_stack.positions[i]):
            result_map.push(above_stack.positions[i])
            result_count += 1
        
    return result_map.positions

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
current_piece = Piece(2)
positions = generate(field, current_piece)

for i in positions:
    print(i.to_tuple())
    field = i.field

    for row in field:
        print(row)

    print(" ")