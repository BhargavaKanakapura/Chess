from constants import *


class GameState:

    def __init__(self):

        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--' for _ in range(COLS)],
            ['--' for _ in range(COLS)],
            ['--' for _ in range(COLS)],
            ['--' for _ in range(COLS)],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        self.white_to_move = True
        
        self.move_log = []
        
        self.pieces = self.Pieces(self)

        self.white_king = (7, 4)
        self.black_king = (0, 4)

        self.castle_rights = CastleRights(True, True, True, True)
        self.castle_log = [ CastleRights( self.castle_rights.wks, self.castle_rights.wqs, self.castle_rights.bks, self.castle_rights.bqs ) ]
        
    def make_move(self, move, final=True):

        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved

        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        
        self.update_castling_rights(move)
        self.castle_log.append( CastleRights( self.castle_rights.wks, self.castle_rights.wqs, self.castle_rights.bks, self.castle_rights.bqs ) )

        if move.piece_moved == 'wK':
            self.white_king = (move.end_row, move.end_col)

        elif move.piece_moved == 'bK':
            self.black_king = (move.end_row, move.end_col)
        '''
        if move.castle_move:
            
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][-3] = self.board[move.end_row][-1]
                self.board[move.end_row][-1] = "--"
            
            else:
                self.board[move.end_row][3] = self.board[move.end_row][0]
                self.board[move.end_row][0] = "--"
        '''
        if final:

            move.print_chess_notation()

            if 'wp' in self.board[0]:
                
                col = self.board[0].index('wp')
                promote = input("PIECE PROMOTION: ").upper()

                if promote in ["N", "B", "R", "Q"]:
                    self.board[0][col] = "w" + promote

            if 'bp' in self.board[ROWS - 1]:
                
                col = self.board[ROWS - 1].index('bp')
                promote = input("PIECE PROMOTION: ").upper()

                if promote in ["N", "B", "R", "Q"]:
                    self.board[ROWS - 1][col] = "b" + promote
            
    def undo_move(self, final=False):
        
        if len(self.move_log) != 0:
            
            move = self.move_log.pop()
            
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            
            self.white_to_move = not self.white_to_move

            if move.piece_moved == 'wK':
                self.white_king = (move.start_row, move.start_col)

            elif move.piece_moved == 'bK':
                self.black_king = (move.start_row, move.start_col)
            
            self.castle_log.pop()
            self.castle_rights = CastleRights( self.castle_log[-1].wks, self.castle_log[-1].wqs, self.castle_log[-1].bks, self.castle_log[-1].bqs )
            
            if move.castle_move and move.piece_moved[1] == "K":
                
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][-1] = self.board[move.end_row][-3]
                    self.board[move.end_row][-3] = "--"
                
                else:
                    self.board[move.end_row][0] = self.board[move.end_row][3]
                    self.board[move.end_row][3] = "--"

    def update_castling_rights(self, move):
        
        if move.piece_moved == "wK":
            self.castle_rights.wks = False
            self.castle_rights.wqs = False

        elif move.piece_moved == "bK":
            self.castle_rights.bks = False
            self.castle_rights.bqs = False

        elif move.piece_moved == "wR":

            if move.start_row == 0:
                self.castle_rights.wqs = False
            
            elif move.start_row == 7:
                self.castle_rights.wks = False

        elif move.piece_moved == "bR":

            if move.start_row == 0:
                self.castle_rights.bqs = False
            
            elif move.start_row == ROWS - 1:
                self.castle_rights.bks = False            

    def legal_moves(self):

        moves = self.blind_legal_moves()
        
        temp_castleing_rights = CastleRights( self.castle_rights.wks, self.castle_rights.wqs, self.castle_rights.bks, self.castle_rights.bqs )
        
        if self.white_to_move:
            self.pieces.castle_moves(self.white_king, moves)
            
        else:
            self.pieces.castle_moves(self.black_king, moves)
        
        for i in range( len(moves) - 1, -1, -1 ):

            self.make_move(moves[i], final=False)
            self.white_to_move = not self.white_to_move
            
            if self.in_check():
                moves.remove(moves[i])

            self.white_to_move = not self.white_to_move
            self.undo_move()
            
        self.castle_rights = temp_castleing_rights

        return moves

    def checkmate(self, player):

        white_to_move = self.white_to_move
        
        if player == "b":
            self.white_to_move = False

        elif player == "w":
            self.white_to_move = True

        moves = self.legal_moves()

        self.white_to_move = white_to_move

        if not moves:
            return True
        else:
            return False

    def in_check(self):
        
        if self.white_to_move:
            return self.controlled_squares( self.white_king )

        else:
            return self.controlled_squares( self.black_king )

    def controlled_squares(self, pos):
        
        r, c = pos
        self.white_to_move = not self.white_to_move

        opponent_moves = self.blind_legal_moves()

        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                self.white_to_move = not self.white_to_move
                return True

        self.white_to_move = not self.white_to_move
        return False
    
    def blind_legal_moves(self):
        
        moves = []
        
        for row in range(ROWS):
            for col in range(COLS):
                
                team = self.board[row][col][0]
                piece = self.board[row][col][1]
                
                if ( (team == "w") and (self.white_to_move) ) or ( (team == "b") and (not self.white_to_move) ):
                    
                    if piece == "R":
                        self.pieces.rook_moves(row, col, moves)
                    
                    elif piece == "B":
                        self.pieces.bishop_moves(row, col, moves)
                    
                    elif piece == "N":
                        self.pieces.knight_moves(row, col, moves)
                    
                    elif piece == "Q":
                        self.pieces.queen_moves(row, col, moves)
                    
                    elif piece == "K":
                        self.pieces.king_moves(row, col, moves)
                    
                    elif piece == "p":
                        self.pieces.pawn_moves(row, col, moves)
            
        return moves
     
    class Pieces:
        
        def __init__(self, outer):
            self.main = outer
            self.board = outer.board

        def pawn_moves(self, row, col, moves):
             
            if self.main.white_to_move:
                 
                if self.board[row - 1][col] == '--':
                    moves.append(Move((row, col), (row - 1, col), self.board, False))
                     
                    if self.board[row - 2][col] == '--' and row == 6:
                        moves.append(Move((row, col), (row - 2, col), self.board, False))

                if col - 1 >= 0:
                    if self.board[row - 1][col - 1][0] == 'b':
                        moves.append(Move((row, col), (row - 1, col - 1), self.board, False))

                if col + 1 <= ROWS - 1:
                    if self.board[row - 1][col + 1][0] == 'b':
                        moves.append(Move((row, col), (row - 1, col + 1), self.board, False))

            if not self.main.white_to_move:
                 
                if self.board[row + 1][col] == '--':
                    moves.append(Move((row, col), (row + 1, col), self.board, False))
                     
                    if self.board[row + 2][col] == '--' and row == 1:
                        moves.append(Move((row, col), (row + 2, col), self.board, False))

                if col - 1 >= 0:
                    if self.board[row + 1][col - 1][0] == 'w':
                        moves.append(Move((row, col), (row + 1, col - 1), self.board, False))

                if col + 1 <= 7: 
                    if self.board[row + 1][col + 1][0] == 'w':
                        moves.append(Move((row, col), (row + 1, col + 1), self.board, False))
        
        def rook_moves(self, row, col, moves):
            
            directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
            enemy_piece = 'b' if self.main.white_to_move else 'w'

            for d in directions:
                for i in range(1, ROWS):

                    end_row, end_col = row + d[0] * i, col + d[1] * i

                    if end_row in range(0, ROWS) and end_col in range(0, ROWS):

                        end_piece = self.board[end_row][end_col]
                    
                        if end_piece == '--':
                            moves.append(Move((row, col), (end_row, end_col), self.board, False))

                        elif end_piece[0] == enemy_piece:
                            moves.append(Move((row, col), (end_row, end_col), self.board, False))
                            break

                        else:
                            break

                    else:
                        break
        
        def knight_moves(self, row, col, moves):
            
            knight_moves = ((-2, 1), (2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
            enemy_piece = 'b' if self.main.white_to_move else 'w'

            for move in knight_moves:

                end_row, end_col = row + move[0], col + move[1]

                if end_row in range(0, ROWS) and end_col in range(0, ROWS):

                    if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] == enemy_piece:
                        moves.append(Move((row, col), (end_row, end_col), self.board, False))
        
        def bishop_moves(self, row, col, moves):
            
            directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))
            enemy_piece = 'b' if self.main.white_to_move else 'w'

            for d in directions:
                for i in range(1, ROWS):

                    end_row, end_col = row + d[0] * i, col + d[1] * i

                    if end_row in range(0, ROWS) and end_col in range(0, ROWS):

                        end_piece = self.board[end_row][end_col]
                    
                        if end_piece == '--':
                            moves.append(Move((row, col), (end_row, end_col), self.board, False))

                        elif end_piece[0] == enemy_piece:
                            moves.append(Move((row, col), (end_row, end_col), self.board, False))
                            break

                        else:
                            break

                    else:
                        break
        
        def queen_moves(self, row, col, moves):
            self.bishop_moves(row, col, moves)
            self.rook_moves(row, col, moves)
        
        def king_moves(self, row, col, moves):
            
            king_moves = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
            enemy_piece = 'b' if self.main.white_to_move else 'w'

            for move in king_moves:

                end_row, end_col = row + move[0], col + move[1]

                if end_row in range(0, ROWS) and end_col in range(0, ROWS):

                    if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] == enemy_piece:
                        moves.append(Move((row, col), (end_row, end_col), self.board, False))
            
        def castle_moves(self, pos, moves):
            
            r, c = pos
            
            if self.main.controlled_squares(pos):
                return None
                
            if (self.main.white_to_move and self.main.castle_rights.wks) or (not self.main.white_to_move and self.main.castle_rights.bks):
                self.ksc(r, c, moves)
                
            if (self.main.white_to_move and self.main.castle_rights.wqs) or (not self.main.white_to_move and self.main.castle_rights.bqs):
                self.qsc(r, c, moves)
                
        def ksc(self, r, c, moves):
            
            if (self.board[r][c + 1], self.board[r][c + 2]) == ("--", "--"):
                if not self.main.controlled_squares((r, c + 1)) and not self.main.controlled_squares((r, c + 2)):
                    moves.append(Move((r, c), (r, c + 2), self.board, True))
        
        def qsc(self, r, c, moves):
            
            if (self.board[r][c - 1], self.board[r][c - 2], self.board[r][c - 3]) == ("--", "--", "--"):
                if not self.main.controlled_squares((r, c - 1)) and not self.main.controlled_squares((r, c - 2)) and not self.main.controlled_squares((r, c - 3)):
                    moves.append(Move((r, c), (r, c - 2), self.board, True))

    def __repr__(self):
        for row in self.board: yield row

    def get_square(self, square):
        return self.board[square[0]][square[1]]


