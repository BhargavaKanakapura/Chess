import copy

def __init__(game_state):
    global gs, all_game_played
    gs = game_state
    all_game_played = {}
    #play_many_games(all_game_played)

def play_many_games(game_log, batch_size=1000):

    print("PROCESSING GAMES...")
    
    for _ in range(batch_size):

        Model = ModelGame()

        Model.play_fake_game()
        game_log[Model.gs.game_log] = Model.review_game()

        del(Model)

    print("DONE PROCESSING GAMES...")

class ModelGame:

    def __init__(self):
        global gs
        self.gs = copy.copy(gs)
        self.valid_moves = []

    def play_fake_game(self):

        running = True
        move_made = False
        
        while running:
            
            if self.gs.white_to_move:
                move, score = self.worst_move()
                self.gs.make_move(move, final=False, computer=True)
                move_made = True

            else:
                move, score = self.best_move()
                self.gs.make_move(move, final=False, computer=True)
                move_made = True

            if move_made:

                self.valid_moves = self.opp_legal_moves
                self.opp_legal_moves, self.opp_blind_legal_moves = self.gs.legal_moves(get_blind_moves=True)

                move_made = False

                if self.gs.checkmate('w'):
                    self.winner = 'w'

                elif self.gs.checkmate('b'):
                    self.winner = 'b'

                if self.gs.white_to_move:
                    if self.gs.stalemate('w'):
                        self.winner = 'N/A'

                else:
                    if self.gs.stalemate('b'):
                        self.winner = 'N/A'

            if self.winner != None:
                running = False

        self.review_game()

    def best_move(self):
        pass

    def worst_move(self):
        pass

    def review_game(self):
        pass

    


    
    
