import pygame
import chess
import UI
import random
import os
from constants import *

IMAGES = {}

os.system('clear')
print("GAME LOG")

def load_images():
    
    for team in ["w", "b"]:
        for piece in ["p", "N", "B", "Q", "K", "R"]:
            
            key = team + piece
            value = pygame.transform.scale(pygame.image.load('pieces/' + key + '.png'), (SQ_SIZE, SQ_SIZE))
            
            IMAGES[key] = value

def random_string(length):

    chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%")
    string = ''

    for _ in range(length):
        string += random.choice(chars)

    return string

def init():

    username = input("USERNAME: ")
    password = input("PADDWORD: ")

    UI.valid_login(username, password)
    
    os.system('clear')

    global mode
    mode = input("PVP or PVC: ").upper()

    if mode not in ["PVP", "PVC"]:
        raise UI.InvalidInput("MODE PVP/PVC --> ENTERED: " + mode)

    else:

        if mode == "PVP":
           
            game_code = input("GAME CODE: ")
            if game_code.upper() == "NEW":
                game_code = random_string(10)
                print("GAME CODE: " + game_code + "\nTHIS IS THE GAME CODE")
                cont = input("PRESS ENTER TO CONTINUE")
                if cont == "":
                    pass
                else:
                    cont = input("PRESS ENTER TO CONTINUE")

        else:
            
            LEVEL = int(input("LEVEL: "))
            if LEVEL not in range(1, 11):
                raise UI.InvalidInput
            
