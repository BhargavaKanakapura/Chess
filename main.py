import pygame, chess, UI
from constants import *

IMAGES = {}

def load_images():
    
    for team in ["w", "b"]:
        for piece in ["p", "N", "B", "Q", "K", "R"]:
            
            key = team + piece
            value = pygame.transform.scale(pygame.image.load('pieces/' + key + '.png'), (SQ_SIZE, SQ_SIZE))
            
            IMAGES[key] = value
            
def main():
    
    pygame.init()
    
    display = pygame.display.set_mode(( WIDTH, HEIGHT ))
    clock = pygame.time.Clock()
    
    display.fill(WHITE)
    
    game_state = chess.GameState()
    valid_moves = game_state.legal_moves()
    mode = "PVP"
    
    load_images()
    
    running = True
    winner = None

    move_played = False
    animate = False
    
    square_selected = ()
    player_clicks = []
    
    print("GAME BEGINS")

    def update_screen():

        if len(player_clicks) > 0: 
            update_board(display, game_state, square_selected=player_clicks[0], win=winner)
            valid_moves_for_piece(display, valid_moves, player_clicks[0])
        else: 
            update_board(display, game_state, win=winner)

        pygame.display.flip()
        clock.tick(FPS)
    
    while running:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                
                x, y = event.pos

                if (game_state.white_to_move or mode == "PVP") and (y < HEIGHT - SQ_SIZE):

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
                            animate = True

                        player_clicks = []
                        square_selected = ()

                if y > HEIGHT - SQ_SIZE and x > 2 * WIDTH // 3:
                    game_state.undo_move(final=True)
                    print("-|" * 10 + "-")
                    move_played = True
                    animate = False
                    if mode == "PVC":
                        pygame.time.wait(1000)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x, y = event.pos
                row, col = row, col = y // SQ_SIZE, x // SQ_SIZE
                print(game_state.get_square((row, col)))
                    
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                if event.key == pygame.K_z:
                    game_state.undo_move(final=True)
                    print("-|" * 10 + "-")
                    move_played = True
                    animate = False
                    if mode == "PVC":
                        pygame.time.wait(1000)

        if not game_state.white_to_move and mode == "PVC":

            move, score = game_state.find_best_move()

            if move in valid_moves:
                game_state.make_move(move)
                move_played = True
                    
            player_clicks = []
            square_selected = ()
 
        if move_played:
            
            if animate:
                animate_move(game_state.move_log[-1], display, game_state.board, clock)

            if game_state.checkmate('w'):
                winner = "BLACK"
                print("BLACK WINS")

            elif game_state.checkmate('b'):
                winner = "WHITE"
                print("WHITE WINS")

            elif game_state.stalemate('w') or game_state.stalemate('b'):
                winner = "NOBODY"
                print("DRAW GAME")

            else: winner = None

            valid_moves = game_state.legal_moves()
            move_played = False

        update_screen()
        
        
def update_board(screen, game_state, square_selected=None, win=None):

    draw_board(screen, square_selected)
    draw_pieces(screen, game_state.board)

    pygame.draw.rect(screen, WHITE, (0, HEIGHT - SQ_SIZE, WIDTH, SQ_SIZE))

    if win == None:
        text = ("WHITE" if game_state.white_to_move else "BLACK") + "'S TURN"
    else:
        text = win + " WINS"

    font = pygame.font.SysFont("freesansbold.ttf", SQ_SIZE - SQ_SIZE//10)

    text_img = font.render(text, False, BLACK)
    screen.blit(text_img, (SQ_SIZE//5, HEIGHT - SQ_SIZE + SQ_SIZE//5))

    pygame.draw.rect(screen, BLACK, ( 2 * WIDTH // 3, HEIGHT - SQ_SIZE, WIDTH // 3, SQ_SIZE ))
    text_img = font.render("UNDO", False, WHITE)
    screen.blit(text_img, (2 * WIDTH // 3 + SQ_SIZE // 2.3, HEIGHT - SQ_SIZE + SQ_SIZE // 5))
    
def draw_board(screen, square_selected = None):
    
    global colors
    colors = [WHITE, GREY]
    
    for r in range(ROWS):
        for c in range(COLS):
            
            color = colors[ (r + c) % 2 ]
            pygame.draw.rect( screen, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE) )

    if square_selected != None:
        r, c = square_selected
        pygame.draw.rect( screen, pygame.Color('blue'), (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE) )

def draw_pieces(screen, board):
    
    for r in range(ROWS):
        for c in range(COLS):
            
            piece = board[r][c]
            
            if piece != "--":
                screen.blit(IMAGES[piece], (c * SQ_SIZE, r * SQ_SIZE)) 

def valid_moves_for_piece(screen, valid_moves, square_selected):

    squares = []
    row, col = square_selected

    for move in valid_moves:
        if move.start_row == row and move.start_col == col:
            squares.append( (move.end_row, move.end_col) )

    for square in squares:     
        r, c = square
        surf = pygame.Surface((SQ_SIZE, SQ_SIZE))
        surf.set_alpha(100)
        surf.fill(pygame.Color('blue'))
        screen.blit(surf, (c * SQ_SIZE, r * SQ_SIZE))

def animate_move(move, screen, board, clock):

    global colors
    coords = []
    rows_traversed = move.end_row - move.start_row
    cols_traversed = move.end_col - move.start_col
    fps = 10
    fc = (abs(rows_traversed) + abs(cols_traversed)) * fps

    for frame in range(fc + 1):

        r, c = move.start_row + rows_traversed * frame / fc, move.start_col + cols_traversed * frame / fc

        draw_board(screen)
        draw_pieces(screen, board)

        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, end_square)

        if move.piece_captured != "--":
            screen.blit(IMAGES[move.piece_captured], end_square)

        screen.blit(IMAGES[move.piece_moved], (pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)))
        pygame.display.flip()
        clock.tick(100)        


if __name__ == "__main__":  
    main()
    
    
    
    
    
    
    
    
    
    
      