def init(main):
    global gs, all_games
    gs = main
    all_games = []

def organize_current_game():
    pass

def move_made():
    all_games.append(gs.board.copy())

