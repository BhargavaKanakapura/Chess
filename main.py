import pygame, chess
from constants import *

IMAGES = {}

def load_images():
    
    for team in ["w", "b"]:
        for piece in ["p", "N", "B", "Q", "K", "R"]:
            
            key = team + piece
            value = pygame.image.load('pieces/' + key + '.png')
            
            IMAGES[key] = value
            
def main():
    
    pygame.init()
    
    display = pygame.display.set_mode(( WIDTH, HEIGHT ))
    clock = pygame.time.Clock()
    
    display.fill(WHITE)
    
    game_state = chess.GameState()
    valid_moves = game_state.legal_moves()
    
    load_images()
    
    running = True
    move_played = False
    
    square_selected = ()
    player_clicks = []
    
    while running:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                x, y = event.pos
                row, col = y // SQ_SIZE, x // SQ_SIZE
                
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []
                    
                else:
                    square_selected = (row, col)
                    if not ( player_clicks == [] and game_state.get_square(square_selected) == "--"):
                        player_clicks.append(square_selected)
                    
                if len(player_clicks) == 2:
                    
                    move = chess.Move( player_clicks[0], player_clicks[1], game_state.board, False )
                                       
                    if move in valid_moves:
                        game_state.make_move(move)
                        move_played = True
                    
                    player_clicks = []
                    square_selected = ()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x, y = event.pos
                row, col = row, col = y // SQ_SIZE, x // SQ_SIZE
                print(game_state.get_square((row, col)))
                    
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                if event.key == pygame.K_z:
                    game_state.undo_move(final=True)
                    move_played = True
                    
        if move_played:

            if game_state.checkmate('w'):
                print("BLACK WINS")

            elif game_state.checkmate('b'):
                print("WHITE WINS")

            valid_moves = game_state.legal_moves()
            move_played = False
                
        update_board(display, game_state, player_clicks[0]) if len(player_clicks) > 0 else update_board(display, game_state)
        pygame.display.flip()
        clock.tick(FPS)
        
def update_board(screen, game_state, square_selected = None):
    draw_board(screen, square_selected)
    draw_pieces(screen, game_state.board)
    
def draw_board(screen, square_selected = None):
    
    colors = [WHITE, GREY]
    
    for r in range(ROWS):
        for c in range(COLS):
            
            color = colors[ (r + c) % 2 ]
            pygame.draw.rect( screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE) )

    if square_selected != None:
        r, c = square_selected
        pygame.draw.rect( screen, (255, 255, 0), (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE) )

def draw_pieces(screen, board):
    
    for r in range(ROWS):
        for c in range(COLS):
            
            piece = board[r][c]
            
            if piece != "--":
                screen.blit(IMAGES[piece], (c * SQ_SIZE, r * SQ_SIZE)) 

if __name__ == "__main__":  
    main()
    
    
    
    
    
    
    
    
    
    
      