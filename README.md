A simple chess game in python pygame
- Login is USERNAME: Guest, PASSWORD: Guest (capitalization matters)
- When asked mode: "PVP" for player vs player, "PVC" for player vs computer (not implemented)
- When asked for GAME CODE, enter any random string
- To move a piece, click on the piece, then on the place you want to move to
- To undo a move, press UNDO or the "z" key

Implemented:
- Basic piece movement including casling and pawn promotion
- Ablity to undo moves
- Checks, Pins, and Ckeckmate
- Stalemate*
- Chess notation log (in console)
- Random AI
- Basic Minimax AI *

Not Implemented:
- En Passant
- Stalemate where either player does not have the pieces required to make checkmate (e.g. one player only has a king and knight)
- Feacible runtime for Minimax AI
- Chess Clock
- Cross-Platform Multiplayer Mode

Requirements:
- pygame library
- random library
- math library