def main():
    
    pygame.init()
    
    display = pygame.display.set_mode(( ACT_WIDTH, HEIGHT ))
    clock = pygame.time.Clock()
    
    display.fill((20, 20, 20))
    
    game_state = chess.GameState()
    move_log = UI.MoveLog(display)
    valid_moves = game_state.legal_moves()
    global mode
    
    load_images()
    
    running = True
    winner = None

    move_played = False
    undo_made = (False, False)
    animate = False
    
    square_selected = ()
    player_clicks = []

    can_undo = True

    os.system('clear')
    print("GAME BEGINS")
    for _ in range(2): print("-" * 20)

    def update_screen():

        if move_log.line == 1 and move_log.breaks >= 1:
            display.fill((20, 20, 20))

        if len(player_clicks) > 0: 
            update_board(display, game_state, square_selected=player_clicks[0], win=winner)
            valid_moves_for_piece(display, valid_moves, player_clicks[0])
        else: 
            update_board(display, game_state, win=winner)

        if undo_made[0]:
            x, y = move_log.c_x, move_log.c_y
            w, h = SQ_SIZE * 2, move_log.txt_size + move_log.padding
            pygame.draw.rect(display, (30, 30, 30), (x, y + h, w, h))

        if undo_made[0] and undo_made[1]:
            x, y = move_log.c_x, move_log.c_y
            w, h = SQ_SIZE * 2, move_log.txt_size + move_log.padding
            pygame.draw.rect(display, (30, 30, 30), (x, y + h, w, h * 2))

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
                            undo_made = (False, False)
                            animate = True

                        player_clicks = []
                        square_selected = ()

                if (y in range( HEIGHT - SQ_SIZE, HEIGHT - SQ_SIZE // 2 ) and x > 2 * WIDTH // 3) and can_undo and winner == None and game_state.move_log:
                    
                    move_log.write_line(game_state.user_move_log[-1], next_line=False, color=(30, 30, 30))
                    game_state.undo_move(final=True)
                    move_log.erase_line()

                    print("\033[A{}\033[A")

                    move_played = True
                    undo_made = (True, False)
                    animate = False

                    if mode == "PVC" or (game_state.white_to_move and len(game_state.move_log) >= 2):

                        move_log.write_line(game_state.user_move_log[-1], next_line=False, color=(30, 30, 30))
                        game_state.undo_move(final=True)
                        move_log.erase_line()

                        print("\033[A{}\033[A")
                        
                        move_played = True
                        undo_made = (True, True)
                        animate = False

                if (y in range( HEIGHT - SQ_SIZE // 2, HEIGHT ) and x > 2 * WIDTH // 3) and (mode == "PVP" or (mode == "PVC" and game_state.white_to_move)) and winner == None:

                    resign = "yes"

                    if resign.upper() == "YES":
                        
                        if game_state.white_to_move:
                            winner = "BLACK"

                        else:
                            winner = "WHITE"

                        print("BLACK RESIGNED" if winner == "WHITE" else "WHITE RESIGNED")
                    
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    running = False

            x, y = pygame.mouse.get_pos()

            if (y in range( HEIGHT - SQ_SIZE, HEIGHT - SQ_SIZE // 2 ) and x > 2 * WIDTH // 3) and can_undo:
                draw_buttons(display, c1=pygame.Color('red'))

            elif (y in range( HEIGHT - SQ_SIZE // 2, HEIGHT ) and x > 2 * WIDTH // 3):
                draw_buttons(display, c2=pygame.Color('red')) if can_undo else draw_buttons(display, c1=pygame.Color('dark grey'), c2=pygame.Color('red'))

            else:
                draw_buttons(display) if can_undo else draw_buttons(display, c1=pygame.Color('dark grey'))

        if move_played:
            
            if animate:
                animate_move(game_state.move_log[-1], display, game_state.board, clock)

            if game_state.checkmate('w'):
                winner = "BLACK"

            elif game_state.checkmate('b'):
                winner = "WHITE"

            elif (game_state.stalemate('w') and game_state.white_to_move) or (game_state.stalemate('b') and not game_state.white_to_move):
                winner = "NOBODY"

            else: winner = None

            valid_moves = game_state.legal_moves()
            if game_state.user_move_log and (not undo_made[1] and not undo_made[0]):
                text = move_log.write_line(game_state.user_move_log[-1])
                display.blit(text[0], text[1])
                if move_log.line == 24:
                    move_log.scroll()
            move_played = False

        update_screen()

        if winner != None:

            download_game_log = True if input("DOWNLOAD GAME LOG: ").upper() == "YES" else False

            if download_game_log:

                file = input("ENTER THE FILE TO WHICH THE GAME LOG IS TO BE SAVED: ")

                with open(file, mode='a'):
                    file = game_state.user_move_log

            os.system('clear')
            print(file)
            exit()

        if not game_state.white_to_move and mode == "PVC":

            game_state.find_best_move()
            move, score = game_state.ai.best_move

            game_state.make_move(move)
            move_played = True
                    
            player_clicks = []
            square_selected = ()
            
def exit():
    print("GOODBYE")
    pygame.quit()
    quit()
    

def draw_buttons(screen, c1=BLACK, c2=BLACK):

    font = pygame.font.SysFont("freesansbold.ttf", SQ_SIZE // 2 - SQ_SIZE//10)

    pygame.draw.rect(screen, c1, ( 2 * WIDTH // 3, HEIGHT - SQ_SIZE, WIDTH // 3, SQ_SIZE // 2 ))
    text_img = font.render("UNDO", False, WHITE)
    screen.blit(text_img, (2 * WIDTH // 3 + SQ_SIZE // 1.1, HEIGHT - SQ_SIZE + SQ_SIZE // 5))

    pygame.draw.rect(screen, c2, ( 2 * WIDTH // 3, HEIGHT - SQ_SIZE // 2, WIDTH // 3, SQ_SIZE // 2 ))
    text_img = font.render("RESIGN", False, WHITE)
    screen.blit(text_img, (2 * WIDTH // 3 + SQ_SIZE // 1.1, HEIGHT - SQ_SIZE // 2 + SQ_SIZE // 5)) 
        
def update_board(screen, game_state, square_selected=None, win=None):

    draw_board(screen, square_selected)
    draw_pieces(screen, game_state.board)

    pygame.draw.rect(screen, WHITE, (0, HEIGHT - SQ_SIZE, 2 * WIDTH // 3, SQ_SIZE))

    if win == None:
        text = ("WHITE" if game_state.white_to_move else "BLACK") + "'S TURN"
    else:
        text = win + " WINS"

    font = pygame.font.SysFont("freesansbold.ttf", SQ_SIZE - SQ_SIZE//10)
    text_img = font.render(text, False, BLACK)
    screen.blit(text_img, (SQ_SIZE//5, HEIGHT - SQ_SIZE + SQ_SIZE//5))
    
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



init()
main()
    
    
    
    
    
    
    
    
    
      