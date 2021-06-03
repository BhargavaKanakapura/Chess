import copy

def __init__(game_state):
    global gs, all_game_played
    gs = game_state
    all_games_played = []
    play_model_games(all_games_played)
    
def play_model_games(game_list, num_games=100):
    for _ in range(num_games):
        model_game = ModelGame()
        model_game.play_fake_game()
        game_list.append(model_game)
        del(model_game)
        
def find_similar_game(current_game_log):
    max_sim = 0
    max_sim_game = None
    for game in all_games_played:
        sim = similarity(game.gs_node.move_log, current_game_log)
        if sim > max_sim:
            max_sim = sim
            max_sim_game = game
    return max_sim_game, max_sim

def similarity(current_array, ref_array):
    pass
        
class ModelGame:
    
    def __init__(self):
        global gs
        self.gs_node = copy.copy(gs)
        self.winner = None
        self.win_chance = 0.45
        
    def play_fake_game(self):
        pass
    
    def review_game(self):
        pass

    
    
