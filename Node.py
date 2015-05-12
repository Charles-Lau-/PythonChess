import chess.pgn
from Gaussian import Gaussian
import random

class Node(chess.pgn.GameNode):
    def __init__(self):
         super(Node, self).__init__()
         self.gDis = Gaussian()
         self.vDis = Gaussian()
         self.rollOut = Gaussian()
         self.messageFromParent = Gaussian()
         self.messageToParent = Gaussian()
         self.visited = False 
     

    def getChild(self):
         if(self.board().is_game_over()):
             return None
         if(len(self.variations)== 0):
             for move in self.board().legal_moves:
                 self.add_variation(move)
         #getRandomChild
         chosenChild = random.randint(0,len(self.variations)-1)
         return self.variations[chosenChild]

    def add_variation(self, move, comment="", starting_comment="", nags=()):
        """Creates a child node with the given attributes."""
        node = Node()
        node.move = move
        node.nags = set(nags)
        node.parent = self
        node.comment = comment
        node.starting_comment = starting_comment
        self.variations.append(node)
        return node

    def setup(self,board):
        self.board_cached = board
