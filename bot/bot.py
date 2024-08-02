from Tetris.tetris import Tetris
from beamSearch import beam_search
import time

tetris = Tetris()

# Main loop
while tetris.running != False:
    events = tetris.handle_events()
    tetris.update(events)
    tetris.render()

    current_piece = tetris.get_current_piece()
    field = tetris.get_game_state()
    queue = tetris.game.queue
    piece_held = tetris.game.piece_held

    best_move = beam_search(field, current_piece, queue, piece_held).initial_moves
    print(best_move)

    for move in best_move:
        tetris.game.enqueue_bot_command(best_move.pop(0))