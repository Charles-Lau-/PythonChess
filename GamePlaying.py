import chess
import chess.pgn
import random
import algorithm
from Node import Node
from Gaussian import Gaussian
"""
    WHITE = 0
    BLACK = 1
"""

WHITE = 0
BLACK = 1
DRAW = "draw"
WHITE_WIN = "white win"
BLACK_WIN = "black win"
san_moves = []

def random_play(node):
    count = 1
    board = node.board()
    length = len(board.legal_moves)
    chosenMove = random.randint(1,length)
    for move in board.legal_moves:
        if(count==chosenMove):
            node.add_variation(move)
            break
        else:
            count +=1

def algorithm_play(root,descent_times):
    #initialize root
    root.visited = True
    root.gDis = Gaussian(0,1)
    while(descent_times>0):
         algorithm.descent(root)
         descent_times -= 1

    for v in root.variations:
        print v.gDis
        print "============"
        print v.board()
        
def random_game(board=None):
    if(board==None):
        board = chess.Board()
    while(True):
        random_play(board)
        print board
        if(board.is_game_over()):
            if(board.is_checkmate()):
                return board.turn==WHITE and BLACK_WIN or WHITE_WIN
            else:
                return DRAW
        else:
            print ""   

if __name__ == "__main__":
    start = Node()
    board = chess.Board()
    start.setup(board)
    print algorithm_play(start.end(),100) 
     
     
