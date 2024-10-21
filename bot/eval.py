from movegen import generate

def bumpiness(field):
    bumpiness = 0
    for col in range(len(field[0]) - 1):
        bumpiness += abs(column_height(field, col) - column_height(field, col + 1))
    return bumpiness

def column_height(field, col):
    for row in range(len(field)):
        if field[row][col] != 0:
            return len(field) - row
    return 0

def holes(field):
    holes = 0
    for row in range(1, len(field)):
        for col in range(10):
            if field[row][col] == 0 and field[row - 1][col] != 0:
                holes += 1
    return holes

def current_height(field):
    for row in range(len(field)):
        for col in field[row]:
            if col != 0:
                height = len(field) - row + 1
                if height >= 17:
                    return height - 10
                return 0 
    return 0

def eval(field, lines_cleared):
    match lines_cleared:
        case 1:
            lines_cleared_cost = -400
        case 2:
            lines_cleared_cost = -500
        case 3:
            lines_cleared_cost = -300
        case 4: 
            lines_cleared_cost = 500
        case _:
            lines_cleared_cost = 0

    return (bumpiness(field) * -25) + (holes(field) * -500) + (current_height(field) * -50) + lines_cleared_cost