class CastleRights:

    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

    def __repr__(self):
        return "WKS: {} || WQS: {} || BKS: {} || BQS: {}".format(self.wks, self.wqs, self.bks, self.bqs)

        
class Move:
    
    def __init__(self, start_square, end_square, board, castle):
        
        self.start_row, self.start_col = tuple(start_square)
        self.end_row, self.end_col = tuple(end_square)
        
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        if self.piece_moved[1] == "K" and abs( self.start_col - self.end_col ) != 1:
            self.castle_move = True

        else:
            self.castle_move = castle

        self.id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):

        if isinstance(other, Move):

            if (other.id == self.id):
                return True

        return False

    def __repr__(self):
        return ("PIECE: {} | START: {} | END: {} | CASTLE_MOVE: {}".format(self.piece_moved, (self.start_row, self.start_col), (self.end_row, self.end_col), self.castle_move))
        
    def print_chess_notation(self):

        if self.castle_move:

            if self.end_col - self.start_col == 2:
                print("O-O")

            else:
                print("O-O-O")

        else:
        
            notation = ''

            col_to_letter = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

            if self.piece_moved[1] != 'p':
                notation += self.piece_moved[1]
            elif self.piece_captured != "--":
                notation += col_to_letter[self.start_col]

            if self.piece_captured != "--":
                notation += 'x'

            notation += col_to_letter[self.end_col]
            notation += str( self.end_row )

            print(notation)
        
        
    