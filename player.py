from board import Direction, Rotation
from random import Random
from time import sleep
from operator import itemgetter

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class KeyursPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
    
    def choose_action(self, board):
        bestScore = 0
        bestMoves = []
        lowestGaps = 1000
        clonedBoard = board.clone()
        for pos1 in range(10):
            for rot1 in range(1, 5):
                for pos2 in range(10):
                    for rot2 in range(1, 5):
                        scores, moves= self.try_move(clonedBoard, pos1, rot1, pos2, rot2)
                        score = scores[0]
                        gaps = scores[1]
                        if score > bestScore or (score==bestScore and gaps<lowestGaps):
                        #if gaps < lowestGaps or (gaps == lowestGaps and score > bestScore):
                            bestScore = score
                            bestMoves = moves
                            lowestGaps = gaps
        return bestMoves
    
    def try_move(self, board, pos1, rot1, pos2, rot2):
        clonedBoard = board.clone()
        moves = []
        for turn in range(rot1):
            test1 = clonedBoard.rotate(Rotation.Clockwise)
            moves.append(Rotation.Clockwise)
            if test1:
                score, gaps, moves = self.try_move2(clonedBoard, pos2, rot2, moves)
                return [score, gaps], moves

        while True:
            if clonedBoard.falling.left < pos1:
                move = Direction.Right
            elif clonedBoard.falling.left > pos1:
                move = Direction.Left
            else:
                move = Direction.Down
            test2 = clonedBoard.move(move)
            moves.append(move)
            if test2:
                score, gaps, moves = self.try_move2(clonedBoard, pos2, rot2, moves)
                return [score, gaps], moves

    def try_move2(self, clonedBoard, pos, rot, moves):
        for turn in range(rot):
            test1 = clonedBoard.rotate(Rotation.Clockwise)
            moves.append(Rotation.Clockwise)
            if test1:
                score, gaps = self.score_board(clonedBoard)
                return score, gaps, moves

        while True:
            if clonedBoard.falling.left < pos:
                move = Direction.Right
            elif clonedBoard.falling.left > pos:
                move = Direction.Left
            else:
                move = Direction.Down
            test2 = clonedBoard.move(move)
            moves.append(move)
            if test2:
                score, gaps = self.score_board(clonedBoard)
                return score, gaps, moves

    def score_board(self, clonedBoard):
        landed = sorted(clonedBoard.cells, key=itemgetter(1))
        total = 0
        for i in range(len(landed)):
            total += landed[i][1]
        average = total/len(landed)
        gaps = self.gapFinder(clonedBoard)
        return average, gaps

    def gapFinder(self, clonedBoard):
        board = sorted(clonedBoard.cells, key=itemgetter(1))
        start = board[0][1]
        end = board[len(board)-1][1]
        gaps = 0
        for row in range(start+1, end+1):
            currentRow = []
            for i in board:
                if i[1]==row:
                    currentRow.append(i)
                #else:
                #    break
            currentRow = sorted(currentRow)
            if len(currentRow)>1:
                potentialGaps = []
                for j in range(10):
                    x = j, row
                    if x not in currentRow:
                        potentialGaps.append(j)
                if len(potentialGaps)>0:
                    for num in potentialGaps:
                        test = num, row-1
                        if test in board:
                            gaps +=1
        return gaps

SelectedPlayer = KeyursPlayer
